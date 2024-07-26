import asyncio
import shutil
import sys
import time
from collections.abc import Callable, Coroutine
from concurrent.futures import Future
from typing import Any

import click
from exponent.commands.common import create_chat, redirect_to_login, start_client
from exponent.commands.settings import use_settings
from exponent.commands.utils import start_background_event_loop
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.mutations import HALT_CHAT_STREAM_MUTATION
from exponent.core.graphql.subscriptions import CHAT_EVENTS_SUBSCRIPTION
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.syntax import Syntax


@click.group()
def shell_cli() -> None:
    pass


@shell_cli.command()
@click.option(
    "--model",
    help="LLM model",
    required=True,
    default="CLAUDE_3_POINT_5_SONNET",
)
@use_settings
def shell(settings: Settings, model: str) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.base_api_url
    gql_client = GraphQLClient(api_key, base_api_url)
    loop = start_background_event_loop()

    def run_coroutine(coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        return asyncio.run_coroutine_threadsafe(coro, loop)

    print("Welcome to ✨ \x1b[1;32mExponent \x1b[4:3mSHELL\x1b[0m ✨")
    print()
    print("Type 'q', 'exit' or press <C-c> to exit")
    print()

    chat_uuid = run_coroutine(create_chat(api_key, base_api_url)).result()

    if chat_uuid is None:
        sys.exit(1)

    client_fut = run_coroutine(start_client(api_key, base_api_url, chat_uuid))
    chat = Shell(chat_uuid, gql_client, model)
    input_handler = InputHandler()
    stream_fut = None

    while True:
        try:
            if stream_fut is not None:
                stream_fut.result()
                stream_fut = None

            text = input_handler.prompt()

            if text == "<c-y>":
                render(
                    ["\r", move_cursor_up_seq(1), reset_attrs_seq(), erase_line_seq()]
                )

                stream_fut = run_coroutine(chat.send_confirmation())
            else:
                print()

                if text in {"q", "exit", "<c-d>"}:
                    break

                if not text:
                    continue

                stream_fut = run_coroutine(chat.send_prompt(text))

        except KeyboardInterrupt:
            if stream_fut is not None:
                run_coroutine(halt_stream(gql_client, chat_uuid)).result()
            else:
                break

    client_fut.cancel()
    print("\rBye!")


async def halt_stream(gql_client: GraphQLClient, chat_uuid: str) -> None:
    await gql_client.query(
        HALT_CHAT_STREAM_MUTATION, {"chatUuid": chat_uuid}, "HaltChatStream"
    )


def pause_spinner(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "Shell", *args: Any, **kwargs: Any) -> Any:
        self.spinner.hide()
        result = func(self, *args, **kwargs)
        self.spinner.show()
        return result

    return wrapper


class Shell:
    def __init__(self, chat_uuid: str, gql_client: GraphQLClient, model: str) -> None:
        self.chat_uuid = chat_uuid
        self.gql_client = gql_client
        self.model = model
        self.parent_uuid = None
        self.block_row_offset = 0
        self.console = Console()
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.block: Block = NullBlock()
        self.last_seqs: list[Any] | None = None
        self.spinner = Spinner()

    async def send_prompt(self, prompt: str) -> str | None:
        return await self.process_chat_subscription(
            {"prompt": {"message": prompt, "attachments": []}}
        )

    async def send_confirmation(self) -> str | None:
        if self.code_block_uuid is not None:
            return await self.process_chat_subscription(
                {
                    "codeBlockConfirmation": {
                        "accepted": True,
                        "codeBlockUuid": self.code_block_uuid,
                    }
                }
            )
        elif self.file_write_uuid is not None:
            return await self.process_chat_subscription(
                {
                    "fileWriteConfirmation": {
                        "accepted": True,
                        "fileWriteUuid": self.file_write_uuid,
                    }
                }
            )

        return None

    async def process_chat_subscription(  # noqa: PLR0912
        self,
        extra_vars: dict[str, Any],
    ) -> str | None:
        result = None

        vars = {
            "chatUuid": self.chat_uuid,
            "parentUuid": self.parent_uuid,
            "model": self.model,
            "useToolsConfig": "read_write",
            "requireConfirmation": True,
        }

        vars.update(extra_vars)
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.spinner.show()

        async for response in self.gql_client.subscribe(CHAT_EVENTS_SUBSCRIPTION, vars):
            event = response["authenticatedChat"]
            kind = event["__typename"]
            self.parent_uuid = event["eventUuid"]

            if kind == "MessageChunkEvent":
                if event["role"] == "assistant":
                    self.handle_message_chunk_event(event)
            elif kind == "MessageEvent":
                if event["role"] == "assistant":
                    self.handle_message_event(event)
            elif kind == "FileWriteChunkEvent":
                self.handle_file_write_chunk_event(event)
            elif kind == "FileWriteEvent":
                self.handle_file_write_event(event)
            elif kind == "FileWriteConfirmationEvent":
                self.handle_file_write_confirmation_event(event)
            elif kind == "FileWriteStartEvent":
                self.handle_file_write_start_event(event)
            elif kind == "FileWriteResultEvent":
                self.handle_file_write_result_event(event)
            elif kind == "CodeBlockChunkEvent":
                self.handle_code_block_chunk_event(event)
            elif kind == "CodeBlockEvent":
                self.handle_code_block_event(event)
            elif kind == "CodeBlockConfirmationEvent":
                self.handle_code_block_confirmation_event(event)
            elif kind == "CodeExecutionStartEvent":
                self.handle_code_execution_start_event(event)
            elif kind == "CodeExecutionEvent":
                self.handle_code_execution_event(event)
            elif kind in [
                "CodeBlockConfirmationEvent",
                "FileWriteConfirmationEvent",
            ]:
                # TODO
                pass
            else:
                # TODO
                pass

        self.spinner.hide()
        return result

    @pause_spinner
    def handle_message_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = MessageBlock(event_uuid)

        self.block.update_content(event["content"])
        self.render_block()

    @pause_spinner
    def handle_message_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = MessageBlock(event_uuid)

        self.block.update_content(event["content"])
        self.block.update_status("done")
        self.render_block()

    @pause_spinner
    def handle_file_write_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = FileWriteBlock(
                event_uuid, event["language"], event["filePath"]
            )

        self.block.update_content(event["content"])
        self.render_block()

    @pause_spinner
    def handle_file_write_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = FileWriteBlock(
                event_uuid, event["language"], event["filePath"]
            )

        self.block.update_content(event["content"])

        if event["requireConfirmation"]:
            self.block.update_status("requires_confirmation")
            self.file_write_uuid = event_uuid
        else:
            self.block.update_status("executing")

        self.render_block()

    @pause_spinner
    def handle_file_write_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["fileWriteUuid"]:
            if event["accepted"]:
                self.block.update_status("executing")
            else:
                # user entered new prompt, cursor moved 2 lines down
                # therefore we need to move it back where it was
                render(move_cursor_up_seq(2))

                self.block.update_status("rejected")

            self.render_block()

    @pause_spinner
    def handle_file_write_start_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["fileWriteUuid"]:
            self.block.update_status("executing")
            self.render_block()

    @pause_spinner
    def handle_file_write_result_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["fileWriteUuid"]:
            assert isinstance(self.block, FileWriteBlock)
            self.block.update_status("done")
            self.block.update_result_content(event["content"])
            self.render_block()

    @pause_spinner
    def handle_code_block_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = CodeExecBlock(event_uuid, event["language"], event["language"])

        self.block.update_content(event["content"])
        self.render_block()

    @pause_spinner
    def handle_code_block_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]

        if self.block.event_uuid != event_uuid:
            self.close_block()
            self.block = CodeExecBlock(event_uuid, event["language"], event["language"])

        self.block.update_content(event["content"])

        if event["requireConfirmation"]:
            self.block.update_status("requires_confirmation")
            self.code_block_uuid = event_uuid
        else:
            self.block.update_status("loading")

        self.render_block()

    @pause_spinner
    def handle_code_block_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["codeBlockUuid"]:
            if event["accepted"]:
                self.block.update_status("executing")
            else:
                # user entered new prompt, cursor moved 2 lines down
                # therefore we need to move it back where it was
                render(move_cursor_up_seq(2))

                self.block.update_status("rejected")

            self.render_block()

    @pause_spinner
    def handle_code_execution_start_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["codeBlockUuid"]:
            self.block.update_status("executing")
            self.render_block()

    @pause_spinner
    def handle_code_execution_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid == event["codeBlockUuid"]:
            assert isinstance(self.block, CodeExecBlock)
            self.block.update_status("done")
            self.block.set_output(event["content"])
            self.render_block()
        else:
            # If the code block UUID doesn't match, create a standalone OutputBlock
            self.close_block()
            self.block = OutputBlock(event["eventUuid"], event["content"])
            self.render_block()

    def close_block(self) -> None:
        self.block_row_offset = 0
        self.last_seqs = None

    def chunk_clear_seq(self) -> list[str]:
        if self.block_row_offset > 0:
            return [
                move_cursor_up_seq(self.block_row_offset),
                "\r",
                erase_display_seq(),
            ]

        return ["\r"]

    def render_block(self) -> None:
        seqs = self.block.render()

        if seqs != self.last_seqs:
            self.block_row_offset = render([self.chunk_clear_seq(), *seqs])
            self.last_seqs = seqs


class Spinner:
    def __init__(self) -> None:
        self.task: asyncio.Task[None] | None = None
        self.base_time = time.time()

    def show(self) -> None:
        if self.task is not None:
            return

        async def spinner(base_time: float) -> None:
            # chars = "/-\\|"
            # chars = "◢◣◤◥"
            chars = "⣷⣯⣟⡿⢿⣻⣽⣾"

            while True:
                t = time.time() - base_time
                i = round(t * 10) % len(chars)
                render(["\r", chars[i], " Exponent is working..."])
                await asyncio.sleep(0.1)

        self.task = asyncio.get_event_loop().create_task(spinner(self.base_time))

    def hide(self) -> None:
        if self.task is None:
            return

        self.task.cancel()
        self.task = None
        render(["\r", reset_attrs_seq(), erase_line_seq()])


class InputHandler:
    def __init__(self) -> None:
        self.kb = KeyBindings()
        self.shortcut_pressed = None

        @self.kb.add("c-y")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-y>"
            event.app.exit()

        @self.kb.add("c-d")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-d>"
            event.app.exit()

    def prompt(self) -> str:
        self.shortcut_pressed = None

        user_input = prompt(
            HTML("<b><ansigreen>></ansigreen></b> "), key_bindings=self.kb
        )

        if self.shortcut_pressed:
            return self.shortcut_pressed
        else:
            return user_input


class Block:
    def __init__(self, event_uuid: str) -> None:
        self.event_uuid = event_uuid
        self.spinner = None
        self.content = ""
        self.block_row_offset = 0
        self.console = Console()
        self.theme = "monokai"

    def update_content(self, content: str) -> None:
        self.content = content

    def update_status(self, status: str) -> None:
        self.status = status

    def render(self) -> list[Any]:
        return []

    def render_header(self, text: str) -> list[str]:
        return [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " " + text,
            reset_attrs_seq(),
            "\n",
        ]

    def render_footer(self, text: str) -> list[str]:
        return [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " " + text,
            reset_attrs_seq(),
            "\n",
        ]

    def render_padding(self) -> list[str]:
        return [
            block_body_bg_seq(),
            erase_line_seq(),
            reset_attrs_seq(),
            "\n",
        ]

    def highlight_code(self, code: str, lang: str, line_numbers: bool = True) -> str:
        syntax = Syntax(
            code,
            lang,
            theme=self.theme,
            line_numbers=line_numbers,
            word_wrap=True,
        )

        with self.console.capture() as capture:
            self.console.print(syntax)

        return capture.get()


class NullBlock(Block):
    def __init__(self) -> None:
        super().__init__("")


class MessageBlock(Block):
    def __init__(self, event_uuid: str) -> None:
        super().__init__(event_uuid)
        self.status = "streaming"

    def render(self) -> list[Any]:
        text = self.content.strip()

        if self.status == "streaming":
            color = 2
        else:
            color = 3

        return [
            fg_color_seq(color),
            (text, text_line_count(text) - 1),
            reset_attrs_seq(),
            "\n\n",
        ]


class CodeExecBlock(Block):
    def __init__(self, event_uuid: str, lang: str, header_text: str) -> None:
        super().__init__(event_uuid)
        self.status = "streaming"  # valid states: streaming, requires_confirmation, rejected, executing, done
        self.lang = lang
        self.header_text = header_text
        self.output_block: OutputBlock | None = None

    def set_output(self, content: str) -> None:
        self.output_block = OutputBlock(self.event_uuid, content)

    def render(self) -> list[Any]:
        header = self.render_header(self.header_text or self.lang)
        code = self.render_code()
        output = self.render_output()
        footer = self.render_status_footer()

        return [header, code, output, footer, "\n"]

    def render_code(self) -> list[Any]:
        padding = self.render_padding()
        code = pad_left(self.content.strip(), "  ")
        code = self.highlight_code(code, self.lang, line_numbers=False)

        return [padding, code, padding]

    def render_output(self) -> list[Any]:
        if self.output_block:
            header = self.render_header("output")
            content = self.output_block.render_content()

            return [header, content]

        return []

    def render_status_footer(self) -> list[Any]:
        if self.status == "requires_confirmation":
            return self.render_footer(
                "Run this code now with <C+y>. Sending a new message will cancel this request."
            )
        elif self.status == "rejected":
            return self.render_footer("✘ Code did not execute")
        elif self.status == "executing":
            return self.render_footer("⚙️ Running code...")

        return []


class FileWriteBlock(Block):
    def __init__(self, event_uuid: str, lang: str, file_path: str) -> None:
        super().__init__(event_uuid)
        self.status = "streaming"  # valid states: streaming, requires_confirmation, rejected, executing, done
        self.lang = lang
        self.file_path = file_path
        self.result_content: str | None = None

    def update_result_content(self, content: str) -> None:
        self.result_content = content

    def render(self) -> list[Any]:
        header = self.render_header(f"Editing file {self.file_path}")
        code = self.render_code()
        footer = self.render_status_footer()

        return [header, code, footer, "\n"]

    def render_code(self) -> list[Any]:
        padding = self.render_padding()
        code = self.highlight_code(self.content.strip(), self.lang)

        return [padding, code, padding]

    def render_status_footer(self) -> list[Any]:
        if self.status == "requires_confirmation":
            return self.render_footer(
                "Confirm edit with <C+y>. Sending a new message will dismiss code changes."
            )
        elif self.status == "rejected":
            return self.render_footer("✘ Edit dismissed")
        elif self.status == "executing":
            return self.render_footer("⚙️ Applying edit...")
        elif self.status == "done":
            return self.render_footer(
                f"✔️ {self.result_content}" if self.result_content else "✔️ Edit applied"
            )

        return []


class OutputBlock(Block):
    def __init__(self, event_uuid: str, content: str) -> None:
        super().__init__(event_uuid)
        self.content = content

    def render(self) -> list[Any]:
        header = self.render_header("output")
        content = self.render_content()

        return [header, content, "\n"]

    def render_content(self) -> list[Any]:
        padding = self.render_padding()
        lines = pad_left(self.content.strip(), "  ").split("\n")

        content = [
            [block_body_bg_seq(), erase_line_seq(), line, "\n"] for line in lines
        ]

        return [padding, content, padding]


def text_line_count(text: str) -> int:
    cols = get_terminal_width()
    count = 0

    for line in text.split("\n"):
        count += len(line) // cols

        if len(line) == 0 or len(line) % cols > 0:
            count += 1

    return count


def get_terminal_width() -> int:
    cols, _ = shutil.get_terminal_size()
    return cols


def pad_left(text: str, padding: str) -> str:
    return "\n".join([padding + line for line in text.strip().split("\n")])


def fg_color_seq(c: int) -> str:
    return f"\x1b[{30 + c}m"


def block_header_bg_seq() -> str:
    return "\x1b[48;2;29;30;24m"


def block_header_fg_seq() -> str:
    return "\x1b[38;5;246m"


def block_body_bg_seq() -> str:
    return "\x1b[48;2;39;40;34m"


def erase_line_seq() -> str:
    return "\x1b[2K"


def erase_display_seq() -> str:
    return "\x1b[0J"


def reset_attrs_seq() -> str:
    return "\x1b[0m"


def move_cursor_up_seq(n: int) -> str:
    return f"\x1b[{n}A"


def render(seqs: str | list[Any] | None) -> int:
    text, newline_count = collect(seqs)
    print(text, end="")
    sys.stdout.flush()

    return newline_count


def collect(seqs: str | list[Any] | None) -> tuple[str, int]:
    if seqs is None:
        return ("", 0)

    if isinstance(seqs, str):
        return (seqs, seqs.count("\n"))

    if isinstance(seqs, tuple):
        return seqs

    assert isinstance(seqs, list)

    text = ""
    newline_count = 0

    for seq in seqs:
        t, c = collect(seq)
        text += t
        newline_count += c

    return (text, newline_count)

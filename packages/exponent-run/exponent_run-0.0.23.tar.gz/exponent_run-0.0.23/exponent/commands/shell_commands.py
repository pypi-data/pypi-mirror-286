import asyncio
import shutil
import sys
from collections.abc import Coroutine
from concurrent.futures import Future
from typing import Any

import click
from exponent.commands.common import create_chat, redirect_to_login, start_client
from exponent.commands.settings import use_settings
from exponent.commands.utils import read_input, start_background_event_loop
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.subscriptions import CHAT_EVENTS_SUBSCRIPTION
from rich.console import Console
from rich.syntax import Syntax

PROMPT = "\x1b[1;32m>\x1b[0m "


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
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    result_queue: asyncio.Queue[bool] = asyncio.Queue()
    loop = start_background_event_loop()

    def run_in_background(coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        return asyncio.run_coroutine_threadsafe(coro, loop)

    async def process_input(text: str) -> bool | None:
        await input_queue.put(text)
        return await result_queue.get()

    print("Welcome to ✨ \x1b[1;32mExponent \x1b[4:3mSHELL\x1b[0m ✨")
    print()
    print("Type 'q', 'exit' or press <C-c> to exit")
    print()

    chat_uuid = run_in_background(create_chat(api_key, base_api_url)).result()

    if chat_uuid is None:
        sys.exit(1)

    client_fut = run_in_background(start_client(api_key, base_api_url, chat_uuid))
    chat = Shell(chat_uuid, gql_client, model)

    while True:
        try:
            text = read_input(PROMPT)
            print()

            if not text:
                break

            text = text.strip()

            if text in {"q", "exit"}:
                break

            if not text:
                continue

            quit = run_in_background(chat.process_input(text)).result()
            print()

            if quit:
                break
        except KeyboardInterrupt:
            break

    client_fut.cancel()
    print("\rBye!")


class Shell:
    def __init__(self, chat_uuid: str, gql_client: GraphQLClient, model: str) -> None:
        self.chat_uuid = chat_uuid
        self.gql_client = gql_client
        self.model = model
        self.parent_uuid = None
        self.block_row_offset = 0
        self.console = Console()
        self.theme = "monokai"

    async def process_input(self, text: str) -> bool:
        spinner = start_spinner()

        async for response in self.gql_client.subscribe(
            CHAT_EVENTS_SUBSCRIPTION,
            {
                "prompt": {"message": text, "attachments": []},
                "chatUuid": self.chat_uuid,
                "parentUuid": self.parent_uuid,
                "model": self.model,
                "useToolsConfig": "read_write",
                "requireConfirmation": True,
            },
        ):
            event = response["authenticatedChat"]
            kind = event["__typename"]
            self.parent_uuid = event["eventUuid"]

            if kind == "MessageChunkEvent":
                if event["role"] == "assistant":
                    spinner.cancel()
                    self.handle_text_block_chunk(event["content"])
            elif kind == "MessageEvent":
                if event["role"] == "assistant":
                    spinner.cancel()
                    self.handle_text_block(event["content"])
            elif kind == "FileWriteChunkEvent":
                spinner.cancel()
                self.handle_code_block_chunk(event["content"], event["language"])
            elif kind == "FileWriteEvent":
                spinner.cancel()
                self.handle_code_block(event["content"], event["language"])
            elif kind == "CodeBlockChunkEvent":
                spinner.cancel()
                self.handle_code_block_chunk(event["content"], event["language"])
            elif kind == "CodeBlockEvent":
                spinner.cancel()
                self.handle_code_block(event["content"], event["language"])
            elif kind in ["CodeBlockConfirmationEvent", "FileWriteConfirmationEvent"]:
                pass
            else:
                spinner.cancel()
                print(event)

        return False

    def handle_text_block_chunk(self, text: str) -> None:
        print(f"{self.chunk_clear_seq()}\x1b[32m{text}\x1b[0m", end="")
        sys.stdout.flush()
        self.block_row_offset = self.text_line_count(text) - 1

    def handle_text_block(self, text: str) -> None:
        print(f"{self.chunk_clear_seq()}\x1b[33m{text}\x1b[0m")
        sys.stdout.flush()
        self.block_row_offset = 0

    def handle_code_block_chunk(self, text: str, lang: str) -> None:
        code = self.highlight_code(text.strip(), lang)
        print(f"{self.chunk_clear_seq()}{code}", end="")
        sys.stdout.flush()
        self.block_row_offset = len(code.split("\n")) - 1

    def handle_code_block(self, text: str, lang: str) -> None:
        self.handle_code_block_chunk(text, lang)
        self.block_row_offset = 0

    def highlight_code(self, code: str, lang: str) -> str:
        syntax = Syntax(code, lang, theme=self.theme, line_numbers=True, word_wrap=True)

        with self.console.capture() as capture:
            self.console.print(syntax)

        return capture.get()

    def chunk_clear_seq(self) -> str:
        if self.block_row_offset > 0:
            return f"\x1b[{self.block_row_offset}A\r\x1b[0J"

        return "\r"

    def text_line_count(self, text: str) -> int:
        cols = self.get_terminal_width()
        count = 0

        for line in text.split("\n"):
            count += max(len(line) // cols, 1)

        return count

    def get_terminal_width(self) -> int:
        cols, _ = shutil.get_terminal_size()
        return cols


def start_spinner() -> asyncio.Task[Any]:
    async def spinner() -> None:
        chars = ["/", "-", "\\", "|"]
        i = 0

        while True:
            print(f"\r{chars[i]}", end="")
            sys.stdout.flush()
            i = (i + 1) % len(chars)
            await asyncio.sleep(0.1)

    return asyncio.get_event_loop().create_task(spinner())

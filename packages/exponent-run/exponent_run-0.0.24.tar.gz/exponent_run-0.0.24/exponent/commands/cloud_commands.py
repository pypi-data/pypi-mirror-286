import os
import sys
import time

import click
from exponent.commands.common import create_chat, redirect_to_login, run_until_complete
from exponent.commands.utils import (
    launch_exponent_browser,
    print_exponent_message,
    write_template_exponent_cloud_config,
)
from exponent.core.config import Environment, ExponentCloudConfig, Settings
from exponent.core.runloop import RunloopClient
from pydantic import ValidationError


@click.group()
def cloud_cli() -> None:
    pass


@cloud_cli.command()
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
def cloud(
    settings: Settings,
    prompt: str | None = None,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        start_cloud(
            settings.environment,
            settings.api_key,
            settings.base_url,
            settings.base_api_url,
            prompt=prompt,
        )
    )


async def start_cloud(
    environment: Environment,
    api_key: str,
    base_url: str,
    base_api_url: str,
    prompt: str | None = None,
) -> None:
    current_working_directory = os.getcwd()

    # Check if an `.exponent.cloud.json` file exists.
    # If so, use it. If not, write a template file and exit.
    file_path = os.path.join(current_working_directory, ".exponent.cloud.json")
    if not os.path.exists(file_path):
        click.secho("No `.exponent.cloud.json` file found, creating one to fill out...")
        write_template_exponent_cloud_config(file_path)
        click.secho(
            "`.exponent.cloud.json` file created, fill out the required fields "
            "and run this command again."
        )
        return

    with open(file_path) as f:
        try:
            exponent_cloud_config = ExponentCloudConfig.model_validate_json(f.read())
        except ValidationError as e:
            click.secho(f"Error in parsing `.exponent.cloud.json`: {e}", fg="red")
            return

    chat_uuid = await create_chat(api_key, base_api_url)

    if chat_uuid is None:
        return

    click.secho(
        "Chat created. Waiting for cloud container to spin up...", fg="green", bold=True
    )

    runloop_client = RunloopClient(
        api_key=exponent_cloud_config.runloop_api_key,
    )

    def join_commands(commands: list[str]) -> str:
        return " && ".join(commands)

    if prompt:
        exponent_command = (
            f'exponent run --prod --chat-id {chat_uuid} --prompt \\"{prompt}\\"'
        )
    else:
        exponent_command = f"exponent run --prod --chat-id {chat_uuid}"

    devbox = await runloop_client.create_devbox(
        entrypoint="/home/user/run.sh",
        environment_variables={"GH_TOKEN": exponent_cloud_config.gh_token},
        setup_commands=[
            join_commands(exponent_cloud_config.repo_specific_setup_commands),
            f'echo "cd /home/user/{exponent_cloud_config.repo_name} && source .venv/bin/activate && uv pip install exponent-run && exponent login --prod --key {api_key} && {exponent_command}" > /home/user/run.sh',
            "chmod +x /home/user/run.sh",
        ],
    )

    # Step 3. Poll Runloop for container spinup and log status
    while True:
        current_devbox = await runloop_client.get_devbox(devbox["id"])
        if current_devbox["status"] != "running":
            print(
                f"Container {devbox['id']} is loading, waiting.... Current status is {current_devbox['status']}"
            )
        elif current_devbox["status"] == "failure":
            click.secho("Devbox failed to start", fg="red", bold=True)
            sys.exit(1)
        else:
            break

        time.sleep(1)

    # Step 4. Open the chat in the browser
    print_exponent_message(base_url, chat_uuid)
    launch_exponent_browser(environment, base_url, chat_uuid)

    # Step 5. Wait for user input with the message "Stop Runloop?"
    input("Stop cloud container?: [press enter to continue]")

    # Step 6. Stop Runloop
    await runloop_client.shutdown_devbox(devbox["id"])
    click.secho("Cloud container stopped", fg="green", bold=True)


@cloud_cli.command()
@click.option(
    "--devbox-id",
    type=str,
    help="Devbox ID to get logs from.",
    required=True,
    prompt=True,
)
def cloud_logs(
    devbox_id: str,
    settings: Settings,
) -> None:
    run_until_complete(start_cloud_logs(devbox_id))


async def start_cloud_logs(
    devbox_id: str,
) -> None:
    current_working_directory = os.getcwd()

    # Check if an `.exponent.cloud.json` file exists.
    # If so, use it. If not, write a template file and exit.
    file_path = os.path.join(current_working_directory, ".exponent.cloud.json")
    if not os.path.exists(file_path):
        click.secho("No `.exponent.cloud.json` file found, creating one to fill out...")
        write_template_exponent_cloud_config(file_path)
        click.secho(
            "`.exponent.cloud.json` file created, fill out the required fields "
            "and run this command again."
        )
        return

    with open(file_path) as f:
        try:
            exponent_cloud_config = ExponentCloudConfig.model_validate_json(f.read())
        except ValidationError as e:
            click.secho(f"Error in parsing `.exponent.cloud.json`: {e}", fg="red")
            return

    runloop_client = RunloopClient(
        api_key=exponent_cloud_config.runloop_api_key,
    )

    response = await runloop_client.devbox_logs(devbox_id)
    for log in response["logs"]:
        click.secho(log["message"])

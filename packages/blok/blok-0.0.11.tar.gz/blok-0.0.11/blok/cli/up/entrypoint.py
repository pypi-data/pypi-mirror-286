from pathlib import Path
import signal
import time
import subprocess
import click
from blok.blok import Command
from blok.registry import BlokRegistry
from blok.renderer import Renderer, Panel

# List to keep track of subprocesses
subprocesses = []


def signal_handler(sig, frame):
    print("Main process received interrupt signal")
    terminate_all_subprocesses()
    print("All subprocesses terminated")
    exit(0)


def terminate_all_subprocesses():
    for p in subprocesses:
        if p.poll() is None:  # Check if process is still running
            print(f"Terminating subprocess with PID: {p.pid}")
            p.terminate()
    for p in subprocesses:
        p.wait()


def secure_path_combine(x: Path, y: Path) -> Path:
    # Resolve the combined path
    mother_path = x.resolve()
    combined_path = (mother_path / y).resolve()

    # Check if the combined path is within the mother path
    if mother_path in combined_path.parents or mother_path == combined_path:
        return combined_path
    else:
        raise ValueError(
            f"The user-defined path traverses out of the mother path. {list(combined_path.parents)} but requested {mother_path}"
        )


@click.pass_context
def entrypoint(
    ctx: click.Context,
    registry: BlokRegistry,
    renderer: Renderer,
    blok_file_name: str,
    **kwargs,
):
    renderer.render(
        Panel("Lets up this project", title="Welcome to Blok!", style="bold magenta")
    )

    path = Path(kwargs.pop("path"))
    yes = kwargs.pop("yes", False)
    select = kwargs.pop("select", [])

    up_commands = ctx.obj.get("up_commands", {})

    selected_commands = []

    if select:
        print("Selecting commands")
        for key in select:
            if key in up_commands:
                selected_commands.append(up_commands[key])
            else:
                raise click.ClickException(f"Command with key {key} not found")

    else:
        selected_commands = list(up_commands.values())
        selected_commands.append(
            {"command": ["docker", "compose", "up", "-d"], "cwd": "."}
        )

    if yes or renderer.confirm(
        "Run up commands? \n\t"
        + "\n\t".join(map(lambda x: " ".join(x["command"]), selected_commands))
        + "\n"
    ):
        print("Running up commands")
    else:
        raise click.Abort("User aborted")
        return

    if len(selected_commands) == 1:
        command = selected_commands[0]
        rel_path = secure_path_combine(path, Path(command["cwd"]))
        p = subprocess.run(
            " ".join(command["command"]),
            shell=True,
            cwd=rel_path,
        )

    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        for command in selected_commands:
            rel_path = secure_path_combine(path, Path(command["cwd"]))
            p = subprocess.Popen(
                command["command"],
                cwd=rel_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            subprocesses.append(p)
            print(f"Started subprocess {command['command']} with PID: {p.pid}")

        try:
            while True:
                for p in subprocesses:
                    if p.poll() is not None:  # Process has terminated
                        if p.returncode != 0:  # Process failed
                            error_output = p.stderr.read().decode()
                            print(
                                f"Subprocess with PID {p.pid} failed with return code {p.returncode}"
                            )
                            print(f"Error output: {error_output}")
                            terminate_all_subprocesses()
                            raise click.ClickException(
                                f"Subprocess failed: {error_output}"
                            )
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

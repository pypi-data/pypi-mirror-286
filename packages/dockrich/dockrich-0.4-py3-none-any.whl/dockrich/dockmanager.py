import subprocess
import sys
from rich.console import Console
from rich.table import Table
import shlex
from rich.panel import Panel
from time import sleep
from rich import print
from rich import spinner
import secrets
import docker


def hasargs():
    args = sys.argv[1:]
    args_dict = {}
    i = 0
    while i < len(args):
        if i + 1 < len(args) and not args[i + 1].startswith('-'):
            args_dict[args[i]] = args[i + 1]
            i += 2
        else:
            args_dict[args[i]] = None
            i += 1
    return args_dict


def stop_containers(container_id_or_name: str):
    client = docker.from_env()
    try:
        console = Console()
        container = client.containers.get(container_id_or_name)
        with console.status("[bold green]Stopping Docker containers...", spinner="bouncingBar"):
            container.stop()
        console.log(f"[bold white]Container stopped: [bold white]{container_id_or_name}")
    except docker.errors.NotFound:
        print(f"[bold red]{container_id_or_name} not found")
    except docker.errors.APIError as e:
        print(f"Error while stopping container {container_id_or_name}:{e}")
    except KeyboardInterrupt:
        print("[bold red] Quitting [/bold red]")


def print_options():
    console = Console()

    table = Table(show_header=False, box=None)
    table.add_column("Option", width=20)
    table.add_column("Description")
    table.add_row(" ", " ")
    table.add_row(" ", "Docker Manage + Pretty", style="purple")
    table.add_row(" ", " ")
    table.add_row("-h, --help", "Show this help message and exit")
    table.add_row("-r, --running", "Print all running containers")
    table.add_row("-i, --images", "List images without 'none' tag and 'none' name")
    table.add_row("-p, --ports", "List all running docker container ports")
    table.add_row("-n, --networks", "List all docker networks")
    table.add_row("-s, --stop", "Stop all running containers")
    table.add_row("-rn, --running","to run an container with image dockrich -rn -image name -t name -c command")

    panel = Panel(
        table, title="[Options]", title_align="left", border_style="bold white"
    )

    console.print(panel)


imagenames = secrets.token_urlsafe(8)


class Dockermanager:
    @staticmethod
    def build(tags="latest", name="imagenames", path="."):
        try:
            dockercommand = f"docker build -t {name}:{tags} {path}"
            result = subprocess.run(
                dockercommand, shell=True, capture_output=True, text=True, check=True
            )
            print(result.stdout)
            print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"[bold red] {e.stderr} [/bold red]")
    @staticmethod
    def stop_all_running_containers():
        client = docker.from_env()
        containers = client.containers.list()
        if len(containers) == 0:
            print("[bold white] [*] No running container to stop [/bold white]")
        else:
            for container in containers:
                stop_containers(container.id)
    @staticmethod
    def run_container(imagename, imagetag="latest",command="tail -f /dev/null"):
        try:
            dockercommand = f"docker run -d {imagename}:{imagetag} {command}"
            console = Console()
            with console.status("[bold green] Starting Docker container...", spinner="bouncingBar"):
                result = subprocess.run(dockercommand,shell=True,capture_output=True,text=True,check=True)
            containerid = result.stdout
            print(f"[bold white] [*] Started :  {containerid}[/bold white] ")
        except subprocess.CalledProcessError as e:
            print(e)
    @staticmethod
    def exec(containerid):
        try:
            dockercommand = f"docker exec -it {containerid} bash"
            result = subprocess.run(
                dockercommand, shell=True, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                print(f"[bold red] {e} [/bold red]")
    @staticmethod
    def list_running_containers():
        try:
            # Run the Docker command to list running containers with networks and command
            out = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--format",
                    "{{.ID}} {{.Image}} {{.Names}} {{.State}} {{.Networks}} {{.Command}} {{.CreatedAt}}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output into a table using rich
            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Container ID", style="cyan")
            table.add_column("Name", style="yellow")
            table.add_column("Image", style="bold green")
            table.add_column("State", style="green")
            table.add_column("Networks", style="red")
            table.add_column("Command", style="blue")
            table.add_column("CreatedAt", style="purple")

            # Process each line of Docker output
            for line in out.stdout.splitlines():
                parts = shlex.split(line)
                container_id, name, image, state, networks, command, createdat = (
                    parts[0],
                    parts[1],
                    parts[2],
                    parts[3],
                    parts[4],
                    parts[5],
                    " ".join(parts[6:]),
                )
                table.add_row(
                    container_id, name, image, state, networks, command, createdat
                )

            console.print(table)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    @staticmethod
    def list_container_ports():
        try:
            containers = subprocess.run(
                ["docker", "ps", "--format", "{{.ID}}"],
                capture_output=True,
                text=True,
                check=True,
            )
            out = subprocess.run(
                ["docker", "ps", "--format", "{{.Ports}}"],
                capture_output=True,
                text=True,
                check=True,
            )
            console = Console()
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )
            table.add_column("Container ID", style="green")
            table.add_column("Ports", style="cyan")
            container_ids = containers.stdout.strip().split("\n")
            ports_list = out.stdout.strip().split("\n")
            for container_id, ports in zip(container_ids, ports_list):
                table.add_row(container_id, ports)
            console.print(table)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    @staticmethod
    def list_true_without_none():
        try:
            docker_command = "docker images --format '{{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}' | grep -v '<none>'"
            containers = subprocess.run(
                docker_command, shell=True, capture_output=True, text=True, check=True
            )
            console = Console()
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )
            table.add_column("Repository", style="cyan")
            table.add_column("Tag", style="yellow")
            table.add_column("Container ID", style="bold green")
            table.add_column("Created Since", style="green")
            table.add_column("Size", style="red")
            output_lines = containers.stdout.strip().split("\n")
            mainlines = output_lines
            for i in range(len(mainlines)):
                cols = mainlines[i].strip().split("\t")
                table.add_row(cols[0], cols[1], cols[2], cols[3], cols[4])
            console.print(table)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    @staticmethod
    def list_networks():
        try:
            docker_commands = "docker network ls --format '{{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}'"
            containers = subprocess.run(
                docker_commands, shell=True, capture_output=True, text=True, check=True
            )
            console = Console()
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )
            table.add_column("NETWORK ID", style="cyan")
            table.add_column("NAME", style="yellow")
            table.add_column("DRIVER", style="bold green")
            table.add_column("SCOPE", style="green")
            # print(type(containers.stdout))
            output_lines = containers.stdout.strip().split("\n")
            mainlines = output_lines
            for i in range(len(mainlines)):
                cols = mainlines[i].strip().split("\t")
                table.add_row(cols[0], cols[1], cols[2], cols[3])
            console.print(table)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
 
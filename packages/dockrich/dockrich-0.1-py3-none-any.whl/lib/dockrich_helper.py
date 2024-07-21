import subprocess
from rich.console import Console
from rich.table import Table
import shlex


class DockrichHelper:
    def __init__(self):
        pass

    def list_running_containers(self):
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

    def list_container_ports(self):
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

    def list_true_without_none(self):
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
                cols = mainlines[i].strip().split('\t')
                table.add_row(cols[0],cols[1],cols[2],cols[3],cols[4])
            console.print(table)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    def list_networks(self):
        try:
            docker_commands = "docker network ls --format '{{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}'"
            containers = subprocess.run(docker_commands, shell=True, capture_output=True, text=True, check=True)
            console = Console()
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )
            table.add_column("NETWORK ID", style="cyan")
            table.add_column("NAME", style="yellow")
            table.add_column("DRIVER", style="bold green")
            table.add_column("SCOPE", style="green")
            # print(type(containers.stdout))
            output_lines = containers.stdout.strip().split('\n')
            mainlines = output_lines
            for i in range(len(mainlines)):
                cols = mainlines[i].strip().split('\t')
                table.add_row(cols[0],cols[1],cols[2],cols[3])
            console.print(table)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
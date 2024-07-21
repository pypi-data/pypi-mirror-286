from dockrich.dockmanager import print_options , Dockermanager,hasargs
from dockrich.dockcompose import load_json

DM = Dockermanager()


def main():
    arg = hasargs()

    commands = {
        "-h": print_options,
        "--help": print_options,
        "-r": DM.list_running_containers,
        "--running": DM.list_running_containers,
        "-i": DM.list_true_without_none,
        "--images": DM.list_true_without_none,
        "-p": DM.list_container_ports,
        "--ports": DM.list_container_ports,
        "-n": DM.list_networks,
        "--networks": DM.list_networks,
        "-s": DM.stop_all_running_containers,
        "--stop": DM.stop_all_running_containers,
    }

    # Call the function if the argument is found in the dictionary
    if arg in commands:
        commands[arg]()
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()

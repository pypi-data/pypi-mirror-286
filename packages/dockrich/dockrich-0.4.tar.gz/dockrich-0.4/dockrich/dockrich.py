from dockrich.dockmanager import print_options , Dockermanager,hasargs
from dockrich.dockcompose import load_json

DM = Dockermanager()

def main():
    arguments = hasargs()
    keys = list(arguments.keys())
    values = list(arguments.values())
    try:
        if values[0] == None:
            for key in keys:
                if key in {'-h','--help'}:
                    print_options()
                elif key in {'-r','--running'}:
                    DM.list_running_containers()
                elif key in {'-i','--images'}:
                    DM.list_true_without_none()
                elif key in {'-p','--ports'}:
                    DM.list_container_ports()
                elif key in {'-n','--networks'}:
                    DM.list_networks()
                elif key in {'-s','--stop'}:
                    DM.stop_all_running_containers()
                else:
                    print_options()
        elif values[0] is not None:
            for key in keys:
                if key in {"-rn"}:
                    userimagename = values[0]
                    usertagname = values[1]
                    command = values[2]
                    DM.run_container(imagename=userimagename,imagetag=usertagname,command=command)
    except IndexError:
        print_options()
if __name__ == "__main__":
    main()

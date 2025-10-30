import argparse
from multiprocessing import (
    Process
)
import subprocess
import os


# Use subprocess to enter command into the container
def exec_into_container(container: str, command: str | list[str]):  # container may be an object in the future
    RUNC_CMD = "podman"  # set by default on machines
    if os.environ.get("RUNC_CMD"):
        RUNC_CMD = os.environ.get("RUNC_CMD")

    result = subprocess.run([RUNC_CMD, "exec", "-d", container, command]) # Ex: podman exec pod1


# Parallel
# Find a way to get the list of container
# Spawn max X number of processes depending on # cores 
# Continue until all work is complete
# Send the command to a unique container from each process
def parallel_exec(containers: list[str], cmd: str | list[str]):     # container may be an object in the future

    num_cont = len(containers)
    num_proc_to_spawn = os.cpu_count()
    index = 0
    processes = []

    while (num_cont > 0 and index < num_cont):

        if (num_cont <= num_proc_to_spawn):
            # Spawn num_cont processes
            for i in range(num_cont + 1):
                p = Process(target=exec_into_container, args=(containers[index], cmd))
                processes.append(p)
                p.start()
                index += 1
            num_cont -= num_cont
        else:
            # Spawn num_proc_to_spawn processes
            for i in range(num_cont + 1):
                p = Process(target=exec_into_container, args=(containers[index], cmd))
                processes.append(p)
                p.start()
                index += 1

            num_cont -= num_proc_to_spawn
    
    for proc in processes:
        proc.join()



# Sequential case
# Parse given list of container
# For loop to send command to each container
def seq_exec(containers: list, cmd: str | list[str], )
    

def main():
    # Adding basic flags
    parser = argparse.ArgumentParser(description="Command line tool to execute commands in Docker/Podman containers sequentially or parallely.")
    parser.add_argument("-c", "--containers", action="store_true", required=True, help="The containers to pass the commands to.", nargs='+')    # + is 1+ args aka list
    parser.add_argument("", "--cmd", required=True, action="store_true", help="The commands to pass to the containers", nargs='+')  
    parser.add_argument("-A", "--all", action="store_true", help="Pass the commands to all the containers.")
    parser.add_mutually_exclusive_group("-p", "--parallel", required=True, action="store_true", help="Run the command across the containers parallely.")
    parser.add_mutually_exclusive_group("-s", "--sequential", required=True, action="store_true", help="Run the command across the containers sequentially.")
    args = parser.parse_args()

    if args.c and args.p and args.cmd:
        parallel_exec(args.c, args.cmd)



if __name__ == "__main__":
    main()

import argparse
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os
import json


# Verbose print, produces output only if verbose mode is toggled
# Configured in main
# Global to enable access in other files
verboseprint = lambda *a, **k: None

RUNC_CMD = "podman"  # set by default on machines
if os.environ.get("RUNC_CMD"):
    RUNC_CMD = os.environ.get("RUNC_CMD")

# Use subprocess to enter command into the container
def exec_into_container(container: str, command: str):  # container may be an object in the future

    result = subprocess.run([RUNC_CMD, "exec", container, "/bin/sh", "-c", command],
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            text=True
    ) # Ex: podman exec pod1
    # print(f'\nresult of execution for container {container}\n', result.stdout)

    if result.returncode != 0:
        print('ERR EXECUTING CMD')

# Parallel
# Find a way to get the list of container
# Spawn max X number of processes depending on # cores 
# Continue until all work is complete
# Send the command to a unique container from each process
def parallel_exec(containers: list[str], cmd: str | list[str]):     # container may be an object in the future

    # num_workers = os.cpu_count() or 1
    # # print('your thread count:', num_workers)

    # tasks = [(container, cmd) for container in containers]

    # # This automatically runs at most num_worker processes and schedules remaining containers when a process finishes
    # with Pool(processes=num_workers) as pool:
    #     pool.starmap(exec_into_container, tasks)

    max_workers = min(len(containers), multiprocessing.cpu_count())
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda c: exec_into_container(c, cmd), containers)

# Sequential case
# Parse given list of container
# For loop to send command to each container
# def seq_exec(containers: list, cmd: str | list[str], )


def main():
    # Adding basic flags
    parser = argparse.ArgumentParser(description="Command line tool to execute commands in Docker/Podman containers sequentially or parallely.")
    container_group = parser.add_mutually_exclusive_group(required=True)
    container_group.add_argument("-c", "--containers", help="The containers to pass the commands to.", nargs='+')    # + is 1+ args aka list
    container_group.add_argument("-A", "--all", action="store_true", help="Pass the commands to all the containers.")
    parser.add_argument("-m", "--cmd", required=True, help="The commands to pass to the containers")  
    execution_group = parser.add_mutually_exclusive_group(required=True)
    execution_group.add_argument("-p", "--parallel", action="store_true", help="Deploy the command(s) across the containers in parallel.")
    execution_group.add_argument("-s", "--sequential", action="store_true", help="Deploy the command(s) across the containers in sequence.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Mode")
    args = parser.parse_args()
    
    # Function to toggle verbose output in functions 
    verboseprint = print if args.verbose else lambda *a, **k: None

    if args.parallel and args.cmd:
        if args.all:
            containers = []
            result = subprocess.run([RUNC_CMD, "ps", "--format", "json"], 
                                    stderr=subprocess.PIPE, 
                                    stdout=subprocess.PIPE
            ).stdout

            for cont in json.loads(result):             # Converts json into dict
                if cont['Names'][0]:
                    containers.append(cont['Names'][0])
        
            parallel_exec(containers, args.cmd)
        
        elif args.containers:
            parallel_exec(args.containers, args.cmd)



if __name__ == "__main__":
    main()


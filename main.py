

import argparse
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os
import json
import podman
import docker


verboseprint = print if os.environ['CCP_VERBOSE']=='TRUE' else lambda *a, **k: None

RUNC_CMD = "podman"  # set by default on machines
if os.environ.get("RUNC_CMD"):
    RUNC_CMD = os.environ.get("RUNC_CMD")

PODMAN_CLIENT = podman.from_env()
DOCKER_CLIENT = docker.from_env()


# Use subprocess to enter command into the container
def exec_into_container(container: str, command: str):  # container may be an object in the future

    if RUNC_CMD == "podman":
        PODMAN_CLIENT.containers.get(container).exec_run(cmd=["/bin/sh", "-c", command], stderr=True, stdout=True, stdin=False, tty=False)

        # create_res = session.post(
        #     create_url,
        #     json={
        #         "Cmd": ["/bin/sh", "-c", command],
        #         "AttachStdout": True,
        #         "AttachStderr": True,
        #         "AttachStdin": False,
        #         "Tty": False
        #     }
        # )         

    elif RUNC_CMD == "docker":
        DOCKER_CLIENT.containers.get(container_id=container).exec_run(cmd=["/bin/sh", "-c", command], stderr=True, stdout=True, stdin=False, tty=False)

        


# Parallel
# Find a way to get the list of container
# Spawn max X number of processes depending on # cores 
# Continue until all work is complete
# Send the command to a unique container from each process
def parallel_exec(containers: list[str], cmd: str | list[str]):     # container may be an object in the future

    max_workers = min(len(containers), multiprocessing.cpu_count())
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(lambda c: exec_into_container(c, cmd), containers))

# Function without ThreadPoolExecutor
def parallel_exec_wo_tpe(containers, cmd):
    processes = []

    for container in containers:
        full_cmd = f"{RUNC_CMD} exec {container} {cmd}"
        proc = subprocess.Popen(
            full_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        processes.append((container, proc))

    # Wait for all processes to finish
    for container, proc in processes:
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print(f"[ERROR] Container {container}: {stderr.decode().strip()}")





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
    execution_group.add_argument("-p", "--parallel", action="store_true", help="Run the command across the containers parallely.")
    execution_group.add_argument("-s", "--sequential", action="store_true", help="Run the command across the containers sequentially.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode") 
    args = parser.parse_args()

    os.environ['CCP_VERBOSE']='TRUE' if args.verbose else os.environ['CCP_VERBOSE']='TRUE'  


    if args.parallel and args.cmd:
        if args.all:
            containers = []
            
            if (RUNC_CMD == "podman"):
                # List containers
                containers = [image.id for image in PODMAN_CLIENT.containers.list()]

            elif RUNC_CMD == "docker":
                containers = [c.id for c in DOCKER_CLIENT.containers.list()]   # TODO: pass all=True to list stopped containers as well
            else:
                return
        
            parallel_exec(containers, args.cmd)
        
        elif args.containers:
            parallel_exec(args.containers, args.cmd)



if __name__ == "__main__":
    main()

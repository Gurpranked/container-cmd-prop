import argparse
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os
import json

RUNC_CMD = "podman"  # set by default on machines
if os.environ.get("RUNC_CMD"):
    RUNC_CMD = os.environ.get("RUNC_CMD")


# Use subprocess to enter command into the container
def exec_into_container(container: str, command: str):  # container may be an object in the future
    import requests_unixsocket
    session = requests_unixsocket.Session()     # creates a socket session for each container/thread

    if RUNC_CMD == "podman":
        # Create exec instance
        sock = f"/run/user/{os.getuid()}/podman/podman.sock".replace("/", "%2F")
        create_url = f"http+unix://{sock}/v4.7.0/libpod/containers/{container}/exec"

        create_res = session.post(
            create_url,
            json={
                "Cmd": ["/bin/sh", "-c", command],
                "AttachStdout": True,
                "AttachStderr": True,
                "AttachStdin": False,
                "Tty": False
            }
        )   
        
        create_res.raise_for_status()
        exec_id = create_res.json()['Id']

        # start the exec instance
        start_url = f"http+unix://{sock}/v4.7.0/libpod/exec/{exec_id}/start"
        start_res = session.post(start_url, json={"Detach": False})
        start_res.raise_for_status()

        if(start_res.text != ""):
            print(start_res.text)

    elif RUNC_CMD == "docker":
        sock = f"/var/run/docker.sock".replace("/", "%2F")
        create_url = f"http+unix://{sock}/containers/{container}/exec"

        create_res = session.post(
            create_url,
            json={
                "Cmd": ["/bin/sh", "-c", command],
                "AttachStdout": True,
                "AttachStderr": True,
                "AttachStdin": False,
                "Tty": False
            }
        )

        create_res.raise_for_status()
        exec = create_res.json()['Id']

        start_url = f"http+unix://{sock}/exec/{exec}/start"
        start_res = session.post(start_url, json={"Detach": False})
        start_res.raise_for_status()

        if start_res.text != "":
            print(start_res.text)

        


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
def parallel_exec_wo_tpe(containers: list[str], cmd):
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
    args = parser.parse_args()

    if args.parallel and args.cmd:
        if args.all:
            containers = []
            result = subprocess.run([RUNC_CMD, "ps", "--format", "json"], 
                                    stderr=subprocess.PIPE, 
                                    stdout=subprocess.PIPE
            ).stdout

            if (RUNC_CMD == "podman"):
                for cont in json.loads(result):             # Converts json into dict
                    if cont['Names'][0]:
                        containers.append(cont['Names'][0])
            elif RUNC_CMD == "docker":
                lines = result.splitlines()
                
                for line in lines:
                    containers.append(json.loads(line)['Names'])
            else:
                return
        
            parallel_exec(containers, args.cmd)
        
        elif args.containers:
            parallel_exec(args.containers, args.cmd)



if __name__ == "__main__":
    main()

import argparse


# Parallel Case
# Find a way to get the list of container
# Spawn X number of threads 
# Send the command to a unique container from each thread
# Join threads and complete
def parallel_exec(containers: list, cmd: str | list[str])


# Sequential case
# Parse given list of container
# For loop to send command to each container
def seq_exec(containers: list, cmd: str | list[str], )
    

def main():
    # Adding basic flags
    parser = argparse.ArgumentParser(description="Command line tool to execute commands in Docker/Podman containers sequentially or parallely.")
    parser.add_argument("-c", "--containers", action="store_true", help="The containers to pass the commands to.")
    parser.add_argument("", "--cmd", action="store_true", help="The commands to pass to the containers")
    parser.add_argument("-A", "--all", action="store_true", help="Pass the commands to all the containers.")
    parser.add_argument("-p", "--parallel", action="store_true", help="Run the command across the containers parallely.")
    parser.add_argument("-s", "--sequential", action="store_true", help="Run the command across the containers sequentially.")

if __name__ == "__main__":
    main()

# Parallel Case
# Find a way to get the list of container
# Spawn X number of threads 
# Send the command to a unique container from each thread
# Join threads and complete

# Sequential case
# Parse given list of container
# For loop to send command to each container

# Copyright 2025
# Author: Gurpreet Singh

import json
from podman import PodmanClient

URI path for libpod service. Unix Domain Socket (UDS). TCP not implemented by PodmanClient Package
uri = "unix:///run/user/1000/podman/podman.sock"

with PodmanClient(base_uri=uri) as client:
    version = client.version()
    print("Release: ", version["Version"])
    print("Compatible API: ", version["ApiVersion"])
    print("Podman API: ", version["Components"][0]["Details"]["ApiVersion"], "\n")
    # Gets containers and prints info
    for container in client.containers.list():
        # Get list of containers with refreshed metadata 
        container.reload()
        print(container, container.id, "\n")
        print(container, container.status, "\n")
        
        # available fields
        print(sorted(container.attrs.keys())


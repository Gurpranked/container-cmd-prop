# container-cmd-prop


## What is it
Container command propagation tool for Podman

[Podman SDK](https://podman-py.readthedocs.io/en/latest/)

## Features we want:
- [ ] Parallel and sequential command propagation
- [ ] Shell script support


## Default run
`ccp --containers pod1 pod2 pod3 --cmd "cd /etc/default/grub"`
- Sequential

Options:
- `-A`: All containers
- `--cmd`: Command to run or file URI
- `--containers`: Arg List or CSV file of all containers
- `-p`: Run in parallel across containers
- `-s`: Run sequentially across containers (random order)

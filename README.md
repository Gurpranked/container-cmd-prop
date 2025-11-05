# container-cmd-prop


## What is it
Container command propagation tool for Podman

[Podman SDK](https://podman-py.readthedocs.io/en/latest/)

## Features we want:
- [ ] Parallel and equential command propagation
- [ ] Shell script support
- [ ] Runtime checks for Podman and Docker

## Default run
`ccp --containers pod1 pod2 pod3 --cmd "cd /etc/default/grub"`
- Sequential

## Options:
| Containers (mutually exclusive) | Execution Mode (mutually exclusive) | Misc. |
| ---------- | -------------- | ----- |
| - `-A`, `--all`: All containers | `-p`: Run in parallel across containers | `-m`,`--cmd`: Command to run or file URI |
| `-c`,`--containers`: Arg List or CSV file of all containers | `-s`: Run sequntially across containers (random order) |`-v`: Verbose mode |

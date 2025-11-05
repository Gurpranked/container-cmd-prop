import shutil
import os
from main import verboseprint

def find_podman_socket():
    """
    Attempt to locate a valid Podman service socket.
    Checks rootless and root Podman socket paths.
    """
    # 1. Check environment variable override first
    socket_env = os.environ.get("PODMAN_SOCKET")
    if socket_env and os.path.exists(socket_env.replace("unix://", "")):
        return socket_env

    # 2. Check for rootless Podman socket (current user)
    uid = os.getuid()
    rootless_socket = f"unix:///run/user/{uid}/podman/podman.sock"
    if os.path.exists(rootless_socket.replace("unix://", "")):
        return rootless_socket

    # 3. Check for root (system-wide) Podman socket
    root_socket = "unix:///run/podman/podman.sock"
    if os.path.exists(root_socket.replace("unix://", "")):
        return root_socket

    # 4. Nothing found
    return None

 def check_podman():
    if shutil.which("podman"):
        verboseprint("✅ Podman binary exists.")
    else:
    
    socket_path = find_podman_socket()
    if not socket_path:
        print("Podman service: ❌ No socket found (Podman may not be running)")
        return false
    
    # Connection attempt via SDK
    try:
        with PodmanClient(base_url=socket_path) as client:
            version = client.version()
            verboseprint(f"Podman service: ✅ Running (version {version['Version']})")
            verboseprint(f"Podman service: {socket_path}")
            return true
    except Exception as e:
        print(f"Podman service: ❌ Could not connect ({e})")
        return false


import os
import subprocess


def _expand_key(private_key):
    if private_key is None:
        private_key = "id_rsa"
    if os.path.exists(private_key):
        return os.path.abspath(private_key)

    if "/" not in private_key:
        if private_key == "":
            private_key = "id_rsa"
        private_key_system = os.path.join(os.path.expanduser("~"), ".ssh", private_key)
        if os.path.exists(private_key_system):
            return os.path.abspath(private_key_system)

    raise ValueError(f"can not find {private_key}")


def _ssh_command(user, private_key, host, port):
    ssh = (
        f"ssh -o 'StrictHostKeyChecking=no' -i {private_key} -o 'BatchMode=yes'"
        f" -p {port} {user}@{host}"
    )
    return ssh


def _rsync_to(ssh_command, host, source, target=""):
    cmd = [
        "rsync",
        "-rav",
        "-e",
        ssh_command,
        source,
        f":{target}",
    ]
    subprocess.run(cmd)


def _rsync_from(ssh_command, host, source, target=""):
    cmd = [
        "rsync",
        "-rav",
        "-e",
        ssh_command,
        f":{source}",
        target,
    ]
    subprocess.run(cmd)


def copy_local_folder(source: str, target: str):
    """
    copies a folder with all files locally. this function is optimized for many
    files, especially on an hpc system.

    :param source: source folder
    :param target: target folder, the basename of ``source`` will be a subfolder in
                   ``target``.
    """
    if not os.path.exists(source):
        raise IOError(f"source folder {source} does not exist.")
    if not os.path.exists(target):
        raise IOError(f"source folder {target} does not exist.")
    if not os.path.isdir(source):
        raise IOError(f"source folder {source} is not a folder.")

    cmd = f"tar cf - {os.path.basename(source)} | {{ cd {target}; tar xf -; }}"
    subprocess.run(cmd, shell=True, cwd=os.path.dirname(source))

import inspect
import os
from contextlib import contextmanager

import portalocker

from .copy_utils import _expand_key, _rsync_from, _rsync_to, _ssh_command


@contextmanager
def BoundedSemaphore(
    n: int,
    timeout: float = 300,
    lock_directory: str = None,
    filename_pattern: str = None,
):
    """
    Contextmanager to implement a bounded semaphore.

    :param n: int, How many jobs/processes can execute the protected area at the same
              time.  The (n + 1)th and later job/process wait max ``timeout`` seconds.
              Else an error will be triggered.

    :param timeout: float, see decription of argument ``n``.

    :param lock_directory: str, per default this is ``~/.copy_guard_locks``.

    :param filename_pattern: str, per default this is the path to the script which
                             calls ``BoundedSemaphore`` including the full path plus
                             a string `-NN.lock` to enumerate locks, spaces are replaced
                             by ``_``.

    """
    directory = lock_directory if lock_directory is not None else _default_lock_folder()

    os.makedirs(directory, exist_ok=True)

    filename_pattern = (
        filename_pattern
        if filename_pattern is not None
        else _default_filename_pattern()
    )

    semaphore = portalocker.BoundedSemaphore(
        n, timeout=timeout, directory=directory, filename_pattern=filename_pattern
    )

    semaphore.acquire()
    try:
        yield
    finally:
        semaphore.release()


def _default_lock_folder():
    return os.path.expanduser(os.path.join("~", ".copy_guard_locks"))


def _default_filename_pattern():
    frame = inspect.currentframe()
    caller_script = frame.f_back.f_back.f_back.f_code.co_filename
    pattern = caller_script.replace("/", "_")
    return pattern + "-{number:02d}.lock"


class Connection:

    """
    Connection is an access object for ``rsync`` based copy operations.

    :param user: str, username on the remote computer.

    :param host: str, host name, e.g. ``remote.unixxx.com``.

    :param private_key: str, path to private key to use. If the path is just a filename
                        which does not exist in the current working folder, the
                        ``~/.ssh`` folder is searched for this filename.

    :param port: int, optional. optional port if the remote machine does not listen
                 on the default port 22.

    """

    def __init__(self, user: str, host: str, private_key: str, port: int = 22):
        self._host = host

        private_key = _expand_key(private_key)
        self._ssh_command = _ssh_command(user, private_key, host, port)

    def rsync_to(self, source: str, target: str):
        """
        copy from local machine to remote machine

        :param source: str, local file, folder of wildcard.
        :param target: str, remote file or folder.
        """
        _rsync_to(self._ssh_command, self._host, source, target)

    def rsync_from(self, source: str, target: str):
        """
        copy from remote machine to local machine

        :param source: str, remote file, folder of wildcard.
        :param target: str, local file or folder.
        """
        _rsync_from(self._ssh_command, self._host, source, target)

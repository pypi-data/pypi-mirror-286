import contextlib
import datetime
import getpass
import stat
from fnmatch import fnmatch
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

import paramiko

from .base import BaseSync, FileInformation

if TYPE_CHECKING:
    import plus_sync.config


class SFTPAccess(BaseSync):
    def __init__(self, sftp_config: 'plus_sync.config.SFTPConfig'):
        self.sftp_config = sftp_config
        self.sftp = SFTPClient.from_config(sftp_config)

    def _get_files(self, with_metadata=True):
        all_files = self.sftp.get_files()
        all_files = [
            FileInformation(
                path=f'{x.path}/{x.filename}', size=x.st_size, last_modified=datetime.datetime.fromtimestamp(x.st_mtime)
            )
            for x in all_files
        ]
        return all_files

    def get_content(self, file: FileInformation) -> bytes:
        with self.sftp.open(file.path, 'rb') as f:
            f.prefetch()
            return f.read()


class SFTPClient(paramiko.SFTPClient):
    def __init__(self, *args, **kwargs):
        self.cfg = None
        super().__init__(*args, **kwargs)

    @classmethod
    def from_config(cls, cfg: 'plus_sync.config.SFTPConfig'):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()

        ssh_config = paramiko.SSHConfig()
        user_config_file = Path('~/.ssh/config').expanduser()

        if user_config_file.exists():
            with user_config_file.open() as f:
                ssh_config.parse(f)
        host_config = ssh_config.lookup(cfg.host)
        key_filename = host_config.get('identityfile', None)

        try:
            ssh.connect(cfg.host, port=cfg.port, username=cfg.user, key_filename=key_filename)
        except paramiko.SSHException:
            password = getpass.getpass(f'Password for {cfg.user}@{cfg.host}: ')
            ssh.connect(cfg.host, username=cfg.user, password=password, port=cfg.port)
        sftp = cls.from_transport(ssh.get_transport())
        sftp.chdir(cfg.remote_folder)
        sftp.cfg = cfg

        return sftp

    @cache
    def get_files(self, folder='.') -> list[paramiko.SFTPAttributes]:
        files = []
        for item in self.listdir_attr(str(folder)):
            if any(fnmatch(item.filename, glob) for glob in self.cfg.globs):
                item.path = str(folder)
                files.append(item)
            elif stat.S_ISDIR(item.st_mode):
                with contextlib.suppress(OSError):
                    files.extend(self.get_files(Path(folder, item.filename)))
        return files

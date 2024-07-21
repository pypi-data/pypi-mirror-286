from pathlib import Path
from typing import Annotated

import typer
from tqdm import tqdm

from ...config import Config
from ..app import app
from ..helpers.typer import HashSubjectIDs


@app.command(no_args_is_help=True)
def sync(
    remote_name: Annotated[str, typer.Argument(help='The name of the remote to use.')],
    hash_subject_ids: HashSubjectIDs(),
    dry_run: Annotated[bool, typer.Option(help='Whether to do a dry run.')] = False,
    limit: Annotated[int, typer.Option(help='Limit the number of subjects to sync.')] = None,
):
    """
    Sync the data.
    """
    typer.echo('Syncing the data.')
    config = Config.from_cmdargs()
    sync = config.get_sync_by_name(remote_name)
    all_subjects = sync.get_all_subjects(hash=False)
    if limit:
        all_subjects = list(all_subjects)[:limit]

    all_files_subjects = sync.get_files_for_subjects(all_subjects)
    orig_files_mapping = {x: sync.get_local_file(x, hash_subject_ids=hash_subject_ids) for x in all_files_subjects}
    orig_files_n = len(orig_files_mapping)
    files_to_sync = {remote: local for remote, local in orig_files_mapping.items() if not remote.matches(local)}
    to_sync_n = len(files_to_sync)

    typer.echo(f'Found {orig_files_n} files, {to_sync_n} need syncing.')

    for remote_file, local_file in tqdm(files_to_sync.items()):
        local_path = Path(local_file.path)
        if dry_run:
            typer.echo(f'Would sync {remote_file.path} to {local_path}.')
        else:
            content = sync.get_content(remote_file)
            if not local_path.parent.exists():
                local_path.parent.mkdir(parents=True)
            with Path(local_path).open('wb') as f:
                f.write(content)

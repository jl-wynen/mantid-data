# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 mantiddata contributors (https://github.com/mantid-data)

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Iterable, Optional, Sequence

MANTID_REPO_URL = 'https://github.com/mantidproject/mantid.git'
MANTID_DATA_DIR = Path('Testing/Data')  # relative to repo base
MANTID_DATA_SUBDIRS = (Path('DocTest'), Path('SystemTest'), Path('UnitTest'))
MANTID_DATA_BASE_URL = 'https://testdata.mantidproject.org/ftp/external-data/MD5/'


@dataclass
class ChecksumFile:
    path: Path
    name: str


def _checksum_files_from_dir(folder: Path, prefix: Path) -> Iterable[ChecksumFile]:
    yield from map(lambda path: ChecksumFile(path=path, name=str(prefix / path.stem)),
                   filter(lambda path: path.suffix == '.md5', folder.iterdir()))
    for sub_folder in filter(lambda path: path.is_dir(), folder.iterdir()):
        yield from _checksum_files_from_dir(sub_folder, prefix / sub_folder.stem)


def _local_checksum_files(base_path: Path, sub_dirs: Sequence[Path]) -> Iterable[ChecksumFile]:
    for folder in map(lambda d: base_path / d, sub_dirs):
        yield from _checksum_files_from_dir(folder, Path(''))


def read_md5_file(filename: Path) -> str:
    with filename.open('r') as f:
        return f.read().strip()


def build_registry(out_file: Path, base_path: Path, sub_dirs: Sequence[Path]) -> None:
    print('Creating registry from', base_path)
    reg = {f.name: read_md5_file(f.path)
           for f in _local_checksum_files(base_path, sub_dirs)}
    with out_file.open('w') as f:
        for name, file_hash in reg.items():
            f.write(f'{name.replace(" ", "_")} md5:{file_hash} {MANTID_DATA_BASE_URL}{file_hash}\n')


def _checkout_mantid_data(target_dir: Path):
    subprocess.check_call(['git', 'clone', '--depth=1', '--filter=blob:none', '--sparse', MANTID_REPO_URL,
                           target_dir])
    subprocess.check_call(['git', 'sparse-checkout', 'set', MANTID_DATA_DIR], cwd=target_dir)


@contextmanager
def _optional_tempdir(path: Optional[Path]) -> Path:
    if path is None:
        with TemporaryDirectory() as d:
            yield Path(d) / 'mantid'
    else:
        yield path


@contextmanager
def _ensure_input_dir(input_dir: Optional[Path]) -> Path:
    if input_dir is not None and input_dir.exists():
        yield input_dir / MANTID_DATA_DIR
    else:
        with _optional_tempdir(input_dir) as d:
            _checkout_mantid_data(d)
            yield d / MANTID_DATA_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=Path, help='Input directory (base of Mantid repo)', default=None)
    parser.add_argument('-o', '--output', type=Path, help='Output registry file', default='registry.txt')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with _ensure_input_dir(args.input) as input_dir:
        build_registry(args.output, input_dir, MANTID_DATA_SUBDIRS)


if __name__ == '__main__':
    main()

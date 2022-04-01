# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 mantiddata contributors (https://github.com/mantid-data)

import importlib.metadata
try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

from importlib import resources
from pathlib import Path
from typing import Optional, Union

import pooch


def create(registry_file: Optional[Union[Path, str]] = None) -> pooch.Pooch:
    """
    Create a pooch.Pooch object for Mantid's data files.

    Parameters
    ----------
    registry_file:
        Path of a pooch registry file.
        Defaults to the file bundled with mantiddata.

    Returns
    -------
    :
        A pooch.Pooch instance.
    """
    inv = pooch.create(
        path=pooch.os_cache('mantid/test_data'),
        env='MANTID_DATA_DIR',
        retry_if_failed=3,
        base_url='https://testdata.mantidproject.org/ftp/external-data/MD5/',
        registry=None)
    if registry_file:
        inv.load_registry(registry_file)
    else:
        inv.load_registry(resources.path('mantiddata', 'registry.txt'))
    return inv

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 mantiddata contributors (https://github.com/mantid-data)

from importlib import resources
from pathlib import Path
from typing import Optional, Union

import pooch


def create(registry_file: Optional[Union[Path, str]]=None) -> pooch.Pooch:
    inv = pooch.create(
        path=pooch.os_cache('mantid/test_data'),
        env='MANTID_DATA_DIR',
        retry_if_failed=3,
        base_url='https://testdata.mantidproject.org/ftp/external-data/MD5/',
        registry=None
    )
    if registry_file:
        inv.load_registry(registry_file)
    else:
        inv.load_registry(resources.path('mantiddata', 'registry.txt'))
    return inv

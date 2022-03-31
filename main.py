from pathlib import Path
from typing import Optional, Union

import pooch


# IMPORTANT: spaces are replaced by _


def create(registry_file: Optional[Union[Path, str]]) -> pooch.Pooch:
    inv = pooch.create(
        path=pooch.os_cache('mantid/test_data'),
        env='MANTID_DATA_DIR',
        retry_if_failed=3,
        base_url='https://testdata.mantidproject.org/ftp/external-data/MD5/',
        registry=None
    )
    if registry_file:
        inv.load_registry(registry_file)
    return inv


def main():
    inv = create(Path('registry.txt'))
    print(inv.registry['PG3_characterization_2011_08_31-HR.txt'])
    p = inv.fetch('PG3_characterization_2011_08_31-HR.txt')
    with open(p, 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()

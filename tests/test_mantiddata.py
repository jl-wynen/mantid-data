# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 mantiddata contributors (https://github.com/mantid-data)

import mantiddata
import pytest


@pytest.fixture
def inventory():
    return mantiddata.create()


def test_PG3_characterization_2011_08_31_HR_txt_is_correct(inventory):
    expected = '''#S 1 characterization runs
#L frequency(Hz) center_wavelength(angstrom) bank_num vanadium_run empty_run vanadium_back d_min(angstrom) d_max(angstrom)
60 0.533  1 4866 0 5226 0.10  2.20 00000.00 16666.67
60 1.066  2 4867 0 5227 0.30  3.20  8333.33 25000.00
60 1.333  3 4868 0 5228 0.43  3.80 12500.00 29166.67	
60 1.599  4 4869 0 5229 0.57  4.25 16666.67 33333.33
60 2.665  5 4870 0 5230 1.15  6.50 33333.33 50000.00
60 3.731  6 4871 0 5232 1.70  8.50 50000.00 66666.67
60 4.797  7 4872 0 5233 2.00 10.30 66666.67 83333.67
30 1.066  1 4873 0 5234 0.10  4.20 00000.00 33333.33
30 3.198  2 4874 0 5235 1.15  8.25 33333.33 66666.67
30 5.330  3 4891 0 5236 2.00 12.50 66666.67 100000.0
10 3.198  1 4920 0 5315 0.10 12.50 00000.0 100000.0
'''
    with open(inventory.fetch('PG3_characterization_2011_08_31-HR.txt'), 'r') as f:
        content = f.read()

    assert content == expected

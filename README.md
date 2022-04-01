# mantiddata
Python package and command line utility for accessing Mantids' data files.

The package uses [pooch](https://www.fatiando.org/pooch/latest/index.html) to download and cache files.
See its documentation for more details on the concrete behaviour.

Note that some files have spaces in their name.
Those are replaced by underscores because pooch's registry files do not support spaces.

## Usage

### Access a file

Get the path to a file and download if necessary.
See https://www.fatiando.org/pooch/latest/multiple-files.html for more information.

#### Python

```python
import mantiddata
inventory = mantiddata.create()
path = inventory.fetch('PG3_characterization_2011_08_31-HR.txt')
# open and read file ...
```
`fetch` returns a path to the file in the local cache directory.

#### Command line
```shell
$ mantiddata fetch PG3_characterization_2011_08_31-HR.txt
/home/jl/.cache/mantid/test_data/PG3_characterization_2011_08_31-HR.txt
```
The concrete path will be different on your system.

Or use
```shell
$ mantiddata fetch -c PG3_characterization_2011_08_31-HR.txt
```
to print the file's contents.

### List files

#### Python
```python
import mantiddata
inventory = mantiddata.create()
reg = inventory.registry
# reg is a dict of file names to hashes
```
The `registry` is a regular Python dict whose keys are the known file names.
The dict values are hashes used to verify that files where downloaded correctly.

### (Re)Generate registry

#### Python
```python
from mantiddata.buildregistry import build_registry
build_registry(output_file='registry.txt')
```
See the docstring of `build_registry` for details.

#### Command line
```shell
$ mantiddata generate
```

## Customization

### Cache
The location of the file cache can be changed by setting the `MANTID_DATA_DIR` environment variable.

### Limit registry
In Python, `build_registry` can take arguments that can be used to limit what files make it into the registry.
See the doctring for more information.
Once you have a custom registry file, you can pass its path to `mantiddata.create`.

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 mantiddata contributors (https://github.com/mantid-data)

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path

from .buildregistry import build_registry
from . import create

_EPILOG = 'See https://github.com/jl-wynen/mantid-data'


def generate(args: Namespace) -> None:
    build_registry(input_dir=args.input, output_file=args.output)


def fetch(args: Namespace) -> None:
    inventory = create()
    path = inventory.fetch(args.name)
    if args.cat:
        with open(path, 'r') as f:
            print(f.read())
    else:
        print(path)


_COMMANDS = {'generate': generate, 'fetch': fetch}


def main():
    parser = ArgumentParser(prog='mantiddata', epilog=_EPILOG)
    subs = parser.add_subparsers(dest='command', required=True)

    gen_parser = subs.add_parser(
        'generate',
        help='Build a new file registry',
        formatter_class=RawTextHelpFormatter,
        epilog=_EPILOG,
        description='Generate a registry of Mantid\'s data files. \n\n'
        'INPUT can point to a source tree of the Mantid '
        'repository in the local filesystem. '
        'If it is not given, the repository will be cloned temporarily.')
    gen_parser.add_argument('-i',
                            '--input',
                            type=Path,
                            help='Input directory (base of Mantid repo)',
                            default=None)
    gen_parser.add_argument('-o',
                            '--output',
                            type=Path,
                            help='Output registry file, default: registry.txt',
                            default='registry.txt')

    fetch_parser = subs.add_parser(
        'fetch',
        help='Access a file',
        epilog=_EPILOG,
        description='Access a data file. Downloads the file if necessary.')
    fetch_parser.add_argument('name', help='Name of the file', type=str)
    fetch_parser.add_argument('-c',
                              '--cat',
                              help='Print the file\'s contents to STDOUT',
                              action='store_true')

    args = parser.parse_args()
    _COMMANDS[args.command](args)


if __name__ == '__main__':
    main()

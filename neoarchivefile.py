#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2018-2024 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2018-2024 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2018-2024 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: neoarchivefile.py - Last Update: 3/7/2025 Ver. 0.19.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import argparse
import pyarchivefile

__project__ = pyarchivefile.__project__
__program_name__ = pyarchivefile.__program_name__
__file_format_name__ = pyarchivefile.__file_format_name__
__file_format_magic__ = pyarchivefile.__file_format_magic__
__file_format_len__ = pyarchivefile.__file_format_len__
__file_format_hex__ = pyarchivefile.__file_format_hex__
__file_format_delimiter__ = pyarchivefile.__file_format_delimiter__
__file_format_dict__ = pyarchivefile.__file_format_dict__
__file_format_default__ = pyarchivefile.__file_format_default__
__use_new_style__ = pyarchivefile.__use_new_style__
__use_advanced_list__ = pyarchivefile.__use_advanced_list__
__use_alt_inode__ = pyarchivefile.__use_alt_inode__
__project_url__ = pyarchivefile.__project_url__
__version_info__ = pyarchivefile.__version_info__
__version_date_info__ = pyarchivefile.__version_date_info__
__version_date__ = pyarchivefile.__version_date__
__version_date_plusrc__ = pyarchivefile.__version_date_plusrc__
__version__ = pyarchivefile.__version__

# Compatibility layer for Python 2 and 3 input
try:
    input = raw_input
except NameError:
    pass

# Determine if rar file support is enabled
rarfile_support = pyarchivefile.rarfile_support
py7zr_support = pyarchivefile.py7zr_support

# Set up the argument parser
argparser = argparse.ArgumentParser(
    description="Manipulates archive files for various operations like creation, extraction, and validation.")
argparser.add_argument("-V", "--version", action="version", version="{0} {1}".format(
    __program_name__, __version__), help="Displays the program's version.")
argparser.add_argument("-i", "--input", nargs="+", required=True,
                       help="Specifies input file(s) for processing.")
argparser.add_argument(
    "-o", "--output", help="Specifies the output file name.")
argparser.add_argument("-d", "--verbose", action="store_true",
                       help="Enables verbose mode for detailed information.")
argparser.add_argument("-c", "--create", action="store_true",
                       help="Creates a new archive file from input.")
argparser.add_argument("-e", "--extract", action="store_true",
                       help="Extracts files from a archive archive.")
argparser.add_argument("-l", "--list", action="store_true",
                       help="Lists contents of a specified archive file.")
argparser.add_argument("-r", "--repack", action="store_true",
                       help="Repacks an existing archive file.")
argparser.add_argument("-v", "--validate", action="store_true",
                       help="Validates a archive file's integrity.")
argparser.add_argument("--checksum", default="crc32",
                       help="Specifies the checksum type (default: crc32).")
argparser.add_argument("--compression", default="auto",
                       help="Specifies the compression method (default: auto).")
argparser.add_argument("--level", help="Specifies the compression level.")
argparser.add_argument("--preserve", action="store_true",
                       help="Preserves file attributes when extracting.")
argparser.add_argument("--convert", choices=['tar', 'zip', '7zip', 'rar'],
                       help="Convert from an archive format (tar, zip, 7zip, rar) to a archive file.")
args = argparser.parse_args()

# Determine the primary action based on user input
primary_action = None
if args.create:
    primary_action = 'create'
elif args.repack:
    primary_action = 'repack'
elif args.extract:
    primary_action = 'extract'
elif args.list:
    primary_action = 'list'
elif args.validate:
    primary_action = 'validate'
input_file = args.input[0]
# Functionality mappings
if primary_action == 'create':
    if args.convert == 'tar':
        pyarchivefile.PackArchiveFileFromTarFile(input_file, args.output, args.compression, args.level, pyarchivefile.compressionlistalt, [args.checksum, args.checksum, args.checksum, args.checksum], [
        ], pyarchivefile.__file_format_dict__, args.verbose, False)
    elif args.convert == 'zip':
        pyarchivefile.PackArchiveFileFromZipFile(input_file, args.output, args.compression, args.level, pyarchivefile.compressionlistalt, [args.checksum, args.checksum, args.checksum, args.checksum], [
        ], pyarchivefile.__file_format_dict__, args.verbose, False)
    elif py7zr_support and args.convert == '7zip':
        pyarchivefile.PackArchiveFileFromSevenZipFile(input_file, args.output, args.compression, args.level, pyarchivefile.compressionlistalt, [args.checksum, args.checksum, args.checksum, args.checksum], [
        ], pyarchivefile.__file_format_dict__, args.verbose, False)
    elif rarfile_support and args.convert == 'rar':
        pyarchivefile.PackArchiveFileFromRarFile(input_file, args.output, args.compression, args.level, pyarchivefile.compressionlistalt, [args.checksum, args.checksum, args.checksum, args.checksum], [
        ], pyarchivefile.__file_format_dict__, args.verbose, False)
    else:
        pyarchivefile.PackArchiveFile(args.input, args.output, args.verbose, args.compression, args.level, pyarchivefile.compressionlistalt,
                                  False, [args.checksum, args.checksum, args.checksum, args.checksum], [], {}, pyarchivefile.__file_format_dict__, args.verbose, False)
elif primary_action == 'repack':
    pyarchivefile.RePackArchiveFile(
        input_file, args.output, args.compression, args.level, pyarchivefile.compressionlistalt, [args.checksum, args.checksum, args.checksum, args.checksum], False, args.verbose)
elif primary_action == 'extract':
    pyarchivefile.UnPackArchiveFile(
        input_file, args.output, False, args.verbose, args.preserve)
elif primary_action == 'list':
    if args.convert == 'tar':
        pyarchivefile.TarFileListFiles(input_file, verbose=args.verbose)
    elif args.convert == 'zip':
        pyarchivefile.ZipFileListFiles(input_file, verbose=args.verbose)
    elif args.convert == '7zip':
        pyarchivefile.SevenZipFileListFiles(input_file, verbose=args.verbose)
    elif rarfile_support and args.convert == 'rar':
        pyarchivefile.RarFileListFiles(input_file, verbose=args.verbose)
    else:
        pyarchivefile.ArchiveFileListFiles(input_file, verbose=args.verbose)
elif primary_action == 'validate':
    is_valid = pyarchivefile.ArchiveFileValidate(input_file, verbose=args.verbose)
    result_msg = "Validation result for {0}: {1}".format(
        input_file, 'Valid' if is_valid else 'Invalid')
    print(result_msg)

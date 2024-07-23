from typing import Callable
from collections import namedtuple

import os
import re
import sys
import dataclasses
import platform
import argparse
import textwrap

from . import parse


@dataclasses.dataclass
class SubCommand:
    name: str
    func: Callable
    category: str
    helptext: str


categories = {
    'image': 'Image Processing',
    'cortex': 'Cortical Surface Processing',
    'dev': 'Development Tools',
}
subcommands = {}


def subcommand(name, category, help):
    """
    Decorator generator that registers a function as a subcommand.
    """
    def decorator(func):
        if category not in categories:
            raise ValueError(f'{category} is not a valid subcommand category. must '
                             f'be one of {subcommands.keys()}')
        if name in subcommands:
            raise ValueError(f'subcommand {name} is already registered')
        subcommands[name] = SubCommand(name, func, category, help)
        return func
    return decorator


def execute():
    """
    Parse the commandline inputs
    """

    # print help and error out if no subcommand is given
    if len(sys.argv) < 2:
        print_help_text()
        return 1

    # get the subcommand
    sc = sys.argv[1]

    # it's possible that a user might run --help, so we should check for this
    if sc.replace('-', '') == 'help':
        return print_help_text()

    # make sure that the given subcommand exists
    matched = subcommands.get(sc)
    if matched is None:
        print(f"error: '{sc}' is not a known deepsurfer subcommand. Run "
               "'deepsurfer help' to output a list of available tools.")
        return 1

    # run the function and return its result
    retcode = matched.func()
    if retcode is None:
        retcode = 0
    return retcode


def help_text_description():
    """
    Help text printed before the subcommand list.
    """
    text = '''
    Learning-based toolbox for brain image analysis.

    The collection of tools is listed below. For more info on each of the
    available methods, append the --help flag to the corresponding subcommand.
    '''
    return text


def help_text_epilogue():
    """
    Help text printed after the subcommand list.
    """
    text = """
    Note that the methods implemented in this package are experimental and
    should not be used for formal analysis without substantial review
    of the outputs.

    For more information, visit the readme at github.com/freesurfer/deepsurfer
    """
    return text


def print_help_text():
    """
    Print complete help text for the base deepsurfer command.
    """

    # print the command usage and introduction
    print(parse.bold('USAGE:'), 'ds <subcommand> [options]\n')
    print(parse.formatted(help_text_description()))

    # group subcommands by their categories and sort alphabetically
    grouped = {k: [] for k, v in categories.items()}
    for _, cmd in sorted(subcommands.items()):
        grouped[cmd.category].append(cmd)

    # cycle through each subcommand and print its help text
    for category, cmds in grouped.items():
        print(f'\n{parse.bold(categories[category].upper())}')
        for cmd in cmds:
            print(parse.formatted(cmd.helptext, preface=cmd.name, indent=20))

    # print the epilogue
    print()
    print(parse.formatted(help_text_epilogue()))

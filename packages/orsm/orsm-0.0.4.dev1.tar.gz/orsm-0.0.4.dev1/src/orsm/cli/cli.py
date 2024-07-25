#!/usr/bin/env python3
"""
Tools for constructing a nice CLI.
"""

import argparse
import sys

from orsm.logger.logger import log as logging
from orsm.logger.logger import set_logging_level, redirect_logging_to_file, suppress_console_output, remove_console_output
from orsm.cli import repo
from textwrap import dedent
from pathlib import Path


class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


verbosity_level = None


def set_verbosity_level(level):
    class SetVerbosityAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            global verbosity_level
            if verbosity_level is not None:
                logging.warning(f"We are trying to set the verbosity level more than once, and are honouring only the first flag.")
            else:
                set_logging_level(level=level)
                verbosity_level = level

    return SetVerbosityAction


class Predicate:

    def __init__(self, value=None, /):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


profiling_disabled = Predicate(True)


class SetProfiling(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        global profiling_disabled
        logging.info(f"Enabling profiling decorators.")
        profiling_disabled.value = False


class SetLogFileAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        filename = "" if values is None else values
        assert filename is not None
        assert isinstance(filename, str)
        redirect_logging_to_file(filename=filename)


class SetConsoleSuppression(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        remove_console_output()
        suppress_console_output()


class ShowVersion(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        print(repo.repo_version())
        sys.exit(0)


class PathToFile(argparse.Action):
    """
    Checks a paths point to an existing file.
    """
    def __call__(self, parser, args, values, option_string=None):
        assert isinstance(values, str) and str
        file_path = Path(values)
        assert file_path.exists(), f"{file_path = } does not exist."
        assert file_path.is_file(), f"{file_path = } is not a file."
        setattr(args, self.dest, file_path)


class PathToDir(argparse.Action):
    """
    Checks a paths point to an existing directory.
    """
    def __call__(self, parser, args, values, option_string=None):
        assert isinstance(values, str) and str
        file_path = Path(values)
        assert file_path.exists(), f"{file_path = } does not exist."
        assert file_path.is_dir(), f"{file_path = } is not a directory."
        setattr(args, self.dest, file_path)


def setup_standard_parser(*argparse_args, **argparse_kwargs) -> argparse.ArgumentParser:
    """
    Sets up a standard argument parser.

    Parameters
    ----------
    argparse_args :
        Positional combinations passed to the parser.
    argparse_kwargs :
        Keyword combinations passed to the parser.

    Returns
    -------
    argparse.ArgumentParser:
        An argument parser.

    """
    epilogue = dedent(f"""
    Version: 
        {repo.repo_name()} {repo.repo_version()}
        
    Author: 
        {repo.repo_author()}
        
    Maintained by: 
        {repo.repo_author()}
        <{repo.repo_email()}>
    """)
    parser = argparse.ArgumentParser(*argparse_args, **argparse_kwargs, formatter_class=HelpFormatter, allow_abbrev=False, epilog=epilogue)
    parser.add_argument("--version", help="Show the version of this program.", action=ShowVersion, nargs=0)
    # How we want to control the logging.
    parser.add_argument("--trace", help="Enable program tracing. Extremely verbose!", action=set_verbosity_level(logging.TRACE), nargs=0)
    parser.add_argument("--debug", help="Enable debug logging. Very verbose!", action=set_verbosity_level(logging.DEBUG), nargs=0)
    parser.add_argument("--verbose", help="Enable verbose logging. Quite verbose!", action=set_verbosity_level(logging.INFO), nargs=0)
    parser.add_argument("--quiet", help="Supress all logging. Quite quiet!", action=set_verbosity_level(logging.WARNING), nargs=0)
    parser.add_argument("--silent", help="Suppress most logging and output. Absolutely silent!", action=set_verbosity_level(logging.ERROR), nargs=0)
    parser.add_argument("--log_files", type=str, metavar="FILENAME", help="Store log output to files. Split into regular output and error output.", action=SetLogFileAction, nargs="?")
    parser.add_argument("--suppress_console_output", help="Whether to suppress output to the console.", action=SetConsoleSuppression, nargs=0)
    parser.add_argument("--profiling", help="Show results from profilers", action=SetProfiling, nargs=0)
    return parser


def standard_parse(*argparse_args, **argparse_kwargs) -> argparse.Namespace:
    """
    Perform a standard parse.

    Parameters
    ----------
    argparse_args :
        Positional combinations passed to the parser.
    argparse_kwargs :
        Keyword combinations passed to the parser.

    Returns
    -------
    argparse.Namespace:
        The namespace generated from the standard parse.

    """
    parser = setup_standard_parser(*argparse_args, **argparse_kwargs)
    return parser.parse_args()


def unit_test_parse(*argparse_args, **argparse_kwargs) -> None:
    """
    Parse command line ahead of forwarding onto the unittests.

    Notes
    -----
        To allow our command line combinations to be parsed ahead of running unit tests. Useful for logging.
        Taken from: https://stackoverflow.com/a/44248445/5134817

    Parameters
    ----------
    argparse_args :
        Positional combinations passed to the parser.
    argparse_kwargs :
        Keyword combinations passed to the parser.

    Returns
    -------
    None:

    """
    import sys
    import unittest
    parser = setup_standard_parser(*argparse_args, **argparse_kwargs)
    ns, parsed_args = parser.parse_known_args(namespace=unittest)
    sys.argv[:] = sys.argv[:1] + parsed_args

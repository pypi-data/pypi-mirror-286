"""The probullstats package CLI."""

from __future__ import annotations

import argparse
import sys

from probullstats import __name__ as program_name
from probullstats import __version__ as program_version


def create_parser() -> argparse.ArgumentParser:
    """Create an input configuration parser.

    Returns:
        argparse.ArgumentParser: An input configuration parser.

    Examples:
        A parser can be used as is, have argument groups added, or have subparsers added.

        >>> parser = create_parser()
        >>> parser.parse_args()
        Namespace()
    """
    parser = argparse.ArgumentParser(
        prog=program_name,
        description=(
            "Pull data from the ProBullStats website and collate raw data to create reports or do custom analysis."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{program_version}")
    parser.add_argument("-f", "--fail", action="store_true", help="Placeholder until real functionality implemented.")

    return parser


def main(args: argparse.Namespace) -> int:
    """Scriptable entrypoint.

    Args:
        args (argparse.Namespace): Parsed script configuration input.

    Returns:
        int: The returncode.  Zero for success, non-zero otherwise.

    Examples:
        >>> parser = create_parser()
        >>> args = parser.parse_args()
        >>> main(args)
        0
    """
    if args.fail:
        sys.stdout.write("The '-f' switch was set.")
        return 1

    sys.stdout.write("Everything is hunky-dory.")
    return 0


def cli() -> None:
    """Main entrypoint for terminal execution."""
    parser = create_parser()
    args = parser.parse_args()

    # TODO(guyhoozdis): Catch unhandled exceptions here
    # https://github.com/ubcotx/probullstats/issues/2
    returncode = main(args)

    sys.exit(returncode)

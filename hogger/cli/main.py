import argparse
import os

from hogger.cli import apply

VERSION = "v0.1.0"


def main():
    parser = argparse.ArgumentParser(
        description="A declarative way to manage your MMO database",
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the 'apply' command
    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply the files to the database",
    )
    apply_parser.add_argument(
        "dir_or_file",
        help="Path to a file or folder where hogger should be invoked from",
    )
    apply_parser.add_argument(
        "-H",
        "--host",
        metavar="HOGGER_HOST",
        help="Database hostname (default='127.0.0.1')",
        default=os.getenv("HOGGER_HOST", "127.0.0.1"),
    )
    apply_parser.add_argument(
        "-P",
        "--port",
        type=int,
        metavar="HOGGER_PORT",
        help="Database port (default='3306')",
        default=os.getenv("HOGGER_PORT", "3306"),
    )
    apply_parser.add_argument(
        "-u",
        "--user",
        metavar="HOGGER_USER",
        help="Database username (default='acore')",
        default=os.getenv("HOGGER_USER", "acore"),
    )
    apply_parser.add_argument(
        "-p",
        "--pass",
        dest="password",
        metavar="HOGGER_PASS",
        help="Database password (default='acore')",
        default=os.getenv("HOGGER_PASS", "acore"),
    )
    apply_parser.add_argument(
        "-w",
        "--world",
        dest="world",
        metavar="HOGGER_WORLD",
        help="Name of the world database (default='acore_world')",
        default=os.getenv("HOGGER_WORLD", "acore_world"),
    )
    apply_parser.add_argument(
        "-y",
        "--skip-confirmation",
        dest="skip_confirmation",
        action="store_true",
        help="Hogger will apply changes without asking",
    )

    # Subparser for the 'destroy' command
    destroy_parser = subparsers.add_parser(
        "destroy",
        help="Apply the files to the database",
    )

    # Subparser for the 'destroy' command
    version_parser = subparsers.add_parser(
        "version",
        help="Print the current version of Hogger",
    )

    args = parser.parse_args()
    if args.command == "apply":
        apply(**vars(args))
    elif args.command == "init":
        pass
    elif args.command == "destroy":
        pass
    elif args.command == "version":
        print(f"Hogger {VERSION}")
    else:
        parser.print_help()

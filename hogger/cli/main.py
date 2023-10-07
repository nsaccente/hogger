import argparse
import os

from hogger.cli import apply


VERSION = "v0.1.0"

def main():
    parser = argparse.ArgumentParser(
        description="A declarative way to manage your WoW database"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the 'apply' command
    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply the files to the database",
    )
    apply_parser.add_argument(
        "dir_or_file",
        help="path to a file or folder where hogger should be invoked from",
    )
    apply_parser.add_argument(
        "--host",
        help="Database hostname (default=localhost)",
        default=os.getenv("HOGGER_DB_HOST", "127.0.0.1"),
    )
    apply_parser.add_argument(
        "--port",
        type=int,
        help="Database port (required)",
        default=os.getenv("HOGGER_DB_PORT", "3306"),
    )
    apply_parser.add_argument(
        "--user",
        help="Database username (required)",
        default=os.getenv("HOGGER_DB_USER", "acore"),
    )
    apply_parser.add_argument(
        "--pass",
        dest="password",
        help="Database password (optional)",
        default=os.getenv("HOGGER_DB_PASS", "acore"),
    )
    apply_parser.add_argument(
        "--world",
        dest="world",
        help="name of the world database",
        default=os.getenv("HOGGER_DB_WORLD", "acore_world"),
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
    elif args.command == "destroy":
        pass
    elif args.command == "version":
        print(f"Hogger {VERSION}")
    else:
        parser.print_help()

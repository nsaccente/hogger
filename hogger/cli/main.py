import argparse
import os

from hogger.cli import apply


def main():
    parser = argparse.ArgumentParser(
        description="A declarative way to manage your WoW database"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the 'apply' command
    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply the blob to the database",
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

    args = parser.parse_args()
    if args.command == "apply":
        apply(**vars(args))
    elif args.command == "destroy":
        pass
    else:
        parser.print_help()

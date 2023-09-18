import argparse

from src.apply import apply


def main():
    parser = argparse.ArgumentParser(description="A declarative way to manage your WoW database")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the 'apply' command
    apply_parser = subparsers.add_parser(
        "apply", 
        help="Apply the blob to the database", 
    )
    apply_parser.add_argument(
        "file", 
        help="Filesystem blob string (required)",
    )
    apply_parser.add_argument(
        "--host", 
        help="Database hostname (default=localhost)", 
        default="127.0.0.1",
    )
    apply_parser.add_argument(
        "--port",
        type=int, 
        help="Database port (required)", 
        default="3306",
    )
    apply_parser.add_argument(
        "--user", 
        help="Database username (required)", 
        default="acore",
    )
    apply_parser.add_argument(
        "--pass", 
        dest="password", 
        help="Database password (optional)", 
        default="acore",
    )
    apply_parser.add_argument(
        "--database", 
        help="Database name (required)",
        default="acore_world"
    )

    args = parser.parse_args()
    if args.command == "apply":
        apply(**vars(args))
    elif args.command == "destroy":
        pass
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

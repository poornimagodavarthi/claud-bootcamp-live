#!/usr/bin/env python3

import argparse
import sys


class UserError(Exception):
    """Raised for invalid user input."""
    pass


def cmd_hello(args):
    """Handle the 'hello' subcommand."""
    greeting = f"Hello, {args.name}!"
    if args.upper:
        greeting = greeting.upper()
    print(greeting)


def main() -> int:
    parser = argparse.ArgumentParser(description="A simple greeting CLI")
    subparsers = parser.add_subparsers(dest="command", help="subcommands")

    # 'hello' subcommand
    hello_parser = subparsers.add_parser("hello", help="Greet someone")
    hello_parser.add_argument("name", help="Name to greet")
    hello_parser.add_argument(
        "--upper", action="store_true", help="Uppercase the greeting"
    )
    hello_parser.set_defaults(func=cmd_hello)

    args = parser.parse_args()

    try:
        if not hasattr(args, "func"):
            parser.print_help()
            return 1
        args.func(args)
        return 0
    except UserError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Internal error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

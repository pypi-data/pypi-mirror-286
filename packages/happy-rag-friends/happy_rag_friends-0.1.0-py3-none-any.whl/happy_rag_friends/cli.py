"""Command-line utility for starting the web app"""

import argparse

from happy_rag_friends import create_app

app = create_app()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("action")
    args = arg_parser.parse_args()
    if args.action == "serve":
        app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()

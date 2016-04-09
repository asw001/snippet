#!/usr/bin/python3
import logging
import argparse

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    store a snippet with an associate name.

    Returns the name and snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def main():
    """"Main funcion"""
    logging.info("Constructing Parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")

    arguments = parser.parse_args()

if __name__ == "__main__":
    main()

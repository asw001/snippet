#!/usr/bin/python3

import logging
import argparse
import psycopg2

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")


def put(name, snippet):
    """
    store a snippet with an associate name.

    Returns the name and snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.info("Storing retrieving snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "select keyword, message from snippets where keyword = %s"
    cursor.execute(command, (name,))
    return_set = cursor.fetchone()[1]
    logging.debug("Snippet stored successfully.")
    return return_set


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
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

if __name__ == "__main__":
    main()

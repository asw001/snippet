#!/usr/bin/python3

import logging
import argparse
from psycopg2.extensions import AsIs
import psycopg2
import sys

def initialize_db(database_name):
    """ constructs database object for reuse """
    
    logging.debug("Connecting to PostgreSQL")
    
    try:
        connection = psycopg2.connect(database=database_name)
    except psycopg2.OperationalError:
        print("Could not connect to {} ...exiting".format(database_name))
        logging.error("Could not connect to {} ...exiting".format(database_name))
        sys.exit()
    
    logging.debug("Database connection established.")
    return connection    
        
def put(database_name, tablename, name, snippet):
    """
    store a snippet with an associated name

    Returns the name and snippet
    """
    connection = initialize_db(database_name)
    
    logging.info("Storing snippet {!r}: {!r} in {!r} database, in table {!r}".format(name, snippet, database_name, tablename))
    cursor = connection.cursor()
    command = "insert into %s values (%s, %s)"
    
    try:
        cursor.execute(command, (AsIs(tablename), name, snippet))
        connection.commit()
        cursor.close()
    except psycopg2.IntegrityError:
        connection.rollback()
        command = "update %s set message=%s where keyword=%s"
        cursor.execute(command, (AsIs(tablename), snippet, name))
        connection.commit()
        cursor.close()
        logging.info("Keyword is present, converted insert to update")
    except psycopg2.ProgrammingError:
        print("Error with SQL statement")
        logging.error("Error with SQL statement")
        connection.rollback()
        return
        
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(database_name, tablename, name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    
    logging.info("Retrieving snippet {!r}: {!r}".format(tablename, name))
    connection = initialize_db(database_name)
    cursor = connection.cursor()
    command = "select keyword, message from %s where keyword = %s"
    
    try:
        cursor.execute(command, (AsIs(tablename), name)) # AsIs needed to not interpolate the table name; quotes will cause the execution to fail
        try:
            return_set = cursor.fetchall()[0][1] # skipped the 'with' invocation because the cursor is closed before 'return_set' can be evaluated 
            cursor.close()
            connection.commit() # present in try and except block, would be more 'pretty' to do this once, but early return
        except IndexError:
            print("No record with keyword {}".format(name))
            logging.error("No record with keyword {}".format(name))
            cursor.close()
            connection.rollback()
            return
    except psycopg2.ProgrammingError:
        print("Error with SQL statement")
        logging.error("Error with SQL statement")
        connection.rollback()
        return
    
    logging.debug("Snippet for {} retrieved successfully.".format(name))
    return return_set


def main():
    """"Main funcion"""
    
    logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
    logging.info("Constructing Parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("database_name", help="Name of the database")
    put_parser.add_argument("tablename", help="Name of database table")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    # subparser for get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("database_name", help="Name of the database to be queried")
    get_parser.add_argument("tablename", help="Name of the database table")
    get_parser.add_argument("name", help="Name of the snippet")
    
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

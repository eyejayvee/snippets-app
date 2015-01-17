import sys, logging, argparse
import psycopg2

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL.")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def get(name):

    logging.info("Getting snippet {}.".format(name))

    cursor = connection.cursor()
    command = "select message from snippets where keyword=%s"
    name_tuple = (name,) # turn name into a one item tuple
    cursor.execute(command, name_tuple)
    connection.commit()
    row = cursor.fetchone()
    
    if row:
    
        logging.debug("Snippet got successfully.")
        print(row[0])
        return
    
    logging.debug("Snippet '{}' requested, but didn't exist.".format(name))
    raise IOError("no snippet named '{}'".format(name))

def put(name, snippet):

    logging.info("Storing snippet {}: {}.".format(name, snippet))

    with connection, connection.cursor() as cursor:
      command = "insert into snippets values (%s, %s)"
      cursor.execute(command, (name, snippet))
    
    try: cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError:
        
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))
        
    connection.commit()

    message = "Snippet put successfully."
    logging.debug(message)
    print(message)

def main():

    logging.info("Constructing the parser.")

    parser = argparse.ArgumentParser(description="Manage text snippets.")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
        )

    logging.debug("Constructing the `get` subparser.")

    get_parser = subparsers.add_parser("get", help="get a snippet")
    get_parser.add_argument("name", help="The name of the snippet.")

    logging.debug("Constructing the `put` subparser.")
    
    put_parser = subparsers.add_parser("put", help="put a snippet")
    put_parser.add_argument("name", help="The name of the snippet.")
    put_parser.add_argument("snippet", help="The snippet text.")
    
    logging.debug("Parsing command line arguments.")

    arguments = vars(parser.parse_args(sys.argv[1:]))
    command = arguments.pop("command") # get the `command` argument

    get(**arguments) if command == "get" else put(**arguments)

if __name__ == "__main__": main()

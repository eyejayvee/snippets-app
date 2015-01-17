import logging
import argparse
import sys
import psycopg2

#Set the output file, and log the level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

#Connect to the database
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
  '''
  Store a snippet with an associated name. 
  Returns the name of the snippet
  '''
  logging.info("Storing put snippet ({!r}: {!r})".format(name, snippet))
  # Add the database bits as suggested in Unit 2 Lesson 1.4
  cursor = connection.cursor()
    
  try:
    print "in try"
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
  except psycopg2.IntegrityError as e:
    print "In fail"
    connection.rollback()
    command = "update snippets set message=%s where keyword=%s"
    cursor.execute(command, (snippet, name))
    
  # Don't forget the commit
  connection.commit()
  
  print snippet
  
  logging.debug("Snippet stored successfully.")
  return name, snippet

def get(name):
  '''
  Retrieve the snippet with a given name.
  If there is no such snippet... # Discuss with Carl (return a blank string?)
  Return the snippet.
  '''
  logging.info("Getting snippet {!r}".format(name))
  #Add the database connection and command statement for the challenge in Unit 2 lesson 1.4
  # Added a change - the with - as per unit 2 lesson 1 point 5
  with connection, connection.cursor() as cursor:
    cursor.execute("SELECT * FROM snippets WHERE keyword = %s", (name,))
    row = cursor.fetchone()
    #logging.debug("COMMAND: ".format(command))
    
  connection.commit()
  logging.debug("Select snippet retrieved the record successfully.")

## Discuss this error handling with Carl  
  if not row:
    logging.debug("The requested snippet '{}' does not exist.".format(name))
    raise IOError("no snippet named '{}'".format(name))
   
  print row[1]
  
  return row[0]

# Add a snippet for delete?
def delete(name):
  logging.error("FIXME: Unimplemented - delete({!r})".format(name))
  return name

def main():
    """
    Main function
    """
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #Subparser for the put command
    logging.debug("Constructing 'put' subparser")
    put_parser = subparsers.add_parser("put", help="Store 'put' a snippet")
    put_parser.add_argument("name", help="The name of the 'put' snippet")
    put_parser.add_argument("snippet", help="The 'put' snippet text")
    
    #Subparser for the get command
    logging.debug("Constructing the 'get' subparser")
    get_parser = subparsers.add_parser("get", help="Store a 'get' snippet")
    get_parser.add_argument("name", help="The name of the 'get' snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    #Convert parsed arguments from the Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
      result = get(**arguments)
      print("Retrieved snippet: {!r}".format(result))

if __name__ == "__main__":
    main()
  
  
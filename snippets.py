## TODO: Do the addional challenge in Unit 2 Lesson 1 Point 5

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
  # changed the cursor by adding a with as described in Unit 2 Lesson 1.5
  with connection, connection.cursor() as cursor:
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))

  ## I have removed the try / except becaus the with does the rollback but not the UPDATE. I am a little confused by that
  ## TODO: Chat with Carl
    
#  try:
#    #print "in try"
#    command = "insert into snippets values (%s, %s)"
#    cursor.execute(command, (name, snippet))
#  except psycopg2.IntegrityError as e:
#    #print "In fail"
#    connection.rollback()
#    command = "update snippets set message=%s where keyword=%s"
#    cursor.execute(command, (snippet, name))
    
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

# Added for Unit 2 Lesson 1 Point 5
def catalog():
  logging.info("Retrieving all of the keywords for review.")
  
  with connection, connection.cursor() as cursor:
    cursor.execute("SELECT keyword FROM snippets ORDER BY keyword")
    rows = cursor.fetchall()
    
  connection.commit()
  
  print rows

# Add a snippet for delete?
def search(snippet):
  '''
  Retrieve the snippet with the text that the user provides as search criteria.
  Return the snippet.
  '''
  logging.info("Getting snippet with the serch criteria: {!r}".format(snippet))

  with connection, connection.cursor() as cursor:
    sql = "SELECT * FROM snippets WHERE message LIKE %s AND hidden = false"
    arg = ["%"+snippet+"%"]
    cursor.execute(sql,arg)
    row = cursor.fetchone()
    
    print row[0] + ' - ' + row[1]
       
  connection.commit()
  logging.debug("Select snippet retrieved the record successfully.")

  
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
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet using 'get'")
    get_parser.add_argument("name", help="The name of the 'get' snippet")
     
    #Subparser for the catalog command
    logging.debug("Constructing the 'catalog' subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve all keywords using 'catalog' ")
    
    #Subparser for the search command
    logging.debug("Constructing the 'search' subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve a snippet using 'search'")
    search_parser.add_argument("snippet", help="The name of the 'search' snippet")
    
    #Subparser commands
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
    elif command == "catalog":
      listing = catalog()
      print("Retrieved snippet all keywords form Snippets".format(result))
    elif command == "search":
      result = search(**arguments)
      print("Retrieved snippet: {!r}".format(result))

if __name__ == "__main__":
    main()
  
  
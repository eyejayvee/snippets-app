import logging
import argparse
import sys

#Set the output file, and log the level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
  '''
  Store a snippet with an associated name.
  
  Returns the name of the snippet
  '''
  logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
  return name, snippet

def get(name):
  '''
  Retrieve the snippet with a given name.
  
  If there is no such snippet... # Discuss with Carl (return a blank string?)
  
  Return the snippet.
  '''
  logging.error("FIXME: Unimplemented - get({!r})".format(name))
  #TO-DO: Check the return value is correct?
  return name #""

# Add a snippet for delete?
def delete(name):
  logging.error("FIXME: Unimplemented - delete({!r})".format(name))
  return name

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store 'put' a snippet")
    put_parser.add_argument("name", help="The name of the 'put' snippet")
    put_parser.add_argument("snippet", help="The 'put' snippet text")
    
    #Subparser for the get command
    logging.debug("Constructing the 'get' subparser")
    get_parser = subparsers.add_parser("get", help="Store a 'get' snippet")
    #TO-DO: Check with Carl if I add the name or the snippet here
    get_parser.add_argument("name", help="The name of the 'get' snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    #Convert parsed arguments from the Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
      snippet = get(**arguments)
      print("Retrieved snippet: {!r}".format(snippet))

if __name__ == "__main__":
    main()
  
  
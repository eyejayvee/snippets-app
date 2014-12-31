import logging

#Set the output file, and log the level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
  '''
  Store a snippet with an associated name.
  
  Returns the name of the snippet
  '''
  logging.error("FIXME: Unimplemented - put({!r}, {!r})")
  return name, snippet

def get(name):
  '''
  Retrieve the snippet with a give name.
  
  If there is no such snippet...
  
  Return the snippet.
  '''
  logging.error("FIXME: Unimplemented - get({!r})".format(name))
  return ""
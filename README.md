# GISTQUERY

gistquery is a utility to query a single user's GitHub gists

## Syntax

`gistquery <username>`

Where `<username>` is the Github user's username.

The first time you query a user's gist it will register the current
gists for that user and show the date of the latest gist. The user
will be registered in a file named `/tmp/gistquery.<username>`. Subsequent
executions for the same username will tell
you if a new gist has been added by the user.

## Requirements

* Python 2.7 or higher
* Apply requirements.txt with pip

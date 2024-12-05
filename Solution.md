# Solution 

1. The solution i'm building here is a CLI tool that runs in background which uses REST API built by interns.I'm saving directly to PG. 

3. Ideal solution would be to have support sign in using google and save sqlite.db and sync across sign in's. This makes us not needing take care of webserver on our own.


4. CLI Tool internals
- Detect terminal (if linux/mac show linux terminal commands else powershell)
- Upon start append history if there is history newer than current history.
- Performs diff to know whether anything new is present.

## Components in Solution

1. CLI tool
2. REST API
3. DB

## CLI Tool (current support for bash and zsh)

1. CLI tool watches history file of bash/zsh if there is a change then it is pushed via API to PG.
2. Push to DB takes place if there is a new command.
 

## REST API

Prepared based on doc prepared by interns

1.  `curl -X POST http://localhost:8080/api/v1/commands -d "command=ls -l"`

2. An additional API GETS all commands by latest timestamp
  `curl -X GET http://localhost:8080/api/v1/commands`  


## DB

DB contains below fields 
- shell (type of shell zsh,bash or powershell)
- command (shell command)
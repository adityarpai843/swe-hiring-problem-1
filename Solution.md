# Solution 

1. The solution i'm building here is a CLI tool that runs in background which uses REST API built by interns to save data directly to PG.

2. Powershell comes with commands to write and read from history which can be used to build solution (refer [here](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_history?view=powershell-7.4#history-cmdlets)) this is really different from Linux terminals.

3. Ideal solution would be to have support sign in using google and save sqlite.db and sync across sign in's. This makes us not needing take care of webserver on our own.


4. CLI Tool internals
- Detect terminal (if linux/mac show linux terminal commands else powershell)
- Upon start append history if there is history newer than current history.Performs diff to know whether anything new is present.
- The history is pushed when a terminal session is ended as terminal writes to corresponding history files when a session is ended.

## Components in Solution

1. CLI tool
2. REST API
3. DB

## CLI Tool (current support for bash and zsh)

1. CLI tool watches history file of bash/zsh if there is a change then it is pushed via API to PG.

2. Push to DB takes place if there is are changes in corresponding history files `.zsh_history` and `.bash_history`. This is done using a python package called watcher.

3. The history is pushed when a terminal session is ended as terminal writes to corresponding history files when a session is ended.

4. History restore takes place when tool is run. It only restores 
 

## REST API

Built based on doc prepared by interns

1.  `curl -X POST http://localhost:8080/api/v1/commands -d "command=ls -l"`

2. An additional API GETS all commands.
  `curl -X GET http://localhost:8080/api/v1/commands`  


## DB

DB contains below fields 
- shell (type of shell zsh,bash or powershell)
- command (shell command)
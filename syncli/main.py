import os
import time
import json
import requests
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class HistoryWatcher:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.last_position = 0
        self.history_file = self._get_history_file()
        
    def _get_history_file(self):
        """Determine which shell is being used and return appropriate history file path."""
        shell = os.environ.get('SHELL', '')
        home = os.path.expanduser('~')
        
        if 'zsh' in shell:
            return os.path.join(home, '.zsh_history')
        return os.path.join(home, '.bash_history')
    
    def _get_local_history(self):
        """Get all commands from local history file."""
        commands = []
        try:
            with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if 'zsh' in self.history_file:
                        # ZSH format: ": timestamp:0;command"
                        if ': ' in line:
                            parts = line.split(';')
                            timestamp = float(parts[0].split(':')[1])
                            command = parts[-1].strip()
                            commands.append({
                                'command': command,
                                'timestamp': timestamp,
                                'raw_line': line.strip()
                            })
                    else:
                        # Bash format is just the command
                        command = line.strip()
                        if command:
                            commands.append({
                                'command': command,
                                'timestamp': None,
                                'raw_line': line.strip()
                            })
        except Exception as e:
            print(f"Error reading local history: {str(e)}")
        
        return commands

    def _send_to_api(self, command, timestamp=None):
        """Send command to API endpoint."""
        try:
            data = {
                'command': command,
                'shell': os.path.basename(os.environ.get('SHELL', ''))
            }
            
            response = requests.post(
                self.api_endpoint + "/api/v1/commands",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code != 201:
                print(f"Failed to send command to API: {response.status_code}")
                
        except Exception as e:
            print(f"Error sending command to API: {str(e)}")

    def _process_new_commands(self):
        """Read and process new commands from history file."""
        try:
            with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self.last_position)
                new_commands = f.readlines()
                self.last_position = f.tell()
                
                for command in new_commands:
                    timestamp = None
                    if 'zsh' in self.history_file:
                        if ': ' in command:
                            parts = command.split(';')
                            timestamp = float(parts[0].split(':')[1])
                            command = parts[-1].strip()
                    else:
                        command = command.strip()
                        
                    if command:
                        self._send_to_api(command, timestamp)
                        
        except Exception as e:
            print(f"Error processing commands: {str(e)}")

    def _normalize_command(self, command):
        """Normalize command string for comparison."""
        return ' '.join(command.split())

    def restore_history(self):
        """Restore history from API using diff approach."""
        try:
            # Get all commands from API
            response = requests.get(
                f"{self.api_endpoint}/api/v1/commands",
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code != 200:
                print(f"Failed to fetch history from API: {response.status_code}")
                return
            
            api_commands = response.json()
            if not api_commands:
                return

            # Get local history
            local_history = self._get_local_history()
            
            # Create sets of normalized commands for comparison
            local_commands_set = {self._normalize_command(cmd['command']) for cmd in local_history}
            
            # Find new commands from API that don't exist locally
            new_commands = []
            for api_cmd in api_commands:
                normalized_cmd = self._normalize_command(api_cmd['command'])
                if normalized_cmd not in local_commands_set:
                    new_commands.append(api_cmd)

            if not new_commands:
                print("No new commands to restore")
                return

            shell = os.path.basename(os.environ.get('SHELL', ''))
            
            # Append new commands to history file
            with open(self.history_file, 'a', encoding='utf-8') as f:
                for cmd in new_commands:
                    if 'zsh' in shell:
                        # Format for zsh history
                        timestamp = int(float(cmd['timestamp']))
                        f.write(f": {timestamp}:0;{cmd['command']}\n")
                    else:
                        # Format for bash history
                        f.write(f"{cmd['command']}\n")
            
            # Reload shell history
            if 'zsh' in shell:
                subprocess.run(['fc', '-R', self.history_file])
            else:
                subprocess.run(['history', '-r'])
            
            print(f"Restored {len(new_commands)} new commands to history")
            
        except Exception as e:
            print(f"Error restoring history: {str(e)}")

class HistoryEventHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher
        super().__init__()
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.watcher.history_file:
            self.watcher._process_new_commands()

def main():
    # Configure your API endpoint
    API_ENDPOINT = "http://localhost:3000"
    
    # Initialize the watcher
    watcher = HistoryWatcher(API_ENDPOINT)
    
    # Restore history from API first
    watcher.restore_history()
    
    # Set up the file system observer
    event_handler = HistoryEventHandler(watcher)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(watcher.history_file), recursive=False)
    
    try:
        print(f"Starting command monitoring for {watcher.history_file}")
        observer.start()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping command monitoring...")
        
    observer.join()

if __name__ == "__main__":
    main()
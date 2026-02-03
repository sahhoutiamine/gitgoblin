"""
GitGoblin Core - File watching and git automation
"""

import os
import time
import subprocess
import signal
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class GoblinFileHandler(FileSystemEventHandler):
    """Handles file system events for GitGoblin"""
    
    def __init__(self, repo_path, debounce_seconds=2):
        self.repo_path = Path(repo_path).resolve()
        self.debounce_seconds = debounce_seconds
        self.pending_files = set()
        self.last_change_time = {}
        
    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if self._should_ignore(file_path):
            return
        
        relative_path = file_path.relative_to(self.repo_path)
        self.pending_files.add(str(relative_path))
        self.last_change_time[str(relative_path)] = time.time()
        
        print(f"👁️  Goblin spotted: {relative_path}")
    
    def _should_ignore(self, file_path):
        """Check if file should be ignored"""
        ignore_patterns = [
            '.git', '__pycache__', '.pyc', '.pyo', '.pyd',
            '.DS_Store', '.swp', '~', '.tmp', 'node_modules',
            '.vscode', '.idea', '.env', '.log', '.pid'
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def get_pending_files(self):
        """Get files that are ready to be committed"""
        current_time = time.time()
        ready_files = []
        
        for file_path in list(self.pending_files):
            if current_time - self.last_change_time[file_path] >= self.debounce_seconds:
                ready_files.append(file_path)
                self.pending_files.remove(file_path)
                del self.last_change_time[file_path]
        
        return ready_files


class GoblinWatcher:
    """Main GitGoblin watcher class"""
    
    def __init__(self, repo_path='.', debounce_seconds=2):
        self.repo_path = Path(repo_path).resolve()
        self.debounce_seconds = debounce_seconds
        self.pid_file = self.repo_path / '.git' / 'gitgoblin.pid'
        
        # Verify git repository
        if not (self.repo_path / '.git').exists():
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def generate_commit_message(self, file_path):
        """Generate a commit message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Get diff stats
            result = subprocess.run(
                ['git', 'diff', '--stat', 'HEAD', file_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            diff_stat = result.stdout.strip()
            
            # Simple message based on changes
            if '+' in diff_stat and '-' in diff_stat:
                message = f"Modified {file_path}"
            elif '+' in diff_stat:
                message = f"Added content to {file_path}"
            elif '-' in diff_stat:
                message = f"Removed content from {file_path}"
            else:
                message = f"Updated {file_path}"
            
            return f"{message} at {timestamp}"
            
        except:
            return f"Updated {file_path} at {timestamp}"
    
    def commit_and_push(self, file_path):
        """Commit and push a file to GitHub"""
        try:
            print(f"🪙 Hoarding commit for: {file_path}")
            
            # Stage
            subprocess.run(
                ['git', 'add', file_path],
                cwd=self.repo_path,
                check=True,
                timeout=10,
                capture_output=True
            )
            
            # Generate message
            commit_message = self.generate_commit_message(file_path)
            print(f"💬 {commit_message}")
            
            # Commit
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.repo_path,
                check=True,
                timeout=10,
                capture_output=True
            )
            
            # Push
            print(f"🚀 Pushing to GitHub...")
            subprocess.run(
                ['git', 'push'],
                cwd=self.repo_path,
                check=True,
                timeout=30,
                capture_output=True
            )
            
            print(f"✅ Successfully hoarded: {file_path}")
            print("-" * 60)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Goblin failed: {e}")
            print("-" * 60)
            return False
    
    def sneak_commit(self, custom_message=None):
        """Perform an immediate commit of all changes"""
        try:
            # Check for changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if not result.stdout.strip():
                print("👻 Nothing to commit - working tree clean")
                return True
            
            # Stage all changes
            print("🗡️  Staging all changes...")
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )
            
            # Generate or use custom message
            if custom_message:
                message = custom_message
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"🗡️  Stealth commit at {timestamp}"
            
            print(f"💬 {message}")
            
            # Commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )
            
            # Push
            print("🚀 Pushing to GitHub...")
            subprocess.run(
                ['git', 'push'],
                cwd=self.repo_path,
                check=True,
                timeout=30
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Stealth operation failed: {e}")
            return False
    
    def run(self):
        """Run the watcher in foreground"""
        event_handler = GoblinFileHandler(self.repo_path, self.debounce_seconds)
        observer = Observer()
        observer.schedule(event_handler, str(self.repo_path), recursive=True)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
                ready_files = event_handler.get_pending_files()
                for file_path in ready_files:
                    self.commit_and_push(file_path)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()
    
    def run_daemon(self):
        """Run as background daemon"""
        import daemon
        import daemon.pidfile
        
        # Create PID file
        pid_context = daemon.pidfile.TimeoutPIDLockFile(str(self.pid_file))
        
        with daemon.DaemonContext(
            pidfile=pid_context,
            working_directory=str(self.repo_path)
        ):
            self.run()
    
    def stop_daemon(self):
        """Stop the background daemon"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
            
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            return True
        except (ProcessLookupError, FileNotFoundError):
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False

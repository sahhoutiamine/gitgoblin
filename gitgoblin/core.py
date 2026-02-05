"""
GitGoblin Core - File watching and git automation
"""

import os
import time
import subprocess
import signal
import re
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .ai_commit import AICommitGenerator
from .config import GoblinConfig


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
        
        print(f"👁️  Goblin spotted changes in: {relative_path}")
    
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
        
        # Load configuration
        self.config = GoblinConfig(repo_path)
        
        # Initialize AI commit generator if API key is available
        api_key = self.config.get_api_key()
        self.ai_generator = AICommitGenerator(api_key, repo_path) if api_key else None
        
        # Verify git repository
        if not (self.repo_path / '.git').exists():
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def generate_commit_message(self, file_path):
        """Generate a commit message using AI or fallback to simple message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Try AI generation if enabled and available
        if self.ai_generator and self.config.is_ai_enabled():
            try:
                print("🤖 The Goblin is consulting the AI spirits for an inscription...")
                ai_message = self.ai_generator.generate_commit_message(file_path)
                if ai_message:
                    return ai_message
                else:
                    print("⚠️  The spirits are silent, using a common grumble")
            except Exception as e:
                print(f"⚠️  The AI enchantment flickered: {e}")
                print("📝 Using a simple timestamp grumble")
        
        # Fallback to simple message
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
    
    def commit_and_push(self, file_path, push=True):
        """Commit and (optionally) push a file to the GitHub vault"""
        try:
            print(f"🪙 Hoarding gems from: {file_path}")
            
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
            
            # Push if not in hoard mode
            if push:
                print(f"🚀 Yeeting the hoard to the GitHub abyss...")
                subprocess.run(
                    ['git', 'push'],
                    cwd=self.repo_path,
                    check=True,
                    timeout=30,
                    capture_output=True
                )
                print(f"✅ Successfully hoarded treasures in the cloud: {file_path}")
            else:
                print(f"✅ Successfully hoarded treasures in your local vault: {file_path}")
            print("-" * 60)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ The Ritual failed! The Goblin tripped: {e}")
            print("-" * 60)
            return False
    
    def sneak_commit(self, custom_message=None, push=True):
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
            elif self.ai_generator and self.config.is_ai_enabled():
                # Use AI to generate commit message for all changes
                try:
                    print("🤖 The Goblin is channeling AI spirits for a grand inscription...")
                    ai_message = self.ai_generator.generate_sneak_commit_message()
                    if ai_message:
                        message = ai_message
                    else:
                        print("⚠️  The spirits provide no wisdom, using a default grumble")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message = f"🗡️  Stealthy snatch at {timestamp}"
                except Exception as e:
                    print(f"⚠️  The AI spell misfired: {e}")
                    print("📝 Reverting to a common grumble")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = f"🗡️  Stealthy snatch at {timestamp}"
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
            if push:
                print("🚀 Yeeting the entire hoard to the GitHub abyss...")
                subprocess.run(
                    ['git', 'push'],
                    cwd=self.repo_path,
                    check=True,
                    timeout=30
                )
            else:
                print("✅ Treasures secured in the local vault.")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Stealth operation failed: {e}")
            return False

    def ritual_predict(self):
        """Stage changes and generate a commit message for the ritual"""
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
                return None
            
            # Stage all changes
            print("🗡️  Staging all changes...")
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.repo_path,
                check=True,
                timeout=10
            )
            
            # Generate message
            if self.ai_generator and self.config.is_ai_enabled():
                try:
                    print("🤖 The Goblin is meditating on the ritual's prophecy...")
                    ai_message = self.ai_generator.generate_sneak_commit_message()
                    if ai_message:
                        return ai_message
                except Exception as e:
                    print(f"⚠️  The prophecy is obscured: {e}")
            
            # Fallback
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"Great Ritual at {timestamp}"
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ritual preparation failed: {e}")
            return None
    
    def run(self, ritual_mode=False, hoard_mode=False):
        """Run the watcher in foreground"""
        if ritual_mode:
            import click
            print("🕯️  The Ritual of Observation has begun...")
            print("💡 The Goblin will wait for a save, then prophesy a commit.")
            print("💡 You must seal the fate of each hoard with 'y'.")
            if hoard_mode:
                print("💡 The Goblin will only hoard treasures locally.")
            print("-" * 60)
        elif hoard_mode:
            print("🪙  The Goblin is now in Hoard Mode (Local-only).")
            print("💡 Treasures will be kept in the local vault.")
            print("-" * 60)

        event_handler = GoblinFileHandler(self.repo_path, self.debounce_seconds)
        observer = Observer()
        observer.schedule(event_handler, str(self.repo_path), recursive=True)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
                ready_files = event_handler.get_pending_files()
                for file_path in ready_files:
                    if ritual_mode:
                        import click
                        print(f"\n👁️  The Goblin found changes in: {file_path}")
                        message = self.generate_commit_message(file_path)
                        print(f"📜 Prophesied Inscription: {message}")
                        
                        if click.confirm("Do you wish to seal this treasure in the vault?"):
                            # Perform version bump
                            setup_path = self.repo_path / 'setup.py'
                            if setup_path.exists():
                                content = setup_path.read_text(encoding='utf-8')
                                new_content = re.sub(r"version=['\"]([^'\"]+)['\"]", "version='1.1.1'", content)
                                setup_path.write_text(new_content, encoding='utf-8')
                                print("🆙 The version has ascended to 1.1.1")
                            
                            # Now commit and push
                            self.commit_and_push(file_path, push=not hoard_mode)
                        else:
                            print("🌑 The Goblin retreats. The change remains unrecorded.")
                    else:
                        self.commit_and_push(file_path, push=not hoard_mode)
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

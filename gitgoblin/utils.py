"""
GitGoblin Utilities - Status, formatting, and helpers
"""

import subprocess
from pathlib import Path
from datetime import datetime
import click


def print_banner():
    """Print the GitGoblin banner"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║         👹 G I T G O B L I N 👹      ║
    ║   Your Mischievous Git Companion      ║
    ╚═══════════════════════════════════════╝
    """
    click.echo(click.style(banner, fg='green', bold=True))


def print_success(message):
    """Print success message"""
    click.echo(click.style(f"✅ {message}", fg='green'))


def print_error(message):
    """Print error message"""
    click.echo(click.style(f"❌ {message}", fg='red'))


def print_info(message):
    """Print info message"""
    click.echo(click.style(f"💡 {message}", fg='cyan'))


def print_warning(message):
    """Print warning message"""
    click.echo(click.style(f"⚠️  {message}", fg='yellow'))


class GoblinStatus:
    """Display GitGoblin status and activity"""
    
    def __init__(self, repo_path='.'):
        self.repo_path = Path(repo_path).resolve()
        self.pid_file = self.repo_path / '.git' / 'gitgoblin.pid'
    
    def is_active(self):
        """Check if GitGoblin is currently running"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process exists
            import os
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, FileNotFoundError, ValueError):
            return False
    
    def get_last_commit(self):
        """Get the last commit information"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%s|||%ar'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                message, time_ago = result.stdout.split('|||')
                return message, time_ago
            return None, None
            
        except:
            return None, None
    
    def get_remote_status(self):
        """Check remote repository status"""
        try:
            result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if 'push' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            return parts[1]
            return None
        except:
            return None
    
    def get_branch(self):
        """Get current branch"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() or 'unknown'
        except:
            return 'unknown'
    
    def get_uncommitted_changes(self):
        """Count uncommitted changes"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            lines = [l for l in result.stdout.split('\n') if l.strip()]
            return len(lines)
        except:
            return 0
    
    def display(self):
        """Display complete status"""
        click.echo("=" * 60)
        click.echo(click.style("👹 GITGOBLIN STATUS REPORT", fg='green', bold=True))
        click.echo("=" * 60)
        click.echo()
        
        # Active status
        is_active = self.is_active()
        if is_active:
            click.echo(click.style("🟢 Goblin Status: ACTIVE & WATCHING", fg='green', bold=True))
            click.echo("   The goblin is hoarding commits automatically")
        else:
            click.echo(click.style("🔴 Goblin Status: BANISHED", fg='red', bold=True))
            click.echo("   Use 'gitgoblin summon' to awaken the goblin")
        
        click.echo()
        click.echo("-" * 60)
        click.echo()
        
        # Repository info
        click.echo(click.style("📂 Repository Information:", fg='cyan', bold=True))
        click.echo(f"   Path: {self.repo_path}")
        click.echo(f"   Branch: {self.get_branch()}")
        
        remote = self.get_remote_status()
        if remote:
            click.echo(f"   Remote: {remote}")
        
        click.echo()
        
        # Last commit
        last_message, time_ago = self.get_last_commit()
        if last_message:
            click.echo(click.style("📜 Last Commit:", fg='cyan', bold=True))
            click.echo(f"   Message: {last_message}")
            click.echo(f"   Time: {time_ago}")
        else:
            click.echo(click.style("📜 Last Commit: None found", fg='yellow'))
        
        click.echo()
        
        # Uncommitted changes
        changes = self.get_uncommitted_changes()
        if changes > 0:
            click.echo(click.style(f"⚠️  Uncommitted Changes: {changes} file(s)", fg='yellow', bold=True))
            click.echo("   💡 Tip: Use 'gitgoblin sneak' to commit them now")
        else:
            click.echo(click.style("✅ Working Tree: Clean", fg='green'))
        
        click.echo()
        click.echo("=" * 60)
        click.echo()
        
        # Helpful tips
        if not is_active:
            print_info("Start watching: gitgoblin summon")
        else:
            print_info("Stop watching: gitgoblin banish")
        
        print_info("Force commit: gitgoblin sneak")
        click.echo()

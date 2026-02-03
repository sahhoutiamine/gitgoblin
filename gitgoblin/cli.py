#!/usr/bin/env python3
"""
GitGoblin CLI - Your mischievous git automation companion
"""

import click
import sys
from .core import GoblinWatcher
from .utils import GoblinStatus, print_banner, print_success, print_error, print_info


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """👹 GitGoblin - Automatic Git Commit & Push Daemon"""
    if ctx.invoked_subcommand is None:
        print_banner()
        click.echo("\n📖 Available Spells:\n")
        click.echo("  👹 gitgoblin summon      - Awaken the goblin (start watching)")
        click.echo("  🗡️  gitgoblin sneak       - Force instant commit & push")
        click.echo("  🔮 gitgoblin crystalball - Check goblin activity")
        click.echo("  🛑 gitgoblin banish      - Expel the goblin (stop watching)")
        click.echo("\n✨ Use 'gitgoblin <command> --help' for more info\n")


@cli.command()
@click.option('--path', '-p', default='.', help='Path to git repository')
@click.option('--debounce', '-d', default=2, help='Seconds to wait before committing')
@click.option('--daemon', '-bg', is_flag=True, help='Run as background daemon')
def summon(path, debounce, daemon):
    """
    👹 Summon GitGoblin to watch your files
    
    The goblin will monitor your repository and automatically
    commit & push changes whenever you save a file.
    """
    print_banner()
    click.echo("👹 Summoning GitGoblin...\n")
    
    try:
        watcher = GoblinWatcher(path, debounce)
        
        if daemon:
            click.echo("🌙 GitGoblin will run in the background...")
            click.echo("💡 Tip: Use 'gitgoblin banish' to stop it\n")
            watcher.run_daemon()
        else:
            click.echo("🔍 GitGoblin is now watching your files...")
            click.echo("🪙 Collecting commits automatically...")
            click.echo("💡 Press Ctrl+C to banish the goblin\n")
            click.echo("-" * 60)
            watcher.run()
            
    except ValueError as e:
        print_error(f"Summoning failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n")
        print_info("🔥 GitGoblin has been banished.")
        print_info("🛑 Auto commits stopped.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--path', '-p', default='.', help='Path to git repository')
@click.option('--message', '-m', default=None, help='Custom commit message')
def sneak(path, message):
    """
    🗡️ Force an instant stealth commit & push
    
    GitGoblin performs a quick smash-and-grab commit operation,
    staging all current changes and pushing them immediately.
    """
    click.echo("🗡️  GitGoblin preparing stealth operation...\n")
    
    try:
        watcher = GoblinWatcher(path)
        success = watcher.sneak_commit(message)
        
        if success:
            print_success("✅ Stealth commit successful!")
            print_success("📦 Changes delivered to GitHub.")
        else:
            print_error("❌ Stealth operation failed!")
            
    except Exception as e:
        print_error(f"Sneak attack failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--path', '-p', default='.', help='Path to git repository')
def crystalball(path):
    """
    🔮 Check GitGoblin's current activity and status
    
    Peer into the goblin's cave to see what it's been hoarding.
    Shows recent commits, push times, and configuration.
    """
    click.echo("🔮 Peering into the crystal ball...\n")
    
    try:
        status = GoblinStatus(path)
        status.display()
        
    except Exception as e:
        print_error(f"Crystal ball is cloudy: {e}")
        sys.exit(1)


@cli.command()
def banish():
    """
    🛑 Banish GitGoblin and stop all automation
    
    Expels the goblin from your project, stopping all file
    monitoring and automatic commits. Configuration is preserved.
    """
    click.echo("🔥 Attempting to banish GitGoblin...\n")
    
    try:
        watcher = GoblinWatcher('.')
        stopped = watcher.stop_daemon()
        
        if stopped:
            print_success("👹 GitGoblin has been banished!")
            print_info("🛑 Auto commits stopped.")
            print_info("💤 The goblin retreats into the shadows...")
        else:
            print_info("👻 No active goblin found in this realm.")
            
    except Exception as e:
        print_error(f"Banishment ritual failed: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()

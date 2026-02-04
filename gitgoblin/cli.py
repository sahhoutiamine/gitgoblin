#!/usr/bin/env python3
"""
GitGoblin CLI - Your mischievous git automation companion
"""

import click
import sys
from .core import GoblinWatcher
from .utils import GoblinStatus, print_banner, print_success, print_error, print_info
from .config import GoblinConfig


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
        click.echo("  🧙 gitgoblin enchant     - Configure AI commit messages")
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


@cli.command()
@click.option('--path', '-p', default='.', help='Path to git repository')
@click.option('--api-key', '-k', default=None, help='Groq API key')
@click.option('--enable/--disable', default=None, help='Enable or disable AI commits')
@click.option('--show', is_flag=True, help='Show current configuration')
def enchant(path, api_key, enable, show):
    """
    🧙 Configure AI-powered commit messages
    
    Set up Groq AI to generate descriptive commit messages
    automatically. Requires a Groq API key from https://console.groq.com/
    """
    try:
        config = GoblinConfig(path)
        
        if show:
            # Show current configuration
            click.echo("🔮 Current AI Configuration:\n")
            current_key = config.get_api_key()
            if current_key:
                masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
                click.echo(f"  API Key: {masked_key}")
            else:
                click.echo("  API Key: Not configured")
            
            ai_enabled = config.is_ai_enabled()
            click.echo(f"  AI Commits: {'✅ Enabled' if ai_enabled else '❌ Disabled'}")
            click.echo()
            return
        
        # Set API key if provided
        if api_key:
            if config.set_api_key(api_key):
                print_success("✅ API key saved successfully!")
                # Auto-enable AI commits when key is set
                config.enable_ai_commits(True)
                print_success("✅ AI commits enabled!")
            else:
                print_error("❌ Failed to save API key")
                sys.exit(1)
        
        # Enable/disable AI commits
        if enable is not None:
            current_key = config.get_api_key()
            if not current_key and enable:
                print_error("❌ Cannot enable AI commits: No API key configured")
                click.echo("💡 Set your API key first: gitgoblin enchant --api-key YOUR_KEY")
                sys.exit(1)
            
            if config.enable_ai_commits(enable):
                if enable:
                    print_success("✅ AI commits enabled!")
                    click.echo("🤖 GitGoblin will now use AI to generate commit messages")
                else:
                    print_success("✅ AI commits disabled!")
                    click.echo("📝 GitGoblin will use simple timestamp messages")
            else:
                print_error("❌ Failed to update configuration")
                sys.exit(1)
        
        # If no options provided, show help
        if not api_key and enable is None and not show:
            click.echo("🧙 GitGoblin AI Configuration\n")
            click.echo("Options:")
            click.echo("  --api-key, -k    Set Groq API key")
            click.echo("  --enable         Enable AI commit messages")
            click.echo("  --disable        Disable AI commit messages")
            click.echo("  --show           Show current configuration")
            click.echo("\nExample:")
            click.echo("  gitgoblin enchant --api-key sk-your-key-here")
            click.echo("  gitgoblin enchant --enable")
            click.echo("  gitgoblin enchant --show")
            
    except Exception as e:
        print_error(f"Enchantment failed: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
GitGoblin CLI - Your mischievous git automation companion
"""

import click
import sys
import re
from pathlib import Path
from .core import GoblinWatcher
from .utils import GoblinStatus, print_banner, print_success, print_error, print_info
from .config import GoblinConfig


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """👹 GitGoblin - The Mischievous Hoarder of Commits"""
    if ctx.invoked_subcommand is None:
        print_banner()
        click.echo("\n📖 The Goblin's Grimoire (Available Spells):\n")
        click.echo("  👹 summon      - Wake the beast and begin the watch")
        click.echo("  🗡️  sneak       - Perform a stealthy smash-and-grab commit")
        click.echo("  🔮 crystalball - Peer into the vault of hoarded treasures")
        click.echo("  🧙 enchant     - Bestow AI wisdom upon the goblin")
        click.echo("  🛑 banish      - Cast the goblin back into the void")
        click.echo("\n✨ Recite 'gitgoblin <spell> --help' to learn more secrets\n")


@cli.command()
@click.option('--path', '-p', default='.', help='Dungeon path (repository)')
@click.option('--debounce', '-d', default=2, help='Seconds to wait for silence')
@click.option('--daemon', '-bg', is_flag=True, help='Run as a lingering spirit')
@click.option('--ritual', is_flag=True, help='Perform the ritual of ascension (v1.1.1)')
@click.option('--hoard', is_flag=True, help='Only hoard treasures locally, do not push')
def summon(path, debounce, daemon, ritual, hoard):
    """
    👹 Awaken GitGoblin to haunt your files
    
    The beast will lurk in your directory, snatching every 
    change and hoarding it in the GitHub vault.
    """
    print_banner()

    if daemon and ritual:
        print_error("A lingering spirit (daemon) cannot perform an interactive ritual!")
        click.echo("💡 Use either --daemon or --ritual, not both.")
        sys.exit(1)
    
    click.echo("👹 Preparing the summoning circles...\n")
    
    try:
        watcher = GoblinWatcher(path, debounce)
        
        if daemon:
            click.echo("🌙 The Goblin is now a lingering spirit in the shadows...")
            click.echo("💡 Tip: Use 'gitgoblin banish' to cast it away\n")
            watcher.run_daemon()
        else:
            if ritual:
                click.echo("🕯️  The Goblin is now watching for changes to perform the Ritual...")
                if hoard:
                    click.echo("🪙  Note: The Goblin is in Hoard Mode (Local-only).")
            elif hoard:
                click.echo("🪙  The Goblin is now in Hoard Mode (Local-only).")
                click.echo("🛡️  Treasures will be kept in the local vault.")
            else:
                click.echo("🔍 The Goblin's eyes are open. It sees your edits...")
                click.echo("🪙 Collecting its hoard of commits automatically...")
            
            click.echo("💡 Press Ctrl+C to send the goblin back to sleep\n")
            click.echo("-" * 60)
            watcher.run(ritual_mode=ritual, hoard_mode=hoard)
            
    except ValueError as e:
        print_error(f"The summoning failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n")
        print_info("🔥 The Goblin has been vanished. The shadows retreat.")
        print_info("🛑 Auto-hoarding has ceased.")
    except Exception as e:
        print_error(f"A dark curse has occurred: {e}")
        sys.exit(1)


@cli.command()
@click.option('--path', '-p', default='.', help='Dungeon path (repository)')
@click.option('--message', '-m', default=None, help='A specific grumble (custom message)')
def sneak(path, message):
    """
    🗡️ Perform an instant stealth commit & push
    
    The goblin performs a quick smash-and-grab operation,
    snatching all changes and yeeting them into the GitHub abyss.
    """
    click.echo("🗡️  The Goblin is preparing a stealthy snatch...\n")
    
    try:
        watcher = GoblinWatcher(path)
        success = watcher.sneak_commit(message)
        
        if success:
            print_success("The loot has been secured in the cloud vault!")
            print_info("📦 Your hoarded gems are safe at GitHub.")
        else:
            print_error("A trap was sprung! The stealth operation failed.")
            
    except Exception as e:
        print_error(f"Sneak attack failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--path', '-p', default='.', help='Dungeon path (repository)')
def crystalball(path):
    """
    🔮 Peer into the Goblin's cavern and check its hoard
    
    Look deep into the crystal ball to see recent hoards,
    push times, and the state of your precious code.
    """
    click.echo("🔮 Focusing your mind on the crystal ball...\n")
    
    try:
        status = GoblinStatus(path)
        status.display()
        
    except Exception as e:
        print_error(f"The crystal ball is cloudy and dark: {e}")
        sys.exit(1)


@cli.command()
def banish():
    """
    🛑 Cast the Goblin back into the void
    
    Expels the lingering spirit from your dungeon, stopping
    all file monitoring and hoarding. The hoard remains safe.
    """
    click.echo("🔥 Reciting the banishment ritual...\n")
    
    try:
        watcher = GoblinWatcher('.')
        stopped = watcher.stop_daemon()
        
        if stopped:
            print_success("The GitGoblin has been banished from this realm!")
            print_info("🛑 The watch has ended.")
            print_info("💤 The beast retreats into the deep shadows...")
        else:
            print_info("👻 There is no entity haunting this dungeon currently.")
            
    except Exception as e:
        print_error(f"Banishment ritual failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--path', '-p', default='.', help='Dungeon path')
@click.option('--api-key', '-k', default=None, help='The Secret Key of AI wisdom')
@click.option('--enable/--disable', default=None, help='Give/take the goblin its voice')
@click.option('--show', is_flag=True, help='Reveal current enchantments')
def enchant(path, api_key, enable, show):
    """
    🧙 Bestow AI wisdom upon the common GitGoblin
    
    Enchant your goblin with Groq AI to generate poetic and
    descriptive inscriptions for its hoard.
    """
    try:
        config = GoblinConfig(path)
        
        if show:
            click.echo("🔮 Active Enchantments:\n")
            current_key = config.get_api_key()
            if current_key:
                masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
                click.echo(f"  Secret Key: {masked_key}")
            else:
                click.echo("  Secret Key: Not bestowed yet")
            
            ai_enabled = config.is_ai_enabled()
            click.echo(f"  AI Voice: {'✅ Enabled' if ai_enabled else '❌ Silenced'}")
            click.echo()
            return
        
        if api_key:
            if config.set_api_key(api_key):
                print_success("The Secret Key has been inscribed into the configuration!")
                config.enable_ai_commits(True)
                print_success("The Goblin's AI voice has been awakened!")
            else:
                print_error("The inscription failed. The key is rejected.")
                sys.exit(1)
        
        if enable is not None:
            current_key = config.get_api_key()
            if not current_key and enable:
                print_error("You cannot wake the voice without a Secret Key!")
                click.echo("💡 Tip: Bestow a key first: gitgoblin enchant --api-key YOUR_KEY")
                sys.exit(1)
            
            if config.enable_ai_commits(enable):
                if enable:
                    print_success("The Goblin now speaks with AI wisdom!")
                    click.echo("🤖 Descriptive inscriptions will now flow like magic.")
                else:
                    print_success("The Goblin's voice has been silenced.")
                    click.echo("📝 It will return to muttering simple timestamps.")
            else:
                print_error("The enchantment failed to take hold.")
                sys.exit(1)
        
        if not api_key and enable is None and not show:
            click.echo("🧙 The Master's Guide to Enchantment\n")
            click.echo("Runes:")
            click.echo("  --api-key, -k    Bestow a Secret Key (Groq API)")
            click.echo("  --enable         Awaken the AI voice")
            click.echo("  --disable        Silence the AI voice")
            click.echo("  --show           Reveal current enchantments")
            click.echo("\nIncantations:")
            click.echo("  gitgoblin enchant --api-key sk-your-key")
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

# 👹 GitGoblin: The Mischievous Hoarder of Commits

**Version 1.1.1** | **Created by the Great Goblin Master: [sahhoutiamine](https://github.com/sahhoutiamine)**

> *"Deep within the `.git` dungeons of your project, a creature stirs. It doesn't sleep. It doesn't drink coffee. It only watches. It only waits. It only... hoards."*

GitGoblin is a mischievous little monster that lives inside your project folder. While you're busy forgetting to stage your files or procrastinating on your commit messages, the Goblin is already at work—sneaking into your terminal, grabbing your changes, and yeeting them into the GitHub abyss before you even realize what's happened.

---

## 📜 The Legend (How it Works)

GitGoblin feeds on two things: **forgotten commits** and **developer laziness**. It sits silently in the shadows (your background processes), watching every file you touch. The moment you save a file, the Goblin's eyes light up. It waits for a moment of silence (the *debounce*), then pounces!

1.  **The Sniff**: It detects a file modification.
2.  **The Hoard**: It stages the change (`git add`).
3.  **The Grumble**: It mutters a timestamped message and commits.
4.  **The Yeet**: It pushes the commit to GitHub immediately.

---

## ✨ Goblin Mutations (Features)

- 🔍 **Goblin Senses**: Real-time monitoring of your codebase. It sees everything.
- 🪙 **Hoarding Instinct**: Automatically commits and pushes files the moment you save them.
- 🏰 **The Local Vault**: Use `--hoard` to keep your treasures in the local dungeon and skip the push! (NEW!)
- 🌀 **Magical Portals**: Instant synchronization with your remote GitHub repository.
- 🤖 **AI Brain**: Generate descriptive commit messages using Groq AI - blazingly fast! (NEW!)
- 🕯️ **Summoning Ritual**: Stage changes, bump project version to 1.1.1, and commit with confirmation! (NEW!)
- 🗡️ **Stealth Operations**: Force a commit with `sneak` when you're feeling especially lazy.
- 🔮 **Crystal Ball**: Peer into the Goblin's mind to see what it's been up to.
- 🎭 **Daemon Possession**: Can run as a background spirit, haunting your directory forever (or until banished).

---

## 🏗️ Summoning the Creature (Installation)

To bring the Goblin into your world, you must use the ancient scrolls of `pip`:

### From the Ether (PyPI)
```bash
pip install gitgoblin
```
> *"Legends say, 'It's not working. Try the second way."*

### From the Source Code Dungeons
```bash
git clone https://github.com/sahhoutiamine/gitgoblin.git
cd gitgoblin
pip install -e .
```

> **🐧 Linux Users:** If you see `ModuleNotFoundError: No module named 'click'`, try running `pip install -r requirements.txt` to ensure all dependencies are installed.

---

## 🧙 The Command Grimoire

### 👹 `gitgoblin summon`
**Awaken the Beast.** This command starts the auto-watch process.
- `--path`: Choose which dungeon (directory) to watch.
- `--debounce`: How many seconds the goblin should wait before pouncing (default: 2s).
- `--daemon`: Turn the goblin into a background spirit (Linux/Mac).
- `--hoard`: **The Hoarder's Path.** Skip the GitHub abyss and keep your commits safe in your local vault.
- `--ritual`: **The Summoning Ritual.** A special ceremony that stages changes, predicts a commit message, asks for your confirmation, and **ascends the project version to 1.1.1** before pushing.

```bash
# Start the ceremony
gitgoblin summon --ritual
```

### ⚡ `gitgoblin sneak`
**A Stealthy Strike.** Force the goblin to grab EVERYTHING and push it right now. No waiting. No mercy.
- `--message`: Give the goblin a specific grumble (commit message) to shout.

```bash
gitgoblin sneak --message "I fixed the thing, don't ask how"
```

### 🔮 `gitgoblin crystalball`
**Peer into the Future (and Past).** See the goblin's status, its last hoarding session, and the health of your repository.

```bash
gitgoblin crystalball
```

### 🧙 `gitgoblin enchant`
**Empower with AI Magic.** Configure AI-powered commit messages using Groq API. Get descriptive, professional commits automatically - blazingly fast!

```bash
# Set your Groq API key
gitgoblin enchant --api-key gsk-your-key-here

# Enable/disable AI commits
gitgoblin enchant --enable
gitgoblin enchant --disable

# Show current configuration
gitgoblin enchant --show
```

📖 **[Read the full AI Commits Guide](AI_COMMITS.md)**

### 🛑 `gitgoblin banish`
**Send it Back to the Void.** Stop the automation and tell the goblin to go to sleep.

```bash
gitgoblin banish
```

---

## 🎯 Is this Goblin for You?

| ✅ Summon if... | ❌ Banish if... |
| :--- | :--- |
| You forget to commit for 3 days straight. | You are in a team with a scary Tech Lead. |
| You want an "Undo" button for your whole life. | You need "meaningful" commit messages. |
| You're working on a solo chaotic project. | You are committing secrets (Don't do that). |
| You like seeing your GitHub graph turn green. | You value manual labor. |

---

## 🛡️ Goblin Ethics (Security)

The Goblin is mischievous, but it isn't stupid. It respects your `.gitignore` and won't hoard your `.env` files or `node_modules` unless you've been very, very naughty and didn't ignore them properly.

**⚠️ WARNING:** The Goblin will commit and push *everything* it sees. Do not leave your API keys lying around in the open. The Goblin has no filter.

---

## 🎭 The Creator

This creature was birthed from the mind of **[sahhoutiamine](https://github.com/sahhoutiamine)**, a sorcerer of automation and a hater of manual commits.

---

## ⚖️ License

The Goblin is bound by the **MIT License**. You can use it, change it, or sell it to a traveling circus, as long as you keep the original notice.

---

**Remember: With great automation comes a very messy commit history. Use GitGoblin wisely! 👹**

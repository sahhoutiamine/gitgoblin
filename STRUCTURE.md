# GitGoblin Project Structure

```
gitgoblin/
│
├── gitgoblin/                  # Main package directory
│   ├── __init__.py            # Package initialization
│   ├── cli.py                 # Command-line interface (click commands)
│   ├── core.py                # Core watcher & git functionality
│   ├── utils.py               # Utilities, status, formatting
│   ├── ai_commit.py           # AI commit message generator (NEW)
│   └── config.py              # Configuration management (NEW)
│
├── setup.py                    # Package installation configuration
├── requirements.txt            # Python dependencies
├── MANIFEST.in                 # Files to include in distribution
├── README.md                   # Main documentation
├── INSTALL.md                  # Installation guide
├── AI_COMMITS.md              # AI feature documentation (NEW)
├── TEST_AI.md                 # AI testing guide (NEW)
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
└── quickstart.sh              # Quick test script

```

## File Descriptions

### Core Package Files

**`gitgoblin/__init__.py`**
- Package initialization
- Version information
- Exports main classes

**`gitgoblin/cli.py`**
- Command-line interface using Click
- Commands: summon, sneak, crystalball, banish
- Entry point for `gitgoblin` command

**`gitgoblin/core.py`**
- `GoblinFileHandler`: Watchdog event handler
- `GoblinWatcher`: Main watcher class
- File monitoring logic
- Git operations (add, commit, push)
- Daemon mode support

**`gitgoblin/utils.py`**
- `GoblinStatus`: Status display class
- Terminal formatting functions
- Banner and message printing
- Repository information retrieval

**`gitgoblin/ai_commit.py`** (NEW)
- `AICommitGenerator`: AI-powered commit message generator
- DeepSeek API integration
- Git diff analysis
- Conventional commits format
- Automatic fallback handling

**`gitgoblin/config.py`** (NEW)
- `GoblinConfig`: Configuration management
- API key storage and retrieval
- AI settings management
- Secure config file handling

### Configuration Files

**`setup.py`**
- Package metadata
- Dependencies
- Entry points (console_scripts)
- PyPI configuration

**`requirements.txt`**
- Runtime dependencies:
  - click (CLI framework)
  - watchdog (file monitoring)
  - python-daemon (background mode)

**`MANIFEST.in`**
- Specifies additional files for distribution
- Includes README, LICENSE, etc.

### Documentation

**`README.md`**
- Full user documentation
- Command reference
- Examples and use cases
- Troubleshooting

**`INSTALL.md`**
- Installation instructions
- Setup guide
- Troubleshooting installation issues

**`LICENSE`**
- MIT License
- Usage permissions

### Scripts

**`quickstart.sh`**
- Automated test setup
- Creates demo repository
- Helps users test GitGoblin quickly

## Command Flow

### `gitgoblin summon`
```
cli.py:summon()
    ↓
core.py:GoblinWatcher.__init__()
    ↓
core.py:GoblinWatcher.run()
    ↓
core.py:GoblinFileHandler (watchdog)
    ↓
core.py:commit_and_push() [on file change]
```

### `gitgoblin sneak`
```
cli.py:sneak()
    ↓
core.py:GoblinWatcher.sneak_commit()
    ↓
Git operations: add -A, commit, push
```

### `gitgoblin crystalball`
```
cli.py:crystalball()
    ↓
utils.py:GoblinStatus.__init__()
    ↓
utils.py:GoblinStatus.display()
    ↓
Git info retrieval & formatting
```

### `gitgoblin banish`
```
cli.py:banish()
    ↓
core.py:GoblinWatcher.stop_daemon()
    ↓
Kill process via PID file
```

## Key Design Decisions

### 1. Click for CLI
- Professional command-line interface
- Built-in help generation
- Easy to extend with new commands

### 2. Watchdog for File Monitoring
- Cross-platform file system events
- Efficient resource usage
- Reliable change detection

### 3. Debouncing
- Prevents commit spam during active editing
- Configurable wait time (default 2s)
- Only commits after changes stabilize

### 4. PID File Management
- Tracks daemon process
- Enables clean shutdown
- Prevents multiple instances

### 5. Modular Structure
- Separation of concerns
- Easy testing and maintenance
- Clean code organization

## Adding New Commands

To add a new command:

1. **Add command in `cli.py`:**
```python
@cli.command()
def mycommand():
    """My new command"""
    # Implementation
```

2. **Add functionality in `core.py` or `utils.py`:**
```python
def my_functionality(self):
    # Core logic
    pass
```

3. **Update documentation:**
   - Add to README.md
   - Update --help text

## Testing

### Manual Testing
```bash
# Install in development mode
pip install -e .

# Run commands
gitgoblin summon
gitgoblin sneak
gitgoblin crystalball
gitgoblin banish
```

### Quick Test
```bash
./quickstart.sh
```

## Distribution

### Build Package
```bash
python setup.py sdist bdist_wheel
```

### Upload to PyPI
```bash
pip install twine
twine upload dist/*
```

### Install from PyPI (after upload)
```bash
pip install gitgoblin
```

# 👹 GitGoblin Installation Guide

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. **Clone or download the GitGoblin package folder**

2. **Navigate to the gitgoblin directory:**
   ```bash
   cd gitgoblin
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```
   
   This installs GitGoblin and makes the `gitgoblin` command available globally.

4. **Verify installation:**
   ```bash
   gitgoblin --help
   ```

### Method 2: Regular Installation

```bash
cd gitgoblin
pip install .
```

### Method 3: Install Dependencies Only

If you just want to install the dependencies:

```bash
cd gitgoblin
pip install -r requirements.txt
```

## Requirements

- Python 3.7 or higher
- Git installed and configured
- Internet connection for pushing to GitHub

## Post-Installation Setup

### 1. Configure Git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Set up GitHub Authentication

**Option A: SSH (Recommended)**
- Generate SSH key: `ssh-keygen -t ed25519 -C "your.email@example.com"`
- Add to GitHub: https://github.com/settings/keys

**Option B: Personal Access Token**
- Create token: https://github.com/settings/tokens
- Use HTTPS URLs with token authentication

### 3. Test Your Installation

Create a test repository:

```bash
# Create test directory
mkdir test-gitgoblin
cd test-gitgoblin

# Initialize git
git init
git remote add origin YOUR_GITHUB_REPO_URL

# Create a test file
echo "# Test" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main

# Summon the goblin
gitgoblin summon
```

Now edit README.md and save - GitGoblin should auto-commit and push!

## Troubleshooting Installation

### "Command not found: gitgoblin"

Your Python scripts directory might not be in PATH.

**Find the installation path:**
```bash
python -m pip show gitgoblin
```

**Add to PATH (Linux/Mac):**
```bash
export PATH="$PATH:$HOME/.local/bin"
```

Add to `~/.bashrc` or `~/.zshrc` to make permanent.

**Windows:**
Add Python Scripts directory to PATH in System Environment Variables.

### "Permission denied"

**Linux/Mac:**
```bash
sudo pip install -e .
```

Or install for current user only:
```bash
pip install --user -e .
```

### Module Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Python Version Issues

Check your Python version:
```bash
python --version  # Should be 3.7+
```

If you have multiple Python versions:
```bash
python3 -m pip install -e .
```

## Uninstallation

```bash
pip uninstall gitgoblin
```

## Updating

```bash
cd gitgoblin
git pull  # If installed from git
pip install --upgrade -e .
```

## Next Steps

After installation, check out:
- `README.md` - Full documentation
- `gitgoblin --help` - Command reference
- `gitgoblin summon --help` - Command-specific help

**Happy goblin summoning! 👹**

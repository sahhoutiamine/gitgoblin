#!/bin/bash

# GitGoblin Quick Start Test Script
# This script helps you test GitGoblin with a demo repository

set -e

echo "============================================"
echo "👹 GitGoblin Quick Start Test"
echo "============================================"
echo ""

# Check if gitgoblin is installed
if ! command -v gitgoblin &> /dev/null; then
    echo "❌ GitGoblin is not installed!"
    echo "📦 Installing GitGoblin..."
    pip install -e .
    echo "✅ GitGoblin installed!"
    echo ""
fi

# Create test directory
TEST_DIR="gitgoblin-test-$(date +%s)"
echo "📁 Creating test repository: $TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Initialize git
echo "🔧 Initializing Git repository..."
git init
git config user.name "GitGoblin Tester"
git config user.email "test@gitgoblin.dev"

# Create initial files
echo "📝 Creating test files..."
cat > README.md << 'EOF'
# GitGoblin Test Repository

This is a test repository for GitGoblin!

## What is this?

Testing the automatic commit and push functionality.
EOF

cat > test.py << 'EOF'
def hello_goblin():
    """Say hello to the goblin!"""
    print("👹 Hello, GitGoblin!")

if __name__ == "__main__":
    hello_goblin()
EOF

# Initial commit
echo "💾 Creating initial commit..."
git add .
git commit -m "Initial commit - GitGoblin test setup"

echo ""
echo "✅ Test repository created successfully!"
echo ""
echo "============================================"
echo "📋 Next Steps:"
echo "============================================"
echo ""
echo "1. (Optional) Add GitHub remote:"
echo "   git remote add origin YOUR_GITHUB_REPO_URL"
echo ""
echo "2. Start GitGoblin:"
echo "   gitgoblin summon"
echo ""
echo "3. In another terminal, edit files:"
echo "   cd $TEST_DIR"
echo "   nano test.py  # or use any editor"
echo ""
echo "4. Save the file and watch GitGoblin work!"
echo ""
echo "5. Check status:"
echo "   gitgoblin crystalball"
echo ""
echo "6. Stop GitGoblin:"
echo "   gitgoblin banish"
echo ""
echo "============================================"
echo "🎉 Happy testing!"
echo "============================================"

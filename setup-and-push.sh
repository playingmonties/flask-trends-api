#!/bin/bash

# Complete setup and push script for Flask Trends API
# GitHub: playingmonties

echo "🚀 Setting up Git and pushing to GitHub..."

# Configure git if needed (uncomment if you need to set these)
# git config user.name "playingmonties"
# git config user.email "thomasmccone@gmail.com"

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
git add .

# Commit if there are changes
if ! git diff --staged --quiet; then
    git commit -m "Initial commit: Flask Trends API"
    echo "✅ Files committed"
fi

# Create GitHub repo and push (if gh CLI is available)
if command -v gh &> /dev/null; then
    echo "📦 Creating GitHub repository..."
    gh repo create flask-trends-api --public --source=. --remote=origin --push
    echo "✅ Repository created and pushed to GitHub!"
    echo ""
    echo "🔗 Your repository: https://github.com/playingmonties/flask-trends-api"
else
    echo "⚠️  GitHub CLI (gh) not found."
    echo ""
    echo "Option 1: Install GitHub CLI and run this script again:"
    echo "  brew install gh"
    echo "  gh auth login"
    echo ""
    echo "Option 2: Create the repo manually on GitHub, then run:"
    echo "  git remote add origin https://github.com/playingmonties/flask-trends-api.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi

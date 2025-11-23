#!/bin/bash

# Git setup script for Flask Trends API
# Run this script from the project directory

echo "🚀 Setting up Git repository..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already exists"
fi

# Add all files
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    git commit -m "Initial commit: Flask Trends API"
    echo "✅ Files committed"
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "ℹ️  Remote 'origin' already exists"
    echo "Current remote URL:"
    git remote get-url origin
else
    echo ""
    echo "📝 To add your GitHub repository, run:"
    echo "   git remote add origin <your-github-repo-url>"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "Or if you have GitHub CLI installed:"
    echo "   gh repo create flask-trends-api --public --source=. --remote=origin --push"
fi

echo ""
echo "✨ Git setup complete!"


# Quick Setup Guide

## Your GitHub Info
- **Username**: playingmonties
- **Email**: thomasmccone@gmail.com
- **Repository URL**: https://github.com/playingmonties/flask-trends-api

## Option 1: Using GitHub CLI (Recommended)

If you have GitHub CLI installed and authenticated:

```bash
cd ~/cursor/flask-trends-api
chmod +x setup-and-push.sh
./setup-and-push.sh
```

This will automatically:
- Initialize git
- Commit all files
- Create the GitHub repository
- Push everything to GitHub

## Option 2: Manual Setup

### Step 1: Initialize and Commit
```bash
cd ~/cursor/flask-trends-api
git init
git add .
git commit -m "Initial commit: Flask Trends API"
```

### Step 2: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `flask-trends-api`
3. Make it Public
4. **Don't** initialize with README (you already have one)
5. Click "Create repository"

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/playingmonties/flask-trends-api.git
git branch -M main
git push -u origin main
```

## After Pushing to GitHub

Once your code is on GitHub, you can deploy to Render:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select the `flask-trends-api` repository
5. Configure:
   - **Name**: flask-trends-api
   - **Environment**: Docker
   - **Port**: 8080
6. Click "Create Web Service"

Your API will be live at: `https://flask-trends-api.onrender.com` (or similar)


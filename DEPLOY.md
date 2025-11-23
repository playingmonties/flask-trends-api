# Deployment Steps

## 1. Initialize Git and Commit

```bash
cd ~/cursor/flask-trends-api
git init
git add .
git commit -m "Initial commit: Flask Trends API"
```

## 2. Create GitHub Repository

1. Go to GitHub and create a new repository (don't initialize with README)
2. Copy the repository URL

## 3. Push to GitHub

```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## 4. Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select the repository
4. Configure:
   - **Name**: flask-trends-api (or your preferred name)
   - **Environment**: Docker
   - **Region**: Choose closest to you
   - **Branch**: main
   - **Root Directory**: (leave empty)
   - **Dockerfile Path**: Dockerfile (should auto-detect)
   - **Port**: 8080
5. Click "Create Web Service"
6. Render will automatically build and deploy your app!

## 5. Test Your API

Once deployed, Render will give you a URL like: `https://flask-trends-api.onrender.com`

Test it:
```bash
curl "https://your-app-url.onrender.com/trends?keywords=runescape"
```


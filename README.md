# Flask Trends API

A Flask API that fetches Google Trends data for specified keywords.

## Endpoints

- `GET /` - Health check endpoint
- `GET /trends?keywords=keyword1,keyword2` - Fetch trends data for the last 30 days

## Example

```bash
curl "http://localhost:8080/trends?keywords=runescape,python"
```

## Deployment

This project is configured for deployment on Render using Docker.


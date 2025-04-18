# Youtube-Video-Description-Translator

A simple Flask web app that fetches YouTube video data and translates video descriptions into multiple languages using Google Cloud Translation API. Designed for real-time access, lightweight deployment, and secure key management.

## 🔧 What It Does

- Fetches video data using YouTube Data API
- Translates descriptions into selected languages
- Stores translations in Google Cloud Storage as JSON
- Uses Docker for optimized deployment
- Runs on Google Cloud Run (fully serverless)
- Manages secrets securely with Google Cloud Secrets Manager

# DayLife Scheduler 🗓️⏳

An AI-powered daily schedule generator that syncs with your calendar, helping you balance job applications, fitness, coding practice, and classes.

## Features ✨
- Generates optimized daily schedules based on your goals
- Integrates with DeepSeek AI for smart scheduling
- Responsive React frontend
- FastAPI backend with CORS support
- Easy calendar export

## Prerequisites 📋
- Python 3.9+
- Node.js 16+
- Pipenv
- Grok API key

## Setup Instructions 🛠️

### 1. Backend Setup
```bash
cd backend
pipenv install
echo "GROK_API_KEY=your_api_key_here" > .env
pipenv run python app.py
# DayLife Scheduler 🗓️⏳

An AI-powered daily schedule generator that creates optimized routines and exports them directly to your calendar.

![Schedule Generator Interface](/Users/maana/Documents/Calendar Syncer/screenshots/cal_scheduler_ss1.png)
![Calendar Export](/Users/maana/Documents/Calendar Syncer/screenshots/cal_scheduler_ss2.png)


## Key Features ✨

- 🧠 **AI-Powered Scheduling** - Uses Groq's ultra-fast LLMs to generate optimal daily plans
- 📅 **Calendar Integration** - One-click export to Apple/Google Calendar via ICS files
- ⚡ **FastAPI Backend** - Robust Python backend with async support
- 🎨 **React Frontend** - Modern, responsive user interface
- 🔄 **CORS Support** - Seamless frontend-backend communication

## Tech Stack 🛠️

| Component       | Technology |
|-----------------|------------|
| Frontend        | React 18   |
| Backend         | FastAPI    |
| AI Integration  | Groq API   |
| Calendar Export | ICS format |
| Package Manager | Pipenv     |

## Setup Guide 🚀

### Prerequisites

- Python 3.9+
- Node.js 16+
- Groq API key ([get one here](https://console.groq.com/keys))
- Pipenv (`pip install pipenv`)

### Backend Installation

```
cd backend

pip install -r requirements.txt

pipenv install
pipenv install ics python-dotenv requests fastapi uvicorn

echo "GROQ_API_KEY=your_api_key_here" > .env

pipenv run uvicorn app:app --reload
```

### Frontend Installation

```
cd ../frontend
npm install
npm start
```
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScheduleRequest(BaseModel):
    goals: str
    constraints: str = ""
    preferred_wakeup: str = "8:00 AM"
    preferred_bedtime: str = "11:00 PM"

@app.post("/generate-schedule")
async def generate_schedule(request: ScheduleRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Create a detailed daily schedule in markdown format with time blocks.
    Goals: {request.goals}
    Constraints: {request.constraints}
    Preferred Wake Up: {request.preferred_wakeup}
    Preferred Bedtime: {request.preferred_bedtime}

    Format each entry like this:
    [start time]-[end time] | [activity] | [category: personal/work/study/fitness]
    """

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        response.raise_for_status()
        
        # Parse the Groq response
        schedule_text = response.json()["choices"][0]["message"]["content"]
        schedule_lines = [line.strip() for line in schedule_text.split('\n') if line.strip()]
        
        schedule = []
        for line in schedule_lines:
            if '|' in line:
                time_range, activity, category = [part.strip() for part in line.split('|')]
                start_time, end_time = [time.strip() for time in time_range.split('-')]
                schedule.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "activity": activity,
                    "category": category.split(':')[-1].strip().lower()
                })
        
        return {"schedule": schedule}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "DayLife Scheduler API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
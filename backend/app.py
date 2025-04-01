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
        "Content-Type": "application/json",
        "User-Agent": "DayLifeScheduler/1.0"
    }

    # Improved prompt formatting
    prompt = f"""Create a detailed daily schedule with these requirements:
    
    Goals: {request.goals}
    Constraints: {request.constraints}
    Wake Up Time: {request.preferred_wakeup}
    Bedtime: {request.preferred_bedtime}
    
    Return the schedule in this EXACT format:
    [start time]-[end time] | [activity] | [category]
    
    Example:
    8:00 AM-9:00 AM | Morning Routine | personal
    9:00 AM-10:30 AM | Job Applications | work
    """

    try:
        response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers=headers,
    json={
        "model": "llama3-70b-8192",  # ✅ Current recommended model
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    timeout=30
)
        
        # Enhanced error handling
        if response.status_code == 400:
            error_detail = response.json().get('error', {}).get('message', 'Invalid request')
            raise HTTPException(
                status_code=400,
                detail=f"Groq API rejected request: {error_detail}"
            )
        response.raise_for_status()
        
        # Parse response with better validation
        groq_response = response.json()
        if not groq_response.get('choices'):
            raise ValueError("Invalid response format from Groq API")
            
        schedule_text = groq_response['choices'][0]['message']['content']
        schedule_lines = [
            line.strip() 
            for line in schedule_text.split('\n') 
            if line.strip() and '|' in line
        ]
        
        schedule = []
        for line in schedule_lines:
            try:
                time_range, activity, category = [
                    part.strip() 
                    for part in line.split('|', 2)  # Split on first 2 pipes only
                ]
                start_time, end_time = [
                    time.strip() 
                    for time in time_range.split('-', 1)  # Split on first hyphen only
                ]
                schedule.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "activity": activity,
                    "category": category.split(':')[-1].strip().lower()
                })
            except ValueError as e:
                continue  # Skip malformed lines
                
        if not schedule:
            raise ValueError("No valid schedule entries found in response")
            
        return {"schedule": schedule}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Network error communicating with Groq API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "DayLife Scheduler API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test successful"}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Changed from 127.0.0.1 to 0.0.0.0
        port=8000,
        log_level="debug"
    )
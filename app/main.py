from fastapi import FastAPI
import uvicorn
from app.services.scheduler_service import start_scheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="BPAR System", lifespan=lifespan)

@app.get("/")
def read_root():
    return {
        "status": "BPAR System is running", 
        "scheduler": "Active"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
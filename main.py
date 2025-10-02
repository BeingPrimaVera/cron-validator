from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from croniter import croniter
from datetime import datetime

app = FastAPI(title="Cron Validator API", version="1.0.0")

class CronRequest(BaseModel):
    cron: str
    tz: str = "UTC"

class CronResponse(BaseModel):
    valid: bool
    next_run: str | None = None
    human_readable: str | None = None

@app.post("/validate", response_model=CronResponse)
async def validate_cron(request: CronRequest):
    try:
        # Validate cron expression
        if not croniter.is_valid(request.cron):
            return CronResponse(valid=False)
        
        # Create croniter object
        cron = croniter(request.cron, datetime.now())
        
        # Get next run time
        next_run = cron.get_next(datetime)
        
        # Generate a simple human-readable description
        human_readable = f"Next run at {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return CronResponse(
            valid=True,
            next_run=next_run.isoformat(),
            human_readable=human_readable
        )
        
    except Exception as e:
        return CronResponse(valid=False, human_readable=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Cron Validator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
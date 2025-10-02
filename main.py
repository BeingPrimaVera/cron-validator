from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from croniter import croniter
from datetime import datetime
import pytz

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
    """
    Validate a cron expression and return the next run time and human-readable description.
    
    Args:
        request: CronRequest with cron expression and timezone
        
    Returns:
        CronResponse with validation result and scheduling info
    """
    try:
        # Validate timezone
        try:
            timezone = pytz.timezone(request.tz)
        except pytz.UnknownTimeZoneError:
            return CronResponse(valid=False)
        
        # Validate cron expression
        if not croniter.is_valid(request.cron):
            return CronResponse(valid=False)
        
        # Create croniter object
        cron = croniter(request.cron, datetime.now(timezone))
        
        # Get next run time
        next_run = cron.get_next(datetime)
        
        # Generate human-readable description
        # This is a simplified version - in production you might want a more sophisticated parser
        human_readable = get_human_readable_description(request.cron)
        
        return CronResponse(
            valid=True,
            next_run=next_run.isoformat(),
            human_readable=human_readable
        )
        
    except Exception:
        return CronResponse(valid=False)

def get_human_readable_description(cron_expr: str) -> str:
    """
    Convert a cron expression to a human-readable description.
    This is a basic implementation that covers common patterns.
    """
    parts = cron_expr.split()
    
    if len(parts) != 5:
        return f"Cron expression: {cron_expr}"
    
    minute, hour, day, month, day_of_week = parts
    
    # Handle common patterns
    if minute == "0" and hour != "*" and day == "*" and month == "*" and day_of_week == "*":
        return f"At {hour.zfill(2)}:00 every day"
    
    if minute == "0" and hour == "4" and day == "*" and month == "*" and day_of_week == "*":
        return "At 04:00 AM every day"
    
    if minute == "0" and hour == "0" and day == "*" and month == "*" and day_of_week == "*":
        return "At midnight every day"
    
    if minute == "0" and hour == "0" and day == "1" and month == "*" and day_of_week == "*":
        return "At midnight on the first day of every month"
    
    if minute == "0" and hour == "0" and day == "*" and month == "*" and day_of_week == "0":
        return "At midnight every Sunday"
    
    if minute == "*" and hour == "*" and day == "*" and month == "*" and day_of_week == "*":
        return "Every minute"
    
    # For more complex patterns, return the raw expression
    return f"Cron: {cron_expr}"

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
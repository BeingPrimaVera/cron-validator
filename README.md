# Cron Validator API

A simple FastAPI service that validates cron expressions and returns next run times with human-readable descriptions.

## Features

- Validate cron expressions
- Get next run time in ISO format
- Human-readable descriptions for common patterns
- Timezone support
- FastAPI with automatic API documentation

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Deploy to Render

1. Create a Render account at [render.com](https://render.com)
2. Connect your GitHub repository or upload this folder
3. Render will automatically detect the `render.yaml` file
4. Deploy the service

### Manual Deployment

If not using the `render.yaml` file:

1. Create a new Web Service on Render
2. Set the environment to Python
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy

## API Usage

### Validate Cron Expression

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "cron": "0 4 * * *",
    "tz": "UTC"
  }'
```

Expected response:
```json
{
  "valid": true,
  "next_run": "2024-01-02T04:00:00+00:00",
  "human_readable": "At 04:00 AM every day"
}
```

### Test Invalid Cron

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "cron": "invalid cron",
    "tz": "UTC"
  }'
```

Expected response:
```json
{
  "valid": false,
  "next_run": null,
  "human_readable": null
}
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

## Testing

Run the included tests with pytest:

```bash
pytest test_main.py -v
```

## Project Structure

```
.
├── main.py          # FastAPI application
├── requirements.txt  # Python dependencies
├── render.yaml     # Render deployment config
├── test_main.py    # Pytest test cases
└── README.md       # This file
```

## License

MIT License - feel free to use this project for any purpose.
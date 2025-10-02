import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_valid_cron():
    """Test valid cron expression"""
    response = client.post(
        "/validate",
        json={"cron": "0 4 * * *", "tz": "UTC"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    assert data["next_run"] is not None
    assert data["human_readable"] is not None
    assert "04:00" in data["human_readable"]

def test_invalid_cron():
    """Test invalid cron expression"""
    response = client.post(
        "/validate",
        json={"cron": "invalid cron", "tz": "UTC"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == False
    assert data["next_run"] is None
    assert data["human_readable"] is None

def test_invalid_timezone():
    """Test invalid timezone"""
    response = client.post(
        "/validate",
        json={"cron": "0 4 * * *", "tz": "Invalid/Timezone"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == False

def test_valid_cron_different_timezone():
    """Test valid cron with different timezone"""
    response = client.post(
        "/validate",
        json={"cron": "0 4 * * *", "tz": "America/New_York"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    assert data["next_run"] is not None
    assert "04:00" in data["human_readable"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Cron Validator API"
    assert "docs" in data

@pytest.mark.parametrize("cron_expr,expected_phrase", [
    ("0 0 * * *", "00:00 every day"),
    ("0 0 1 * *", "first day of every month"),
    ("0 0 * * 0", "every Sunday"),
    ("* * * * *", "Every minute"),
])
def test_common_cron_patterns(cron_expr, expected_phrase):
    """Test common cron patterns return human-readable descriptions"""
    response = client.post(
        "/validate",
        json={"cron": cron_expr, "tz": "UTC"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    assert expected_phrase in data["human_readable"]
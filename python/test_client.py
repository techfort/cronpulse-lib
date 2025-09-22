import pytest
from cronpulse_lib import CronPulse
from datetime import datetime, UTC

@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception("HTTP Error")

    def mock_post(*args, **kwargs):
        return MockResponse({"id": "123"}, 200)

    monkeypatch.setattr("requests.post", mock_post)
    monkeypatch.setattr("requests.delete", mock_post)

def test_create_monitor(mock_requests):
    cp = CronPulse("test_api_key")
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    assert monitor.monitor_id == "123"

def test_ping(mock_requests):
    cp = CronPulse("test_api_key")
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    monitor.ping()  # Should not raise

def test_delete(mock_requests):
    cp = CronPulse("test_api_key")
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    monitor.delete()  # Should not raise

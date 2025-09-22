import pytest
from cronpulse_lib import CronPulse
from datetime import datetime, UTC, timedelta

@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self._json = json_data
            self.status_code = status_code
            self.url = "https://example.test/mock"
            self.reason = "OK" if status_code < 400 else "ERR"

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP Error {self.status_code}")

    calls = []  # capture calls for assertions

    def fake_request(method, url, json=None, headers=None, timeout=None):
        calls.append({"method": method, "url": url, "json": json, "headers": headers})
        if method == "POST" and url.endswith("/monitors"):
            return MockResponse({"id": "123"})
        if method == "POST" and url.endswith("/ping"):
            return MockResponse({}, 200)
        if method == "DELETE" and "/monitors/" in url:
            return MockResponse({}, 200)
        if method == "POST" and url.endswith("/monitors") and json and json.get("name") == "fail":
            return MockResponse({"error": "bad"}, 400)
        return MockResponse({}, 404)

    # Patch after client instantiation; we patch on session object.
    def patch_session(client: CronPulse):
        monkeypatch.setattr(client._session, "request", fake_request)
        # attach calls list for assertions
        client._test_calls = calls  # type: ignore[attr-defined]
        return client

    return patch_session

def test_create_monitor(mock_requests):
    cp = mock_requests(CronPulse("test_api_key"))
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    assert monitor.monitor_id == "123"
    # verify authorization header used on first call
    first = cp._test_calls[0]  # type: ignore[index]
    assert first["headers"]["Authorization"].startswith("Bearer ")
    # verify expires_at isoformat serialization
    assert "T" in first["json"]["expires_at"]

def test_ping(mock_requests):
    cp = mock_requests(CronPulse("test_api_key"))
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    monitor.ping()  # Should not raise
    # ensure ping path called
    urls = [c["url"] for c in cp._test_calls]  # type: ignore[attr-defined]
    assert any(u.endswith("/ping") for u in urls)

def test_delete(mock_requests):
    cp = mock_requests(CronPulse("test_api_key"))
    monitor = cp.create_monitor("Test Monitor", 60, "test@example.com", datetime.now(UTC))
    monitor.delete()  # Should not raise
    urls = [c["url"] for c in cp._test_calls]  # type: ignore[attr-defined]
    expected_delete_prefix = f"{cp.base_url}/monitors/{monitor.monitor_id}"
    assert any(u == expected_delete_prefix for u in urls), "Delete endpoint not called"

def test_error_raises(monkeypatch):
    cp = CronPulse("test_api_key")
    # patch to raise 400
    class BadResponse:
        status_code = 400
        def raise_for_status(self):
            raise Exception("HTTP Error 400")
        def json(self):
            return {"error": "bad"}
    def bad_request(method, url, json=None, headers=None, timeout=None):
        return BadResponse()
    monkeypatch.setattr(cp._session, "request", bad_request)
    with pytest.raises(Exception):
        cp.create_monitor("Bad", 60, "x@y.com", datetime.now(UTC) + timedelta(hours=1))

from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    # Restore the original state to keep tests isolated.
    client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )


def test_unregister_missing_participant_returns_404():
    response = client.delete(
        "/activities/Chess Club/unregister?email=ghost@mergington.edu"
    )

    assert response.status_code == 404

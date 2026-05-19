from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 200

    # Verify participant present on subsequent fetch
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_duplicate_signup_returns_400():
    activity = "Chess Club"
    email = "michael@mergington.edu"  # initial participant
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 400


def test_signup_missing_activity_returns_404():
    resp = client.post(f"/activities/{quote('Nonexistent')}/signup?email={quote('a@b.com')}")
    assert resp.status_code == 404


def test_remove_participant_success():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    resp = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert resp.status_code == 200

    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    activity = "Chess Club"
    email = "noone@mergington.edu"
    resp = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert resp.status_code == 404

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_user_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    chess_club = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in chess_club["participants"]


def test_unregister_nonexistent_participant_returns_not_found():
    response = client.delete("/activities/Chess Club/participants/not-a-student@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"

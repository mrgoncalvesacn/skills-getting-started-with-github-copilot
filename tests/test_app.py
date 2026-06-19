"""
FastAPI backend tests for the Mergington High School Activities API.
Uses Arrange-Act-Assert structure for clarity and maintainability.
"""

from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swim Team",
        "Art Club",
        "Drama Club",
        "Math Club",
        "Debate Team",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == expected_activity_names
    assert len(data) == 9


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Math Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1

    # Cleanup
    activities[activity_name]["participants"].remove(email)


def test_signup_duplicate_fails():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert len(activities[activity_name]["participants"]) == initial_count


def test_remove_participant_removes_participant():
    # Arrange
    activity_name = "Art Club"
    email = "lucas@mergington.edu"
    assert email in activities[activity_name]["participants"]
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1

    # Cleanup
    activities[activity_name]["participants"].append(email)


def test_remove_nonexistent_participant_returns_404():
    # Arrange
    activity_name = "Soccer Team"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_nonexistent_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

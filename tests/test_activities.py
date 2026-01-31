"""Tests for the activities endpoints"""
import pytest


def test_get_activities(client, reset_activities):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert len(data) == 9


def test_get_activities_has_required_fields(client, reset_activities):
    """Test that activities have all required fields"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_chess_club_participants(client, reset_activities):
    """Test that Chess Club has initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    participants = data["Chess Club"]["participants"]
    assert len(participants) == 2
    assert "michael@mergington.edu" in participants
    assert "daniel@mergington.edu" in participants


def test_root_redirects_to_index(client):
    """Test that root path redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

"""Tests for the unregister endpoint"""
import pytest


def test_unregister_success(client, reset_activities):
    """Test successfully unregistering from an activity"""
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregistering actually removes the participant"""
    # Verify participant is initially there
    response = client.get("/activities")
    assert "michael@mergington.edu" in response.json()["Chess Club"]["participants"]
    
    # Unregister
    client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant is removed
    response = client.get("/activities")
    assert "michael@mergington.edu" not in response.json()["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity(client, reset_activities):
    """Test unregistering from an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_not_registered(client, reset_activities):
    """Test unregistering when not registered for the activity"""
    response = client.post(
        "/activities/Basketball Team/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_multiple_participants(client, reset_activities):
    """Test unregistering one participant doesn't affect others"""
    # Get initial participants
    response = client.get("/activities")
    chess_participants = response.json()["Chess Club"]["participants"].copy()
    initial_count = len(chess_participants)
    
    # Unregister one
    client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Check that only one was removed
    response = client.get("/activities")
    remaining = response.json()["Chess Club"]["participants"]
    assert len(remaining) == initial_count - 1
    assert "daniel@mergington.edu" in remaining
    assert "michael@mergington.edu" not in remaining


def test_unregister_then_signup_same_activity(client, reset_activities):
    """Test that a student can sign up after unregistering from another activity"""
    # Unregister from Chess Club
    client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Now they should be able to sign up for another activity
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    
    # Verify they're in Basketball Team
    activities_response = client.get("/activities")
    assert "michael@mergington.edu" in activities_response.json()["Basketball Team"]["participants"]

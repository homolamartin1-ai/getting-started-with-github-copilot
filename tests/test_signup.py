"""Tests for the signup endpoint"""
import pytest


def test_signup_for_activity_success(client, reset_activities):
    """Test successfully signing up for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "new.student@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "new.student@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_for_activity_adds_participant(client, reset_activities):
    """Test that signing up actually adds the participant"""
    client.post(
        "/activities/Basketball Team/signup",
        params={"email": "new.student@mergington.edu"}
    )
    
    response = client.get("/activities")
    data = response.json()
    assert "new.student@mergington.edu" in data["Basketball Team"]["participants"]


def test_signup_for_nonexistent_activity(client, reset_activities):
    """Test signing up for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "new.student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_already_registered(client, reset_activities):
    """Test signing up when already registered for an activity"""
    # Try to sign up with an email that's already registered
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_different_activities(client, reset_activities):
    """Test signing up for different activities"""
    email = "student@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Try to sign up for second activity (should fail - can only be in one)
    response2 = client.post(
        "/activities/Soccer Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 400


def test_signup_with_email_parameter(client, reset_activities):
    """Test that email parameter is used correctly"""
    test_email = "test.user@mergington.edu"
    response = client.post(
        "/activities/Art Club/signup",
        params={"email": test_email}
    )
    assert response.status_code == 200
    
    # Verify the email was added
    activities_response = client.get("/activities")
    assert test_email in activities_response.json()["Art Club"]["participants"]

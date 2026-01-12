import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """アクティビティの一覧を取得できることを確認するテスト"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    """新しい参加者がアクティビティに正常にサインアップできることを確認するテスト"""
    # Test signing up for an activity
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_already_signed_up():
    """既にサインアップ済みの参加者が再度サインアップしようとするとエラーになることを確認するテスト"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    """存在しないアクティビティにサインアップしようとするとエラーになることを確認するテスト"""
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    """サインアップ済みの参加者がアクティビティから正常にアンサインアップできることを確認するテスト"""
    # First signup
    client.post("/activities/Programming%20Class/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Programming%20Class/participants/unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Programming Class"]["participants"]

def test_unregister_not_signed_up():
    """サインアップしていない参加者をアンサインアップしようとするとエラーになることを確認するテスト"""
    response = client.delete("/activities/Chess%20Club/participants/notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    """存在しないアクティビティからアンサインアップしようとするとエラーになることを確認するテスト"""
    response = client.delete("/activities/Nonexistent/participants/test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
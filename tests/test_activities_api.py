import pytest


class TestActivitiesAPI:
    
    def test_get_activities(self, client, reset_activities):
        """Arrange, Act, Assert: Retrieve all activities."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert data["Chess Club"]["max_participants"] == 12
    
    def test_signup_for_activity(self, client, reset_activities):
        """Arrange, Act, Assert: Successfully sign up for an activity."""
        activity_name = "Chess Club"
        email = "newparticipant@mergington.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant(self, client, reset_activities):
        """Arrange, Act, Assert: Reject duplicate signup for same activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_delete_participant(self, client, reset_activities):
        """Arrange, Act, Assert: Successfully remove participant from activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        
        activities_response = client.get("/activities")
        assert email not in activities_response.json()["Chess Club"]["participants"]
    
    def test_delete_missing_participant(self, client, reset_activities):
        """Arrange, Act, Assert: Fail when trying to remove non-existent participant."""
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
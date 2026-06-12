def test_get_activities_returns_activities(client):
    # Arrange (handled by fixture)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "test_student@example.com"

    # Act
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_existing_returns_400(client):
    # Arrange
    email = "existing@example.com"

    # Act
    first = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert first.status_code == 200
    second = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert second.status_code == 400


def test_remove_participant_removes_user(client):
    # Arrange
    email = "removable@example.com"
    signup = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert signup.status_code == 200

    # Act
    resp = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]

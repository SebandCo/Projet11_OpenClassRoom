def test_showSummary_with_valid_email(mocker, client, club_fixture, backup_json):

    # Permet au mock de renvoyer la liste de clubs fictifs venant de fixture
    mocker.patch("server.loadClubs", return_value=club_fixture)
    response = client.post('/showSummary', data={'email': club_fixture[0]["email"]})

    expected_value_name = club_fixture[0]["name"].encode()
    expected_value_email = club_fixture[0]["email"].encode()
    expected_value_points = club_fixture[0]["points"].encode()

    assert response.status_code == 200
    assert expected_value_name in response.data
    assert expected_value_email in response.data
    assert expected_value_points in response.data


def test_showSummary_invalid_mail(client):
    response = client.post("/showSummary", data={"email": "invalid@test.com"})
    donnee_decryptee = response.data.decode()
    expected_value = "Unknown Email"
    assert response.status_code == 200
    assert expected_value in donnee_decryptee


def test_showSummary_no_mail(client):
    response = client.post("/showSummary", data={"email": ""})
    donnee_decryptee = response.data.decode()
    expected_value = "No Email"
    assert response.status_code == 200
    assert expected_value in donnee_decryptee

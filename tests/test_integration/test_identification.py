from bs4 import BeautifulSoup


def test_showSummary_send_valid_email(mocker, client, club_fixture, competition_fixture, backup_json):

    # Permet au mock de renvoyer la liste de clubs fictifs venant de fixture
    mocker.patch("server.loadClubs", return_value=club_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)
    response = client.post('/showSummary', data={'email': club_fixture[0]["email"]})

    soup = BeautifulSoup(response.data, "html.parser")

    competition_valid = soup.find(lambda tag: tag.name == "li" and "competition_valid_test" in tag.text).decode()
    expected_value_competition_valid = "Book Places"

    competition_invalid = soup.find(lambda tag: tag.name == "li" and "competition_invalid_test" in tag.text).decode()
    expected_value_competition_invalid = "La compétition est terminée"

    assert response.status_code == 200
    assert expected_value_competition_valid in competition_valid
    assert expected_value_competition_invalid in competition_invalid

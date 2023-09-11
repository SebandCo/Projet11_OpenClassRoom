def test_affichageReservation(mocker, client, historique_fixture, competition_fixture, club_fixture, backup_json):

    # Permet au mock de renvoyer la liste de clubs fictifs venant de fixture
    mocker.patch("server.loadHistoryReservation", return_value=historique_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)
    mocker.patch("server.loadClubs", return_value=club_fixture)

    response = client.get('/affichageReservation')

    expected_value_competition_valid_test = "5"
    expected_value_competition_valid_test2 = "25"

    donnee_decryptee = response.data.decode()

    assert response.status_code == 200
    assert expected_value_competition_valid_test in donnee_decryptee
    assert expected_value_competition_valid_test2 in donnee_decryptee

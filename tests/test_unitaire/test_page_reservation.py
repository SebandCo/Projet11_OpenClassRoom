def lancement_page_booking(mocker,
                           client,
                           club_fixture,
                           competition_fixture,
                           data_club,
                           data_competition,
                           expected_value_booking):
    # Permet au mock de renvoyer les listes venant de fixture
    mocker.patch("server.loadClubs", return_value=club_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)

    expected_value_name_competition = data_competition["name"]
    expected_value_points_club = data_club["points"]

    response = client.get(f"/book/{data_competition['name']}/{data_club['name']}")
    donnee_decryptee = response.data.decode()

    assert response.status_code == 200
    assert expected_value_booking in donnee_decryptee
    assert expected_value_name_competition in donnee_decryptee
    assert expected_value_points_club in donnee_decryptee


def test_affichage_booking_page_competition_valid(mocker, client, club_fixture, competition_fixture, backup_json):
    data_club = club_fixture[0]
    data_competition = competition_fixture[0]

    expected_value_booking = "Book"

    lancement_page_booking(mocker,
                           client,
                           club_fixture,
                           competition_fixture,
                           data_club,
                           data_competition,
                           expected_value_booking)


def test_affichage_booking_page_competition_invalid(mocker, client, club_fixture, competition_fixture, backup_json):
    data_club = club_fixture[0]
    data_competition = competition_fixture[1]

    expected_value_booking = "Festival Over"

    lancement_page_booking(mocker,
                           client,
                           club_fixture,
                           competition_fixture,
                           data_club,
                           data_competition,
                           expected_value_booking)


def test_affichage_booking_erreur_club_navigation(mocker, client, club_fixture, competition_fixture, backup_json):

    mocker.patch("server.loadClubs", return_value=club_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)

    data_club = club_fixture[0]

    response = client.get(f"/book/competition_erroné/{data_club['name']}")
    donnee_decryptee = response.data.decode()

    expected_value_booking = "Something went wrong"

    assert response.status_code == 200
    assert expected_value_booking in donnee_decryptee


def test_affichage_booking_erreur_competition_navigation(mocker, client, club_fixture, competition_fixture, backup_json):

    mocker.patch("server.loadClubs", return_value=club_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)

    data_competition = competition_fixture[0]

    response = client.get(f"/book/{data_competition['name']}/club_erroné")
    donnee_decryptee = response.data.decode()

    expected_value_booking = "Something went wrong"

    assert response.status_code == 200
    assert expected_value_booking in donnee_decryptee

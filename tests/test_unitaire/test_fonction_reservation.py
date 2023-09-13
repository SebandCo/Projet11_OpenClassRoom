def lancement_purchasePlaces(mocker,
                             client,
                             club_fixture,
                             competition_fixture,
                             historique_fixture,
                             data_place_reservee,
                             expected_value_point_club,
                             expected_value_point_competition):
    # Permet au mock de renvoyer les listes venant de fixture
    mocker.patch("server.loadClubs", return_value=club_fixture)
    mocker.patch("server.loadCompetitions", return_value=competition_fixture)
    mocker.patch("server.loadHistoryReservation", return_value=historique_fixture)

    data_club = club_fixture[0]["name"]
    data_competition = competition_fixture[0]["name"]
    data_place_reservee = data_place_reservee

    data = {
        "club": data_club,
        "competition": data_competition,
        "places": str(data_place_reservee)
    }

    response = client.post("/purchasePlaces", data=data)

    # Vérifie que la requete fonctionne
    assert response.status_code == 200
    # Vérifie que le nombre de point du club est à jour
    assert club_fixture[0]["points"] == expected_value_point_club.decode()
    # Vérifie que le nombre de point de la compétition est à jour
    assert (competition_fixture[0]["numberOfPlaces"]) == expected_value_point_competition.decode()

    return response


def test_purchasePlaces_valid(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    data_place_reservee = 4
    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    expected_value_point_club = str(int(points_club_start) - data_place_reservee).encode()
    expected_value_point_competition = str(int(place_competition_start) - data_place_reservee).encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Great-booking complete!" in response.data
    assert expected_value_point_club in response.data
    assert expected_value_point_competition in response.data


def test_purchasePlaces_zero_place(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    data_place_reservee = 0
    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    expected_value_point_club = str(int(points_club_start) - data_place_reservee).encode()
    expected_value_point_competition = str(int(place_competition_start) - data_place_reservee).encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Zero Place" in response.data


def test_purchasePlaces_negative_place(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    data_place_reservee = -1
    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Negative Place" in response.data


def test_purchasePlaces_invalid_overtaking_club_place(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    data_place_reservee = 11
    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Overtaking Club Place" in response.data


def test_purchasePlaces_invalid_overtaking_festival_place(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    competition_fixture[0]["numberOfPlaces"] = "0"

    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    data_place_reservee = 4
    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Overtaking Festival Place" in response.data


def test_purchasePlaces_invalid_too_many_athletes(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    club_fixture[0]["points"] = "50"

    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    data_place_reservee = 13
    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Too Many Athletes" in response.data


def test_purchasePlaces_invalid_no_tickets_purchased(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    data_place_reservee = "erreur de saisie"
    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"No Tickets Purchased" in response.data


def test_purchasePlaces_invalid_festival_over(mocker, client, club_fixture, competition_fixture, historique_fixture, backup_json):

    competition_fixture[0]["date"] = "1901-01-01 12:00:00"

    points_club_start = club_fixture[0]["points"]
    place_competition_start = competition_fixture[0]["numberOfPlaces"]

    data_place_reservee = "2"
    expected_value_point_club = points_club_start.encode()
    expected_value_point_competition = place_competition_start.encode()

    response = lancement_purchasePlaces(mocker,
                                        client,
                                        club_fixture,
                                        competition_fixture,
                                        historique_fixture,
                                        data_place_reservee,
                                        expected_value_point_club,
                                        expected_value_point_competition)

    # Vérifie que la réponse est correcte
    assert b"Festival Over" in response.data

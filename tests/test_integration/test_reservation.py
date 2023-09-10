import json


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
    # Vérifie que le fichier json historique se met correctement à jour
    with open("historique_reservation.json", "r") as historique_json:
        data = json.load(historique_json)
        for reservation in data["reservation"]:
            if reservation["competition"] == competition_fixture[0]["name"]:
                assert True
                break
        else:
            assert False

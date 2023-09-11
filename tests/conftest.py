import pytest
import os
from server import app


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        with app.app_context():
            yield c


@pytest.fixture(scope="function")
def backup_json():
    # Sauvegarde une copie du fichier historique_reservation
    with open("historique_reservation.json", "r") as histo_json:
        data_histo = histo_json.read()
    with open("data_histo_backup.json", "w") as histo_json:
        histo_json.write(data_histo)

    # Sauvegarde une copie du fichier club
    with open("clubs.json", "r") as club_json:
        data_club = club_json.read()
    with open("data_club_backup.json", "w") as club_json:
        club_json.write(data_club)

    # Sauvegarde une copie du fichier competition
    with open("competitions.json", "r") as comp_json:
        data_comp = comp_json.read()
    with open("data_comp_backup.json", "w") as comp_json:
        comp_json.write(data_comp)

    # Code à exécuter avant chaque test
    yield

    # Restaure le fichier JSON original à partir de data_histo_backup
    with open("data_histo_backup.json", "r") as histo_json:
        data_histo = histo_json.read()
    with open("historique_reservation.json", "w") as histo_json:
        histo_json.write(data_histo)

    # Restaure le fichier JSON original à partir de data_club_backup
    with open("data_club_backup.json", "r") as club_json:
        data_club = club_json.read()
    with open("clubs.json", "w") as club_json:
        club_json.write(data_club)

    # Restaure le fichier JSON original à partir de data_comp_backup
    with open("data_comp_backup.json", "r") as comp_json:
        data_comp = comp_json.read()
    with open("competitions.json", "w") as comp_json:
        comp_json.write(data_comp)

    # Supprime le fichier de sauvegarde
    os.remove("data_histo_backup.json")
    os.remove("data_club_backup.json")
    os.remove("data_comp_backup.json")


@pytest.fixture
def club_fixture():
    club = [{
        "name": "club_test",
        "email": "email@test.com",
        "points": "10"
    }]
    return club


@pytest.fixture
def competition_fixture():
    competition = [{
        "name": "competition_valid_test",
        "date": "2025-01-01 12:00:00",
        "numberOfPlaces": "100"
        },
        {
        "name": "competition_invalid_test",
        "date": "1901-01-01 12:00:00",
        "numberOfPlaces": "200"
        },
        {
        "name": "competition_valid_test2",
        "date": "2025-01-01 12:00:00",
        "numberOfPlaces": "100"
    }]
    return competition


@pytest.fixture
def historique_fixture():
    historique = [{
        "competition": "competition_valid_test",
        "club": "club_test",
        "date": "2022-01-01 12:00:00",
        "numberOfReservation": "5"
        },
        {
        "competition": "competition_valid_test2",
        "club": "club_test",
        "date": "2022-01-01 12:00:00",
        "numberOfReservation": "10"
        },
        {
        "competition": "competition_valid_test2",
        "club": "club_test",
        "date": "2022-01-01 12:00:00",
        "numberOfReservation": "15"
    }]
    return historique

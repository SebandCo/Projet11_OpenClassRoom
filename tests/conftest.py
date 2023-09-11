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
        data = histo_json.read()
    with open("data_backup.json", "w") as histo_json:
        histo_json.write(data)

    # Code à exécuter avant chaque test
    yield

    # Restaure le fichier JSON original à partir de data_backup
    with open("data_backup.json", "r") as histo_json:
        data = histo_json.read()
    with open("historique_reservation.json", "w") as histo_json:
        histo_json.write(data)

    # Supprime le fichier de sauvegarde
    os.remove("data_backup.json")


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
        }
        ]
    return historique

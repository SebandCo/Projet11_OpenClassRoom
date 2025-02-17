import json
from flask import Flask, render_template, request, redirect, flash, url_for
from remise_zero_bdd import remise_zero_bdd
from datetime import datetime

ATHLETES_MAX_COMPETITION = 12
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

app = Flask(__name__)
app.secret_key = "something_special"


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def loadHistoryReservation():
    with open("historique_reservation.json")as histo:
        listOfHistoryReservation = json.load(histo)["reservation"]
        return listOfHistoryReservation


def controleDate(competitions):
    for competition in competitions:
        format_date_valid = datetime.strptime(competition["date"], FORMAT_DATE)
        if format_date_valid > datetime.now():
            competition["valid"] = True
        else:
            competition["valid"] = False
    return


def historiqueReservation():
    competitions = loadCompetitions()
    clubs = loadClubs()
    history_reservation = loadHistoryReservation()

    data_global = {}
    for competition in competitions:
        data_global[competition["name"]] = {}
        for club in clubs:
            data_global[competition["name"]][club["name"]] = 0

    for historique in history_reservation:
        history_competition = historique["competition"]
        history_club = historique["club"]
        history_number = int(historique["numberOfReservation"])

        data_global[history_competition][history_club] += history_number

    return data_global


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    competitions = loadCompetitions()
    clubs = loadClubs()
    if len(request.form["email"]) == 0:
        message = "No Email : Merci de rentrer une adresse email avant de valider"
    else:
        # Charger la liste des clubs : permet de passer les tests
        clubs = loadClubs()
        for club in clubs:
            if club["email"] == request.form["email"]:
                club_connected = club
                controleDate(competitions)
                return render_template("welcome.html", club=club_connected, competitions=competitions)
            else:
                message = "Unknown Email : L'adresse email n'est pas connu de la base de données"

    return render_template("index.html", message=message)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    competitions = loadCompetitions()
    clubs = loadClubs()

    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        controleDate(competitions)
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    # Charger la liste des compétitions et clubs : permet de passer les tests
    competitions = loadCompetitions()
    clubs = loadClubs()
    dataReservation = historiqueReservation()

    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]

    format_date_valid = datetime.strptime(competition["date"], FORMAT_DATE)
    Reponse_valide = True

    if format_date_valid < datetime.now():
        competition["valid"] = False
        message = "Festival Over : Le festival est terminé, donc impossible de réserver"
        Reponse_valide = False

    else:
        competition["valid"] = True
        try:
            placesRequired = int(request.form["places"])
            placeTotalRequired = placesRequired + dataReservation[competition["name"]][club["name"]]

            # Controle de la réponse utilisateur
            # Si le nombre de place est supérieur au nombre de point du club
            if placesRequired == 0:
                message = "Zero Place : Vous n'avez acheté aucune place"
                Reponse_valide = False
            elif placesRequired < 0:
                message = "Negative Place : Merci de rentrer un nombre positif"
                Reponse_valide = False

            if placesRequired > int(club["points"]):
                message = "Overtaking Club Place : Trop de place acheté par rapport au nombre du club"
                Reponse_valide = False
            # Si le nombre de place est supérieur au nombre de place du festival
            elif placesRequired > int(competition["numberOfPlaces"]):
                message = "Overtaking Festival Place : Trop de place acheté par rapport au nombre du festival"
                Reponse_valide = False
            # Si le nombre de place est supérieur à la limite du max autorisé
            elif placeTotalRequired > ATHLETES_MAX_COMPETITION:
                message = "Too Many Athletes : Trop d'athletes inscrit"
                Reponse_valide = False
        except ValueError:
            # Si le nombre de place est vide
            message = "No Tickets Purchased : Aucune place achetée"
            Reponse_valide = False

    if Reponse_valide:
        # Modification du fichier competition json
        with open("competitions.json", "w") as competition_json:
            competition["numberOfPlaces"] = str(int(competition["numberOfPlaces"])-placesRequired)
            json.dump({"competitions": competitions}, competition_json, sort_keys=False, indent=4)
        # Modification du fichier club json
        with open("clubs.json", "w") as club_json:
            club["points"] = str(int(club["points"])-placesRequired)
            json.dump({"clubs": clubs}, club_json, sort_keys=False, indent=4)
        # Modification du fichier historique json
        with open("historique_reservation.json", "r") as historique_json:
            data = json.load(historique_json)
            new_data = {"competition": competition["name"],
                        "club": club["name"],
                        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "numberOfReservation": request.form["places"]}
            data['reservation'].append(new_data)
        with open("historique_reservation.json", "w") as historique_json:
            json.dump(data, historique_json, sort_keys=False, indent=4)

        flash(f"Great-booking complete! : You have reserved {placesRequired} places")
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        # Si il y a une erreur, on reste sur la page booking.html
        return render_template("booking.html", club=club, competition=competition, message=message)


@app.route("/affichageReservation", methods=["GET"])
def affichageReservation():
    data_global = historiqueReservation()
    return render_template("reservation.html", historique=data_global)


# TODO: Add route for points display
@app.route("/logout")
def logout():
    return redirect(url_for("index"))


# Rajout pour le lancement du programme
if __name__ == "__main__":
    # Réinitialise la base de données json au lancement du programme
    # Environnement de developpement seulement
    remise_zero_bdd()
    app.run(debug=True)

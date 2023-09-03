import json
from flask import Flask,render_template,request,redirect,flash,url_for
from remise_zero_bdd import remise_zero_bdd

ATHLETES_MAX_COMPETITION = 12

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


competitions = loadCompetitions()
clubs = loadClubs()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/showSummary",methods=["POST"])
def showSummary():
    if len(request.form["email"]) == 0:
        message = "No Email : Merci de rentrer une adresse email avant de valider"
    else:
        # Charger la liste des clubs : permet de passer les tests
        clubs = loadClubs()
        for club in clubs:
            if club["email"] == request.form["email"]:
                club_connected=club
                return render_template("welcome.html",club=club_connected,competitions=competitions)
            else:
                message = "Unknown Email : L'adresse email n'est pas connu de la base de données"

    return render_template("index.html", message=message)


@app.route("/book/<competition>/<club>")
def book(competition,club):
    competitions = loadCompetitions()
    clubs = loadClubs()
    
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html",club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces",methods=["POST"])
def purchasePlaces():
    # Charger la liste des compétitions et clubs : permet de passer les tests
    competitions = loadCompetitions()
    clubs = loadClubs()

    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    
    try:
        placesRequired = int(request.form["places"])
        Reponse_valide = True

        # Controle de la réponse utilisateur
        # Si le nombre de place est supérieur au nombre de point du club
        if placesRequired > int(club["points"]):
            message = "Overtaking Club Place : Trop de place acheté par rapport au nombre du club"
            Reponse_valide = False
        # Si le nombre de place est supérieur au nombre de place du festival
        elif placesRequired > int(competition["numberOfPlaces"]):
            message = "Overtaking Festival Place : Trop de place acheté par rapport au nombre du festival"
            Reponse_valide = False
        # Si le nombre de place est supérieur à la limite du max autorisé
        elif placesRequired > ATHLETES_MAX_COMPETITION:
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
                json.dump({"competitions":competitions}, competition_json, sort_keys=False, indent=4 )
            # Modification du fichier club json
            with open("clubs.json", "w") as club_json:
                club["points"] = str(int(club["points"])-placesRequired)
                json.dump({"clubs": clubs}, club_json, sort_keys=False, indent=4)
            
            flash("Great-booking complete!")
            return render_template("welcome.html", club=club, competitions=competitions)
    else:
        # Si il y a une erreur, on reste sur la page booking.html
        return render_template("booking.html",club=club,competition=competition,message=message)


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
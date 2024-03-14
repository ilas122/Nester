from flask import Flask
from flask import render_template, request, redirect, url_for, make_response
import json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


@app.route('/login', methods=['GET', 'POST'])  # Définit la route pour la page de connexion.
def login():
    # Traitement des requêtes POST pour la connexion utilisateur.
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Vérifie si les identifiants fournis correspondent à un utilisateur autorisé.
        if username == USERNAME and password == PASSWORD:
            # Création d'une réponse qui redirige l'utilisateur vers la page des scans après une connexion réussie.
            response = make_response(redirect(url_for('hello')))
            # Stocke le nom d'utilisateur dans un cookie pour maintenir la session.
            response.set_cookie('username', username)
            return response
        else:
            # Retourne un message d'erreur en cas d'échec de la connexion.
            return "Échec de la connexion. Veuillez réessayer."
    # Affiche la page de connexion pour les requêtes GET.
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])  # Définit la route pour la déconnexion.
def logout():
    if request.method == 'POST':
        # Supprime le cookie de l'utilisateur pour terminer la session.
        response = make_response(redirect(url_for('login')))
        response.set_cookie('username', '', expires=0)
        return response
    else:
        
        return  redirect(url_for('login'))

def is_logged_in():
    # Vérifie si l'utilisateur actuel est connecté en recherchant son cookie.
    username = request.cookies.get('username')
    return username in [USERNAME]


@app.route("/result")
def hello():
    with open("test.json","r") as f:
        data = json.load(f)
        devices_list = data["devices_list"]
    return render_template ("template.html", devices_list = devices_list)



@app.route('/infos', methods=['POST'])
def get_info():
    print(request.json)
    data = request.json
    with open("test.json","w") as f:
        json.dump(data, f)

    return "success"

if __name__ == "__main__":
    app.run(debug=True)

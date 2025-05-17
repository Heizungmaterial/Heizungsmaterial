from flask import Flask, render_template, request, redirect
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

produkty = [
    {
        "id": 1,
        "nazwa": "Sunny Tripower 10 Smart Energy",
        "cena": 4146.54,
        "status": "OPŁACALNY",
        "opis": "Idealna propozycja PV. Gwarancja 15 lat.",
        "zdjecie": ""
    },
    {
        "id": 2,
        "nazwa": "STP 25-50 Garantie",
        "cena": 6877.52,
        "status": "OPŁACALNY",
        "opis": "Rozszerzona gwarancja na 15 lat.",
        "zdjecie": ""
    }
]

@app.route("/")
def index():
    return render_template("index.html", produkty=produkty)

@app.route("/produkt/<int:id>")
def produkt(id):
    p = next((x for x in produkty if x["id"] == id), None)
    return render_template("produkt.html", produkt=p)

@app.route("/kontakt/<int:id>", methods=["POST"])
def kontakt(id):
    p = next((x for x in produkty if x["id"] == id), None)
    if not p:
        return "Produkt nie istnieje", 404

    imie = request.form["imie"]
    email = request.form["email"]
    wiadomosc = request.form["wiadomosc"]

    msg = Message(
        subject=f"Zapytanie: {p['nazwa']}",
        sender=app.config['MAIL_USERNAME'],
        recipients=[os.getenv("MAIL_RECEIVER")]
    )

    msg.body = f"""Imię: {imie}
Email: {email}

{wiadomosc}

Produkt: {p['nazwa']} ({p['cena']} CHF)
"""

    mail.send(msg)
    return render_template("potwierdzenie.html", imie=imie, produkt=p)

if __name__ == "__main__":
    app.run(debug=True)

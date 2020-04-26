from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cocacola1!@localhost/hipnozacrud'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rctnperdwdihlk:00826ac59b7d9348b4b450eb1503ff95e778bf756facac7bb1c0635d627e6d7c@ec2-3-234-109-123.compute-1.amazonaws.com:5432/davg6a3vvn4dkb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQL alchemy object
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naslov = db.Column(db.String(100))
    slika = db.Column(db.String(500))
    tekst = db.Column(db.Text())
    korisnik = db.Column(db.String(100))

    def __init__(self, naslov, slika, tekst, korisnik):
        self.naslov = naslov
        self.slika = slika
        self.tekst = tekst
        self.korisnik = korisnik


@app.route('/')
def Index():
    return render_template("index.html")


@app.route('/admin')
def Admin():
    all_data = Data.query.order_by(Data.id).all()
    return render_template("admin.html", vijesti = all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        naslov = request.form['naslov']
        slika = request.form['slika']
        tekst = request.form['tekst']
        korisnik = 'Arijana Tema'

        my_data = Data(naslov, slika, tekst, korisnik)
        db.session.add(my_data)
        db.session.commit()

        flash("Vijest je uspjesno dodana!")

        return redirect(url_for('Admin'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        
        my_data.id = request.form['id']
        my_data.naslov = request.form['naslov']
        my_data.slika = request.form['slika']
        my_data.tekst = request.form['tekst']
        my_data.korisnik = 'Arijana Tema'

        db.session.commit()
        flash("Izmjene uspjesno izvrsene !")
        return redirect(url_for('Admin'))

@app.route('/delete/<id>/', methods=['POST', 'GET'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Vijest uspjesno izbrisana !")
    return redirect(url_for('Admin'))

@app.route('/kolumne')
def Kolumne():
    all_data = Data.query.order_by(Data.id).all()
    return render_template("kolumne.html", vijesti = all_data)

@app.route('/kolumna/<id>', methods=['GET'])
def Kolumna(id):
    my_data = Data.query.get(id)
    if(my_data):
        return render_template("kolumna.html", kolumna = my_data)
    else:
        pass



if __name__ == "__main__":
    app.run(debug=True)

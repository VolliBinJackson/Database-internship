from flask import Flask, render_template;
from flask import request
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            vorname = request.form['vorname']
            nachname = request.form['nachname']
            password = request.form['password']
            adresse = request.form['adresse']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customers (Vorname, Nachname, Password, CustomerAddress) VALUES (?,?,?,?)",(vorname, nachname, password, adresse))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('login.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

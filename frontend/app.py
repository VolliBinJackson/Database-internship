from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
from appHelperFunctions import isUserRegistered

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if isUserRegistered(username, password):
            return redirect(url_for('main'))
    
    return render_template('login.html')


@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    if request.method == 'POST':
        return redirect(url_for('login'))
    

@app.route('/main')
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
            with sql.connect('database.db') as con:
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

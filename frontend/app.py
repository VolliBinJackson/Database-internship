from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import pyscript
from io import BytesIO

from appHelperFunctions import isUserRegistered, isRestaurantRegistered

app = Flask(__name__)


# MAIN ROUTE: LOGIN LOGIC (User)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if isUserRegistered(username, password):
            return redirect(url_for('main'))
    
    return render_template('login.html')


# MAIN ROUTE: LOGIN LOGIC (RESTAURANT)
@app.route('/Rlogin', methods=['GET', 'POST'])
def Rlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if isRestaurantRegistered(username, password):
            return render_template('Rmain.html')
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


@app.route('/restaurant')
def restaurant():
    with sql.connect('database.db') as con:
        cur = con.cursor()
        data = cur.execute("select * from restaurants")
        
    return render_template('restaurant.html', all_data=data )


@app.route('/restaurant_register.html')
def restaurant_register():
    return render_template('restaurant_register.html')


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
        


@app.route("/Raddrec", methods = ['POST', 'GET'])
def Raddrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            name = request.form['vorname']
            password = request.form['password']
            adresse = request.form['adresse']
            beschreibung = request.form['description']

            # Connect to SQLite3 database and execute the INSERT
            with sql.connect('database.db') as cons:
                cur = cons.cursor()
                cur.execute("INSERT INTO restaurants (Name, Password, RestaurantAddress, RestaurantDescription) VALUES (?,?,?,?)",(name, password, adresse, beschreibung))

                cons.commit()
                msg = "Record successfully added to database"
        except:
            cons.rollback()
            msg = "Error in the INSERT"

        finally:
            cons.close()
            # Send the transaction message to result.html
            return render_template('login.html', message = msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

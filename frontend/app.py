from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql
from PIL import Image, ImageTk
from io import BytesIO
from appHelperFunctions import *

app = Flask(__name__)
app.secret_key = 'Ihr_geheimer_Schlüssel_hier'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if isUserRegistered(username, password):
            session['username'] = username
            return redirect(url_for('restaurant'))
    
    return render_template('login.html')

@app.route('/Rlogin', methods=['GET', 'POST'])
def Rlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        restaurant_id = isRestaurantRegistered(username, password)
        if restaurant_id:
            session['restaurant_id'] = restaurant_id
            return render_template('Rmain.html')
    
    return render_template('login.html')



@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/restaurant')
def restaurant():
    with sql.connect('database.db') as con:
        cur = con.cursor()
        data = cur.execute("select * from restaurants")
        
    return render_template('restaurant.html', all_data=data )

@app.route('/restaurant_register.html')
def restaurant_register():
    return render_template('restaurant_register.html')


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
            strasse = request.form['adresse']
            PLZ = request.form['plz']

            # Connect to SQLite3 database and execute the INSERT
            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customers (Vorname, Nachname, Password, CustomerStrasse_HausNr, CustomerPLZ) VALUES (?,?,?,?,?)",(vorname, nachname, password, strasse, PLZ ))

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
        

@app.route("/add_item", methods=['POST'])
def add_item():
    if 'restaurant_id' in session:
        try:
            item_name = request.form['item_name']
            price = request.form['price']
            description = request.form['description']
            restaurant_id = session['restaurant_id']

            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (ItemName, Price, ItemDescription, RestaurantID) VALUES (?, ?, ?, ?)", 
                            (item_name, price, description, restaurant_id))

                con.commit()
                msg = "Gericht erfolgreich hinzugefügt."
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            con.close()
            return render_template('Rmain.html', message=msg)
    else:
        return redirect(url_for('Rlogin'))
    

@app.route('/remove_item', methods=['POST'])
def remove_item():
    if 'restaurant_id' in session:
        con = None

        try:
            item_to_remove = request.form['item_to_remove']
            restaurant_id = session['restaurant_id']

            if is_item_in_restaurant(item_to_remove, restaurant_id):
                con = sql.connect('database.db')
                cur = con.cursor()
                cur.execute("DELETE FROM items WHERE ItemName=? AND RestaurantID=?", (item_to_remove, restaurant_id))
                con.commit()
                msg = "Gericht erfolgreich entfernt."
            else:
                msg = "Dieses Gericht gibt es nicht!"
        except Exception as e:
            con.rollback()
            msg=f"Error in delete operation: {e}"
        finally:
            if con:
                con.close()
            # Hier holst du die aktualisierte Liste der Artikel für das bestimmte Restaurant
            items = get_items_for_restaurant(restaurant_id)
            return render_template('Rmain.html', items=items, message=msg)
    else:
        return redirect(url_for('Rlogin'))
    

@app.route('/edit_item', methods=['POST'])
def edit_item():
    if 'restaurant_id' in session:
        con = None

        try:
            item_to_edit = request.form.get('item_to_edit')
            new_price = float(request.form.get('new_price'))
            new_description = request.form.get('new_description')
            restaurant_id = session['restaurant_id']

            if is_item_in_restaurant(item_to_edit, restaurant_id):
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute("UPDATE items SET Price=?, ItemDescription=? WHERE ItemName=?", (new_price, new_description, item_to_edit))
                con.commit()
                msg = "Gericht wurde bearbeitet."
            else:
                msg = "Fehler beim Bearbeiten!"
        except Exception as e:
            con.rollback()
            msg = f"Error in edit operation: {e}"
        finally:
            if con:
                con.close()
            items = get_items_for_restaurant(restaurant_id)
            return render_template('Rmain.html', items=items, message=msg)
    else:
        return redirect(url_for('Rlogin'))
    


@app.route('/restaurant_info', methods=['POST'])
def save_restaurant_info():
    if request.method == 'POST':
        opening_hours = request.form['opening_hours']
        delivery_radius = request.form['delivery_radius']
        restaurant_info = {'opening_hours': opening_hours, 'delivery_radius': delivery_radius}
        return render_template('Rmain.html', restaurant_infos=[restaurant_info])


    
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_items(restaurant_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        items = cur.execute("SELECT * FROM items WHERE RestaurantID = ?", (restaurant_id,)).fetchall()
        return render_template('restaurant_items.html', items=items)

        

@app.route('/cart')
def cart():
    return render_template('cart.html')







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

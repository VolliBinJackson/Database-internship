import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql
from PIL import Image, ImageTk
from io import BytesIO
from appHelperFunctions import *
import sys

app = Flask(__name__)
app.secret_key = 'Ihr_geheimer_Schlüssel_hier'


@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialisieren einer Variablen für Fehlermeldungen

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        registered, user_plz, user_id = isUserRegistered(username, password)
        if registered:
            session['username'] = username
            session['user_plz'] = user_plz
            session['user_id'] = user_id
            return redirect(url_for('restaurant'))
        else:
            error_message = "Benutzername oder Passwort falsch."  # Setzen der Fehlermeldung

    return render_template('login.html', error=error_message)


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
    user_plz = str(session.get('user_plz'))  # str da sonst fehler auftritt bei der like Operatio, da es anscheinend als int angesehen wird
    # Abfrage der Datenbank nach Restaurants, die an die Benutzer-PLZ liefern
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM restaurants WHERE Lieferradius LIKE ?", ('%' + user_plz + '%',))
        restaurants = cur.fetchall()

    return render_template('restaurant.html', restaurants=restaurants)

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
                cur.execute("INSERT INTO users (Vorname, Nachname, Password, CustomerStrasse_HausNr, CustomerPLZ) VALUES (?,?,?,?,?)",(vorname, nachname, password, strasse, PLZ ))

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
    if request.method == 'POST':
        try:
            name = request.form['vorname']
            password = request.form['password']
            adresse = request.form['adresse']
            beschreibung = request.form['description']
            plz = request.form['plz']  

            # Datenbankverbindung herstellen und Daten einfügen
            with sql.connect('database.db') as cons:
                cur = cons.cursor()
                cur.execute("INSERT INTO restaurants (Name, Password, RestaurantAddress, RestaurantDescription, Lieferradius) VALUES (?, ?, ?, ?, ?)", 
                            (name, password, adresse, beschreibung, plz))

                cons.commit()
                msg = "Restaurant erfolgreich zur Datenbank hinzugefügt."
        except:
            cons.rollback()
            msg = "Fehler beim Einfügen des Datensatzes in die Datenbank."

        finally:
            cons.close()
            return render_template('login.html', message=msg)  

    

        

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
    
    
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_items(restaurant_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        items = cur.execute("SELECT * FROM items WHERE RestaurantID = ?", (restaurant_id,)).fetchall()
        return render_template('restaurant_items.html', items=items, restaurant_id = restaurant_id)

        

@app.route('/add_to_cart/<int:item_id>/<int:restaurant_id>', methods=['POST'])
def add_to_cart(item_id, restaurant_id):
   
    user_id = session.get('user_id')
    quantity = request.form.get('quantity', 1)

    if add_item_to_cart(user_id, item_id, quantity, restaurant_id):
        return redirect(url_for('restaurant_items', restaurant_id=restaurant_id))
    
    else:
        flash('Sie können nicht gleichzeitig bei verschiedenen Restaurants bestellen. Leeren Sie Ihren Warenkorb oder fügen Sie Artikel aus demselben Restaurant hinzu.', 'warning')
        return redirect(url_for('restaurant_items', restaurant_id=restaurant_id))

def add_item_to_cart(user_id, item_id, quantity, restaurant_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT restaurantID FROM cart WHERE userID = ?", (user_id,))
        existing_restaurant_id = cur.fetchone()
        if existing_restaurant_id and existing_restaurant_id[0] != restaurant_id:
            return False

        cur.execute("SELECT quantity FROM cart WHERE userID = ? AND itemID = ? AND restaurantID = ?", (user_id, item_id, restaurant_id))
        result = cur.fetchone()
        if result:
            new_quantity = result[0] + int(quantity)
            cur.execute("UPDATE cart SET quantity = ? WHERE userID = ? AND itemID = ? AND restaurantID = ?", (new_quantity, user_id, item_id, restaurant_id))
        else:
            cur.execute("INSERT INTO cart (userID, itemID, restaurantID, quantity) VALUES (?, ?, ?, ?)", (user_id, item_id, restaurant_id, quantity))
        con.commit()
    return True

@app.route('/remove_from_cart', methods=['GET'])
def remove_from_cart():
    item_id = request.args.get('item_id')
    user_id = session.get('user_id')
   
    with sql.connect('database.db') as con:
        cur = con.cursor()
        try:
            print(user_id)
            print(item_id)
            cur.execute("DELETE FROM cart WHERE userID = ? AND itemID = ?", (user_id, item_id))
            con.commit()
        except Exception as e:
            print(f"Fehler: {e}")
            # Optional: Weitere Fehlerbehandlung hier

    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    # Hier müssen Sie die Benutzer-ID des aktuellen Benutzers abrufen
    user_id = session.get('user_id') 
    items_details = get_cart_items_for_user(user_id)

    total_price = sum(item['total_price'] for item in items_details)
    return render_template('cart.html', cart_items=items_details, total_price=total_price)

@app.route('/place_order', methods=['POST'])
def place_order():
    user_id = session.get('user_id')
    delivery_address = get_delivery_address_for_user(user_id)
    order_note = request.form.get('orderNote')
    print(order_note)
    cart_items = get_cart_items_for_user(user_id)

    if not cart_items:
        flash('Ihr Warenkorb ist leer. Bitte fügen Sie Artikel hinzu, bevor Sie die Bestellung aufgeben.', 'danger')
        return redirect(url_for('cart'))

    # Extrahieren der RestaurantID vom ersten Artikel im Warenkorb
    restaurant_id = cart_items[0]['restaurant_id'] if cart_items else None

    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sql.connect('database.db') as con:
        cur = con.cursor()

        # Speichern der Bestellung einschließlich der RestaurantID
        cur.execute("INSERT INTO orders (UserID, RestaurantID, DeliveryAddress, OrderNote, OrderDate) VALUES (?, ?, ?, ?, ?)",
                    (user_id, restaurant_id, delivery_address, order_note, order_date))
        order_id = cur.lastrowid

        # Fügen Sie Artikel aus dem Warenkorb zur Bestellung hinzu
        for item in cart_items:
            item_id = item['item_id']
            quantity = item['quantity']
            cur.execute("INSERT INTO order_items (OrderID, ItemID, Quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))

        # Löschen des Warenkorbs nach dem Aufgeben der Bestellung
        cur.execute("DELETE FROM cart WHERE userID = ?", (user_id,))
        session.pop('cart', None)

        con.commit()

    flash('Ihre Bestellung wurde erfolgreich aufgegeben! Vielen Dank für Ihren Einkauf.', 'success')
    return redirect(url_for('order_history'))


@app.route('/order_history')
def order_history():
    user_id = session.get('user_id')
    if not user_id:
        flash('Bitte melden Sie sich an, um auf die Bestellhistorie zuzugreifen.', 'warning')
        return redirect(url_for('login'))

    orders = []
    with sql.connect('database.db') as con:
        cur = con.cursor()
        # Abrufen aller Bestellungen des Benutzers, sortiert nach Status und Datum/Uhrzeit
        cur.execute("""
            SELECT OrderID, DeliveryAddress, DeliveryState, OrderDate, OrderNote 
            FROM orders 
            WHERE UserID = ? 
            ORDER BY 
                CASE 
                    WHEN DeliveryState IN ('In Bearbeitung', 'Unterwegs') THEN 1 
                    ELSE 2 
                END, 
                OrderDate DESC
            """, (user_id,))
        orders_data = cur.fetchall()

        for order in orders_data:
            order_id, address, state, date, order_note = order
            # Abrufen der Artikel für jede Bestellung
            cur.execute("SELECT i.ItemName, i.Price, oi.Quantity FROM order_items oi JOIN items i ON oi.ItemID = i.ItemID WHERE oi.OrderID = ?", (order_id,))
            items = cur.fetchall()

            total_price = sum(item[1] * item[2] for item in items)  # Berechnung des Gesamtpreises

            order_details = {
                'order_id': order_id,
                'address': address,
                'state': state,
                'date': date,
                'order_note': order_note,
                'items': [{'name': item[0], 'price': item[1], 'quantity': item[2]} for item in items],
                'total_price': total_price
            }
            orders.append(order_details)

    return render_template('order_history.html', orders=orders)

@app.route('/view_restaurant_orders')
def view_restaurant_orders():
    restaurant_id = session.get('restaurant_id')
    if not restaurant_id:
        flash('Bitte melden Sie sich an, um Bestellungen zu sehen.', 'warning')
        return redirect(url_for('login'))

    orders = []
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT OrderID, DeliveryAddress, DeliveryState, OrderNote, OrderDate FROM orders WHERE RestaurantID = ?", (restaurant_id,))
        orders_data = cur.fetchall()

        for order in orders_data:
            order_id, address, state, OrderNote, OrderDate = order
            # Abrufen der Artikel für jede Bestellung
            cur.execute("SELECT i.ItemName, i.Price, oi.Quantity FROM order_items oi JOIN items i ON oi.ItemID = i.ItemID WHERE oi.OrderID = ?", (order_id,))
            items = cur.fetchall()

            # Berechnung des Gesamtpreises
            total_price = sum(item[1] * item[2] for item in items)

            # Hinzufügen der Bestellung und ihrer Details
            orders.append({
                'order_id': order_id,
                'status': state,
                'date': OrderDate,
                'address': address,
                'items': items,
                'total_price': total_price,
                'order_note': OrderNote  # Angenommen, die Order-Note ist an der 7. Position
            })


    return render_template('Rorder_history.html', orders=orders)


# Beispielroute für die Bestätigung der Bestellung durch das Restaurant
@app.route('/accept_order/<int:order_id>')
def accept_order(order_id):
    # Hier können Sie die Logik für die Bestätigung implementieren
    # Z.B. Aktualisieren Sie den Status in der Datenbank auf 'In Zubereitung'
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE orders SET DeliveryState = 'In Zubereitung' WHERE OrderID = ?", (order_id,))
        con.commit()

    flash('Bestellung wurde bestätigt und befindet sich jetzt in Zubereitung.', 'success')
    return redirect(url_for('view_restaurant_orders'))


# Beispielroute für das Stornieren einer Bestellung durch das Restaurant
@app.route('/cancel_order/<int:order_id>')
def cancel_order(order_id):
    # Hier können Sie die Logik für die Stornierung implementieren
    # Z.B. Aktualisieren Sie den Status in der Datenbank auf 'Storniert'
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE orders SET DeliveryState = 'Storniert' WHERE OrderID = ?", (order_id,))
        con.commit()

    flash('Bestellung wurde storniert.', 'danger')
    return redirect(url_for('view_restaurant_orders'))

# Beispielroute für das Abschließen einer Bestellung durch das Restaurant
@app.route('/complete_order/<int:order_id>')
def complete_order(order_id):
    # Hier können Sie die Logik für den Abschluss implementieren
    # Z.B. Aktualisieren Sie den Status in der Datenbank auf 'Abgeschlossen'
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE orders SET DeliveryState = 'Abgeschlossen' WHERE OrderID = ?", (order_id,))
        con.commit()

    flash('Bestellung wurde abgeschlossen und versandt.', 'success')
    return redirect(url_for('view_restaurant_orders'))


if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=5000)

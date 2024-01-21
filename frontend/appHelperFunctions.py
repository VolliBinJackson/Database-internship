import sqlite3 as sql
from flask import session

# Check if User is already registered
def isUserRegistered(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE Vorname=? AND Password=?", (username,password))
    user = cur.fetchone()
    con.close()
    
    if user:
        user_plz = user[4]
        user_id = user[5]
        return True, user_plz, user_id
    else:
        return False, None, None
    

# Same scenario, but for restaurants    
def isRestaurantRegistered(name, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM restaurants WHERE name=? AND Password=?", (name,password))
    restaurant = cur.fetchone()
    con.close()
    
    if restaurant:
        restaurant_ID = restaurant[6]
        return restaurant_ID
    else:
        return None
    

# Retrieve items from specific restaurant
def get_items_for_restaurant(restaurant_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM items WHERE RestaurantID=?", (restaurant_id,))
        items = cur.fetchall()
    return items


# Check if this specific restaurant has this item
def is_item_in_restaurant(item_name, restaurant_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM items WHERE ItemName=? AND RestaurantID=?", (item_name, restaurant_id))
        count = cur.fetchone()[0]
    return count > 0

def load_user_cart(user_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT itemID, quantity FROM cart WHERE userID = ?", (user_id,))
        cart_items = cur.fetchall()
    return cart_items

def get_delivery_address_for_user(user_id):
    with sql.connect('database.db') as con:
        cur = con.cursor()
        # Angenommen, die Spalten für die Adresse heißen 'CustomerStrasse_HausNr' und 'CustomerPLZ'
        cur.execute("SELECT CustomerStrasse_HausNr, CustomerPLZ FROM users WHERE UserID = ?", (user_id,))
        result = cur.fetchone()
        if result:
            street_house_nr, plz = result
            return f"{street_house_nr}, {plz}"  # Gibt die Lieferadresse zurück
        else:
            return None  # Keine Adresse gefunden oder Benutzer existiert nicht
        
def get_cart_items_for_user(user_id):
    items_details = []
    with sql.connect('database.db') as con:
        cur = con.cursor()
        # Ergänzung der RestaurantID in der SELECT-Abfrage
        cur.execute("SELECT i.ItemID, i.ItemName, i.Price, i.ItemDescription, c.quantity, i.RestaurantID FROM items i INNER JOIN cart c ON i.ItemID = c.itemID WHERE c.userID = ?", (user_id,))
        rows = cur.fetchall()

        for row in rows:
            item_id, name, price, description, quantity, restaurant_id = row  
            items_details.append({
                'name': name,
                'price': price,
                'description': description,
                'quantity': quantity,
                'total_price': price * quantity,
                'item_id': item_id,
                'restaurant_id': restaurant_id  
            })
    return items_details




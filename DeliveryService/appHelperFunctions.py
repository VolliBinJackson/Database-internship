import sqlite3 as sql


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
        restaurant_ID = restaurant[8]
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
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT items.ItemName, items.Price, cart.quantity, cart.itemID, cart.restaurantID, (items.Price * cart.quantity) as total_price FROM cart JOIN items ON cart.itemID = items.itemID WHERE cart.userID = ?", (user_id,))
    items_details = [{'name': row[0], 'price': row[1], 'quantity': row[2], 'item_id': row[3], 'restaurant_id': row[4], 'total_price': row[5]} for row in cur.fetchall()]
    con.close()
    return items_details





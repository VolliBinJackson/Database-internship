import sqlite3 as sql


# Check if User is already registered
def isUserRegistered(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE Vorname=? AND Password=?", (username,password))
    user = cur.fetchone()
    con.close()
    
    if user:
        return True
    else:
        return False
    

# Same scenario, but for restaurants    
def isRestaurantRegistered(name, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM restaurants WHERE name=? AND Password=?", (name,password))
    restaurant = cur.fetchone()
    con.close()
    
    if restaurant:
        restaurant_ID = restaurant[5]
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


# simple query
def query_items():
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items
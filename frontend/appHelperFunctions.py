import sqlite3 as sql

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
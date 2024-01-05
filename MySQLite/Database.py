import sqlite3 as sql
con = sql.connect("database.db")

#Create tables
def createCustomerTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS customers")
    cur.execute("CREATE TABLE customers (firstname VARCHAR(30) NOT NULL, lastname VARCHAR(30) NOT NULL, password STRING NOT NULL, customeraddress STRING NOT NULL, customerID INTEGER PRIMARY KEY AUTOINCREMENT)")
    con.commit()
    con.close()


def createRestaurantTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS restaurants")
    cur.execute("CREATE TABLE restaurants (name VARCHAR(30) NOT NULL, restaurantaddress STRING NOT NULL, restaurantdescription STRING NOT NULL, restaurantpicture BLOB, restaurantID INTEGER PRIMARY KEY)")
    con.commit()
    con.close()


def createOrderTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("CREATE TABLE orders (deliveryaddress STRING NOT NULL, deliverystate STRING NOT NULL, orderID INTEGER PRIMARY KEY)")
    con.commit()
    con.close()



def createItemTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS items")
    cur.execute("CREATE TABLE items (itemname STRING NOT NULL, price FLOAT, picture BLOB, itemdescription STRING NOT NULL, itemID INTEGER PRIMARY KEY)")
    con.commit()
    con.close()


createCustomerTable()
createRestaurantTable()
createOrderTable()
createItemTable()

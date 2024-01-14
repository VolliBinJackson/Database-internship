import sqlite3 as sql
con = sql.connect("database.db")

#Create tables
def createCustomerTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS customers")
    cur.execute("CREATE TABLE customers (Vorname VARCHAR(30) NOT NULL, Nachname VARCHAR(30) NOT NULL, Password STRING NOT NULL, CustomerAddress STRING NOT NULL, CustomerID INTEGER PRIMARY KEY AUTOINCREMENT)")
    con.commit()
    con.close()


def createRestaurantTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS restaurants")
    cur.execute("CREATE TABLE restaurants (Name VARCHAR(30) NOT NULL, RestaurantAddress STRING NOT NULL, RestaurantDescription STRING NOT NULL, RestaurantPicture BLOB, RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT)")
    con.commit()
    con.close()


def createOrderTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("CREATE TABLE orders (DeliveryAddress STRING NOT NULL, DeliveryState STRING NOT NULL, OrderID INTEGER PRIMARY KEY AUTOINCREMENT)")
    con.commit()
    con.close()



def createItemTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS items")
    cur.execute("CREATE TABLE items (ItemName STRING NOT NULL, Price FLOAT, Picture BLOB, ItemDescription STRING NOT NULL, ItemID INTEGER PRIMARY KEY AUTOINCREMENT)")
    con.commit()
    con.close()


createCustomerTable()
createRestaurantTable()
createOrderTable()
createItemTable()

import sqlite3 as sql
con = sql.connect("database.db")


#Create tables
def createUserTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS customers")
    cur.execute("""
                CREATE TABLE users (
                    Vorname VARCHAR(30) NOT NULL, 
                    Nachname VARCHAR(30) NOT NULL, 
                    Password STRING NOT NULL, 
                    CustomerStrasse_HausNr STRING NOT NULL, 
                    CustomerPLZ INTEGER NOT NULL, 
                    UserID INTEGER PRIMARY KEY AUTOINCREMENT)""")
    con.commit()
    con.close()


def createRestaurantTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS restaurants")
    cur.execute("""
                CREATE TABLE restaurants (
                    Name VARCHAR(30) NOT NULL,
                    Password STRING NOT NULL,
                    RestaurantAddress STRING NOT NULL,
                    RestaurantDescription STRING NOT NULL, 
                    RestaurantPicture BLOB, 
                    Lieferradius TEXT, 
                    OpenTime TIME, 
                    CloseTime TIME,
                    RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT)""")
    con.commit()
    con.close()


def createOrderTable():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS orders")
        cur.execute("""
            CREATE TABLE orders (
                OrderID INTEGER PRIMARY KEY,
                UserID INT,
                RestaurantID INT,
                DeliveryAddress STRING NOT NULL,
                DeliveryState STRING DEFAULT 'in Bearbeitung',
                OrderNote TEXT,
                OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (UserID) REFERENCES users(UserID),
                FOREIGN KEY (RestaurantID) REFERENCES restaurants(RestaurantID)
            )
        """)
        con.commit()

def createOrderItemsTable():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS order_items")
        cur.execute("""
            CREATE TABLE order_items (
                OrderItemID INTEGER PRIMARY KEY,
                OrderID INT,
                ItemID INT,
                Quantity INT,
                FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
                FOREIGN KEY (ItemID) REFERENCES items(ItemID)
            )
        """)
        con.commit()



def createItemTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS items")
    cur.execute("""CREATE TABLE items (
                    ItemName STRING NOT NULL,
                    Price FLOAT, Picture BLOB, 
                    ItemDescription STRING NOT NULL, 
                    RestaurantID INTEGER, 
                    ItemID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    FOREIGN KEY (RestaurantID) REFERENCES restaurants (RestaurantID))""")
    con.commit()
    con.close()

def createCartTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cart")
    cur.execute("""CREATE TABLE cart (
                    userID INT, 
                    itemID INT, 
                    restaurantID INT, 
                    quantity INT,  
                    note TEXT, 
                    FOREIGN KEY (userID) REFERENCES users(userID),
                    FOREIGN KEY (itemID) REFERENCES items(ItemID))""")
    con.commit()
    con.close()



createUserTable()
createRestaurantTable()
createOrderTable()
createOrderItemsTable()
createItemTable()
createCartTable()


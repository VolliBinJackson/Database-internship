import sqlite3 as sql
con = sql.connect("database.db")


#Create tables
def createUserTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
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
    cur.execute("""
                INSERT INTO restaurants (Name, Password, RestaurantAddress, RestaurantDescription, Lieferradius, OpenTime, CloseTime) VALUES 
    ('Bella Italia', 'passwort1', '123 Hauptstraße', 'Authentische italienische Küche', '11111', '18:00', '22:00'),
    ('Spice Paradise', 'passwort2', '456 Eichenstraße', 'Ein Hauch von Indien', '22222, 11111', '11:00', '23:00'),
    ('Sushi Delight', 'passwort3', '789 Ulmenstraße', 'Frisches Sushi und japanische Gerichte', '33333, 11111', '12:00', '21:00'),
    ('Taco Haven', 'passwort4', '321 Kieferstraße', 'Verlockende Tacos und mexikanische Aromen', '44444, 11111', '09:00', '20:00'),
    ('Mediterranean Oasis', 'passwort5', '555 Zedernstraße', 'Mediterrane Köstlichkeiten', '55555, 11111', '14:00', '18:00'),
    ('Gourmet Grill', 'passwort6', '888 Birkenstraße', 'Gegrillte Spezialitäten und BBQ', '66666, 11111', '15:00', '19:00'),
    ('Vegetarian Haven', 'passwort7', '999 Walnussstraße', 'Gesunde und geschmackvolle vegetarische Optionen', '77777, 11111', '16:00', '20:00'),
    ('Seafood Sensation', 'passwort8', '777 Ahornstraße', 'Frische Meeresfrüchtekreationen', '88888, 11111', '17:00', '21:00'),
    ('Burger Bistro', 'passwort9', '222 Eichenstraße', 'Leckere Burger und Pommes', '99999, 11111', '13:00', '22:00'),
    ('Sweet Treats Café', 'passwort10', '111 Kieferstraße', 'Genießen Sie Desserts und Kaffee', '11112, 11111', '08:00', '23:00');""")

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
    cur.execute("""INSERT INTO items (ItemName, Price, ItemDescription, RestaurantID) VALUES 
                    ('Doener', 7.50, 'Leckerer Doener', 1),
    ('Doener Spezial', 8.50, 'Spezieller Doener mit Extras', 1),
    ('Pasta Carbonara', 12.99, 'Klassische Carbonara Pasta', 1),
    ('Gemüsepfanne', 9.95, 'Gebratenes Gemüse mit Reis', 1),
    ('Pizza Salami', 10.50, 'Pizza mit Salami und Tomaten', 1),
    ('Burger Classic', 11.75, 'Klassischer Burger mit Pommes', 1),
    ('Sushi Mix', 18.50, 'Verschiedene Sushi Sorten', 1),
    ('Taco Fiesta', 7.99, 'Taco mit bunter Füllung', 1),
    ('Curry Hähnchen', 13.25, 'Curry mit zartem Hähnchen', 1),
    ('Eisbecher Deluxe', 6.50, 'Verschiedene Eissorten mit Toppings', 1),
('Pizza Margherita', 8.50, 'Klassische Margherita Pizza', 2),
    ('Pizza Quattro Formaggi', 11.99, 'Pizza mit vier Käsesorten', 2),
    ('Sushi Deluxe', 21.95, 'Deluxe Sushi Platte', 2),
    ('Taco Supreme', 8.75, 'Taco mit allem Drum und Dran', 2),
    ('Mediterrane Gemüseplatte', 14.99, 'Gegrilltes Gemüse mit Dip', 2),
    ('BBQ Burger', 10.95, 'Saftiger Burger mit BBQ-Sauce', 2),
    ('Vegetarisches Curry', 12.50, 'Curry mit frischem Gemüse', 2),
    ('Meeresfrüchte-Pasta', 16.75, 'Pasta mit frischen Meeresfrüchten', 2),
    ('Cheeseburger Deluxe', 9.99, 'Burger mit extra viel Käse', 2),
    ('Schokoladen-Muffin', 4.50, 'Leckerer Muffin mit Schokolade', 2),
('Sushi California Roll', 14.50, 'California Roll mit Krabben', 3),
    ('Teriyaki Hähnchen', 16.99, 'Teriyaki Hähnchen mit Reis', 3),
    ('Edamame', 6.75, 'Gedämpfte Sojabohnen', 3),
    ('Miso Suppe', 5.50, 'Traditionelle Miso-Suppe', 3),
    ('Lachs Sashimi', 18.95, 'Frischer Lachs in Scheiben', 3),
    ('Veganes Sushi', 12.75, 'Sushi ohne tierische Produkte', 3),
    ('Tofu Ramen', 11.99, 'Ramen mit Tofu und Gemüse', 3),
    ('Ebi Nigiri', 9.50, 'Nigiri mit Garnelen', 3),
    ('Matcha Eis', 8.25, 'Grünes Tee Eis', 3),
    ('Seetang Salat', 7.50, 'Salat mit Seetang und Dressing', 3),
('Mexikanischer Burrito', 9.99, 'Gefüllter Burrito mit Hackfleisch', 4),
    ('Nachos Supreme', 12.50, 'Nachos mit Käse und Extras', 4),
    ('Quesadilla', 8.75, 'Gefüllte Quesadilla mit Guacamole', 4),
    ('Enchiladas', 14.95, 'Gefüllte Enchiladas mit Bohnen', 4),
    ('Guacamole', 6.50, 'Frische Guacamole mit Tortilla-Chips', 4),
    ('Churros', 5.99, 'Süße Churros mit Zimtzucker', 4),
    ('Taco Salad', 10.50, 'Salat mit Tacos und Dressing', 4),
    ('Fajitas Mixtas', 17.75, 'Gemischte Fajitas mit Fleisch und Gemüse', 4),
    ('Salsa Verde', 4.50, 'Würzige grüne Salsa', 4),
    ('Mango Margarita', 8.99, 'Erfrischender Mango-Margarita', 4),
('Griechischer Salat', 10.99, 'Klassischer griechischer Salat', 5),
    ('Souvlaki Teller', 13.50, 'Gegrillte Fleischspieße mit Beilage', 5),
    ('Hummus mit Pita', 8.25, 'Hummus-Dip mit Pita-Brot', 5),
    ('Moussaka', 15.95, 'Traditionelles griechisches Moussaka', 5),
    ('Tzatziki', 6.50, 'Joghurt-Dip mit Gurken und Knoblauch', 5),
    ('Saganaki', 11.75, 'Gebratener Käse mit Zitrone', 5),
    ('Spanakopita', 9.99, 'Blätterteig mit Spinat und Feta', 5),
    ('Gyro Wrap', 12.50, 'Wrap mit gegrilltem Fleisch und Gemüse', 5),
    ('Baklava', 7.50, 'Süßes Gebäck mit Nüssen und Honig', 5),
    ('Ouzo Cocktail', 8.25, 'Cocktail mit griechischem Anisschnaps', 5),
('BBQ Ribs', 18.99, 'Spare Ribs mit Barbecue-Sauce', 6),
    ('Steakhouse Burger', 15.50, 'Burger mit gegrilltem Steak und Käse', 6),
    ('Gegrillte Hähnchenbrust', 12.75, 'Saftige gegrillte Hähnchenbrust', 6),
    ('Brisket Sandwich', 14.95, 'Sandwich mit geräuchertem Brisket', 6),
    ('Pommes Frites', 6.50, 'Knusprige Pommes mit Gewürzen', 6),
    ('Maiskolben', 5.99, 'Gegrillter Maiskolben mit Kräuterbutter', 6),
    ('Coleslaw', 4.99, 'Fruchtiger Krautsalat', 6),
    ('Mac n Cheese', 9.50, 'Käse-Nudelauflauf', 6),
    ('Gegrillte Maiskolben', 7.25, 'Maiskolben vom Grill mit Gewürzen', 6),
    ('Brownie Sundae', 8.99, 'Brownie mit Eis und Toppings', 6),
('Falafel Wrap', 9.99, 'Wrap mit Falafelbällchen und Gemüse', 7),
    ('Vegetarische Lasagne', 12.50, 'Lasagne mit Gemüse und Bechamelsauce', 7),
    ('Quinoa Salat', 8.75, 'Salat mit Quinoa, Gemüse und Feta', 7),
    ('Hummus Plate', 10.95, 'Platte mit verschiedenen Hummus-Sorten', 7),
    ('Avocado Toast', 7.50, 'Getoastetes Brot mit Avocado und Tomaten', 7),
    ('Gemüseburger', 11.75, 'Burger mit pflanzlichem Patty und Toppings', 7),
    ('Chickpea Curry', 14.99, 'Kichererbsen-Curry mit Reis', 7),
    ('Sweet Potato Fries', 6.50, 'Süßkartoffel-Pommes mit Dip', 7),
    ('Caprese Sandwich', 9.25, 'Sandwich mit Tomate, Mozzarella und Pesto', 7),
    ('Smoothie Bowl', 8.99, 'Frühstücks-Bowl mit frischem Obst', 7),
('Garlic Butter Shrimp', 16.50, 'Garnelen in Knoblauchbutter', 8),
    ('Lobster Roll', 22.99, 'Brötchen mit Hummerfleisch', 8),
    ('Clam Chowder', 11.75, 'Cremige Muschelsuppe', 8),
    ('Fish and Chips', 14.95, 'Fisch mit Pommes und Tartar-Sauce', 8),
    ('Grilled Calamari', 13.50, 'Gegrillte Tintenfischringe', 8),
    ('Seafood Paella', 18.75, 'Paella mit Meeresfrüchten', 8),
    ('Crab Legs', 20.99, 'Krabbenbeine mit Knoblauchbutter', 8),
    ('Oyster Shooters', 9.50, 'Austern mit Wodka und Sauce', 8),
    ('Shrimp Scampi', 15.25, 'Gebratene Garnelen in Knoblauchbutter', 8),
    ('Key Lime Pie', 7.99, 'Key Lime Pie mit Baiserhaube', 8),
('Classic Cheeseburger', 10.99, 'Klassischer Cheeseburger mit Pommes', 9),
    ('Bacon Avocado Wrap', 12.50, 'Wrap mit Bacon, Avocado und Hühnchen', 9),
    ('Caesar Salad', 8.75, 'Caesar Salat mit Hähnchen', 9),
    ('Chili Cheese Fries', 11.95, 'Pommes mit Chili und Käse', 9),
    ('Philly Cheesesteak', 13.50, 'Cheesesteak Sandwich mit Paprika', 9),
    ('Onion Rings', 6.75, 'Knusprige Zwiebelringe', 9),
    ('Buffalo Wings', 9.99, 'Scharfe Chicken Wings mit Dip', 9),
    ('Shrimp Po Boy', 14.50, 'Shrimp Sandwich mit Remoulade', 9),
    ('Loaded Nachos', 8.25, 'Nachos mit allem Drum und Dran', 9),
    ('Chocolate Shake', 5.50, 'Schokoladen-Shake mit Sahne', 9),
('Classic Sundae', 7.99, 'Klassische Eis-Sundae mit Toppings', 10),
    ('Banana Split', 9.50, 'Banana Split mit verschiedenen Eissorten', 10),
    ('Caramel Popcorn', 5.75, 'Karamell-Popcorn als Snack', 10),
    ('Strawberry Shortcake', 11.95, 'Erdbeer-Schichtkuchen mit Sahne', 10),
    ('Blueberry Cheesecake', 12.50, 'Blaubeer-Käsekuchen mit Fruchtsoße', 10),
    ('Pecan Pie', 8.75, 'Pekannusskuchen mit Vanilleeis', 10),
    ('Mint Chocolate Chip Ice Cream', 6.99, 'Eiscreme mit Minze und Schokolade', 10),
    ('Cherry Almond Tart', 10.25, 'Tarte mit Kirschen und Mandeln', 10),
    ('Pumpkin Spice Latte', 4.50, 'Kürbisgewürz-Latte als Heißgetränk', 10),
    ('Cookie Dough Blizzard', 8.25, 'Blizzard mit Keksteig-Stücken', 10)  """)
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


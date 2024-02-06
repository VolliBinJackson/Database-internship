In diesem Projekt geht es um die Implementation und Bereitstellung eines Online Lieferdienstes. Dafür wurde HTML/CSS für die Frontendseite verwendet und Flask für die serverseitige Logik. Als Datenbank für die Speicherung von User, Restaurants,
Bestellungsdetails etc. wird MySQLite3 verwendet.
Die Funktionalität der Webseite war bei der Implementierung im Fokus gewesen, somit wurde der stilistische Aspekt mit CSS etwas nachgelassen. Als Nutzer kann man sich in der Anwendung aber sehr wohl zurechtfinden.

Um die Anwendung zum Laufen zu bringen, sollte vor allem Flask installiert sein. Dann muss man im Terminal zum Verzeichnis "DeliveryService" navigieren und dann per "flask run" die Anwendung starten.
Es erscheint eine IP-Adresse, die man mit strg + mausklick öffnen kann. 

Wie genau die Anwendung funktioniert lässt sich folgend beschreiben:

Ein User sollte Essen bestellen können. Kunden können auf Lieferspatz einen Kundenaccount anlegen.
Nach erfolgreichem Login sehen Kunden eine Übersicht an Restaurants, die zu ihrer PLZ 
liefern können und aktuell geöffnet haben. Bei einem Klick auf ein Restaurant gelangen 
Kunden zu der Detailansicht mit der Beschreibung des Restaurants und der entsprechenden 
Speisekarte. Kunden stellen sich ihre Mahlzeit aus den verfügbaren Items von der Speisekarte 
zusammen. Bei jedem Item kann eine Mengenangabe getätigt werden. Sobald die 
gewünschten Items ausgesucht wurden, navigieren Kunden zur Übersichtsseite ihrer 
Bestellung. Hier werden nochmal alle Items inklusive Preisen gelistet. 
In dieser Übersicht können einzelne Items direkt gelöscht werden, 
und es gibt eine Möglichkeit, einen optionalen Zusatztext für das Restaurant zu verfassen. 
Sind die Kunden mit der Auswahl zufrieden, können sie nun die Bestellung abschicken. 
Nach dem Abschicken der Bestellung können Kunden jederzeit den Status einer Bestellung  
einsehen. Ferner können Kunden jederzeit auf ihre Bestellhistorie zugreifen und die 
Details früherer Bestellungen einsehen. 


Ein Restaurant kann einen Geschäftsaccount anlegen. Dazu müssen ein Name, eine Adresse (Straße und Postleitzahl) 
und eine Beschreibung angegeben werden. Ferner wird beim Anlegen des Accounts ein Passwort 
ausgesucht, welches für zukünftige Logins benötigt wird. Jedes Restaurant besitzt eine 
individuelle Speisekarte. Zur Einfachheit bezeichnen wir die Speisen/Getränke auf der Speisekarte 
als Items. Ein Restaurant kann jederzeit Items zur Karte hinzufügen, von der Karte entfernen oder verändern. 
Jedes Item hat einen Namen, eine Beschreibung und einen Preis. Zur Einfachheit kann 
jedes Item beliebig oft zubereitet werden. Ferner legt jedes Restaurant Öffnungszeiten (von/bis) und 
Lieferradius fest. Der Lieferradius wird einfach als eine Liste an zulässigen Postleitzahlen angegeben.
Sobald eine Bestellung für ein Restaurant eingeht, wird in der Webanwendung darauf 
hingewiesen. Das Restaurant kann die Bestellung dann sichten und entweder ablehnen 
oder bestätigen. Ferner kann ein Restaurant jederzeit die Bestellhistorie einsehen. 
Die Historie enthält sowohl abgeschlossene, als auch laufende (also nicht abgeschlossene oder stornierte) Bestellungen. 




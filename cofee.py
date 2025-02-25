import sqlite3

connection = sqlite3.connect('coffee.sqlite')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT NOT NULL,
    ground TEXT NOT NULL,
    taste_description TEXT NOT NULL,
    price REAL NOT NULL,
    volume REAL NOT NULL
);
''')

cursor.execute('''
INSERT INTO coffee (name, roast_level, ground, taste_description, price, volume)
VALUES
    ('Arabica', 'Medium', 'Ground', 'Fruity and sweet', 10.5, 250),
    ('Robusta', 'Dark', 'Beans', 'Strong and bitter', 8.0, 500),
    ('Ethiopian Yirgacheffe', 'Light', 'Beans', 'Floral and citrusy', 15.0, 250);
''')

connection.commit()
connection.close()

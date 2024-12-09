import sqlite3

def initialize_database():
    conn = sqlite3.connect("ice_cream_parlor.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS flavors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        season TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        stock INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flavor_name TEXT NOT NULL,
                        FOREIGN KEY(flavor_name) REFERENCES flavors(name))''')
    conn.commit()
    return conn

def add_flavor(conn, name, season):
    try:
        conn.execute("INSERT INTO flavors (name, season) VALUES (?, ?)", (name, season))
        conn.commit()
        print(f"Flavor '{name}' added for {season} season.")
    except sqlite3.IntegrityError:
        print("Flavor already exists!")

def add_ingredient(conn, name, stock):
    try:
        conn.execute("INSERT INTO ingredients (name, stock) VALUES (?, ?)", (name, stock))
        conn.commit()
        print(f"Ingredient '{name}' added with stock {stock}.")
    except sqlite3.IntegrityError:
        print("Ingredient already exists!")

def add_allergen(conn, name):
    try:
        conn.execute("INSERT INTO allergens (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Allergen '{name}' added.")
    except sqlite3.IntegrityError:
        print("Allergen already exists!")

def search_flavors(conn, keyword):
    cursor = conn.execute("SELECT * FROM flavors WHERE name LIKE ?", (f"%{keyword}%",))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Flavor: {row[1]}, Season: {row[2]}")
    else:
        print("No matching flavors found.")

def add_to_cart(conn, flavor_name):
    try:
        conn.execute("INSERT INTO cart (flavor_name) VALUES (?)", (flavor_name,))
        conn.commit()
        print(f"'{flavor_name}' added to cart.")
    except sqlite3.IntegrityError:
        print("Error adding to cart. Flavor might not exist.")

def view_cart(conn):
    cursor = conn.execute("SELECT * FROM cart")
    items = cursor.fetchall()
    if items:
        print("Cart Items:")
        for item in items:
            print(f"- {item[1]}")
    else:
        print("Cart is empty.")

def main():
    conn = initialize_database()

    while True:
        print("\n--- Ice Cream Parlor Menu ---")
        print("1. Add Flavor")
        print("2. Add Ingredient")
        print("3. Add Allergen")
        print("4. Search Flavors")
        print("5. Add to Cart")
        print("6. View Cart")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter flavor name: ")
            season = input("Enter season (e.g., Summer, Winter): ")
            add_flavor(conn, name, season)
        elif choice == "2":
            name = input("Enter ingredient name: ")
            stock = int(input("Enter stock quantity: "))
            add_ingredient(conn, name, stock)
        elif choice == "3":
            name = input("Enter allergen name: ")
            add_allergen(conn, name)
        elif choice == "4":
            keyword = input("Enter keyword to search flavors: ")
            search_flavors(conn, keyword)
        elif choice == "5":
            flavor_name = input("Enter flavor name to add to cart: ")
            add_to_cart(conn, flavor_name)
        elif choice == "6":
            view_cart(conn)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

import json
import os

inventory_file = "inventory.json"

def load_inventory(filename=inventory_file):
    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with an empty inventory.")
        return []

    print(f"{filename} found.")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            inventory = json.load(file)
        print("Inventory loaded successfully.")
        return inventory
    except json.JSONDecodeError:
        print("Warning: Inventory file is corrupted. Starting with an empty inventory.")
        return []

def save_inventory(inventory, filename=inventory_file):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
        return True
    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False

def find_product(inventory, item_id):
    for product in inventory:
        if product["id"].lower() == item_id.lower():
            return product
    return None

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    else:
        for p in inventory:
            print(f"ID: {p['id']} | Name: {p['name']} | "
                  f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


def add_product(inventory):
    print("\nAdd New Product")

    while True:
        item_id = input("Product ID: ").strip()
        if not item_id:
            print("Product ID Cannot Be Empty")
        elif find_product(inventory, item_id):
            print("Product ID Already Exists")
        else:
            break

    while True:
        item_name = input("Product Name: ").strip()
        if item_name:
            break
        print("Product Name Cannot Be Empty")

    while True:
        try:
            item_price = float(input("Price: "))
            if item_price >= 0:
                break
            print("Price Cannot Be Negative")
        except ValueError:
            print("Please Enter A Valid Number")

    while True:
        try:
            stock_quantity = int(input("Stock Quantity: ").strip())
            if stock_quantity > 0:
                break
            print("Quantity Must Be Greater Than 0")
        except ValueError:
            print("Please Enter An Integer")

    inventory.append({
        "id": item_id,
        "name": item_name,
        "price": item_price,
        "stock": stock_quantity,
    })
    print("Product added successfully")

def update_stock(inventory):
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, item_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    while True:
        try:
            new_stock = int(input("New Stock Quantity: ").strip())
            if new_stock >= 0:
                break
            print("Stock Cannot Be Negative")
        except ValueError:
            print("Please Enter An Integer")

    product["stock"] = new_stock
    print("Stock updated successfully!")

def search_product(inventory):
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, item_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)

def main_menu():
    print("\n" + "-" * 11 , " MENU " , "-" * 11)
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        main_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
import json
import os

from product_class import Product
from inventory_class import Inventory

inventory_file = "inventory.json"

def load_inventory(filename=inventory_file):
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        loaded = Inventory()
        for item in data:
            if not loaded.add_product(Product.from_dict(item)):
                print(f"Warning: duplicate ID '{item['id']}' in file was skipped.")
        print("Inventory loaded successfully.")
        return loaded
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print("Warning: Inventory file is corrupted. Starting with an empty inventory.")
        return inventory


def save_inventory(inventory, filename=inventory_file):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
        return True
    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False


def add_product(inventory):
    print("\nAdd New Product")

    while True:
        item_id = input("Product ID: ").strip()
        if not item_id:
            print("Product ID Cannot Be Empty")
        elif inventory.search_product(item_id):
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

    product = Product(item_id, item_name, item_price, stock_quantity)
    inventory.add_product(product)
    print("Product added successfully")


def update_stock(inventory):
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(item_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    while True:
        try:
            new_stock = int(input("New Stock Quantity: ").strip())
        except ValueError:
            print("Please Enter An Integer")
            continue

        try:
            product.update_stock(new_stock)  # Product validates its own state
            break
        except ValueError as error:
            print(error)

    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(item_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    product.display_information()


def main_menu():
    print("\n" + "-" * 11, " MENU ", "-" * 11)
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
            inventory.display_all()
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
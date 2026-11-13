import json
import os

from inventory_class import Inventory
from physical_product_class import PhysicalProduct
from digital_product_class import DigitalProduct
from can_be_shipped_class import CanBeShipped

inventory_file = "inventory.json"

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


# ---------- File Handling ----------
def create_product_from_dict(data):
    product_type = str(data["type"]).lower()
    product_class = PRODUCT_TYPES.get(product_type)
    if product_class is None:
        raise ValueError(f"Unknown product type '{product_type}'.")
    return product_class.from_dict(data)


def load_inventory(filename=inventory_file):
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise TypeError("Inventory data must be a list.")
    except (json.JSONDecodeError, TypeError, OSError):
        print("Warning: Inventory file is corrupted. Starting with an empty inventory.")
        return inventory

    for item in data:
        try:
            product = create_product_from_dict(item)
        except (KeyError, ValueError, TypeError):
            print(f"Warning: skipped an invalid entry: {item}")
            continue
        if not inventory.add_product(product):
            print(f"Warning: duplicate ID '{product.product_id}' in file was skipped.")

    print("Inventory loaded successfully.")
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


# ---------- Input Helpers ----------
def ask_positive_float(prompt, label):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print(f"{label} Must Be Greater Than 0")
        except ValueError:
            print("Please Enter A Valid Number")


# ---------- Menu Actions ----------
def add_product(inventory):
    print("\nAdd New Product")

    while True:
        print("Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        product_type = input("Choose type (1/2): ").strip()
        if product_type in ("1", "2"):
            break
        print("Please Enter 1 or 2")

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

    if product_type == "1":
        weight = ask_positive_float("Weight (kg): ", "Weight")
        product = PhysicalProduct(item_id, item_name, item_price, stock_quantity, weight)
    else:
        size = ask_positive_float("Download Size (MB): ", "Download Size")
        product = DigitalProduct(item_id, item_name, item_price, stock_quantity, size)

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
            product.update_stock(new_stock)
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
    print("-" * 48)
    product.display_information()          # overridden by each subclass
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):  # only shippable products
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


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
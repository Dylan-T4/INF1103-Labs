import csv
import math

from inventory_class import Inventory
from supplier_class import Supplier
from order_class import Order
from product_class import Product
from product_factory_class import ProductFactory
from can_be_shipped_class import CanBeShipped
from discount_strategy_class import DiscountStrategy
from no_discount_class import NoDiscount
from percentage_discount_class import PercentageDiscount
from bulk_discount_class import BulkDiscount
from student_discount_class import StudentDiscount

inventory_file = "products.csv"

CSV_HEADER = ["product_type", "product_id", "name", "price", "stock_quantity",
              "weight_or_size", "supplier_id", "supplier_name", "supplier_email"]

# Used only for CSV rows that do not include supplier columns
# (e.g. the lab's products.csv, which has just 5 columns).
DEFAULT_SUPPLIER = Supplier("UNKNOWN", "Unknown Supplier", "unknown@example.com")

def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value):
                raise ValueError("not a finite number")
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def ask_supplier(inventory: Inventory) -> Supplier:
    while True:
        supplier_id = input("Supplier ID: ").strip()
        if supplier_id:
            break
        print("Supplier ID Cannot Be Empty")

    for product in inventory.products:
        if product.supplier.supplier_id.lower() == supplier_id.lower():
            print(f"Existing supplier found: {product.supplier}")
            return product.supplier

    while True:
        name = input("Supplier Name: ").strip()
        email = input("Supplier Email: ").strip()
        try:
            return Supplier(supplier_id, name, email)
        except ValueError as error:
            print(error)


PRODUCT_CHOICES = {
    "1": ("physical", "Weight (kg): "),
    "2": ("digital", "Download Size (MB): "),
}


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")

    while True:
        print("Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        choice = input("Choose type (1/2): ").strip()
        if choice in PRODUCT_CHOICES:
            product_type, specific_prompt = PRODUCT_CHOICES[choice]
            break
        print("Please Enter 1 or 2")

    while True:
        item_id = input("Product ID: ").strip()
        if not item_id:
            print("Product ID Cannot Be Empty")
        elif inventory.find_product(item_id):
            print("Product ID Already Exists")
        else:
            break

    while True:
        item_name = input("Product Name: ").strip()
        if item_name:
            break
        print("Product Name Cannot Be Empty")

    item_price = get_positive_float("Price: ")

    while True:
        try:
            stock_quantity = int(input("Stock Quantity: ").strip())
            if stock_quantity > 0:
                break
            print("Quantity Must Be Greater Than 0")
        except ValueError:
            print("Please Enter An Integer")

    supplier = ask_supplier(inventory)
    specific_value = get_positive_float(specific_prompt)

    product: Product = ProductFactory.create(product_type, item_id, item_name,
                                             item_price, stock_quantity,
                                             supplier, specific_value)
    inventory.add_product(product)
    print("Product added successfully")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(item_id)

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


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(item_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    item_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(item_id)

    if product is None:
        print("Product not found.")
        return

    print(f"Product Found: {product}")
    confirm = input("Remove this product from the inventory? (y/n): ").strip().lower()
    if confirm != "y":
        print("Removal cancelled.")
        return

    inventory.remove_product(product.product_id)
    print("Product removed from inventory.")


def create_product_from_row(row: list[str], default_supplier: Supplier) -> Product:
    """Build one product from a CSV row. Raises ValueError with a clear message.

    Columns: product_type, product_id, name, price, stock_quantity,
    then optionally weight_or_size, supplier_id, supplier_name, supplier_email.
    If the supplier columns are missing or blank, default_supplier is used.
    """
    if len(row) < 5:
        raise ValueError("expected at least 5 columns "
                         "(product_type, product_id, name, price, stock_quantity)")
    product_type, product_id, name, price_text, stock_text = (c.strip() for c in row[:5])
    extra_text = row[5].strip() if len(row) > 5 else ""
    supplier_fields = [c.strip() for c in row[6:9]]

    try:
        price = float(price_text)
    except ValueError:
        raise ValueError(f"Price must be a number, got '{price_text}'.") from None
    try:
        stock = int(stock_text)
    except ValueError:
        raise ValueError(f"Stock quantity must be a whole number, got '{stock_text}'.") from None
    try:
        specific_value = float(extra_text) if extra_text else None
    except ValueError:
        raise ValueError(f"Weight/size must be a number, got '{extra_text}'.") from None

    supplier = default_supplier
    if any(supplier_fields):
        if len(supplier_fields) < 3:
            raise ValueError("supplier needs an ID, name and email.")
        supplier = Supplier(*supplier_fields)

    return ProductFactory.create(product_type, product_id, name, price,
                                 stock, supplier, specific_value)


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    except PermissionError:
        print(f"Not allowed to read the products file: {path}")
    else:
        with file:
            try:
                reader = csv.reader(file)
                next(reader, None)                     # skip the header row
                for line_number, row in enumerate(reader, start=2):
                    if not row:
                        continue                       # ignore blank lines
                    try:
                        product = create_product_from_row(row, supplier)
                    except ValueError as error:
                        print(f"Row {line_number} skipped: {error}")
                        continue
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Row {line_number} skipped: duplicate ID '{product.product_id}'.")
            except (csv.Error, UnicodeDecodeError) as error:
                print(f"Could not read the rest of the file: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory(filename: str = inventory_file) -> Inventory:
    """Start-up load: read the CSV file into a new Inventory using load_products()."""
    inventory = Inventory()
    load_products(filename, inventory, DEFAULT_SUPPLIER)
    return inventory


def save_inventory(inventory: Inventory, filename: str = inventory_file) -> bool:
    """Write every product to a CSV file (with a header row)."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
            for product in inventory.products:
                data = product.to_dict()
                supplier = data["supplier"]
                specific_value = data.get("weight", data.get("download_size", ""))
                writer.writerow([data["type"], data["id"], data["name"],
                                 data["price"], data["stock"], specific_value,
                                 supplier["supplier_id"], supplier["name"],
                                 supplier["contact_email"]])
        print(f"Inventory saved successfully to {filename}.")
        return True
    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False


def import_products(inventory: Inventory) -> None:
    print("\nImport Products From CSV")
    path = input("CSV file path (e.g. products.csv): ").strip()
    if not path:
        print("No file entered.")
        return
    print("Enter the supplier to use for any rows that do not list their own.")
    supplier = ask_supplier(inventory)
    load_products(path, inventory, supplier)


def choose_discount() -> DiscountStrategy:
    """Menu helper: turn the user's choice into a strategy object."""
    while True:
        print("Discount:")
        print("1. No discount")
        print("2. Percentage discount")
        print("3. Bulk discount")
        print("4. Student discount (5%)")
        choice = input("Choose discount (1-4): ").strip()
        try:
            if choice == "1":
                return NoDiscount()
            elif choice == "2":
                return PercentageDiscount(get_positive_float("Percentage off (e.g. 10): "))
            elif choice == "3":
                threshold = get_positive_float("Order total needed for the discount: ")
                amount = get_positive_float("Amount taken off: ")
                return BulkDiscount(threshold, amount)
            elif choice == "4":
                return StudentDiscount()
            print("Please enter a number from 1 to 4.")
        except ValueError as error:
            print(error)


def find_order(orders: list[Order], order_id: str) -> Order | None:
    for order in orders:
        if order.order_id.lower() == order_id.strip().lower():
            return order
    return None


def add_line_to_order(inventory: Inventory, order: Order, item_id: str) -> None:
    product = inventory.find_product(item_id)
    if product is None:
        print("Product not found.")
        return

    while True:
        try:
            quantity = int(input(f"Quantity of {product.name}: ").strip())
        except ValueError:
            print("Please Enter An Integer")
            continue
        try:
            order.add_order_line(product, quantity)
            break
        except ValueError as error:
            print(error)

    print(f"Added {quantity} x {product.name}.")


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    print("\nCreate Order")

    if not inventory.products:
        print("The inventory is empty. Add products before creating an order.")
        return

    while True:
        order_id = input("Order ID: ").strip()
        if not order_id:
            print("Order ID Cannot Be Empty")
        elif find_order(orders, order_id) is not None:
            print("Order ID Already Exists")
        else:
            break

    order = Order(order_id)

    while True:
        item_id = input("Product ID to add (or press Enter to finish): ").strip()
        if not item_id:
            if order.order_lines:
                break
            print("An order needs at least one product.")
            continue
        add_line_to_order(inventory, order, item_id)

    order.set_discount(choose_discount())

    orders.append(order)
    print("\nOrder created successfully")
    print("-" * 48)
    order.display_order()
    print("-" * 48)


def modify_order(inventory: Inventory, orders: list[Order]) -> None:
    print("\nModify Order")

    if not orders:
        print("No orders have been created yet.")
        return

    order = find_order(orders, input("Enter Order ID: "))
    if order is None:
        print("Order not found.")
        return

    while True:
        print("-" * 48)
        order.display_order()
        print("-" * 48)
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Change Discount")
        print("4. Done")
        choice = input("Choose option: ").strip()

        if choice == "1":
            item_id = input("Product ID to add: ").strip()
            add_line_to_order(inventory, order, item_id)
        elif choice == "2":
            item_id = input("Product ID to remove: ").strip()
            if len(order.order_lines) == 1 and any(
                    line.product.product_id.lower() == item_id.lower()
                    for line in order.order_lines):
                print("An order needs at least one product. Add another before removing this one.")
            elif order.remove_order_line(item_id):
                print("Product removed from order.")
            else:
                print("That product is not in this order.")
        elif choice == "3":
            order.set_discount(choose_discount())
        elif choice == "4":
            print("Order updated.")
            break
        else:
            print("Please enter 1, 2, 3 or 4.")


def view_orders(orders: list[Order]) -> None:
    print("\nAll Orders")
    print("-" * 48)
    if not orders:
        print("No orders have been created yet.")
    else:
        for order in orders:
            order.display_order()
            print("-" * 48)
        print(f"Total orders: {len(orders)}")


def main_menu() -> None:
    print("\n" + "-" * 11, " MENU ", "-" * 11)
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Modify Order")
    print("8. View All Orders")
    print("9. Import Products From CSV")
    print("10. Save Inventory")
    print("11. Exit")
    print("-" * 28)


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    orders: list[Order] = []

    while True:
        main_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            remove_product(inventory)
        elif option == "6":
            create_order(inventory, orders)
        elif option == "7":
            modify_order(inventory, orders)
        elif option == "8":
            view_orders(orders)
        elif option == "9":
            import_products(inventory)
        elif option == "10":
            print("Saving inventory...")
            save_inventory(inventory)
        elif option == "11":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 11.")


if __name__ == "__main__":
    main()
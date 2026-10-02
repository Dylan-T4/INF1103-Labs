def get_valid_input(order_id):
    current_orders = {}
    while True:
        while True:
            item_name = input("Enter Product Name: ").strip()
            if item_name:
                break
            print("Product Name Cannot Be Empty")
        if item_name == "quit":
            print("Exiting Inventory Manager...")
            break
        
        while True:
            stock_quantity = input("Enter Stock Quantity To Be Added: ").strip()
            if stock_quantity == "quit":
                break
            try:
                check_quantity = int(stock_quantity)
                if check_quantity > 0:
                    break
                print("Quantity Must Be Greater Than 0")
            except ValueError:
                print("Please Enter An Integer")
        if stock_quantity == "quit":
            print("Exiting Inventory Manager...")
            break

        current_orders[order_id]={"product": item_name, "quantity": check_quantity}
        save_inventory(order_id, item_name, check_quantity)

        print("\nNew Order Added:")
        print(f"{order_id} | {item_name} | {check_quantity}\n")
        order_id += 1
        print("Order Has Been Saved To orders.txt\n")

        print("Current Orders:")
        for past_order_id, details in current_orders.items():
            print(f"{past_order_id} | {details['product']} | {details['quantity']}")
        print()

def load_inventory():
    file_path = "orders.txt"
    order_count = 0
    default_order_id = 1001
    try:
        with open(file_path, 'r') as file:
            print("Transaction History Found, Printing.")
            print("Order ID | Product Name | Quantity")
            print("=========================================")
            for content in file:
                print(content.strip())
                order_count += 1
            print("=========================================")
            print("Type 'quit' To Exit The Inventory Manager")
            print("=========================================")
    except FileNotFoundError:
        print("No Prior Transaction History Found, Creating New File.")
        print("Type 'quit' To Exit The Inventory Manager")
        print("======================================================")
        open(file_path, 'a')

    return default_order_id + order_count

def save_inventory(order_id, item_name, stock_quantity):
    file_path = "orders.txt"
    with open(file_path, 'a') as file:
        file.write(f"{order_id} | {item_name} | {stock_quantity}\n")




current_order_id = load_inventory()

get_valid_input(current_order_id)
        
        

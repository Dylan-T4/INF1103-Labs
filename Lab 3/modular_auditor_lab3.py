def get_valid_input():
    current_inventory = 0
    stock_quantity = 0
    rejects = 0
    while stock_quantity != "quit":
        stock_quantity = input("Please Enter Stock Quantity To Be Added: ")
        if stock_quantity.isdigit():
            new_total = process_delivery(int(current_inventory),int(stock_quantity))
            print("Stock Quantity Added: ", stock_quantity, "units")
            print("Calculated Tax: ", calculate_tax(int(stock_quantity)), "units")
            current_inventory = new_total
            print("New Inventory Total: ", current_inventory, "units")
            if current_inventory > 500:
                print("Critical Error! Inventory Cannot Go Above 500 Units!")
                break
        elif stock_quantity.lstrip('-').isdigit():
            if stock_quantity.count('-') > 1:
                print("Error! Not A Valid Integer!")
                rejects = rejects + 1
                continue
            if int(stock_quantity) < 0:
                print("Error! Negative Numbers Not Accepted!")
                rejects = rejects + 1
        elif stock_quantity == "quit":
            generate_report(current_inventory,rejects)
            continue
        else:
            print("Error! Please Enter Only Integers!")
            rejects = rejects + 1

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("Final Inventory Report")
    print("======================")
    print("Total Units Processed: ", total_units, "Units")    
    print("No. Of Rejected Entries: ", failed_attempts)



get_valid_input()
        
        

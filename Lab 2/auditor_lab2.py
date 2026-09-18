inventory = 0
stock_quantity = 0
rejects = 0

while stock_quantity != "quit":
    stock_quantity = input("Please Enter Stock Quantity To Be Added: ")
    if stock_quantity.isdigit():
        inventory = inventory + int(stock_quantity)
        if inventory > 500:
                    print("Error! Inventory Cannot Go Above 500 Units!")
                    break
        print("Updated Inventory Total: ", inventory, "Units")
    elif stock_quantity.lstrip('-').isdigit():
        if int(stock_quantity) < 0:
            print("Error! Negative Numbers Not Accepted!")
            rejects = rejects + 1
    elif stock_quantity == "quit":
        print("Final Inventory Report")
        print("======================")
        print("Total Units Processed: ", inventory, "Units")    
        print("No. Of Rejected Entries: ", rejects)
        continue
    else:
        print("Error! Please Enter Only Integers!")
        rejects = rejects + 1
        
        



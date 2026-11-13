from product_class import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, item_id):
        for product in self.__products:
            if product.product_id.lower() == item_id.strip().lower():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                print(product)
        print("-" * 48)

    def to_list(self):
        return [product.to_dict() for product in self.__products]
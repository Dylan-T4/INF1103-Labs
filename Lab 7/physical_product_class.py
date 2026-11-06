from product_class import Product
from can_be_shipped_class import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Physical product: Requires physical shipping."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING + self.COST_PER_KG * self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["weight"])

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"

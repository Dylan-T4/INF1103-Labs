from product_class import Product
from can_be_shipped_class import CanBeShipped
from supplier_class import Supplier

class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        self.__weight = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "Physical product: Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
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
    def from_dict(cls, data: dict):
        supplier = Supplier.from_dict(data["supplier"])
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], supplier, data["weight"])

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"

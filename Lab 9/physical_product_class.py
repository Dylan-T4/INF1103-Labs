from product_class import Product
from can_be_shipped_class import CanBeShipped
from supplier_class import Supplier

class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING = 5.00
    COST_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
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

    def to_csv_row(self) -> list:
        return ["physical", self.product_id, self.name, self.price, self.stock,
                self.__weight, self.supplier.supplier_id, self.supplier.name,
                self.supplier.contact_email]

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"
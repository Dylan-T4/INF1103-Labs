import math
from abc import ABC, abstractmethod
from supplier_class import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = str(product_id).strip()
        self.__name: str = str(name).strip()
        try:
            self.__price: float = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number.") from None
        self.__stock: int = 0

        if not self.__product_id:
            raise ValueError("Product ID cannot be empty.")
        if not self.__name:
            raise ValueError("Product name cannot be empty.")
        if not math.isfinite(self.__price) or self.__price <= 0:
            raise ValueError("Price must be greater than zero.")
        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")

        self.__supplier: Supplier = supplier
        self.update_stock(stock)

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be an integer.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        self.__supplier.display_information()

    @abstractmethod
    def to_csv_row(self) -> list:
        pass

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
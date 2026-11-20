from product_class import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("OrderLine needs a Product object.")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def __str__(self) -> str:
        return (f"{self.__product.name} x {self.__quantity} "
                f"@ ${self.__product.price:.2f} = ${self.calculate_subtotal():.2f}")
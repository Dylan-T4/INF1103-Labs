from order_line_class import OrderLine
from product_class import Product

class Order:

    def __init__(self, order_id: str) -> None:
        order_id = str(order_id).strip()
        if not order_id:
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        for index, line in enumerate(self.__order_lines):
            if line.product is product:
                self.__order_lines[index] = OrderLine(product, line.quantity + quantity)
                return
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.product.product_id.lower() == product_id.strip().lower():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        for line in self.__order_lines:
            print(f"  {line}")
        print(f"  Total: ${self.calculate_total():.2f}")
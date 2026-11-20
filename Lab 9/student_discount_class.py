from discount_strategy_class import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """Fourth strategy: added without changing Order at all."""

    RATE: float = 5.0

    def apply(self, total: float) -> float:
        return round(total * (100 - self.RATE) / 100, 2)

    def __str__(self) -> str:
        return f"{self.RATE:g}% student discount"
from discount_strategy_class import DiscountStrategy


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"
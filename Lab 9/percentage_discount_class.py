import math

from discount_strategy_class import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        try:
            percentage = float(percentage)
        except (TypeError, ValueError):
            raise ValueError("Percentage must be a number.") from None
        if not math.isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return round(total * (100 - self.__percentage) / 100, 2)

    def __str__(self) -> str:
        return f"{self.__percentage:g}% off"
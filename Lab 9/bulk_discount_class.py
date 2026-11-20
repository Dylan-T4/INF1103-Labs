import math

from discount_strategy_class import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        try:
            threshold = float(threshold)
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Threshold and amount must be numbers.") from None
        if not (math.isfinite(threshold) and math.isfinite(amount)):
            raise ValueError("Threshold and amount must be finite numbers.")
        if threshold <= 0:
            raise ValueError("Threshold must be greater than zero.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        if amount > threshold:
            raise ValueError("Discount amount cannot be larger than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(total - self.__amount, 2)
        return total

    def __str__(self) -> str:
        return f"${self.__amount:g} off orders of ${self.__threshold:g} or more"
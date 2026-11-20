from digital_product_class import DigitalProduct
from physical_product_class import PhysicalProduct
from product_class import Product
from supplier_class import Supplier


class ProductFactory:

    DEFAULT_WEIGHT_KG: float = 1.0
    DEFAULT_DOWNLOAD_SIZE_MB: float = 1.0

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               specific_value: float | None = None) -> Product:
        kind = str(product_type).strip().lower()
        if kind == "physical":
            weight = (ProductFactory.DEFAULT_WEIGHT_KG
                      if specific_value is None else specific_value)
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif kind == "digital":
            size = (ProductFactory.DEFAULT_DOWNLOAD_SIZE_MB
                    if specific_value is None else specific_value)
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_from_dict(data: dict) -> Product:
        kind = str(data["type"]).strip().lower()
        if kind == "physical":
            return PhysicalProduct.from_dict(data)
        elif kind == "digital":
            return DigitalProduct.from_dict(data)
        else:
            raise ValueError(f"Unknown product type: {data['type']}")
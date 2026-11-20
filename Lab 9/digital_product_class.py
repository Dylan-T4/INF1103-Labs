from product_class import Product
from supplier_class import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        download_size = float(download_size)
        if download_size <= 0:
            raise ValueError("Download size must be greater than 0.")
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Digital product: Delivered digitally via download link."

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_csv_row(self) -> list:
        return ["digital", self.product_id, self.name, self.price, self.stock,
                self.__download_size, self.supplier.supplier_id, self.supplier.name,
                self.supplier.contact_email]

    def __str__(self) -> str:
        return f"{super().__str__()} | Download Size: {self.__download_size:.2f} MB"
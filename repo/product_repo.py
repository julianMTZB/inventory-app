import os
import json 
from models.product import Product
from exceptions import ProductNotFound

class ProductRepo:
    def __init__(self, route="inventory.json"):
        self.route = route
        self._products = self.load_inventory()

    def load_inventory(self):
        products = {}
        if os.path.exists(self.route):
            with open(self.route, "r") as f:
                data = json.load(f)
            for d in data:
                product = Product(d["sku"], d["name"], d["price"], d["stock"])
                products[product.sku] = product       
        return products

    def save_inventory(self):
        data = []
        for product in self._products.values():
            data.append(product.to_dict())
        with open(self.route, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def next_sku(self):
        if not self._products:
            return 1
        return max(self._products) + 1

    def add_product(self, product):
        self._products[product.sku] = product

    def remove_product(self, sku):
        del self._products[sku]

    def get_product(self, sku):
        if self._products.get(sku) is None:
            raise ProductNotFound(f"Producto con SKU: '{sku}' no encontrado.")
        return self._products.get(sku)

    def list_products(self):
        return list(self._products.values())


    


    
        
from models.product import Product

class InventoryService:
    def __init__(self, repo):
        self.repo = repo

    def create_product(self, sku, name, price, stock):
        product = Product(sku, name, price, stock)
        self.repo.add_product(product)
        return sku

    def delete_product(self, sku):
        self.repo.get_product(sku)
        self.repo.remove_product(sku)
        return sku
          
    def product_info(self, sku):
        return self.repo.get_product_info(sku)

    def products_info(self):
        return self.repo.list_products()


        
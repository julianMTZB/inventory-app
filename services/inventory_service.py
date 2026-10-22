from models.product import Product

class InventoryService:
    def __init__(self, repo):
        self.repo = repo

    def create_product(self, name, price, stock):
        sku = self.repo.next_sku()
        product = Product(sku, name, price, stock)
        self.repo.add_product(product)
        self.repo.save_inventory()
        return sku

    def delete_product(self, sku):
        if self.repo.get_product(sku):
            self.repo.remove_product(sku)
            self.repo.save_inventory()
            return sku

    def find_product_info(self, sku):
        product = self.repo.get_product(sku)
        return product.to_dict()

    def products_info(self):
        data = []
        products = self.repo.list_products()
        for product in products:
            data.append(product.to_dict())
        return data


        
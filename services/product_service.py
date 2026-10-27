
class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def change_price(self, sku, new_price):
        product = self.repo.get_product(sku)
        product.price = new_price
        self.repo.update_product(product) 

    def register_entry(self, sku, quantity):
        product = self.repo.get_product(sku)
        product.add_stock(quantity)
        self.repo.update_product(product)
    
    def register_exit(self, sku, quantity):
        product = self.repo.get_product(sku)
        product.remove_stock(quantity)
        self.repo.update_product(product)

    def change_name(self, sku, new_name):
            product = self.repo.get_product(sku)
            product.change_name(new_name)
            self.repo.update_product(product) 

        
        


        

    
        
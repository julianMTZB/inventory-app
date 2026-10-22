class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def change_price(self, sku, new_price):
        product = self.repo.get_product(sku)
        product.price = new_price
        self.repo.save_inventory() 

    def register_entry(self, sku, quantity):
        product = self.repo.get_product(sku)
        product.add_stock(quantity)
        self.repo.save_inventory() 
    
    def register_exit(self, sku, quantity):
        product = self.repo.get_product(sku)
        product.remove_stock(quantity)
        self.repo.save_inventory() 

    def change_name(self, sku, new_name):
            product = self.repo.get_product(sku)
            product.change_name(new_name)
            self.repo.save_inventory() 

        
        


        

    
        
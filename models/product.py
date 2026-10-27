
from exceptions import NegativePrice, NegativeStock, InsufficientStock

class Product:
    def __init__(self, sku, name, price, stock=0):
        self.sku = sku
        self.name = name
        self._stock = stock
        self._price = price

    # -- Cambiar precio --
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        new_price = float(new_price)
        if new_price <= 0:
            raise NegativePrice("El precio debe ser mayor a cero.")
        self._price = new_price
    
    # -- Cambiar stock --
    @property
    def stock(self):
        return self._stock

    def add_stock(self, quantity):
        if quantity <= 0:
            raise NegativeStock("La entrada debe ser mayor a cero.")
        self._stock += quantity

    def remove_stock(self, quantity):
        if quantity <= 0:
            raise NegativeStock("La salida debe ser mayor a cero.")
        if quantity > self._stock:
            raise InsufficientStock("No hay suficiente stock disponible.")
        self._stock -= quantity 

    # -- Cambiar nombre --
    def change_name(self, new_name):
        self.name = new_name



        
from models.product import Product
import sqlite3
from exceptions import ProductNotFound, DuplicateSku

"""
Falta establecer el ciclo de transacciones. 
(Cerrar las conexiones con la base de datos después de usar
cada método de la clase) El encargado de cerrar el repo es quien lo crea
"""

class ProductRepo:
    def __init__(self, path="product_repo.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False) #Aquí se crea la conexion
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def create_table(self):
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            price REAL CHECK (price > 0),
            stock INTEGER NOT NULL DEFAULT 0
            )""")

    def get_product(self, sku):
        row = self.conn.execute(
            "SELECT sku, name, price, stock FROM products WHERE sku = ?", (sku,)
            ).fetchone()
        if row:
            return Product(**dict(row))
        raise ProductNotFound(f"Producto con SKU: '{sku}' NO encontrado")

    def get_product_info(self, sku):
        row = self.conn.execute(
            "SELECT * FROM products WHERE sku = ?", (sku,)
            ).fetchone()
        if row:
            return dict(row)
        raise ProductNotFound(f"Producto con SKU: '{sku}' NO encontrado")
                
    def add_product(self, product):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO products (sku, name, price, stock) VALUES (?,?,?,?)",
                                (product.sku, product.name, product.price, product.stock))
        except sqlite3.IntegrityError as error:
            if "UNIQUE" in str(error):
                raise DuplicateSku(f"Ya existe un producto con el sku '{product.sku}'.")
            raise
                        
    def remove_product(self, sku):
        with self.conn:
            self.conn.execute("DELETE FROM products WHERE sku = ?", (sku,))

    def update_product(self, product: Product):
        with self.conn:
            self.conn.execute(
                "UPDATE products SET sku = ?, name = ?, price = ?, stock = ? WHERE sku = ?",
                (product.sku, product.name, product.price, product.stock, product.sku))

    def list_products(self): #REVISAR
        rows = self.conn.execute(
            "SELECT * FROM products ORDER BY name"
        ).fetchall()     
        return [dict(row) for row in rows]


            

    

    
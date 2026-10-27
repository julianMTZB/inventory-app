import math
import os
import re

from flask import Flask, flash, redirect, render_template, request, url_for

from markupsafe import Markup
from exceptions import (InsufficientStock, NegativePrice, 
                        DuplicateSku, NegativeStock, ProductNotFound)
from repo.product_repo import ProductRepo
from services.inventory_service import InventoryService
from services.product_service import ProductService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = os.environ.get("STOCKTRACKER_SECRET", "stocktracker-dev")

# Mismas piezas que en test.py: un repo compartido por los dos servicios.
repo = ProductRepo(os.path.join(BASE_DIR, "inventory.db"))
repo.create_table()
inventory_service = InventoryService(repo)
product_service = ProductService(repo)

# Todo lo que el backend (o la lectura del formulario) puede lanzar y que
# queremos mostrarle al usuario como mensaje, no como página de error.
EXPECTED_ERRORS = (ValueError, NegativePrice, NegativeStock, 
                   DuplicateSku, InsufficientStock, ProductNotFound)

@app.template_global()
def icon(name):
    return Markup(f'<svg class="i" aria-hidden="true"><use href="#i-{name}"/></svg>')

# ---------- Lectura de formularios ----------
# Los formularios entregan texto. El backend espera números, así que se
# convierten aquí, antes de llamar a los servicios.

def read_name(raw):
    name = (raw or "").strip()
    if not name:
        raise ValueError("El nombre no puede estar vacío.")
    return name

def read_sku(raw):
    sku = (raw or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,32}", sku):
        raise ValueError("El SKU solo puede llevar letras, números, punto, guion y guion bajo (máximo 32).")
    return sku

def read_price(raw):
    try:
        price = float((raw or "").strip())
    except ValueError:
        raise ValueError("El precio debe ser un número. Usa punto para los decimales, por ejemplo 49.90.")
    if not math.isfinite(price):
        raise ValueError("El precio debe ser un número válido.")
    if price <= 0:
        raise NegativePrice("El precio debe ser mayor a cero.")
    return price


def read_int(raw, label):
    try:
        return int((raw or "").strip())
    except ValueError:
        raise ValueError(f"{label} debe ser un número entero.")


def attempt(action):
    """Ejecuta una acción y devuelve el error esperado, o None si salió bien."""
    try:
        action()
    except EXPECTED_ERRORS as error:
        return error
    return None


def back_to_product(sku, error, success_message):
    if isinstance(error, ProductNotFound):
        flash(str(error), "error")
        return redirect(url_for("index"))
    if error:
        flash(str(error), "error")
    else:
        flash(success_message, "success")
    return redirect(url_for("product_detail", sku=sku))


# ---------- Filtros de plantilla ----------

@app.template_filter("money")
def money(value):
    return f"${value:,.2f}"


@app.template_filter("num")
def num(value):
    return f"{value:,}"


# ---------- Páginas ----------

@app.get("/")
def index():
    products = sorted(inventory_service.products_info(), key=lambda p: p["sku"])
    summary = {
        "count": len(products),
        "units": sum(p["stock"] for p in products),
        "value": sum(p["price"] * p["stock"] for p in products),
    }
    return render_template("index.html", products=products, summary=summary)


@app.route("/products/new", methods=["GET", "POST"])
def new_product():
    form = {"sku": "","name": "", "price": "", "stock": "0"}
    if request.method == "POST":
        form = {key: request.form.get(key, "") for key in form}
        try:
            sku = read_sku(form["sku"])
            name = read_name(form["name"])
            price = read_price(form["price"])
            stock = read_int(form["stock"], "El stock inicial")
            if stock < 0:
                raise NegativeStock("El stock inicial no puede ser negativo.")
            sku = inventory_service.create_product(sku, name, price, stock)
        except EXPECTED_ERRORS as error:
            flash(str(error), "error")
        else:
            flash(f"Producto creado con SKU {sku}.", "success")
            return redirect(url_for("product_detail", sku=sku))
    return render_template("new_product.html", form=form)


@app.get("/products/<sku>")
def product_detail(sku):
    try:
        product = inventory_service.product_info(sku)
    except ProductNotFound as error:
        flash(str(error), "error")
        return redirect(url_for("index"))
    return render_template("product.html", p=product)


# ---------- Acciones (siempre POST, siempre redirigen) ----------

@app.post("/products/<sku>/entry")
def register_entry(sku):
    error = attempt(lambda: product_service.register_entry(
        sku, read_int(request.form.get("quantity"), "La cantidad")))
    return back_to_product(sku, error, "Entrada registrada.")


@app.post("/products/<sku>/exit")
def register_exit(sku):
    error = attempt(lambda: product_service.register_exit(
        sku, read_int(request.form.get("quantity"), "La cantidad")))
    return back_to_product(sku, error, "Salida registrada.")


@app.post("/products/<sku>/name")
def change_name(sku):
    error = attempt(lambda: product_service.change_name(
        sku, read_name(request.form.get("name"))))
    return back_to_product(sku, error, "Nombre actualizado.")


@app.post("/products/<sku>/price")
def change_price(sku):
    error = attempt(lambda: product_service.change_price(
        sku, read_price(request.form.get("price"))))
    return back_to_product(sku, error, "Precio actualizado.")


@app.post("/products/<sku>/delete")
def delete_product(sku):
    error = attempt(lambda: inventory_service.delete_product(sku))
    if error is None:
        flash("Producto eliminado.", "success")
        return redirect(url_for("index"))
    return back_to_product(sku, error, "")


if __name__ == "__main__":
    app.run(debug=True)

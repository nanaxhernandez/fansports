"""
Rutas principales del proyecto FANSPORTS con Flask.
"""

from datetime import datetime
from flask import render_template, request, redirect
from fansports import app
from fansports import db
from fansports.services.product_service import ProductService
from fansports.services.client_service import ClientService
from fansports.services.sales_service import SalesService
from fansports.services.employee_service import EmployeeService

# Inicializar servicios
product_service = ProductService(db)
client_service = ClientService(db)
sales_service = SalesService(db)
employee_service = EmployeeService(db)

# -----------------------------
# HOME
# -----------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'base.html',
        title='Fansports | Inicio',
        year=datetime.now().year
    )

# -----------------------------
# PRODUCTOS
# -----------------------------
@app.route('/productos')
def productos():
    productos = product_service.listar_productos()
    return render_template(
        'productos.html',
        title='Productos',
        productos=productos,
        year=datetime.now().year
    )

@app.route('/productos/crear', methods=["POST"])
def crear_producto():
    product_service.registrar_producto(
        request.form.get("nombre"),
        request.form.get("descripcion"),
        float(request.form.get("precio") or 0),
        int(request.form.get("stock") or 0),
        int(request.form.get("categoria") or 0),
        int(request.form.get("sede") or 0)
    )
    return redirect('/productos')

# -----------------------------
# CLIENTES
# -----------------------------
@app.route('/clientes')
def clientes():
    clientes = client_service.listar_clientes()
    return render_template(
        'clientes.html',
        title='Clientes',
        clientes=clientes,
        year=datetime.now().year
    )

@app.route('/clientes/crear', methods=["POST"])
def crear_cliente():
    client_service.registrar_cliente(
        request.form.get("nombre"),
        request.form.get("correo"),
        request.form.get("telefono"),
        request.form.get("direccion")
    )
    return redirect('/clientes')

# -----------------------------
# VENTAS
# -----------------------------
@app.route('/ventas')
def ventas():
    return render_template(
        'ventas.html',
        title='Ventas',
        year=datetime.now().year
    )

@app.route('/ventas/crear', methods=["POST"])
def crear_venta():
    cliente = int(request.form.get("cliente"))
    empleado = int(request.form.get("empleado"))
    producto = int(request.form.get("producto"))
    cantidad = int(request.form.get("cantidad"))

    productos = [{"id": producto, "cantidad": cantidad}]
    sales_service.crear_venta_simple(cliente, empleado, productos)

    return redirect('/ventas')

# -----------------------------
# EMPLEADOS
# -----------------------------
@app.route('/empleados')
def empleados():
    empleados = employee_service.listar_empleados()
    return render_template(
        'empleados.html',
        title='Empleados',
        empleados=empleados,
        year=datetime.now().year
    )

@app.route('/empleados/crear', methods=["POST"])
def crear_empleado():
    employee_service.registrar_empleado(
        request.form.get("nombre"),
        request.form.get("apellido"),
        request.form.get("cargo"),
        request.form.get("telefono"),
        request.form.get("correo"),
        int(request.form.get("sede") or 0)
    )
    return redirect('/empleados')

# -----------------------------
# CONTACT & ABOUT (opcional)
# -----------------------------
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contacto',
        year=datetime.now().year,
        message='Pagina de contacto.'
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='Acerca de FANSPORTS',
        year=datetime.now().year,
        message='Informacion sobre la aplicacion.'
    )

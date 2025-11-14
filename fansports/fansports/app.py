from flask import Flask, render_template, request, redirect
from database import OracleDB
from services.product_service import ProductService
from services.client_service import ClientService
from services.sales_service import SalesService
from services.inventory_service import InventoryService
from services.employee_service import EmployeeService

app = Flask(__name__)

# --- CONFIGURAR CONEX AQUI - No tengo la base aca ---
DB_USER = "USUARIO"
DB_PASS = "PASS"
DB_DSN  = "localhost/XEPDB1"   # CAMBIAR 0PR LO CORRECTO
# -------------------------------

db = OracleDB(DB_USER, DB_PASS, DB_DSN)
db.connect()

product_service = ProductService(db)
client_service = ClientService(db)
sales_service = SalesService(db)
inventory_service = InventoryService(db)
employee_service = EmployeeService(db)

@app.route("/")
def home():
    return render_template("base.html")

# Productos
@app.route("/productos")
def productos():
    productos = product_service.listar_productos()
    return render_template("productos.html", productos=productos)

@app.route("/productos/crear", methods=["POST"])
def crear_producto():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    precio = float(request.form.get("precio") or 0)
    stock = int(request.form.get("stock") or 0)
    categoria = int(request.form.get("categoria") or 0)
    sede = int(request.form.get("sede") or 0)
    product_service.registrar_producto(nombre, descripcion, precio, stock, categoria, sede)
    return redirect("/productos")

# Clientes
@app.route("/clientes")
def clientes():
    clientes = client_service.listar_clientes()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/crear", methods=["POST"])
def crear_cliente():
    client_service.registrar_cliente(
        request.form.get("nombre"),
        request.form.get("correo"),
        request.form.get("telefono"),
        request.form.get("direccion"),
    )
    return redirect("/clientes")

# Ventas
@app.route("/ventas")
def ventas():
    return render_template("ventas.html")

@app.route("/ventas/crear", methods=["POST"])
def crear_venta():
    cliente = int(request.form.get("cliente"))
    empleado = int(request.form.get("empleado"))
    producto = int(request.form.get("producto"))
    cantidad = int(request.form.get("cantidad"))
    ventas = [{"id": producto, "cantidad": cantidad}]
    sales_service.crear_venta_simple(cliente, empleado, ventas)
    return redirect("/ventas")

# Empleados
@app.route("/empleados")
def empleados():
    empleados = employee_service.listar_empleados()
    return render_template("empleados.html", empleados=empleados)

@app.route("/empleados/crear", methods=["POST"])
def crear_empleado():
    employee_service.registrar_empleado(
        request.form.get("nombre"),
        request.form.get("apellido"),
        request.form.get("cargo"),
        request.form.get("telefono"),
        request.form.get("correo"),
        int(request.form.get("sede") or 0)
    )
    return redirect("/empleados")

if __name__ == "__main__":
    app.run(debug=True)

# services/product_service.py
class ProductService:
    def __init__(self, db):
        self.db = db

    def registrar_producto(self, nombre, descripcion, precio, stock, categoria, sede):
        # Llama al procedimiento sp_insertar_producto (creado en PL/SQL)
        self.db.call_procedure("sp_insertar_producto", [nombre, descripcion, precio, stock, categoria, sede])

    def listar_productos(self):
        return self.db.select("SELECT ID_producto, nombre, descripcion, precio, stock, ID_categoria, ID_sede FROM Producto ORDER BY ID_producto")

    def listar_bajo_stock(self):
        return self.db.select("SELECT ID_producto, nombre, stock, ID_sede FROM vw_productos_bajo_stock")

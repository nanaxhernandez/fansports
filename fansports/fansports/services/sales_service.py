# services/sales_service.py
import oracledb

class SalesService:
    def __init__(self, db):
        self.db = db

    def crear_venta_simple(self, id_cliente, id_empleado, productos):
        """
        productos: lista de dicts -> [{"id": id_producto, "cantidad": n}, ...]
        Flujo:
          - Crear venta (usamos sp_registrar_venta que devuelve p_id_venta OUT en tu PL/SQL original;
            si el procedimiento en DB no devuelve, se puede usar una función fn_crear_venta).
          - Insertar detalle con sp_registrar_detalle_venta
          - Generar factura con sp_generar_factura
        Nota: Adaptá nombres si tus procedimientos devuelven distintos parámetros.
        """
        # 1) Crear la venta — si tu sp_registrar_venta necesita p_total OUT y p_id_venta OUT,
        # en Python con oracledb hay que preparar variables (aquí suponemos una función fn_crear_venta que devuelve ID)
        try:
            # Intentamos usar una función auxiliar fn_crear_venta (si existe)
            venta_id = None
            try:
                venta_id = self.db.call_function("fn_crear_venta", oracledb.NUMBER, [id_cliente, id_empleado])
            except Exception:
                # Si no existe fn_crear_venta, llamamos al procedimiento sp_registrar_venta
                # que en el script inicial definimos con OUTs — adaptar según implementación en DB.
                cur = self.db.connection.cursor()
                # Asumiendo sp_registrar_venta(p_id_cliente, p_id_empleado, p_total OUT, p_id_venta OUT)
                total_var = cur.var(oracledb.NUMBER)
                idventa_var = cur.var(oracledb.NUMBER)
                cur.callproc("sp_registrar_venta", [id_cliente, id_empleado, total_var, idventa_var])
                venta_id = int(idventa_var.getvalue())
                cur.close()

            # 2) Insertar detalles
            for p in productos:
                self.db.call_procedure("sp_registrar_detalle_venta", [venta_id, p["id"], p["cantidad"]])
                # Reducir stock (si no lo hace trigger/proc)
                # self.db.call_procedure("sp_actualizar_stock", [p["id"], p["cantidad"]])

            # 3) Generar factura
            self.db.call_procedure("sp_generar_factura", [venta_id])

            return venta_id

        except Exception as e:
            raise

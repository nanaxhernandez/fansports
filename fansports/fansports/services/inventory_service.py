# services/inventory_service.py
class InventoryService:
    def __init__(self, db):
        self.db = db

    def registrar_entrada(self, producto_id, cantidad, empleado_id, sede_id):
        self.db.call_procedure("sp_registrar_movimiento_inventario", ['Entrada', cantidad, producto_id, empleado_id, sede_id])
        # También actualiza inventario en el mismo procedimiento body

    def registrar_salida(self, producto_id, cantidad, empleado_id, sede_id):
        self.db.call_procedure("sp_registrar_movimiento_inventario", ['Salida', cantidad, producto_id, empleado_id, sede_id])

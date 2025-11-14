# services/client_service.py
class ClientService:
    def __init__(self, db):
        self.db = db

    def registrar_cliente(self, nombre, correo, telefono, direccion):
        self.db.call_procedure("sp_insertar_cliente", [nombre, correo, telefono, direccion])

    def listar_clientes(self):
        return self.db.select("SELECT ID_cliente, nombre, correo, telefono, direccion FROM Cliente ORDER BY ID_cliente")

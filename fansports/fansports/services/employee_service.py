# services/employee_service.py
class EmployeeService:
    def __init__(self, db):
        self.db = db

    def registrar_empleado(self, nombre, apellido, cargo, telefono, correo, sede_id):
        self.db.call_procedure("sp_insertar_empleado", [nombre, apellido, cargo, telefono, correo, sede_id])

    def listar_empleados(self):
        return self.db.select("SELECT ID_empleado, nombre, apellido, cargo, telefono, correo, ID_sede FROM Empleado ORDER BY ID_empleado")

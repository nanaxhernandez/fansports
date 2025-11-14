from flask import Flask
from fansports.database import OracleDB

app = Flask(__name__)

# Crear instancia global de la base de datos
db = OracleDB("system", "12345", "localhost/XEPDB1")
db.connect()

# Cargar vistas después de crear app y db
import fansports.views

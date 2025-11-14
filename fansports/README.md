FANSPORTS - Proyecto Web Flask (conexión Oracle)

Requisitos:
- Python 3.9+ instalado
- Oracle Database accesible (XE, ORCL, etc)
- (Opcional) Oracle Instant Client si usas oracledb en modo thick

Instalación:
1. Crear y activar un entorno virtual:
   python -m venv venv
   venv\Scripts\activate   (Windows)
   source venv/bin/activate (Linux/Mac)

2. Instalar dependencias:
   pip install -r requirements.txt

3. Configurar la conexión en database.py (usuario, password, dsn).

Ejecución:
   python app.py

Notas:
- Asegurate que las tablas, secuencias y paquetes PL/SQL ya estén creados en la BD.
- Los nombres de procedimientos usados en este proyecto (sp_insertar_producto, sp_insertar_cliente, etc.)
  deben coincidir con los que están en la BD. Si tus nombres difieren, ajustá las llamadas en los servicios.

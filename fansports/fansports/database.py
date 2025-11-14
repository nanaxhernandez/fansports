import oracledb

class OracleDB:
    def __init__(self, user, password, dsn, mode="thin"):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.connection = None
        self.mode = mode

    def connect(self):
        try:
            # Si necesitamos modo thick (Instant Client), se puede hab8litar aqui
            # oracledb.init_oracle_client(lib_dir=r"path_to_instant_client")
            self.connection = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
            print("✔ Conexión establecida con Oracle.")
        except Exception as e:
            print("❌ Error al conectar a Oracle:", e)
            raise

    def select(self, query, params=None):
        cur = self.connection.cursor()
        cur.execute(query, params or {})
        rows = cur.fetchall()
        cur.close()
        return rows

    def execute(self, query, params=None):
        cur = self.connection.cursor()
        cur.execute(query, params or {})
        self.connection.commit()
        cur.close()

    def call_procedure(self, name, params=None):
        cur = self.connection.cursor()
        cur.callproc(name, params or [])
        self.connection.commit()
        cur.close()

    def call_function(self, name, return_type, params=None):
        cur = self.connection.cursor()
        result = cur.callfunc(name, return_type, params or [])
        cur.close()
        return result

    def call_proc_with_refcursor(self, name, params=None):
        cur = self.connection.cursor()
        ref = cur.var(oracledb.CURSOR)
        params = params or []
        params.append(ref)
        cur.callproc(name, params)
        out = ref.getvalue()
        rows = out.fetchall()
        cur.close()
        return rows

    def close(self):
        if self.connection:
            self.connection.close()
            print("✔ Conexión cerrada.")

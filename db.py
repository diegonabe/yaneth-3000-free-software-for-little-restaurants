'''The idea of this script was tu sumarize all backend sql logic here, but it didn't go as that, so i think it is not working'''
import sqlite3

class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect('datos.db')
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
     # Crear la tabla "PLATOS" si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PLATOS (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                precio REAL
                             )''')
        self.conexion.commit()
    
    def registrar_plato(self, nombre, precio_final):
        # Insertar un nuevo plato en la tabla "PLATOS"
        self.cursor.execute("INSERT INTO PLATOS (nombre, precio_final) VALUES (?, ?)", (nombre, precio_final))
        self.conexion.commit()

    def obtener_platos(self):
        # Obtener todos los platos de la tabla "PLATOS"
        self.cursor.execute("SELECT * FROM PLATOS")
        platos = self.cursor.fetchall()
        return platos
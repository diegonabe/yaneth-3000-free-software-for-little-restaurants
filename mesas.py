import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from db import BaseDatos
import re

class VentanaMesas:
    def __init__(self, master):
        self.master = master
        self.ventana_mesas = tk.Toplevel(self.master)
        self.ventana_mesas.title("MESAS")
        self.pedidos = []

        self.crear_tabla_pedidos()

        # Configurar tamaño de la ventana
        ancho_pantalla = self.ventana_mesas.winfo_screenwidth()
        alto_pantalla = self.ventana_mesas.winfo_screenheight()
        ancho_ventana = int(ancho_pantalla * 0.75)  # 75% del ancho de la pantalla
        alto_ventana = int(alto_pantalla * 0.75)    # 75% del alto de la pantalla
        x = (ancho_pantalla - ancho_ventana) // 2   # Centrar horizontalmente
        y = (alto_pantalla - alto_ventana) // 2     # Centrar verticalmente
        self.ventana_mesas.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Botones de las mesas
        mesas = ["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5", "Mesa 6", "Mesa 7", "Mesa 8", "Mesa 9", "Mesa 10", "Mesa 11", "Mesa 12", "Mesa 13", "Mesa 14", "Mesa 15"]
        for i, nombre_mesa in enumerate(mesas):
            boton_mesa = tk.Button(self.ventana_mesas, text=nombre_mesa, font=("Arial", 18), width=15, height=3, bg="green", command=lambda mesa=nombre_mesa: self.abrir_ventana_pedidos(mesa))
            boton_mesa.grid(row=i // 5, column=i % 5, padx=10, pady=10)  # Ajustar el padding interno y externo de los botones

        # Botón "REGRESAR"
        boton_regresar = tk.Button(self.ventana_mesas, text="REGRESAR", font=("Arial", 12), width=10, command=self.ventana_mesas.destroy)
        boton_regresar.grid(row=len(mesas) // 5, column=0, columnspan=5, padx=5, pady=10)

    def crear_tabla_pedidos(self):
        try:
            conexion = sqlite3.connect('datos.db')
            cursor = conexion.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                                id INTEGER PRIMARY KEY,
                                plato TEXT,
                                precio REAL,
                                mesa TEXT
                             )''')

            conexion.commit()
            conexion.close()

        except Exception as e:
            print("Error al crear tabla Pedidos:", e)

    def abrir_ventana_pedidos(self, mesa):
        ventana_pedidos = tk.Toplevel(self.ventana_mesas)
        ventana_pedidos.title(f"Pedidos - {mesa}")

        # Configurar tamaño de la ventana de pedidos
        ventana_pedidos.geometry("800x600")

        # Frame izquierdo para la lista de platos
        frame_izquierdo = tk.Frame(ventana_pedidos)
        frame_izquierdo.pack(side="left", fill="both", expand=True)

        # Obtener los datos de la tabla Platos de la base de datos
        datos_platos = self.obtener_datos_platos()  # Función para obtener datos de la base de datos

        # Obtener los datos de los pedidos para la mesa específica
        
        # Cuadro tipo excel con los datos de la tabla Platos en el frame izquierdo
        self.tree = ttk.Treeview(frame_izquierdo, columns=("Nombre", "Precio"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        for plato in datos_platos:
            self.tree.insert("", "end", values=(plato["nombre"], plato["precio"]))
        self.tree.pack(fill="both", expand=True)

        # Frame derecho para los botones y detalles del pedido
        frame_derecho = tk.Frame(ventana_pedidos)
        frame_derecho.pack(side="right", fill="both", expand=True)

        # Botón AÑADIR
        boton_anadir = tk.Button(frame_izquierdo, text="AÑADIR", command=lambda mesa=mesa: self.abrir_ventana_anadir(mesa))
        boton_anadir.pack()

        # Botón QUITAR
        boton_quitar = tk.Button(frame_izquierdo, text="QUITAR", command=self.abrir_ventana_quitar)
        boton_quitar.pack()

        # Frame central 
        frame_central = tk.Frame(ventana_pedidos, bg="gray")
        frame_central.pack(side="left", padx=5, pady=5, fill="y")

        # Obtener los datos de los pedidos para la mesa específica

        datos_pedidos = self.cargar_pedidos(mesa)

       # Cuadro tipo excel con los datos de la tabla Platos en el frame central
        self.tree_central = ttk.Treeview(frame_central, columns=("Nombre", "Precio"), show="headings")
        self.tree_central.heading("Nombre", text="Nombre")
        self.tree_central.heading("Precio", text="Precio")
        for pedido in datos_pedidos:
            self.tree_central.insert("", "end", values=(pedido["plato"], pedido["precio"]))
        self.tree_central.pack(fill="both", expand=True)


    def obtener_datos_platos(self):
        try:
            # Conexión a la base de datos SQLite
            conexion = sqlite3.connect('datos.db')
            cursor = conexion.cursor()
            
            # Obtener los datos de la tabla Platos
            cursor.execute("SELECT nombre, precio FROM platos")
            datos_platos = cursor.fetchall()

            # Convertir los datos a una lista de diccionarios
            platos = []
            for plato in datos_platos:
                plato_dict = {"nombre": plato[0], "precio": plato[1]}
                platos.append(plato_dict)

            # Cerrar la conexión a la base de datos
            conexion.close()
            return platos
        
        except Exception as e:
            print("Error al obtener datos de platos:", e)
            return []

    def abrir_ventana_anadir(self, mesa):
        # Obtener el elemento seleccionado en el TreeView de frame_izquierdo
        item = self.tree.focus()
        if item:
            plato = self.tree.item(item, "values")
            # Insertar el elemento en el TreeView del frame_central
            self.tree_central.insert("", "end", values=plato)

            # Guardar el pedido en la base de datos
            self.guardar_pedido(plato[0], plato[1], mesa)
            self.actualizar_pedidos()

    def guardar_pedido(self, nombre_plato, precio_plato, mesa):
        try:
            # Conexión a la base de datos SQLite
            conexion = sqlite3.connect('datos.db')
            cursor = conexion.cursor()

            # Obtener el último ID de la tabla de pedidos
            cursor.execute("SELECT MAX(id) FROM pedidos")
            max_id = cursor.fetchone()[0]
            new_id = max_id + 1 if max_id else 1

            # Insertar el nuevo pedido en la tabla "Pedidos"
            cursor.execute("INSERT INTO pedidos (id, plato, precio, mesa) VALUES (?, ?, ?, ?)", (new_id, nombre_plato, precio_plato, mesa))
            conexion.commit()

            print("Pedido guardado correctamente.")

            self.pedidos.append({"nombre": nombre_plato, "precio": precio_plato, "mesa": mesa})

        except Exception as e:
            print("Error al guardar el pedido:", e)

        finally:
            # Cerrar la conexión a la base de datos
            conexion.close()

    def cargar_pedidos(self, mesa):
        try:
            # Conexión a la base de datos SQLite
            conexion = sqlite3.connect('datos.db')
            cursor = conexion.cursor()
            # Obtener los datos de la tabla Pedidos para la mesa específica
            cursor.execute("SELECT plato, precio FROM pedidos WHERE mesa = ?", (mesa,))
            datos_pedidos = cursor.fetchall()
            # Convertir los datos a una lista de diccionarios
            pedidos = []
            for pedido in datos_pedidos:
                pedido_dict = {"plato": pedido[0], "precio": pedido[1]}
                pedidos.append(pedido_dict)
            # Cerrar la conexión a la base de datos
            conexion.close()
            return pedidos
        except Exception as e:
            print("Error al obtener datos de pedidos:", e)
            return []

    def abrir_ventana_quitar(self):
        # Obtener el elemento seleccionado en el TreeView central
        item = self.tree_central.focus()
        if item:
            # Obtener los datos del plato seleccionado
            plato_seleccionado = self.tree_central.item(item, "values")
            nombre_plato = plato_seleccionado[0]
            precio_plato = plato_seleccionado[1]

            # Eliminar el elemento seleccionado del TreeView central
            self.tree_central.delete(item)

            # Eliminar el plato de la base de datos
            self.eliminar_pedido(nombre_plato, precio_plato)
    
    def eliminar_pedido(self, nombre_plato, precio_plato):
        try:
            # Conexión a la base de datos SQLite
            conexion = sqlite3.connect('datos.db')
            cursor = conexion.cursor()

            # Eliminar el pedido de la tabla "Pedidos"
            cursor.execute("DELETE FROM pedidos WHERE plato = ? AND precio = ?", (nombre_plato, precio_plato))
            conexion.commit()

            print("Pedido eliminado correctamente.")

        except Exception as e:
            print("Error al eliminar el pedido:", e)

        finally:
            # Cerrar la conexión a la base de datos
            conexion.close()

    def actualizar_pedidos(self):
        # Actualiza el TreeView central con los datos de la lista de pedidos
        # Borra todos los elementos del TreeView central
        for item in self.tree_central.get_children():
            self.tree_central.delete(item)
        # Inserta los pedidos de la lista en el TreeView central
        for pedido in self.pedidos:
            self.tree_central.insert("", "end", values=(pedido["nombre"], pedido["precio"]))

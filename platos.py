import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class VentanaPlatos:
    def __init__(self, master):
        self.master = master
        self.ventana_platos = tk.Toplevel(self.master)
        self.ventana_platos.title("PLATOS")

        # Configurar tamaño de la ventana
        self.ventana_platos.geometry("600x400")  # Tamaño de la ventana

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.ventana_platos.winfo_screenwidth()
        alto_pantalla = self.ventana_platos.winfo_screenheight()

        # Calcular las coordenadas para que la ventana aparezca en el centro de la pantalla
        x = (ancho_pantalla - 600) // 2  # Centrar horizontalmente (600 es el ancho de la ventana)
        y = (alto_pantalla - 400) // 2    # Centrar verticalmente (400 es el alto de la ventana)

        # Establecer la posición de la ventana en el centro de la pantalla
        self.ventana_platos.geometry(f"600x400+{x}+{y}")

        # Interfaz estilo cuadro de Excel
        self.tree = ttk.Treeview(self.ventana_platos, columns=("Plato", "Precio final"), show="headings")
        self.tree.heading("Plato", text="Plato")
        self.tree.heading("Precio final", text="Precio final")
        self.tree.pack(padx=20, pady=20)

        # Botón CREAR
        self.crear_button = tk.Button(self.ventana_platos, text="CREAR", bg="green", command=self.mostrar_ventana_crear_plato)
        self.crear_button.pack(side="left", padx=10, pady=10)

        # Botón MODIFICAR
        self.modificar_button = tk.Button(self.ventana_platos, text="MODIFICAR", bg="yellow", command=self.mostrar_ventana_modificar_plato)
        self.modificar_button.pack(side="left", padx=10, pady=10)

        # Botón ELIMINAR
        self.eliminar_button = tk.Button(self.ventana_platos, text="ELIMINAR", bg="red", command=self.eliminar_plato)
        self.eliminar_button.pack(side="left", padx=10, pady=10)

        # Conexión a la base de datos SQLite
        self.conexion = sqlite3.connect('datos.db')
        self.crear_tabla()

        # Actualizar tabla de platos
        self.actualizar_tabla_platos()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS platos (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            precio REAL NOT NULL
                        )''')
        self.conexion.commit()

    def mostrar_ventana_crear_plato(self):
        ventana_crear_plato = tk.Toplevel(self.master)
        ventana_crear_plato.title("Crear Plato")

        # Configurar tamaño de la ventana
        ventana_crear_plato.geometry("300x150")  # Tamaño de la ventana

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = ventana_crear_plato.winfo_screenwidth()
        alto_pantalla = ventana_crear_plato.winfo_screenheight()

        # Calcular las coordenadas para que la ventana aparezca en el centro de la pantalla
        x = (ancho_pantalla - 300) // 2  # Centrar horizontalmente (300 es el ancho de la ventana)
        y = (alto_pantalla - 150) // 2    # Centrar verticalmente (150 es el alto de la ventana)

        # Establecer la posición de la ventana en el centro de la pantalla
        ventana_crear_plato.geometry(f"300x150+{x}+{y}")

        # Etiqueta y campo de entrada para el nombre del plato
        tk.Label(ventana_crear_plato, text="Plato:").pack()
        plato_entry = tk.Entry(ventana_crear_plato)
        plato_entry.pack()

        # Etiqueta y campo de entrada para el precio final
        tk.Label(ventana_crear_plato, text="Precio Final:").pack()
        precio_entry = tk.Entry(ventana_crear_plato)
        precio_entry.pack()

        # Botón CONFIRMAR
        def guardar_plato():
            # Obtener el nombre del plato y el precio final ingresados por el usuario
            nombre_plato = plato_entry.get()
            precio_final = precio_entry.get()

            # Verificar si se ingresaron datos en ambos campos
            if nombre_plato and precio_final:
                # Agregar los datos a la tabla de la base de datos
                cursor = self.conexion.cursor()
                cursor.execute("INSERT INTO platos (nombre, precio) VALUES (?, ?)", (nombre_plato, precio_final))
                self.conexion.commit()

                # Actualizar la tabla de platos
                self.actualizar_tabla_platos()

                # Cerrar la ventana de creación de plato
                ventana_crear_plato.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete ambos campos.")

        confirmar_button = tk.Button(ventana_crear_plato, text="CONFIRMAR", command=guardar_plato)
        confirmar_button.pack(pady=10)
    
    def actualizar_tabla_platos(self):
        # Limpiar la tabla antes de actualizarla para evitar duplicados
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener los datos de la base de datos
        cursor = self.conexion.cursor()
        cursor.execute("SELECT nombre, precio FROM platos")
        datos = cursor.fetchall()
        
        # Insertar los datos en la tabla
        for plato in datos:
            self.tree.insert("", "end", values=plato)

    def mostrar_ventana_modificar_plato(self):
        # Obtener el índice seleccionado en el árbol
        seleccion = self.tree.selection()
        if len(seleccion) != 1:
            messagebox.showerror("Error", "Por favor, seleccione un plato para modificar.")
            return

        # Obtener los datos del plato seleccionado
        datos_plato = self.tree.item(seleccion)['values']
        nombre_plato = datos_plato[0]
        precio_plato = datos_plato[1]

        # Crear ventana para modificar plato
        ventana_modificar_plato = tk.Toplevel(self.master)
        ventana_modificar_plato.title("Modificar Plato")

        # Configurar tamaño de la ventana
        ventana_modificar_plato.geometry("300x150")  # Tamaño de la ventana

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = ventana_modificar_plato.winfo_screenwidth()
        alto_pantalla = ventana_modificar_plato.winfo_screenheight()

        # Calcular las coordenadas para que la ventana aparezca en el centro de la pantalla
        x = (ancho_pantalla - 300) // 2  # Centrar horizontalmente (300 es el ancho de la ventana)
        y = (alto_pantalla - 150) // 2    # Centrar verticalmente (150 es el alto de la ventana)

        # Establecer la posición de la ventana en el centro de la pantalla
        ventana_modificar_plato.geometry(f"300x150+{x}+{y}")

        # Etiqueta y campo de entrada para el nombre del plato
        tk.Label(ventana_modificar_plato, text="Plato:").pack()
        plato_entry = tk.Entry(ventana_modificar_plato)
        plato_entry.insert(0, nombre_plato)
        plato_entry.pack()

        # Etiqueta y campo de entrada para el precio final
        tk.Label(ventana_modificar_plato, text="Precio Final:").pack()
        precio_entry = tk.Entry(ventana_modificar_plato)
        precio_entry.insert(0, precio_plato)
        precio_entry.pack()

        # Botón CONFIRMAR
        def confirmar_modificacion():
            nuevo_nombre = plato_entry.get()
            nuevo_precio = precio_entry.get()

            if nuevo_nombre and nuevo_precio:
                cursor = self.conexion.cursor()
                cursor.execute("UPDATE platos SET nombre=?, precio=? WHERE nombre=?", (nuevo_nombre, nuevo_precio, nombre_plato))
                self.conexion.commit()
                self.actualizar_tabla_platos()
                ventana_modificar_plato.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete ambos campos.")

        confirmar_button = tk.Button(ventana_modificar_plato, text="CONFIRMAR", command=confirmar_modificacion)
        confirmar_button.pack(pady=10)

        # Botón ATRÁS
        def volver_atras():
            ventana_modificar_plato.destroy()

        atras_button = tk.Button(ventana_modificar_plato, text="ATRÁS", command=volver_atras)
        atras_button.pack(pady=10)

    def eliminar_plato(self):
        # Obtener el índice seleccionado en el árbol
        seleccion = self.tree.selection()
        if len(seleccion) != 1:
            messagebox.showerror("Error", "Por favor, seleccione un plato para eliminar.")
            return

        # Preguntar al usuario si está seguro de eliminar
        if messagebox.askyesno("Eliminar plato", "¿Está seguro de eliminar este plato?"):
            # Obtener el nombre del plato seleccionado
            nombre_plato = self.tree.item(seleccion)['values'][0]

            # Eliminar el plato de la base de datos
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM platos WHERE nombre=?", (nombre_plato,))
            self.conexion.commit()

            # Eliminar el plato del árbol
            self.tree.delete(seleccion)

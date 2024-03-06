import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db import BaseDatos
from mesas import VentanaMesas
from platos import VentanaPlatos
import re

class InterfazRegistro:
    def __init__(self, master):
        self.master = master
        self.master.title("YANETH 3000 - Bienvenido!!")
        
        # Frame principal
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=80, pady=20)

        # Expresión regular para validar números de hasta 4 dígitos
        self.validacion = self.master.register(self.validar_entrada)

        # Etiquetas y campos de entrada
        tk.Label(self.frame, text="USUARIO:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = tk.Entry(self.frame, validate="key", validatecommand=(self.validacion, '%P'))
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="CLAVE:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.frame, validate="key", validatecommand=(self.validacion, '%P'))
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        self.enviar_button = tk.Button(self.frame, text="Entrar", command=self.mostrar_ventana_menu)
        self.enviar_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Inicializar la clase BaseDatos
        self.base_datos = BaseDatos()
    
    def validar_entrada(self, valor):
        return re.match(r'^\d{0,4}$', valor) is not None

    def mostrar_ventana_menu(self):
        VentanaMenu(self.master)


class VentanaMenu:
    def __init__(self, master):
        self.master = master
        self.ventana_menu = tk.Toplevel(self.master)
        self.ventana_menu.title("Menú Principal")

        # Configurar tamaño de la ventana
        self.ventana_menu.geometry("300x400")  # Cambia el tamaño de la ventana a 300x400 píxeles

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.ventana_menu.winfo_screenwidth()
        alto_pantalla = self.ventana_menu.winfo_screenheight()

        # Calcular las coordenadas para que la ventana aparezca en el centro de la pantalla
        x = (ancho_pantalla - 300) // 2  # Centrar horizontalmente (300 es el ancho de la ventana)
        y = (alto_pantalla - 400) // 2    # Centrar verticalmente (400 es el alto de la ventana)

        # Establecer la posición de la ventana en el centro de la pantalla
        self.ventana_menu.geometry(f"300x400+{x}+{y}")

        # Botones del menú
        botones = ["MESAS", "PLATOS", "USUARIOS", "INFORMES", "SALIR"]
        for i, texto_boton in enumerate(botones):
            # Configurar los botones
            boton = tk.Button(self.ventana_menu, text=texto_boton, font=("Arial", 14), width=20, height=2)
            boton.pack(pady=5, padx=20)  # Ajustar el padding interno y externo de los botones

            # Vincular el botón "MESAS" con la clase VentanaMesas
            if texto_boton == "MESAS":
                boton.config(command=self.mostrar_ventana_mesas)
            
            # Vincular el botón "PLATOS" con la clase VentanaPlatos
            elif texto_boton == "PLATOS":
                boton.config(command=self.mostrar_ventana_platos)

    def mostrar_ventana_mesas(self):
        VentanaMesas(self.master)

    def mostrar_ventana_platos(self):
        VentanaPlatos(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazRegistro(root)

    # Centrar la ventana principal en la pantalla
    ancho_ventana = 400
    alto_ventana = 300
    x = (root.winfo_screenwidth() - ancho_ventana) // 2
    y = (root.winfo_screenheight() - alto_ventana) // 2
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    root.mainloop()


import tkinter as tk
from tkinter import messagebox

# Colores de la interfaz
FONDO = "#172033"
TEXTO = "#F8FAFC"
AZUL = "#38BDF8"

def iniciar_juego():
    messagebox.showinfo(
        "Tres en raya",
        "¡El proyecto está listo para comenzar!"
    )

# Ventana principal
ventana = tk.Tk()
ventana.title("Agentes Inteligentes - Tres en raya")
ventana.geometry("600x500")
ventana.resizable(False, False)
ventana.configure(bg=FONDO)

# Título
titulo = tk.Label(
    ventana,
    text="TRES EN RAYA",
    font=("Arial", 26, "bold"),
    bg=FONDO,
    fg=TEXTO
)
titulo.pack(pady=35)

# Subtítulo
subtitulo = tk.Label(
    ventana,
    text="Humano vs. Agente Inteligente",
    font=("Arial", 13),
    bg=FONDO,
    fg="#CBD5E1"
)
subtitulo.pack(pady=5)

# Botón inicial
boton = tk.Button(
    ventana,
    text="Comenzar",
    font=("Arial", 14, "bold"),
    bg=AZUL,
    fg=FONDO,
    width=18,
    cursor="hand2",
    command=iniciar_juego
)
boton.pack(pady=35)

ventana.mainloop()

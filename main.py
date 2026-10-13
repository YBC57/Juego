
import tkinter as tk
from tkinter import messagebox


# CONFIGURACIÓN

FONDO = "#172033"
TEXTO = "#F8FAFC"
AZUL = "#38BDF8"
ROJO = "#FB7185"
CASILLA = "#263449"
CASILLA_HOVER = "#3B4D66"

HUMANO = "X"
AGENTE = "O"

tablero = [""] * 9
botones = []
partida_terminada = False
turno_pendiente = None

# REGLAS DEL JUEGO

def obtener_ganador(estado):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if estado[a] and estado[a] == estado[b] == estado[c]:
            return estado[a]

    return None

def actualizar_estado():    
    ganador = obtener_ganador(tablero)

    if ganador == HUMANO:
        finalizar_partida("¡Ganaste!")
        return True

    if ganador == AGENTE:
        finalizar_partida("Perdiste. El agente ha ganado.")
        return True

    if "" not in tablero:
        finalizar_partida("¡Empate!")
        return True

    return False


def finalizar_partida(mensaje):
    global partida_terminada
    partida_terminada = True
    estado_label.config(text=mensaje)

    # Desactivar las casillas al terminar.
    for boton in botones:
        boton.config(state="disabled")

    messagebox.showinfo("Fin de la partida", mensaje)

# TURNO DEL AGENTE

def turno_agente():
    global turno_pendiente
    turno_pendiente = None

    if partida_terminada:
        return

    # La IA selecciona una jugada según la dificultad elegida.
    posicion = elegir_jugada(tablero.copy(), dificultad.get())

    # Comprobar que la jugada sea válida.
    if (
        posicion is None
        or not isinstance(posicion, int)
        or posicion < 0
        or posicion >= 9
        or tablero[posicion] != ""
    ):
        messagebox.showerror(
            "Error del agente",
            "La IA no pudo seleccionar una casilla válida."
        )
        return

    tablero[posicion] = AGENTE

    botones[posicion].config(
        text=AGENTE,
        fg=ROJO,
        state="disabled"
    )

    if not actualizar_estado():
        estado_label.config(text="Tu turno: coloca una X")


# TURNO DEL JUGADOR

def jugar(posicion):
    global turno_pendiente

    if partida_terminada or tablero[posicion] != "":
        return

    tablero[posicion] = HUMANO

    botones[posicion].config(
        text=HUMANO,
        fg=AZUL,
        state="disabled"
    )

    if not actualizar_estado():
        estado_label.config(text="Turno del agente...")

        # Evita programar más de un turno del agente.
        turno_pendiente = ventana.after(400, turno_agente)



# REINICIAR PARTIDA

def reiniciar():
    global tablero, partida_terminada, turno_pendiente

    # Cancelar el turno pendiente para evitar movimientos tardíos.
    if turno_pendiente is not None:
        ventana.after_cancel(turno_pendiente)
        turno_pendiente = None

    tablero = [""] * 9
    partida_terminada = False

    for boton in botones:
        boton.config(
            text="",
            state="normal",
            bg=CASILLA,
            fg=TEXTO,
            activebackground=CASILLA_HOVER
        )

    estado_label.config(
        text="Tu turno: coloca una X",
        fg=AZUL
    )



# INTERFAZ GRÁFICA

ventana = tk.Tk()
ventana.title("Agente Inteligente - Gato")
ventana.configure(bg=FONDO)

# Tamaño compacto para que el botón quede visible.
ANCHO = 420
ALTO = 590

ventana.geometry(f"{ANCHO}x{ALTO}")
ventana.resizable(False, False)

# Centrar la ventana en la pantalla.
ventana.update_idletasks()
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

x = max(0, (ancho_pantalla - ANCHO) // 2)
y = max(0, (alto_pantalla - ALTO) // 2)

ventana.geometry(f"{ANCHO}x{ALTO}+{x}+{y}")



# ENCABEZADO

titulo = tk.Label(
    ventana,
    text="Gato",
    font=("Arial", 23, "bold"),
    bg=FONDO,
    fg=TEXTO
)
titulo.pack(pady=(15, 3))

subtitulo = tk.Label(
    ventana,
    text="Humano (X) vs. Agente (O)",
    font=("Arial", 11),
    bg=FONDO,
    fg="#CBD5E1"
)
subtitulo.pack(pady=3)

estado_label = tk.Label(
    ventana,
    text="Tu turno: coloca una X",
    font=("Arial", 11, "bold"),
    bg=FONDO,
    fg=AZUL
)
estado_label.pack(pady=10)



# TABLERO 3 X 3

marco_tablero = tk.Frame(
    ventana,
    bg=FONDO
)
marco_tablero.pack(pady=5)

for fila in range(3):
    for columna in range(3):
        posicion = fila * 3 + columna

        boton = tk.Button(
            marco_tablero,
            text="",
            font=("Arial", 26, "bold"),
            width=4,
            height=1,
            bg=CASILLA,
            fg=TEXTO,
            activebackground=CASILLA_HOVER,
            relief="flat",
            cursor="hand2",
            command=lambda p=posicion: jugar(p)
        )

        boton.grid(
            row=fila,
            column=columna,
            padx=4,
            pady=4,
            ipadx=4,
            ipady=5
        )

        botones.append(boton)



# BOTÓN DE REINICIO

boton_reiniciar = tk.Button(
    ventana,
    text="Reiniciar partida",
    font=("Arial", 12, "bold"),
    bg=AZUL,
    fg=FONDO,
    activebackground="#7DD3FC",
    relief="flat",
    cursor="hand2",
    command=reiniciar
)

boton_reiniciar.pack(
    side="bottom",
    pady=18,
    ipadx=12,
    ipady=5
)


# Iniciar aplicación
ventana.mainloop()

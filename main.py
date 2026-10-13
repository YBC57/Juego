import tkinter as tk
from tkinter import messagebox
from agente import elegir_jugada


# CONFIGURACIÓN
FONDO = "#172033"
TEXTO = "#F8FAFC"
AZUL = "#38BDF8"
ROJO = "#FB7185"
CASILLA = "#263449"
CASILLA_HOVER = "#3B4D66"
VERDE = "#34D399"

HUMANO = "X"
AGENTE = "O"

tablero = [""] * 9
botones = []
partida_terminada = False
turno_pendiente = None

victorias = 0
derrotas = 0
empates = 0


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Agente Inteligente - Gato")
ventana.configure(bg=FONDO)

ANCHO = 440
ALTO = 680
ventana.geometry(f"{ANCHO}x{ALTO}")
ventana.resizable(False, False)

ventana.update_idletasks()
x = max(0, (ventana.winfo_screenwidth() - ANCHO) // 2)
y = max(0, (ventana.winfo_screenheight() - ALTO) // 2)
ventana.geometry(f"{ANCHO}x{ALTO}+{x}+{y}")


# FUNCIONES DEL JUEGO
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


def actualizar_marcador():
    marcador_label.config(
        text=f"Victorias: {victorias}    "
             f"Derrotas: {derrotas}    "
             f"Empates: {empates}"
    )


def finalizar_partida(mensaje, resultado):
    global partida_terminada, victorias, derrotas, empates

    if partida_terminada:
        return

    partida_terminada = True

    for boton in botones:
        boton.config(state="disabled")

    if resultado == "victoria":
        victorias += 1
    elif resultado == "derrota":
        derrotas += 1
    elif resultado == "empate":
        empates += 1

    actualizar_marcador()
    estado_label.config(text=mensaje)
    messagebox.showinfo("Resultado de la partida", mensaje)


def actualizar_estado():
    ganador = obtener_ganador(tablero)

    if ganador == HUMANO:
        finalizar_partida("🏆 ¡Ganaste!", "victoria")
        return True
    if ganador == AGENTE:
        finalizar_partida("😿 Perdiste. El agente ha ganado.", "derrota")
        return True
    if "" not in tablero:
        finalizar_partida("🤝 ¡Empate!", "empate")
        return True
    return False


# TURNO DEL AGENTE
def turno_agente():
    global turno_pendiente
    turno_pendiente = None

    if partida_terminada:
        return

    posicion = elegir_jugada(tablero.copy(), dificultad.get())

    if (
        posicion is None
        or not isinstance(posicion, int)
        or not 0 <= posicion < 9
        or tablero[posicion] != ""
    ):
        messagebox.showerror(
            "Error del agente",
            "La IA no pudo seleccionar una casilla válida."
        )
        estado_label.config(text="Error al realizar la jugada.")
        return

    tablero[posicion] = AGENTE
    botones[posicion].config(text=AGENTE, fg=ROJO, state="disabled")

    if not actualizar_estado():
        estado_label.config(text="Tu turno: coloca una X")


# TURNO DEL JUGADOR
def jugar(posicion):
    global turno_pendiente

    if partida_terminada or tablero[posicion] != "":
        return

    tablero[posicion] = HUMANO
    botones[posicion].config(text=HUMANO, fg=AZUL, state="disabled")

    if not actualizar_estado():
        estado_label.config(text="Turno del agente...")
        turno_pendiente = ventana.after(400, turno_agente)


# REINICIAR PARTIDA
def reiniciar():
    global tablero, partida_terminada, turno_pendiente

    if turno_pendiente is not None:
        try:
            ventana.after_cancel(turno_pendiente)
        except tk.TclError:
            pass
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

    estado_label.config(text="Tu turno: coloca una X", fg=AZUL)


# NAVEGACIÓN ENTRE PANTALLAS
def mostrar_menu():
    global turno_pendiente

    if turno_pendiente is not None:
        try:
            ventana.after_cancel(turno_pendiente)
        except tk.TclError:
            pass
        turno_pendiente = None

    pantalla_juego.pack_forget()
    pantalla_menu.pack(fill="both", expand=True)


def iniciar_partida():
    reiniciar()
    pantalla_menu.pack_forget()
    pantalla_juego.pack(fill="both", expand=True)


def salir():
    if messagebox.askyesno("Salir del juego", "¿Seguro que deseas salir?"):
        ventana.destroy()


def mostrar_reglas():
    mensaje = (
        "REGLAS DE TRES EN RAYA\n\n"
        "1. El tablero tiene 3 filas y 3 columnas.\n\n"
        "2. Tú juegas con X y el agente con O.\n\n"
        "3. Los turnos se realizan de manera alternada.\n\n"
        "4. No puedes ocupar una casilla que ya esté utilizada.\n\n"
        "5. Gana quien consiga tres fichas iguales en una fila, "
        "columna o diagonal.\n\n"
        "6. Si se llenan las nueve casillas sin un ganador, "
        "la partida termina en empate."
    )
    messagebox.showinfo("Reglas del juego", mensaje)


# PANTALLA DEL MENÚ PRINCIPAL
pantalla_menu = tk.Frame(ventana, bg=FONDO)

titulo_menu = tk.Label(
    pantalla_menu, text="🐱 GATO",
    font=("Segoe UI Emoji", 27, "bold"), bg=FONDO, fg=TEXTO
)
titulo_menu.pack(pady=(65, 8))

subtitulo_menu = tk.Label(
    pantalla_menu, text="PROYECTO DE AGENTES INTELIGENTES",
    font=("Arial", 10, "bold"), bg=FONDO, fg=AZUL
)
subtitulo_menu.pack(pady=(0, 20))

descripcion = tk.Label(
    pantalla_menu, text="Humano (X) contra Agente (O)",
    font=("Arial", 12), bg=FONDO, fg="#CBD5E1"
)
descripcion.pack(pady=8)

etiqueta_dificultad = tk.Label(
    pantalla_menu, text="Selecciona la dificultad:",
    font=("Arial", 12, "bold"), bg=FONDO, fg=TEXTO
)
etiqueta_dificultad.pack(pady=(20, 8))

dificultad = tk.StringVar(value="Medio")

selector_dificultad = tk.OptionMenu(
    pantalla_menu, dificultad, "Fácil", "Medio", "Difícil"
)
selector_dificultad.config(
    font=("Arial", 12), bg=CASILLA, fg=TEXTO,
    activebackground=CASILLA_HOVER, activeforeground=TEXTO,
    relief="flat", highlightthickness=0, width=15, cursor="hand2"
)
selector_dificultad["menu"].config(
    font=("Arial", 11), bg=CASILLA, fg=TEXTO
)
selector_dificultad.pack(pady=5)

boton_jugar = tk.Button(
    pantalla_menu, text="▶  JUGAR", font=("Segoe UI Emoji", 14, "bold"),
    bg=AZUL, fg=FONDO, activebackground="#7DD3FC",
    relief="flat", cursor="hand2", command=iniciar_partida, width=17
)
boton_jugar.pack(pady=(28, 10), ipady=6)

# BOTÓN NUEVO: REGLAS DEL JUEGO
boton_reglas = tk.Button(
    pantalla_menu, text="📖  Reglas del juego", font=("Segoe UI Emoji", 11),
    bg=CASILLA, fg=TEXTO, activebackground=CASILLA_HOVER,
    relief="flat", cursor="hand2", command=mostrar_reglas, width=17
)
boton_reglas.pack(pady=5, ipady=4)

boton_salir = tk.Button(
    pantalla_menu, text="🚪  Salir", font=("Segoe UI Emoji", 11),
    bg=CASILLA, fg=TEXTO, activebackground=CASILLA_HOVER,
    relief="flat", cursor="hand2", command=salir, width=17
)
boton_salir.pack(pady=5, ipady=4)

pie_menu = tk.Label(
    pantalla_menu, text="Selecciona una dificultad y comienza a jugar",
    font=("Arial", 9), bg=FONDO, fg="#94A3B8"
)
pie_menu.pack(side="bottom", pady=20)


# PANTALLA DEL JUEGO
pantalla_juego = tk.Frame(ventana, bg=FONDO)

titulo_juego = tk.Label(
    pantalla_juego, text="🐱 GATO",
    font=("Segoe UI Emoji", 23, "bold"), bg=FONDO, fg=TEXTO
)
titulo_juego.pack(pady=(22, 4))

subtitulo_juego = tk.Label(
    pantalla_juego, text="Humano (X) vs. Agente (O)",
    font=("Arial", 11), bg=FONDO, fg="#CBD5E1"
)
subtitulo_juego.pack(pady=3)

dificultad_juego_label = tk.Label(
    pantalla_juego, text="Dificultad: Medio",
    font=("Arial", 10, "bold"), bg=FONDO, fg=VERDE
)
dificultad_juego_label.pack(pady=5)


def actualizar_dificultad_juego(*args):
    dificultad_juego_label.config(text=f"Dificultad: {dificultad.get()}")


dificultad.trace_add("write", actualizar_dificultad_juego)

estado_label = tk.Label(
    pantalla_juego, text="Tu turno: coloca una X",
    font=("Arial", 11, "bold"), bg=FONDO, fg=AZUL
)
estado_label.pack(pady=8)

marcador_label = tk.Label(
    pantalla_juego, text="Victorias: 0    Derrotas: 0    Empates: 0",
    font=("Arial", 10, "bold"), bg=FONDO, fg=TEXTO
)
marcador_label.pack(pady=5)

marco_tablero = tk.Frame(pantalla_juego, bg=FONDO)
marco_tablero.pack(pady=12)

for fila in range(3):
    for columna in range(3):
        posicion = fila * 3 + columna
        boton = tk.Button(
            marco_tablero, text="", font=("Arial", 26, "bold"),
            width=4, height=1, bg=CASILLA, fg=TEXTO,
            activebackground=CASILLA_HOVER, relief="flat",
            cursor="hand2", command=lambda p=posicion: jugar(p)
        )
        boton.grid(row=fila, column=columna, padx=4, pady=4, ipadx=4, ipady=5)
        botones.append(boton)

boton_reiniciar = tk.Button(
    pantalla_juego, text="🔄  Reiniciar partida",
    font=("Segoe UI Emoji", 11, "bold"), bg=AZUL, fg=FONDO,
    activebackground="#7DD3FC", relief="flat", cursor="hand2",
    command=reiniciar
)
boton_reiniciar.pack(pady=(12, 7), ipadx=10, ipady=4)

boton_menu = tk.Button(
    pantalla_juego, text="🏠  Volver al menú", font=("Segoe UI Emoji", 10),
    bg=CASILLA, fg=TEXTO, activebackground=CASILLA_HOVER,
    relief="flat", cursor="hand2", command=mostrar_menu
)
boton_menu.pack(pady=5, ipadx=10, ipady=3)


# INICIAR APLICACIÓN
actualizar_marcador()
pantalla_menu.pack(fill="both", expand=True)
ventana.mainloop()

import random

HUMANO = "X"
AGENTE = "O"


def obtener_ganador(tablero):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if (
            tablero[a]
            and tablero[a] == tablero[b]
            and tablero[b] == tablero[c]
        ):
            return tablero[a]

    return None


def buscar_jugada_ganadora(tablero, ficha):
    """Busca una jugada que permita ganar o bloquear al rival."""
    for posicion in range(9):
        if tablero[posicion] == "":
            tablero[posicion] = ficha
            ganador = obtener_ganador(tablero)
            tablero[posicion] = ""

            if ganador == ficha:
                return posicion

    return None


def agente_facil(tablero):
    """Elige una casilla vacía al azar."""
    disponibles = [
        i for i in range(9) if tablero[i] == ""
    ]

    return random.choice(disponibles) if disponibles else None


def agente_medio(tablero):
    """Prioriza ganar, bloquear y ocupar posiciones estratégicas."""
    # 1. Si puede ganar, gana.
    posicion = buscar_jugada_ganadora(tablero, AGENTE)
    if posicion is not None:
        return posicion

    # 2. Si el humano puede ganar, bloquea.
    posicion = buscar_jugada_ganadora(tablero, HUMANO)
    if posicion is not None:
        return posicion

    # 3. Prefiere el centro.
    if tablero[4] == "":
        return 4

    # 4. Después intenta ocupar una esquina.
    esquinas = [
        i for i in (0, 2, 6, 8) if tablero[i] == ""
    ]
    if esquinas:
        return random.choice(esquinas)

    # 5. Si no hay opciones estratégicas, elige al azar.
    return agente_facil(tablero)



def minimax(tablero, maximizando, profundidad=0):
    """Evalúa resultados y prioriza las victorias más rápidas."""

    ganador = obtener_ganador(tablero)

    if ganador == AGENTE:
        return 10 - profundidad

    if ganador == HUMANO:
        return profundidad - 10

    if "" not in tablero:
        return 0

    if maximizando:
        mejor_puntuacion = -float("inf")

        for posicion in range(9):
            if tablero[posicion] == "":
                tablero[posicion] = AGENTE
                puntuacion = minimax(
                    tablero, False, profundidad + 1
                )
                tablero[posicion] = ""

                mejor_puntuacion = max(
                    mejor_puntuacion, puntuacion
                )

        return mejor_puntuacion

    mejor_puntuacion = float("inf")

    for posicion in range(9):
        if tablero[posicion] == "":
            tablero[posicion] = HUMANO
            puntuacion = minimax(
                tablero, True, profundidad + 1
            )
            tablero[posicion] = ""

            mejor_puntuacion = min(
                mejor_puntuacion, puntuacion
            )

    return mejor_puntuacion


def agente_dificil(tablero):
    """Selecciona la mejor jugada mediante Minimax."""
    mejor_puntuacion = -float("inf")
    mejor_posicion = None

    for posicion in range(9):
        if tablero[posicion] == "":
            tablero[posicion] = AGENTE
            puntuacion = minimax(tablero, False, 1)
            tablero[posicion] = ""

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_posicion = posicion

    return mejor_posicion


def elegir_jugada(tablero, dificultad):
    """Selecciona la estrategia según la dificultad."""
    if dificultad == "Fácil":
        return agente_facil(tablero)

    if dificultad == "Medio":
        return agente_medio(tablero)

    return agente_dificil(tablero)
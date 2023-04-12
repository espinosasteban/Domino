from logica.jugador import Jugador


class Rival(Jugador):
    def __init__(self, nombre, fichas):
        super().__init__(nombre, fichas)
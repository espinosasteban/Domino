from collections import deque
from random import sample
from logica.ficha import Ficha
from logica.jugador import Jugador
from logica.rival import Rival
import pygame
import os

class Tablero:
    _jugadores = []
    _tablero = deque([])

    def __init__(self):
        pass

    @classmethod
    def generar_fichas(cls):
        fichas_totales = []
        for i in range(0, 7):
            for j in range(i, 7):
                ruta = os.path.join(os.getcwd(), 'parteGrafica', 'imagenes')
                fichas_totales.append(Ficha(i,j,pygame.image.load(os.path.join(ruta, f"ficha_{i}_{j}.png"))))

        for p in range(4):
            mano = sample(fichas_totales, 7) #Evita la repeticion de elementos
            if p == 0:
                cls._jugadores.append(Jugador("Principal", deque(mano)))
            else:
                cls._jugadores.append(Rival(f"Rival{p}", deque(mano)))
            for elemento in mano:
                fichas_totales.remove(elemento)

    @classmethod
    def getJugadores(cls)-> list:
        return cls._jugadores

    @classmethod
    def encontrarSaque(cls) -> Jugador:
        for jugador in cls._jugadores:
            for ficha_jugador in jugador.getFichas():
                tupla_valores = ficha_jugador.getValores()
                if sum(tupla_valores) == 12:
                    return jugador

    def verEstado(self):
        for jugador in self._jugadores:
            print(f"{jugador.getNombre()}")
            for ficha in jugador.getFichas():
                print(ficha.getValores())
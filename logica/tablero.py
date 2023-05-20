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
                fichas_totales.append(Ficha(i, j, pygame.image.load(os.path.join(ruta, f"ficha_{i}_{j}.png"))))

        for p in range(4):
            mano = sample(fichas_totales, 7)  # Evita la repeticion de elementos
            if p == 0:
                cls._jugadores.append(Jugador("Principal", deque(mano)))
            else:
                cls._jugadores.append(Rival(f"Rival{p}", deque(mano)))
            for elemento in mano:
                fichas_totales.remove(elemento)

    @classmethod
    def getJugadores(cls) -> list:
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

    def getGanadorPorPuntaje(self) -> Jugador:
        ganador = self._jugadores[0]
        for jugador in self._jugadores[1:]:
            puntaje_jugador = jugador.calcularPuntos()
            if puntaje_jugador < ganador.calcularPuntos():
                ganador = jugador
        return ganador

    @classmethod
    def generarPartidaPrueba(cls):
        ruta = os.path.join(os.getcwd(), 'parteGrafica', 'imagenes')
        fichaR1 = Ficha(6,6, pygame.image.load(os.path.join(ruta, f"ficha_{6}_{6}.png")))
        ficha2R1 = Ficha(3,0, pygame.image.load(os.path.join(ruta, f"ficha_{3}_{0}.png")))

        fichaR2 = Ficha(6, 1, pygame.image.load(os.path.join(ruta, f"ficha_{6}_{1}.png")))
        ficha2R2 = Ficha(3,3, pygame.image.load(os.path.join(ruta, f"ficha_{3}_{3}.png")))
        #cls._jugadores.append(Jugador("Principal",[fichaR1 fichaR2]))

        #fichaR1 = Ficha(5,4, pygame.image.load(os.path.join(ruta, f"ficha_{5}_{4}.png")))
        #fichaR2 = Ficha(3, 4, pygame.image.load(os.path.join(ruta, f"ficha_{3}_{4}.png")))
        fichaR3 = Ficha(2, 6, pygame.image.load(os.path.join(ruta, f"ficha_{2}_{6}.png")))
        ficha2R3 = Ficha(3,4, pygame.image.load(os.path.join(ruta, f"ficha_{3}_{4}.png")))

        fichaP1 = Ficha(1,1, pygame.image.load(os.path.join(ruta, f"ficha_{1}_{1}.png")))
        fichaP2 = Ficha(2,2, pygame.image.load(os.path.join(ruta, f"ficha_{2}_{2}.png")))

        cls._jugadores.append(Jugador("Principal", [fichaP1, fichaP2]))
        for i, ficha in enumerate([(fichaR1,ficha2R1), (fichaR2,ficha2R2), (fichaR3,ficha2R3)]):
            cls._jugadores.append(Rival(f"Rival{i+1}", [ficha[0], ficha[1]]))

    @classmethod
    def generarPartidaPrueba2(cls):
        ruta = os.path.join(os.getcwd(), 'parteGrafica', 'imagenes')
        fichaP = Ficha(6, 6, pygame.image.load(os.path.join(ruta, f"ficha_{6}_{6}.png")))

        fichaP2 = Ficha(0, 0, pygame.image.load(os.path.join(ruta, f"ficha_{0}_{0}.png")))
        cls._jugadores.append(Jugador("Principal", [fichaP, fichaP2]))

        fichaR1 = Ficha(5, 4, pygame.image.load(os.path.join(ruta, f"ficha_{5}_{4}.png")))
        fichaR2 = Ficha(3, 4, pygame.image.load(os.path.join(ruta, f"ficha_{3}_{4}.png")))
        fichaR3 = Ficha(1, 5, pygame.image.load(os.path.join(ruta, f"ficha_{1}_{1}.png")))

        for i, ficha in enumerate([fichaR1, fichaR2, fichaR3]):
            cls._jugadores.append(Rival(f"Rival{i + 1}", [ficha]))









import os
from logica.ficha import Ficha
from logica.tablero import Tablero

import pygame


class GameDisplay:


    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

        # Inicializar Pygame
        pygame.init()

        # Crear la ventana del juego
        self.screen = pygame.display.set_mode((ancho, alto))

        # Establecer el título de la ventana
        pygame.display.set_caption("Mi Juego")

        # Establecer el color de fondo de la ventana
        self.background_color = (0, 128, 10)

        # Establecer el estado de la ventana a "abierto"
        self.is_running = True


    def ponerFichaTablero(self, ficha: Ficha):
        self.screen.blit(ficha.getImagen(), (self.ancho/2, self.alto/2))



    def run(self):
        # Ciclo principal del juego
        tablero = Tablero()
        tablero.generar_fichas()
        jugador_saque = tablero.encontrarSaque()




        while self.is_running:
            # Procesar eventos
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False

            # Dibujar el fondo
            self.screen.fill(self.background_color)
            self.ponerFichaTablero(jugador_saque.buscarFicha(6,6))




            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.quit()

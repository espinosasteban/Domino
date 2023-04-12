import os

import pygame


class GameDisplay:


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

        # Inicializar Pygame
        pygame.init()

        # Crear la ventana del juego
        self.screen = pygame.display.set_mode((width, height))

        # Establecer el título de la ventana
        pygame.display.set_caption("Mi Juego")

        # Establecer el color de fondo de la ventana
        self.background_color = (0, 128, 10)

        # Establecer el estado de la ventana a "abierto"
        self.is_running = True

    def run(self):
        # Ciclo principal del juego
        while self.is_running:
            # Procesar eventos
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False

            # Dibujar el fondo
            self.screen.fill(self.background_color)

            ancho_total_fichas = (128 * 7)

            # Calcula la posición del primer sprite
            posicion_x = (self.width - ancho_total_fichas) / 2


            posicion_y = 700
            separacion = 10


            fichas = [pygame.image.load(os.path.join(self.ruta_imagenes, f"ficha_{i}_1.png")) for i in range(7)]
            for ficha in fichas:
                ficha_rotada = pygame.transform.rotate(ficha, 90)

                self.screen.blit(ficha_rotada, (posicion_x, posicion_y))
                posicion_x += 128 + separacion













                # Actualiza la posición x para la siguiente ficha


            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.quit()

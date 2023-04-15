import os
from collections import deque


import pygame


class GameDisplay:

    def ponerFicha(self, tablero_fisico: deque, imagen_ficha, lado):

        #se transforma la imagen para que sea de menor tamaño
        ficha_transformada = pygame.transform.scale(imagen_ficha, (int(imagen_ficha.get_width() / 4), int(imagen_ficha.get_height() / 4)))
        if len(tablero_fisico) == 0:
            #si el tablero está vacío, se coloca en el centro
            print("hola1")

            #se muestra en el tablero en unas coordenadas que más o menos sea la mitad
            #(el centrado lo hice con prueba y error)
            self.screen.blit(ficha_transformada, (int(self.ancho/2)-ficha_transformada.get_width(),int(self.alto/2)-150))

            tablero_fisico.append((ficha_transformada,(int(self.ancho/2)-ficha_transformada.get_width(),int(self.alto/2)-150)))
            #y se agrega a tablero físico de la siguiente forma: (imagen de la ficha transformada, (posicion_x, posicion_y)
            #esto con el objetivo de que después sea fácil obtener las coordenadas de dónde está la ficha dibujada.
            pygame.display.update()

        else:
            #si ya hay una ficha en el tablero, entonces:

            #si la quiero poner a la derecha entonces mi ficha "anterior" es la ficha [-1] en el deque porque está
            #a la derecha del todo
            if lado == "derecho":
                print("derecho")

                ficha_derecha = tablero_fisico[-1]
                x_anterior, y_anterior = ficha_derecha[1] # se obtiene la tupla con las coordenadas
                print(x_anterior, y_anterior)



                self.screen.blit(ficha_transformada, (x_anterior+int((270/4)),y_anterior)) # se dibuja la nueva ficha
                #para dibujar en x, tengo que correrla el ancho de la ficha anterior (256/4) y sumarle el x de la anterior.
                #coloco + 270 para darle un poco de espacio y que no esté tan pegada.
                tablero_fisico.append((ficha_transformada, (x_anterior+int((270/4)), y_anterior)))
                #se agrega la ficha

                pygame.display.update()

            if lado == "izquierdo":
                #misma lógica que antes pero acá la ficha de la izquierda del deque es la [0]
                print("izquierdo")
                ficha_derecha = tablero_fisico[0]
                x_anterior, y_anterior = ficha_derecha[1]


                self.screen.blit(ficha_transformada, (x_anterior - int((270 / 4)), y_anterior))
                #acá en lugar de sumar hay que restar en x.

                tablero_fisico.appendleft((ficha_transformada, (x_anterior - int((270 / 4)), y_anterior)))
                #IMPORTANTE: se agrega la ficha al inicio
                pygame.display.update()


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

    def run(self):
        tablero_fisico = deque()  # tablero que representa el juego (físicamente)

        # generación de fichas (PRUEBA)
        fichas = [pygame.image.load(os.path.join(self.ruta_imagenes, f"ficha_{i}_{j}.png")) for i in range(7) for j in
                  range(i, 7)]

        # GENERACIÓN  DE BOTONES PARA PRUEBAS
        boton_superficie = pygame.Surface((100, 50))
        boton_superficie.fill((255, 255, 255))  # Establecer el color del botón

        # Crear el rectángulo del botón derecho
        boton_rect = boton_superficie.get_rect()
        boton_rect.x = 40  # Establecer la coordenada x del botón
        boton_rect.y = 40  # Establecer la coordenada y del botón
        self.screen.fill(self.background_color)
        self.screen.blit(boton_superficie, boton_rect)
        pygame.display.update()

        # crear el rectangulo del botón izquierdo

        boton_superficie_izq = pygame.Surface((100, 50))
        boton_superficie_izq.fill((255, 255, 255))

        boton_rect_izq = boton_superficie_izq.get_rect()
        boton_rect_izq.x = 40 + 110  # Establecer la coordenada x del botón
        boton_rect_izq.y = 40  # Establecer la coordenada y del botón

        self.screen.blit(boton_superficie_izq, boton_rect_izq)
        pygame.display.update()

        # generación de fichas POV jugador
        ancho_total_fichas = (128 * 7)
        posicion_x = (self.ancho - ancho_total_fichas) / 2

        posicion_y = 700
        separacion = 10
        for j in range(0, 7):
            ficha_rotada = pygame.transform.rotate(fichas[j], 90)

            self.screen.blit(ficha_rotada, (posicion_x, posicion_y))
            posicion_x += 128 + separacion
            fichas.remove(fichas[j])

        # Ciclo principal del juego
        while self.is_running:

            # Procesar eventos
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False

                # si le doy click al boton de la izquierda, entonces ponerficha a la izquierda
                elif event.type == pygame.MOUSEBUTTONDOWN and boton_rect.collidepoint(event.pos):
                    self.ponerFicha(tablero_fisico, fichas[0], "izquierdo")
                    fichas.remove(fichas[0])

                # si le doy click al boton de la derecha, entonces ponerficha a la derecha
                elif event.type == pygame.MOUSEBUTTONDOWN and boton_rect_izq.collidepoint(event.pos):
                    self.ponerFicha(tablero_fisico, fichas[0], "derecho")
                    fichas.remove(fichas[0])

            # Dibujar el fondo

            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.quit()

import os
from collections import deque
from logica.tablero import Tablero
from random import randint
from logica.jugador import Jugador
from logica.rival import Rival

import pygame


class GameDisplay:

    def ponerFicha(self, tablero_fisico: deque, imagen_ficha, lado):

        #se transforma la imagen para que sea de menor tamaño
        ficha_transformada = pygame.transform.scale(imagen_ficha, (int(imagen_ficha.get_width() / 4), int(imagen_ficha.get_height() / 4)))
        if len(tablero_fisico) == 0:
            #si el tablero está vacío, se coloca en el centro


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
        tablero_logico = deque() #tablero que representa el juego (logicamente)

        # generación de fichas (PRUEBA)
        partida = Tablero()
        partida.generar_fichas()




        jugador_saque = partida.encontrarSaque()

        ficha_saque = jugador_saque.buscarFicha(6,6)
        jugador_saque.eliminarFicha(ficha_saque)

        jugador_principal = partida.getJugadores()[0]


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

        # generación de fichas POV jugador
        def generar_pov_jugador(fichas_jugador_principal):

            ancho_total_fichas = (128 * 7)
            posicion_x = (self.ancho - ancho_total_fichas) / 2

            posicion_y = 700
            separacion = 10
            fondo = pygame.Surface((ancho_total_fichas+128, 256))
            fondo.fill((0, 100, 10))
            self.screen.blit(fondo, (posicion_x, posicion_y))

            for j in range(0, len(fichas_jugador_principal)):
                print(j)
                ficha_rotada = pygame.transform.rotate(fichas_jugador_principal[j].getImagen(), 90)

                self.screen.blit(ficha_rotada, (posicion_x, posicion_y))
                posicion_x += 128 + separacion

        # Ciclo principal del juego

        self.ponerFicha(tablero_fisico, ficha_saque.getImagen(), "derecho")
        tablero_logico.append(ficha_saque)
        generar_pov_jugador(jugador_principal.getFichas())


        while self.is_running:
            fichas_validas = jugador_principal.determinarFichasValidas(tablero_logico)
            print(len(fichas_validas))
            if len(fichas_validas) > 0:
                datos_ficha = fichas_validas[randint(0,len(fichas_validas)-1)]
            

            for ficha_logica in tablero_logico:
                print(ficha_logica.getValores())

            # Procesar eventos
            for event in pygame.event.get():
                lado = []
                if len(fichas_validas) > 0:
                    tupla_condicion = datos_ficha[1]
                    if tupla_condicion[0]:
                        lado.append("izquierdo")
                    if tupla_condicion[1]:
                        lado.append("derecho")
                    print(lado)
                

                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False

                # si le doy click al boton de la izquierda, entonces ponerficha a la izquierda
                elif event.type == pygame.MOUSEBUTTONDOWN and boton_rect.collidepoint(event.pos):
                    
                    
                    if len(fichas_validas) > 0:
                        mi_ficha = datos_ficha[0]
                        lado_str = lado[randint(0,len(lado)-1)]
                        if lado_str == "derecho":
                            if mi_ficha.getValores()[0] != tablero_logico[-1].getValores()[-1]:
                                mi_ficha.voltearFicha()
                            self.ponerFicha(tablero_fisico, mi_ficha.getImagen(), "derecho" )
                            tablero_logico.append(mi_ficha)


                        
                        elif lado_str == "izquierdo":
                            if mi_ficha.getValores()[-1] != tablero_logico[0].getValores()[0]:
                                mi_ficha.voltearFicha()

                            self.ponerFicha(tablero_fisico, mi_ficha.getImagen(), "izquierdo")
                            tablero_logico.appendleft(mi_ficha)

                        
                        jugador_principal.getFichas().remove(mi_ficha)
                        generar_pov_jugador(jugador_principal.getFichas())




            # Dibujar el fondo

            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.quit()

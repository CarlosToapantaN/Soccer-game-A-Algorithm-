import pygame
import math
from queue import PriorityQueue
from random import randint

blanco = (255, 255, 255)
negro = (0, 0, 0)
gris = (128, 128, 128)
rojo = (255, 0, 0)
turquesa = (0, 171 ,169)
magenta = (216, 0, 115)
amarillo = (255, 255, 0)
naranja = (240, 163, 10)
azul = (0, 80, 239)
rosa = (244, 114, 208)
verde = (0, 255, 0)

class Lugar:
    def __init__(self,fila,columna,ancho,alto,total_filas,total_columnas):
        self.fila = fila
        self.columna = columna
        self.x = columna * ancho
        self.y = fila * alto
        self.color = blanco
        self.ancho = ancho
        self.alto = alto
        self.total_filas = total_filas
        self.total_columnas = total_columnas
        self.juntos = []
    
    def get_posicion(self):
        return self.fila, self.columna

    def esta_cerrado(self):
        return self.color == gris

    def esta_abierto(self):
        return self.color == amarillo
    
    def es_obstaculo(self):
        return self.color == magenta or self.color == azul or self.color == verde

    def es_inicio(self):
        return self.color == rojo
    
    def es_final(self):
        return self.color == negro
    
    def ubicar_jugador1(self):
        self.color = turquesa
    
    def ubicar_jugador2(self):
        self.color = magenta
    
    def ubicar_porteria(self):
        self.color = verde
    
    def borrar(self):
        self.color = blanco
    
    def cerrar(self):
        self.color = gris
    
    def abrir(self):
        self.color = amarillo
    
    def hacer_obstaculo(self):
        self.color = azul
    
    def hacer_inicio(self):
        self.color = rojo

    def hacer_final(self):
        self.color = negro
    
    def hacer_camino(self):
        self.color = naranja

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.alto))
        pass
    
    def actualizar_juntos(self, cuadricula):
        self.juntos = []
        if self.fila < self.total_filas - 1 and not cuadricula[self.fila + 1][self.columna].es_obstaculo():
            self.juntos.append(cuadricula[self.fila + 1][self.columna])

        if self.fila > 0 and not cuadricula[self.fila - 1][self.columna].es_obstaculo():
            self.juntos.append(cuadricula[self.fila - 1][self.columna])

        if self.columna < self.total_columnas - 1 and not cuadricula[self.fila][self.columna + 1].es_obstaculo():
            self.juntos.append(cuadricula[self.fila][self.columna + 1])

        if self.columna > 0 and not cuadricula[self.fila][self.columna - 1].es_obstaculo():
            self.juntos.append(cuadricula[self.fila][self.columna - 1])

    def __lt__(self, other):
        return False

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def algoritmo(graficar, cuadricula, inicio, final):
    i = 0
    conjunto = PriorityQueue()
    conjunto.put((0, i, inicio))
    origen = {}
    g = {lugar: float("inf") for fila in cuadricula for lugar in fila}
    g[inicio]= 0
    f = {lugar: float("inf") for fila in cuadricula for lugar in fila}
    f[inicio] = h(inicio.get_posicion(), final.get_posicion())

    conjunto_hash = {inicio}
    
    while not conjunto.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        actual = conjunto.get()[2]
        conjunto_hash.remove(actual)

        if actual == final:
            formar_camino(origen,final,graficar)
            final.hacer_final()
            return True

        for junto in actual.juntos:
            g_temporal = g[actual] +1

            if g_temporal < g[junto]:
                origen[junto] = actual
                g[junto] = g_temporal
                f[junto] = g_temporal + h(junto.get_posicion(), final.get_posicion())

                if junto not in conjunto_hash:
                    i += 1
                    conjunto.put((f[junto], i, junto))
                    conjunto_hash.add(junto)
                    junto.abrir()
        
        graficar()

        if actual != inicio:
            actual.cerrar()
        
def formar_camino(origen, actual, graficar):
    while actual in origen:
        actual = origen[actual]
        actual.hacer_camino()
        graficar()

def lineas_cuadricula(ventana, filas, columnas, ancho, alto):
    espacio_horizontal = ancho // columnas
    espacio_vertical = alto // filas
    for i in range(filas):
        pygame.draw.line(ventana, negro, (0, i * espacio_vertical), (ancho, i * espacio_vertical))
        for j in range(columnas):
            pygame.draw.line(ventana, negro, (j * espacio_horizontal, 0), (j * espacio_horizontal, alto))

def hacer_cuadricula(filas, columnas, ancho, alto):
    cuadricula = []
    espacio_horizontal = ancho // columnas
    espacio_vertical = alto // filas
    for i in range(filas):
        cuadricula.append([])
        for j in range(columnas):
            lugar = Lugar(i, j, espacio_horizontal, espacio_vertical, filas, columnas)
            cuadricula[i].append(lugar)

    return cuadricula

def graficar(ventana, cuadricula, filas, columnas, ancho, alto):
    ventana.fill(blanco)

    for fila in cuadricula:
        for lugar in fila:
            lugar.dibujar(ventana)

    lineas_cuadricula(ventana, filas, columnas, ancho, alto)
    pygame.display.update()

def click_posicion(pos, filas, columnas, ancho, alto):
    espacio_horizontal = ancho // columnas
    espacio_vertical = alto // filas
    y, x = pos
    fila = x // espacio_horizontal
    columna = y // espacio_vertical
    return fila, columna

def alinear_equipo(alineacion, porterias, arquero1, arquero2, alineacion1_442, alineacion1_4231, alineacion2_442, alineacion2_4231, r, cuadricula):
    
    y,x = arquero1
    lugar = cuadricula[y][x]
    lugar.ubicar_jugador1()

    y,x = arquero2
    lugar = cuadricula[y][x]
    lugar.ubicar_jugador2()

    for pos in porterias:
            y,x = pos
            lugar = cuadricula[y][x]
            lugar.ubicar_porteria()
    
    if alineacion == 1:
        for linea in alineacion1_442:
            for pos in linea:
                y,x = pos
                lugar = cuadricula[y][x]
                lugar.ubicar_jugador1()
    elif alineacion == 2:
        for linea in alineacion1_4231:
            for pos in linea:
                y,x = pos
                lugar = cuadricula[y][x]
                lugar.ubicar_jugador1()
    else:
        raise ValueError

    if r == 1:
        for linea in alineacion2_442:
            for pos in linea:
                y,x = pos
                lugar = cuadricula[y][x]
                lugar.ubicar_jugador2()
    elif r == 2:
        for linea in alineacion2_4231:
            for pos in linea:
                y,x = pos
                lugar = cuadricula[y][x]
                lugar.ubicar_jugador2()

def main():
    ancho = 600
    alto = 800
    filas = 40
    columnas = 30
    cuadricula = hacer_cuadricula(filas, columnas, ancho, alto)

    inicio = None
    final = None

    run = True

    porterias = [[0,13],[1,13],[1,14],[1,15],[1,16],[0,16],[38,13],[39,13],[39,14],[39,14],[39,15],[39,16],[38,16]]

    arquero1 = [0,15]
    arquero2 = [38,15]

    defensas1_4 = [[6,4],[6,11],[6,18],[6,25]]
    mediocampistas1_4 = [[11,3],[11,10],[11,19],[11,26]]
    delanteros1_2 = [[16,12],[16,17]]

    mediocampistas1_23 = [[10,12],[10,17],[15,8],[15,15],[15,21]]
    delanteros1_1 = [[18,15]]

    defensas2_4 = [[33,4],[33,11],[33,18],[33,25]]
    mediocampistas2_4 = [[29,12],[29,17],[24,8],[24,15],[24,21]]
    delanteros2_2 = [[21,15]]

    mediocampistas2_23 = [[28,3],[28,10],[28,19],[28,26]]
    delanteros2_1 = [[23,15]]

    alineacion1_442 = [defensas1_4, mediocampistas1_4, delanteros1_2]
    alineacion1_4231 = [defensas1_4, mediocampistas1_23, delanteros1_1]
    alineacion2_442 = [defensas2_4, mediocampistas2_4, delanteros2_2]
    alineacion2_4231 = [defensas2_4, mediocampistas2_23, delanteros2_1]

    try:
        alineacion = int(input("¿Qué alineación deseas para tu equipo? Para (4-4-2) ingresa 1 o para (4-2-3-1) ingresa 2: "))

        ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("A* Algoritmo")
        r = randint(1,2)

        while run:
            graficar(ventana, cuadricula, filas, columnas, ancho, alto)
            alinear_equipo(alineacion, porterias, arquero1, arquero2, alineacion1_442, alineacion1_4231, alineacion2_442, alineacion2_4231, r, cuadricula)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    fila, columna = click_posicion(pos, filas, columnas, ancho, alto)
                    lugar = cuadricula[fila][columna]
                    if not inicio and lugar != final:
                        inicio = lugar
                        inicio.hacer_inicio()
                    elif not final and lugar != inicio:
                        final = lugar
                        final.hacer_final()
                    elif lugar != inicio and lugar != final:
                        lugar.hacer_obstaculo() 
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    fila, columna = click_posicion(pos, filas, columnas, ancho, alto)
                    lugar = cuadricula[fila][columna]
                    lugar.borrar()
                    if lugar == inicio:
                        inicio = None
                    elif lugar == final:
                        final = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame. K_SPACE and inicio and final:
                        for fila in cuadricula:
                            for lugar in fila:
                                lugar.actualizar_juntos(cuadricula)
                        
                        algoritmo(lambda: graficar(ventana, cuadricula, filas, columnas, ancho, alto), cuadricula, inicio, final)

                    if event.key == pygame.K_DELETE:
                        inicio = None
                        final = None
                        cuadricula = hacer_cuadricula(filas, columnas, ancho, alto)
                    
                    if event.key == pygame.K_s:
                        if alineacion == 1:
                            for linea in alineacion1_442:
                                for pos in linea:
                                    y,x = pos
                                    lugar_anterior = cuadricula[y][x]
                                    lugar_anterior.borrar()
                                for i in range(0,len(linea)):
                                    linea[i][0] += 1
                                
                        elif alineacion == 2:
                            for linea in alineacion1_4231:
                                for pos in linea:
                                    y,x = pos
                                    lugar_anterior = cuadricula[y][x]
                                    lugar_anterior.borrar()
                                for i in range(0,len(linea)):
                                    linea[i][0] += 1
                    
                    if event.key == pygame.K_w:
                        if alineacion == 1:
                            for linea in alineacion1_442:
                                for pos in linea:
                                    y,x = pos 
                                    lugar_anterior = cuadricula[y][x]
                                    lugar_anterior.borrar()
                                for i in range(0,len(linea)):
                                    linea[i][0] -= 1
                                
                        elif alineacion == 2:
                            for linea in alineacion1_4231:
                                for pos in linea:
                                    y,x = pos
                                    lugar_anterior = cuadricula[y][x]
                                    lugar_anterior.borrar()
                                for i in range(0,len(linea)):
                                    linea[i][0] -= 1

    except ValueError:
        print("\n  No se reconoce la entrada, vuelve a intentarlo")
        pygame.quit()
        main()
    except Exception:
        print("\n  Ocurrió un error, se ejecutará de nuevo el juego")
        pygame.quit()
        main()
main()
import pygame
import random

# --- CONFIGURACIÓN ---
ANCHO_VENTANA, ALTO_VENTANA = 400, 600
ANCHO_BLOQUE = 30
COLUMNAS, FILAS = 10, 20

# Calculamos los márgenes para que el tablero esté centrado
MARGEN_X = (ANCHO_VENTANA - COLUMNAS * ANCHO_BLOQUE) // 2
MARGEN_Y = (ALTO_VENTANA - FILAS * ANCHO_BLOQUE) // 2

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (30, 30, 30)
COLORES_PIEZAS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128), 
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]

# Piezas
PIEZAS = [
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[0, 1, 0], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]], 
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]]
]

class Tetris:
    def __init__(self):
        # El tablero se inicializa con el color NEGRO (vacío)
        self.tablero = [[NEGRO for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.game_over = False
        self.nueva_pieza()

    def nueva_pieza(self):
        self.forma = random.choice(PIEZAS)
        self.color = random.choice(COLORES_PIEZAS)
        # Centrar la pieza al aparecer
        self.x = COLUMNAS // 2 - len(self.forma[0]) // 2
        self.y = 0
        # Si al aparecer ya choca, es Game Over
        if self.choca(self.x, self.y, self.forma):
            self.game_over = True

    def choca(self, nx, ny, forma):
        for r, fila in enumerate(forma):
            for c, valor in enumerate(fila):
                if valor:
                    # REVISIÓN DE BORDES: Izquierda, Derecha y Suelo
                    if nx + c < 0 or nx + c >= COLUMNAS or ny + r >= FILAS:
                        return True
                    # REVISIÓN DE COLISIÓN con otras piezas ya fijas
                    if self.tablero[ny + r][nx + c] != NEGRO:
                        return True
        return False

    def rotar(self):
        nueva_forma = list(zip(*self.forma[::-1]))
        # Solo rota si la nueva posición no choca con nada
        if not self.choca(self.x, self.y, nueva_forma):
            self.forma = nueva_forma

    def fijar(self):
        for r, fila in enumerate(self.forma):
            for c, valor in enumerate(fila):
                if valor:
                    self.tablero[self.y + r][self.x + c] = self.color
        self.eliminar_lineas()
        self.nueva_pieza()

    def eliminar_lineas(self):
        # Filtramos las filas que no estén llenas
        filas_libres = [f for f in self.tablero if any(celda == NEGRO for celda in f)]
        cuantas_borradas = FILAS - len(filas_libres)
        # Añadimos nuevas filas vacías arriba
        self.tablero = [[NEGRO for _ in range(COLUMNAS)] for _ in range(cuantas_borradas)] + filas_libres

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Mi Tetris")
    reloj = pygame.time.Clock()
    juego = Tetris()
    
    caida_timer = 0
    velocidad = 500 # Milisegundos entre caídas

    while not juego.game_over:
        pantalla.fill((10, 10, 10)) # Fondo casi negro
        caida_timer += reloj.get_rawtime()
        reloj.tick()

        # --- Lógica de caida ---
        if caida_timer > velocidad:
            if not juego.choca(juego.x, juego.y + 1, juego.forma):
                juego.y += 1
            else:
                juego.fijar()
            caida_timer = 0

        # --- Eventos de teclado ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not juego.choca(juego.x - 1, juego.y, juego.forma):
                    juego.x -= 1
                if event.key == pygame.K_RIGHT and not juego.choca(juego.x + 1, juego.y, juego.forma):
                    juego.x += 1
                if event.key == pygame.K_DOWN and not juego.choca(juego.x, juego.y + 1, juego.forma):
                    juego.y += 1
                if event.key == pygame.K_UP:
                    juego.rotar()

        # --- DIBUJO ---
        # 1. Dibujar el fondo del tablero (Gris oscuro)
        pygame.draw.rect(pantalla, GRIS, (MARGEN_X, MARGEN_Y, COLUMNAS*ANCHO_BLOQUE, FILAS*ANCHO_BLOQUE))

        # 2. Dibujar bloques fijos en el tablero
        for r in range(FILAS):
            for c in range(COLUMNAS):
                color_celda = juego.tablero[r][c]
                if color_celda != NEGRO:
                    pygame.draw.rect(pantalla, color_celda, 
                                   (MARGEN_X + c*ANCHO_BLOQUE, MARGEN_Y + r*ANCHO_BLOQUE, ANCHO_BLOQUE-1, ANCHO_BLOQUE-1))

        # 3. Dibujar pieza actual
        for r, fila in enumerate(juego.forma):
            for c, valor in enumerate(fila):
                if valor:
                    pygame.draw.rect(pantalla, juego.color, 
                                   (MARGEN_X + (juego.x+c)*ANCHO_BLOQUE, MARGEN_Y + (juego.y+r)*ANCHO_BLOQUE, ANCHO_BLOQUE-1, ANCHO_BLOQUE-1))

        pygame.display.flip()

    print("Fin del juego")
    pygame.quit()

if __name__ == "__main__":
    main()
import random
import sys
import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la ventana (Diseño vertical tipo slot / móvil)
ANCHO, ALTO = 480, 720
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Slingo WonderBelle")

# Paleta de colores (Inspirada en tonos vibrantes y artísticos)
COLOR_FONDO = (30, 25, 45)  # Fondo oscuro elegante
COLOR_PANEL = (50, 40, 75)  # Contenedores
COLOR_TEXTO = (255, 255, 255)  # Blanco
COLOR_ACCENT = (255, 105, 180)  # Tono Rosa / Fucsia WonderBelle
COLOR_CASILLA = (70, 60, 100)
COLOR_MARCADA = (46, 204, 113)  # Verde al acertar número
COLOR_BOTON = (231, 76, 60)  # Botón de Tirar

# Fuentes
FUENTE_TITULO = pygame.font.SysFont("Arial", 28, bold=True)
FUENTE_TEXTO = pygame.font.SysFont("Arial", 20, bold=True)
FUENTE_NUMEROS = pygame.font.SysFont("Arial", 24, bold=True)

# Generación del tablero Slingo (Columnas 5x5 con rangos clásicos)
# Col 1: 1-15, Col 2: 16-30, Col 3: 31-45, Col 4: 46-60, Col 5: 61-75


def generar_tablero():
  tablero = []
  for col in range(5):
    inicio = col * 15 + 1
    fin = inicio + 15
    numeros_col = random.sample(range(inicio, fin), 5)
    tablero.append(numeros_col)
  # Transponer para matriz de 5 filas x 5 columnas
  matriz = [[tablero[c][r] for c in range(5)] for r in range(5)]
  return matriz


# Estado del juego
tablero_juego = generar_tablero()
# Matriz de booleanos para saber qué casillas están marcadas
marcados = [[False for _ in range(5)] for _ in range(5)]

# Rodillo inferior (5 números actuales)
rodillo_actual = ["?", "?", "?", "?", "?"]
tiradas_restantes = 10


def generar_tirada():
  global rodillo_actual, tiradas_restantes
  if tiradas_restantes > 0:
    # Selecciona 5 números aleatorios únicos del rango 1-75 para simular el rodillo
    rodillo_actual = random.sample(range(1, 76), 5)
    tiradas_restantes -= 1


# Bucle principal del juego
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
  VENTANA.fill(COLOR_FONDO)

  # --- EVENTOS ---
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      ejecutando = False

    elif evento.type == pygame.MOUSEBUTTONDOWN:
      pos_x, pos_y = evento.pos

      # Clic en el botón de Tirar (Spin)
      if 140 <= pos_x <= 340 and 620 <= pos_y : 680:
        generar_tirada()

      # Clic en la cuadrícula para marcar números si coinciden con el rodillo
      # Cuadrícula centrada: X de 40 a 440, Y de 120 a 420
      elif 40 <= pos_x <= 440 and 120 <= pos_y <= 520:
        col_idx = (pos_x - 40) // 80
        fila_idx = (pos_y - 120) // 80
        if 0 <= col_idx < 5 and 0 <= fila_idx < 5:
          num_casilla = tablero_juego[fila_idx][col_idx]
          # Si el número de la casilla está en el rodillo actual, se marca
          if num_casilla in rodillo_actual:
            marcados[fila_idx][col_idx] = True

  # --- DIBUJO DE INTERFAZ ---

  # 1. Título del Juego
  superficie_titulo = FUENTE_TITULO.render("SLINGO WONDERBELLE", True, COLOR_ACCENT)
  VENTANA.blit(
      superficie_titulo, (ANCHO // 2 - superficie_titulo.get_width() // 2, 20)
  )

  # 2. Dibujar Cuadrícula de 5x5
  tam_celda = 75
  margen = 8
  inicio_x = 40
  inicio_y = 120

  for fila in range(5):
    for col in range(5):
      x = inicio_x + col * (tam_celda + margen)
      y = inicio_y + fila * (tam_celda + margen)

      # Color de la celda según si está marcada o no
      color_actual = COLOR_MARCADA if marcados[fila][col] else COLOR_CASILLA
      pygame.draw.rect(
          VENTANA, color_actual, (x, y, tam_celda, tam_celda), border_radius=8
      )

      # Número de la casilla
      num_texto = str(tablero_juego[fila][col])
      superficie_num = FUENTE_NUMEROS.render(num_texto, True, COLOR_TEXTO)
      VENTANA.blit(
          superficie_num,
          (
              x + (tam_celda // 2 - superficie_num.get_width() // 2),
              y + (tam_celda // 2 - superficie_num.get_height() // 2),
          ),
      )

  # 3. Rodillo inferior (Slots)
  slot_y = 540
  slot_ancho = 80
  slot_alto = 60
  slot_inicio_x = 40
  slot_margen = 10

  for i, num in enumerate(rodillo_actual):
    sx = slot_inicio_x + i * (slot_ancho + slot_margen)
    pygame.draw.rect(
        VENTANA,
        COLOR_PANEL,
        (sx, slot_y, slot_ancho, slot_alto),
        border_radius=6,
    )
    s_texto = FUENTE_NUMEROS.render(str(num), True, COLOR_ACCENT)
    VENTANA.blit(
        s_texto,
        (
            sx + (slot_ancho // 2 - s_texto.get_width() // 2),
            slot_y + (slot_alto // 2 - s_texto.get_height() // 2),
        ),
    )

  # 4. Panel de Tiradas Restantes y Botón
  info_tiradas = FUENTE_TEXTO.render(
      f"Tiradas: {tiradas_restantes}", True, COLOR_TEXTO
  )
  VENTANA.blit(info_tiradas, (40, 630))

  # Botón de Tirar
  pygame.draw.rect(
      VENTANA, COLOR_BOTON, (260, 620, 180, 50), border_radius=10
  )
  txt_boton = FUENTE_TEXTO.render("¡GIRAR!", True, COLOR_TEXTO)
  VENTANA.blit(
      txt_boton,
      (
          260 + (180 // 2 - txt_boton.get_width() // 2),
          620 + (50 // 2 - txt_boton.get_height() // 2),
      ),
  )

  pygame.display.flip()
  reloj.tick(30)

pygame.quit()
sys.exit()

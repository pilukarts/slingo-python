import os
import random
import sys
import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la ventana (Formato horizontal o vertical optimizado)
ANCHO, ALTO = 960, 540  # Formato panorámico ideal para el diseño conceptual
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Slingo WonderBelle: Galactic Punk")

# Paleta de colores de respaldo (Neón / Galáctico)
COLOR_FONDO = (15, 10, 25)
COLOR_TEXTO = (255, 255, 255)
COLOR_NEON_ROSA = (255, 0, 127)
COLOR_NEON_CELESTE = (0, 240, 255)

# Fuentes
FUENTE_TITULO = pygame.font.SysFont("Arial", 24, bold=True)
FUENTE_NUMEROS = pygame.font.SysFont("Arial", 22, bold=True)

# --- CARGA DE RECURSOS (ASSETS) ---
# Intentará cargar las imágenes de WonderBelle si existen en la carpeta assets/images/
DIRECTORIO_ASSETS = os.path.join("assets", "images")


def cargar_imagen(nombre, ancho, alto):
  ruta = os.path.join(DIRECTORIO_ASSETS, nombre)
  if os.path.exists(ruta):
    img = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(img, (ancho, alto))
  return None


# Cargar imágenes (si no están creadas todavía, se quedan como None y el juego dibujará formas limpias)
img_fondo = cargar_imagen("fondo.png", ANCHO, ALTO)
img_casilla = cargar_imagen("casilla.png", 65, 65)
img_casilla_hit = cargar_imagen("casilla_hit.png", 65, 65)
img_boton = cargar_imagen("boton_spin.png", 200, 50)


# Generación del tablero Slingo (5x5, números de 1 a 75)
def generar_tablero():
  tablero = []
  for col in range(5):
    inicio = col * 15 + 1
    fin = inicio + 15
    numeros_col = random.sample(range(inicio, fin), 5)
    tablero.append(numeros_col)
  return [[tablero[c][r] for c in range(5)] for r in range(5)]


# Estado del juego
tablero_juego = generar_tablero()
marcados = [[False for _ in range(5)] for _ in range(5)]
rodillo_actual = ["?", "?", "?", "?", "?"]
tiradas_restantes = 14


def generar_tirada():
  global rodillo_actual, tiradas_restantes
  if tiradas_restantes > 0:
    rodillo_actual = random.sample(range(1, 76), 5)
    tiradas_restantes -= 1


# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
  # --- GESTIÓN DE EVENTOS ---
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      ejecutando = False

    elif evento.type == pygame.MOUSEBUTTONDOWN:
      pos_x, pos_y = evento.pos

      # Botón SPIN (ubicado a la derecha abajo en el concepto)
      if 680 <= pos_x <= 880 and 450 <= pos_y <= 500:
        generar_tirada()

      # Clic en el tablero central (ajustado al centro de la pantalla 960x540)
      inicio_x_tablero = 310
      inicio_y_tablero = 80
      if (
          inicio_x_tablero <= pos_x <= inicio_x_tablero + (5 * 75)
          and inicio_y_tablero <= pos_y <= inicio_y_tablero + (5 * 75)
      ):
        col_idx = (pos_x - inicio_x_tablero) // 75
        fila_idx = (pos_y - inicio_y_tablero) // 75
        if 0 <= col_idx < 5 and 0 <= fila_idx < 5:
          num_casilla = tablero_juego[fila_idx][col_idx]
          if num_casilla in rodillo_actual:
            marcados[fila_idx][col_idx] = True

  # --- RENDERIZADO / DIBUJO ---
  if img_fondo:
    VENTANA.blit(img_fondo, (0, 0))
  else:
    VENTANA.fill(COLOR_FONDO)  # Fondo oscuro de respaldo si no hay imagen

  # 1. Dibujar Cuadrícula de Juego (Centrada)
  inicio_x_tablero = 310
  inicio_y_tablero = 80
  tam_celda = 70
  espacio = 5

  for fila in range(5):
    for col in range(5):
      x = inicio_x_tablero + col * (tam_celda + espacio)
      y = inicio_y_tablero + fila * (tam_celda + espacio)

      # Dibujar casilla según estado
      if marcados[fila][col]:
        if img_casilla_hit:
          VENTANA.blit(img_casilla_hit, (x, y))
        else:
          pygame.draw.rect(
              VENTANA, COLOR_NEON_ROSA, (x, y, tam_celda, tam_celda), border_radius=6
          )
      else:
        if img_casilla:
          VENTANA.blit(img_casilla, (x, y))
        else:
          pygame.draw.rect(
              VENTANA, (40, 30, 60), (x, y, tam_celda, tam_celda), border_radius=6
          )
          pygame.draw.rect(
              VENTANA, COLOR_NEON_CELESTE, (x, y, tam_celda, tam_celda), 1, border_radius=6
          )

      # Texto del número
      num_texto = str(tablero_juego[fila][col])
      superficie_num = FUENTE_NUMEROS.render(num_texto, True, COLOR_TEXTO)
      VENTANA.blit(
          superficie_num,
          (
              x + (tam_celda // 2 - superficie_num.get_width() // 2),
              y + (tam_celda // 2 - superficie_num.get_height() // 2),
          ),
      )

  # 2. Rodillo Inferior (Slots de números)
  slot_inicio_x = 310
  slot_y = 460
  slot_ancho = 65
  slot_alto = 50
  slot_espacio = 10

  for i, num in enumerate(rodillo_actual):
    sx = slot_inicio_x + i * (slot_ancho + slot_espacio)
    pygame.draw.rect(
        VENTANA, (25, 20, 45), (sx, slot_y, slot_ancho, slot_alto), border_radius=8
    )
    pygame.draw.rect(
        VENTANA, COLOR_NEON_CELESTE, (sx, slot_y, slot_ancho, slot_alto), 2, border_radius=8
    )

    s_texto = FUENTE_NUMEROS.render(str(num), True, COLOR_NEON_CELESTE)
    VENTANA.blit(
        s_texto,
        (
            sx + (slot_ancho // 2 - s_texto.get_width() // 2),
            slot_y + (slot_alto // 2 - s_texto.get_height() // 2),
        ),
    )

  # 3. Panel Lateral / Inferior (Tiradas y Botón Spin)
  fuente_panel = pygame.font.SysFont("Arial", 18, bold=True)
  texto_tiradas = fuente_panel(f"SPINS LEFT: {tiradas_restantes}", True, COLOR_NEON_CELESTE)
  VENTANA.blit(texto_tiradas, (70, 475))

  # Botón de Girar
  bx, by = 680, 455
  if img_boton:
    VENTANA.blit(img_boton, (bx, by))
  else:
    pygame.draw.rect(
        VENTANA, COLOR_NEON_ROSA, (bx, by, 200, 45), border_radius=10
    )
    txt_b = fuente_panel("SPIN! (GALACTIC)", True, COLOR_TEXTO)
    VENTANA.blit(txt_b, (bx + (200 // 2 - txt_b.get_width() // 2), by + 12))

  pygame.display.flip()
  reloj.tick(30)

pygame.quit()
sys.exit()

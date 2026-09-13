import os
import random
import sys
import pygame

# Inicializar Pygame
pygame.init()

ANCHO, ALTO = 960, 540
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Slingo WonderBelle: Galactic Punk (Daub Edition)")

# Paleta de colores Neón / Galáctico
COLOR_FONDO = (15, 10, 25)
COLOR_TEXTO = (255, 255, 255)
COLOR_NEON_ROSA = (255, 0, 127)
COLOR_NEON_CELESTE = (0, 240, 255)
COLOR_NEON_AMARILLO = (255, 220, 0)

FUENTE_TITULO = pygame.font.SysFont("Arial", 22, bold=True)
FUENTE_NUMEROS = pygame.font.SysFont("Arial", 22, bold=True)
FUENTE_PANEL = pygame.font.SysFont("Arial", 16, bold=True)

DIRECTORIO_ASSETS = os.path.join("assets", "images")


def cargar_imagen(nombre, ancho, alto):
  ruta = os.path.join(DIRECTORIO_ASSETS, nombre)
  if os.path.exists(ruta):
    img = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(img, (ancho, alto))
  return None


img_fondo = cargar_imagen("fondo.png", ANCHO, ALTO)
img_casilla = cargar_imagen("casilla.png", 65, 65)
img_casilla_hit = cargar_imagen("casilla_hit.png", 65, 65)
img_boton = cargar_imagen("boton_spin.png", 200, 50)


def generar_tablero():
  tablero = []
  for col in range(5):
    inicio = col * 15 + 1
    fin = inicio + 15
    numeros_col = random.sample(range(inicio, fin), 5)
    tablero.append(numeros_col)
  return [[tablero[c][r] for c in range(5)] for r in range(5)]


tablero_juego = generar_tablero()
marcados = [[False for _ in range(5)] for _ in range(5)]
rodillo_actual = [12, 45, "W", 23, 67]
tiradas_restantes = 14
puntuacion = 0
mensaje_bonus = ""
temporizador_mensaje = 0


def generar_tirada():
  global rodillo_actual, tiradas_restantes, puntuacion, mensaje_bonus, temporizador_mensaje
  if tiradas_restantes > 0:
    tiradas_restantes -= 1
    nuevo_rodillo = []
    for _ in range(5):
      # 20% de probabilidad de que salga el comodín estilo "Dab" (W)
      if random.random() < 0.2:
        nuevo_rodillo.append("W")
      else:
        nuevo_rodillo.append(random.randint(1, 75))
    rodillo_actual = nuevo_rodillo
    mensaje_bonus = ""


# Mecánica Daub (1 a 5 casillas) al activar el comodín "W"
def activar_daub_galactico():
  global puntuacion, mensaje_bonus, temporizador_mensaje
  # Buscar casillas que aún no estén marcadas
  no_marcadas = []
  for f in range(5):
    for c in range(5):
      if not marcados[f][c]:
        no_marcadas.append((f, c))

  if not no_marcadas:
    return

  # Decidir aleatoriamente cuántas casillas marcar (de 1 a 5, con más peso a valores bajos)
  cantidad_a_marcar = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[
      0
  ]
  cantidad_a_marcar = min(cantidad_a_marcar, len(no_marcadas))

  seleccionadas = random.sample(no_marcadas, cantidad_a_marcar)
  for f, c in seleccionadas:
    marcados[f][c] = True

  puntuacion += cantidad_a_marcar * 100

  # Si alcanza las 5 casillas de golpe, ¡Súper Bonus Galáctico!
  if cantidad_a_marcar == 5:
    mensaje_bonus = "¡¡SÚPER BONUS GALÁCTICO (5 DAUBS)! +1000 PTS"
    puntuacion += 1000
  else:
    mensaje_bonus = f"¡DAUB GALÁCTICO! {cantidad_a_marcar} casillas marcadas"
  temporizador_mensaje = 90  # Frames que dura el aviso en pantalla


# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      ejecutando = False

    elif evento.type == pygame.MOUSEBUTTONDOWN:
      pos_x, pos_y = evento.pos

      # Botón SPIN
      if 680 <= pos_x <= 880 and 450 <= pos_y <= 500:
        generar_tirada()

      # Clic en el rodillo: Si pulsas sobre un comodín "W", se activa el Daub automático (1 a 5 casillas)
      slot_inicio_x = 310
      slot_y = 460
      slot_ancho = 65
      slot_alto = 50
      slot_espacio = 10

      for i, item in enumerate(rodillo_actual):
        sx = slot_inicio_x + i * (slot_ancho + slot_espacio)
        if sx <= pos_x <= sx + slot_ancho and slot_y <= pos_y <= slot_y + slot_alto:
          if item == "W":
            activar_daub_galactico()

      # Clic en la cuadrícula clásica para marcar números coincidentes
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
          if num_casilla in rodillo_actual and not marcados[fila_idx][col_idx]:
            marcados[fila_idx][col_idx] = True
            puntuacion += 50

  # --- RENDERIZADO ---
  if img_fondo:
    VENTANA.blit(img_fondo, (0, 0))
  else:
    VENTANA.fill(COLOR_FONDO)

  # 1. Cuadrícula 5x5
  inicio_x_tablero = 310
  inicio_y_tablero = 80
  tam_celda = 70
  espacio = 5

  for fila in range(5):
    for col in range(5):
      x = inicio_x_tablero + col * (tam_celda + espacio)
      y = inicio_y_tablero + fila * (tam_celda + espacio)

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

      num_texto = str(tablero_juego[fila][col])
      superficie_num = FUENTE_NUMEROS.render(num_texto, True, COLOR_TEXTO)
      VENTANA.blit(
          superficie_num,
          (
              x + (tam_celda // 2 - superficie_num.get_width() // 2),
              y + (tam_celda // 2 - superficie_num.get_height() // 2),
          ),
      )

  # 2. Rodillo Inferior
  slot_inicio_x = 310
  slot_y = 460
  slot_ancho = 65
  slot_alto = 50
  slot_espacio = 10

  for i, item in enumerate(rodillo_actual):
    sx = slot_inicio_x + i * (slot_ancho + slot_espacio)
    color_borde = (
        COLOR_NEON_AMARILLO if item == "W" else COLOR_NEON_CELESTE
    )
    pygame.draw.rect(
        VENTANA, (25, 20, 45), (sx, slot_y, slot_ancho, slot_alto), border_radius=8
    )
    pygame.draw.rect(
        VENTANA, color_borde, (sx, slot_y, slot_ancho, slot_alto), 2, border_radius=8
    )

    texto_item = "W" if item == "W" else str(item)
    color_txt = COLOR_NEON_AMARILLO if item == "W" else COLOR_NEON_CELESTE
    s_texto = FUENTE_NUMEROS.render(texto_item, True, color_txt)
    VENTANA.blit(
        s_texto,
        (
            sx + (slot_ancho // 2 - s_texto.get_width() // 2),
            slot_y + (slot_alto // 2 - s_texto.get_height() // 2),
        ),
    )

  # 3. Paneles laterales (Puntuación y Tiradas)
  txt_tiradas = FUENTE_PANEL(f"SPINS LEFT: {tiradas_restantes}", True, COLOR_NEON_CELESTE)
  txt_puntos = FUENTE_PANEL(f"SCORE: {puntuacion}", True, COLOR_NEON_AMARILLO)
  VENTANA.blit(txt_tiradas, (70, 465))
  VENTANA.blit(txt_puntos, (70, 490))

  # Mensaje temporal de Bonus / Daub
  if temporizador_mensaje > 0:
    s_bonus = FUENTE_TITULO.render(mensaje_bonus, True, COLOR_NEON_AMARILLO)
    VENTANA.blit(s_bonus, (ANCHO // 2 - s_bonus.get_width() // 2, 35))
    temporizador_mensaje -= 1

  # Botón SPIN
  bx, by = 680, 455
  if img_boton:
    VENTANA.blit(img_boton, (bx, by))
  else:
    pygame.draw.rect(
        VENTANA, COLOR_NEON_ROSA, (bx, by, 200, 45), border_radius=10
    )
    txt_b = FUENTE_PANEL("SPIN! (DAUB)", True, COLOR_TEXTO)
    VENTANA.blit(txt_b, (bx + (200 // 2 - txt_b.get_width() // 2), by + 14))

  pygame.display.flip()
  reloj.tick(30)

pygame.quit()
sys.exit()

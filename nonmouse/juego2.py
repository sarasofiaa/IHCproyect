import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traza el número")

# Colores
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Lista de colores de fondo amigables
background_colors = [
    (173, 216, 230),  # Azul cielo
    (221, 160, 221),  # Lila
    (255, 239, 213),  # Amarillo suave
    (255, 182, 193),  # Coral claro
    (245, 245, 220),  # Beige
    (240, 255, 255),  # Azul claro
    (240, 255, 240),  # Verde claro
    (255, 228, 225),  # Rosa claro
    (255, 240, 245),  # Rosa pálido
    (255, 228, 196),  # Melocotón
    (255, 250, 205),  # Lemon chiffon
    (255, 255, 240),  # Ivory
    (255, 250, 240),  # Floral white
    (240, 248, 255),  # Alice blue
    (240, 255, 255),  # Azure
    (255, 105, 180),  # Hot pink
    (255, 165, 0),    # Orange
    (0, 128, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (128, 0, 128),    # Purple
    (255, 0, 0),      # Red
    (0, 255, 255),    # Cyan
    (255, 20, 147),   # Deep pink
    (0, 255, 0),      # Lime
]

# Fuente para textos
font = pygame.font.SysFont(None, 500)  # Fuente para el número
button_font = pygame.font.SysFont(None, 40)  # Fuente para los botones

# Variables del juego
current_number = 0
current_color_index = 0
user_path = []  # Lista para almacenar el trazo del usuario
drawing = False  # Estado de dibujo
message = ""  # Mensaje de resultado

# Botones
button_width, button_height = 150, 50
button_margin = 20

# Botón "Anterior"
prev_button_rect = pygame.Rect(
    button_margin, HEIGHT - button_height - button_margin, button_width, button_height
)
prev_button_text = button_font.render("Anterior", True, BLACK)

# Botón "Siguiente"
next_button_rect = pygame.Rect(
    WIDTH - button_width - button_margin,
    HEIGHT - button_height - button_margin,
    button_width, button_height,
)
next_button_text = button_font.render("Siguiente", True, BLACK)

# Botón "Evaluar"
evaluate_button_rect = pygame.Rect(
    WIDTH // 2 - button_width // 2, HEIGHT - 2 * button_height - button_margin, button_width, button_height
)
evaluate_button_text = button_font.render("Evaluar", True, BLACK)

# Número predefinido como ruta de puntos
number_paths = {
    0: [
        (WIDTH // 2 + int(60 * math.cos(2 * math.pi * t / 100)), HEIGHT // 2 - 70 + int(110 * math.sin(2 * math.pi * t / 100)))
        for t in range(600)
    ],

    1: [
        # Generar la curva de la cabeza del 1 (parte superior)
        (WIDTH // 2 - 35 + int(50 * math.cos(math.radians(angle))), HEIGHT // 2 - 170 - int(40 * math.sin(math.radians(angle))))
        for angle in range(250, 360)  # Curva semicircular
    ] + [
        (WIDTH // 2 + 15, HEIGHT // 2 - 175 + y) for y in range(220)
    ],

    2: [
        # Curva superior (parte superior del 2)
        (WIDTH // 2 + int(65 * math.cos(math.radians(angle))), HEIGHT // 2 - 120 + int(60 * math.sin(math.radians(angle))))
        for angle in range(180, 420)  # Curva semicircular
    ] + [
        (WIDTH // 2 + 34 - 1.08 * x, HEIGHT // 2 - 70 + x) for x in range(40)  # Línea vertical izquierda
    ] + [
        # Línea diagonal descendente (parte central del 2)
        (WIDTH // 2 - int(60 * math.sin(math.radians(x))), HEIGHT // 2 + 30 + int(60 * math.cos(math.radians(x))))
        for x in range(90, 170) 
    ] + [
        # Línea horizontal inferior (base del 2)
        (WIDTH // 2 - 60 + x, HEIGHT // 2 + 35) for x in range(120)  # Línea base
    ],

    3: [
        # Curva superior (parte superior del 3)
        (WIDTH // 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 120 + int(55 * math.sin(math.radians(angle))))
        for angle in range(180, 360)  # Curva semicircular
    ] + [
        # Curva superior (parte superior del 3)
        (WIDTH // 2 - 15 + int(70 * math.cos(math.radians(angle))), HEIGHT // 2 - 120 + int(50 * math.sin(math.radians(angle))))
        for angle in range(360, 450)  # Curva semicircular
    ] + [
        # Curva inferior (parte inferior del 3)
        (WIDTH // 2 - 15 + int(70 * math.cos(math.radians(angle))), HEIGHT // 2 - 17 - int(50 * math.sin(math.radians(angle))))
        for angle in range(360, 450)  # Curva semicircular
    ] + [
        # Curva inferior (parte inferior del 3)
        (WIDTH // 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2  - 10 + int(55 * math.sin(math.radians(angle))))
        for angle in range(0, 180)  # Curva semicircular
    ],

    4: [
        # Línea vertical (parte izquierda del 4)
        (WIDTH // 2 + 35, HEIGHT // 2 - 180 + y) for y in range(220)
    ] + [
        # Línea horizontal (parte superior del 4)
        (WIDTH // 2 - 75 + x, HEIGHT // 2 - 20) for x in range(150)
    ] + [
        # Línea diagonal (parte inferior del 4)
        (WIDTH // 2 - 70 + x, HEIGHT // 2 - 40 - 1.5 * x) for x in range(90)
    ],

    5: [
        # Línea horizontal superior (parte superior del 5)
        (WIDTH // 2 - 40 + x, HEIGHT // 2 - 170) for x in range(100)
    ] + [
        # Línea diagonal descendente (parte central del 5)
        (WIDTH // 2 - 5 + int(60 * math.cos(math.radians(x))), HEIGHT // 2 - 25 + int(70 * math.sin(math.radians(x)))
        ) for x in range(220, 520)
    ] + [
        # Línea horizontal inferior (parte inferior del 5)
        (WIDTH // 2 - 55 + x, HEIGHT // 2 - 70 - 6 * x) for x in range(18)
    ],

    6: [
        # Curva superior (parte superior del 6)
        (WIDTH // 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 120 + int(60 * math.sin(math.radians(angle)))
        ) for angle in range(180, 340)
    ] + [
        # Línea vertical (parte central del 6)
        (WIDTH // 2 - 52, HEIGHT // 2 - 120 + y) for y in range(120)
    ] + [
        # Curva inferior (parte inferior del 6)
        (WIDTH // 2 + 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 20 + int(70 * math.sin(math.radians(angle)))
        ) for angle in range(0, 360)
    ],

    7: [
        # Línea horizontal superior (parte superior del 7)
        (WIDTH // 2 - 70 + x, HEIGHT // 2 - 170) for x in range(140)
    ] + [
        # Línea diagonal descendente (parte central del 7)
        (WIDTH // 2 + 130 + int(150 * math.cos(math.radians(x))), HEIGHT // 2 + 50 + int(225 * math.sin(math.radians(x)))
        ) for x in range(185, 245)
    ],

    8: [
        # Curva superior (parte superior del 8)
        (WIDTH // 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 125 + int(50 * math.sin(math.radians(angle)))
        ) for angle in range(0, 360)
    ] + [
        # Curva inferior (parte inferior del 8)
        (WIDTH // 2 + int(60 * math.cos(math.radians(angle))), HEIGHT // 2 - 20 + int(60 * math.sin(math.radians(angle)))
        ) for angle in range(0, 360)
    ],

    9: [
        # Curva superior (parte superior del 9)
        (WIDTH // 2 - 5 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 110 + int(70 * math.sin(math.radians(angle)))
        ) for angle in range(0, 360)
    ] + [
        # Línea vertical (parte central del 9)
        (WIDTH // 2 + 52, HEIGHT // 2 - 100 + y) for y in range(80)
    ] + [
        # Curva inferior (parte inferior del 9)
        (WIDTH // 2 + int(55 * math.cos(math.radians(angle))), HEIGHT // 2 - 15 + int(60 * math.sin(math.radians(angle)))
        ) for angle in range(340, 520)
    ]
    # Agrega rutas para los demás números según sea necesario
}

# Función para cambiar al siguiente número y color
def next_number():
    global current_number, current_color_index, user_path, message
    current_number = (current_number + 1) % 10  # Ciclo entre 0 y 9
    current_color_index = (current_color_index + 1) % len(background_colors)
    user_path = []  # Limpiar el trazo al cambiar de número
    message = ""

# Función para cambiar al número anterior y color
def previous_number():
    global current_number, current_color_index, user_path, message
    current_number = (current_number - 1) % 10  # Ciclo entre 0 y 9
    current_color_index = (current_color_index - 1) % len(background_colors)
    user_path = []  # Limpiar el trazo al cambiar de número
    message = ""

def evaluate_path():
    global message
    if current_number not in number_paths:
        message = "Número no implementado"
        return
    
    target_path = number_paths[current_number]
    correct_points = sum(
        any(math.sqrt((px - tx) ** 2 + (py - ty) ** 2) <= 15 for tx, ty in target_path)
        for px, py in user_path
    )
    
    accuracy = correct_points / len(user_path) if user_path else 0
    message = "Correcto" if correct_points >= (len(target_path) * 0.85) and accuracy > 0.8 else "Incorrecto"
    
    # Mostrar las estadísticas en la consola
    print(f"Evaluación del trazo para el número {current_number}:")
    print(f"  Puntos a trazar: {len(target_path)}")
    print(f"  Puntos dibujados correctamente: {correct_points}")
    print(f"  Total de puntos dibujados: {len(user_path)}")
    print(f"  Precisión: {accuracy * 100:.2f}%")
    print(f"  Resultado: {message}")

# Bucle principal
running = True
while running:
    # Llenar la pantalla con el color de fondo actual
    screen.fill(background_colors[current_color_index])

    # Mostrar el número actual
    number_text = font.render(str(current_number), True, BLACK)
    number_rect = number_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(number_text, number_rect)

    # Dibujar el botón "Anterior"
    pygame.draw.rect(screen, GRAY, prev_button_rect)
    screen.blit(prev_button_text, prev_button_rect.move(
        (button_width - prev_button_text.get_width()) // 2,
        (button_height - prev_button_text.get_height()) // 2,
    ))

    # Dibujar el botón "Siguiente"
    pygame.draw.rect(screen, GRAY, next_button_rect)
    screen.blit(next_button_text, next_button_rect.move(
        (button_width - next_button_text.get_width()) // 2,
        (button_height - next_button_text.get_height()) // 2,
    ))

    # Dibujar el botón "Evaluar"
    pygame.draw.rect(screen, GRAY, evaluate_button_rect)
    screen.blit(evaluate_button_text, evaluate_button_rect.move(
        (button_width - evaluate_button_text.get_width()) // 2,
        (button_height - evaluate_button_text.get_height()) // 2,
    ))

    # Dibujar los puntos de la ruta del número objetivo
    target_path = number_paths.get(current_number, [])
    for tx, ty in target_path:
        pygame.draw.circle(screen, GREEN, (tx, ty), 5)

    # Dibujar el trazo del usuario
    if len(user_path) > 1:  # Asegurarse de que haya al menos 2 puntos
        pygame.draw.lines(screen, WHITE, False, user_path, 15)

    # Mostrar mensaje de evaluación
    if message:
        result_text = button_font.render(message, True, GREEN if message == "Correcto" else RED)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 150))

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if prev_button_rect.collidepoint(event.pos):
                previous_number()
            elif next_button_rect.collidepoint(event.pos):
                next_number()
            elif evaluate_button_rect.collidepoint(event.pos):
                evaluate_path()
            else:
                drawing = True
                user_path = []  # Limpiar el trazo anterior
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            user_path.append(event.pos)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()

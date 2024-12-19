# Define el estado del juego activo //variables globales 
GAME_ACTIVE = None  # Valor inicial ningun juego por default
INSTRUCTION_ACTIVE = None
# Función para obtener el valor de GAME_ACTIVE Setters y Getters
def get_game_active():
    global GAME_ACTIVE
    return GAME_ACTIVE

# Función para actualizar el valor de GAME_ACTIVE
def set_game_active(value):
    global GAME_ACTIVE
    GAME_ACTIVE = value

def get_instruction_active():
    global INSTRUCTION_ACTIVE
    return INSTRUCTION_ACTIVE

def set_instruction_active(value):
    global INSTRUCTION_ACTIVE
    GINSTRUCTION_ACTIVE = value
from pygame import Color

# Configurações de cores
COLORS = {
    'bg': Color(30, 30, 46),
    'text': Color(255, 255, 255),
    'selected': Color(255, 215, 0),
    'border': Color(100, 100, 100),
    'button_bg': Color(50, 50, 70),
    'about_text': Color(200, 200, 200)
}

# Configurações de fonte
FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
FONT_SIZE = 16
FONT_SIZE_SMALL = 12
FONT_FALLBACK = "Arial"

# Configurações de animação
FADE_SPEED = 5
GLITCH_DURATION = 200  # ms

# Dificuldades
DIFFICULTIES = ["FÁCIL", "MÉDIO", "DIFÍCIL"]

# Informações sobre o jogo
ABOUT_INFO = {
    "title": "SOBRE O JOGO",
    "description": [
        "Sudoku 8-bit - Projeto para a matéria SPOLOG 1",
        "",
        "Desenvolvido com:",
        "- Python",
        "- Pygame",
        "",
        "Lógica principal:",
        "- Geração de tabuleiros Sudoku",
        "- Algoritmo otimizado para resolução"
    ],
    "team": [
        "Integrantes:",
        "Marcos Paulo de Santana (SP3214966)",
        "Mariana Calvao Weng (SP3198715)",
        "Luis Cleber Majima (SP320958X)",
        "Luiz Otávio de Lima Rodrigues (SP3211959)"
    ]
}

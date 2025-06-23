import pygame
from src.ui.menu import Menu
from src.ui.difficulty_menu import DifficultyMenu
from src.ui.about_screen import AboutScreen
from src.ui.game_screen import GameScreen

def main():
    pygame.init()
    print("PyGame inicializado")  # Debug
    
    # Configurações iniciais
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sudoku 8-bit")
    print("Tela principal criada")  # Debug
    
    # Cria os menus e telas
    print("Criando menus...")  # Debug
    main_menu = Menu(screen)
    difficulty_menu = DifficultyMenu(screen)
    about_screen = AboutScreen(screen)
    
    # Loop principal do jogo
    print("Iniciando loop principal")  # Debug
    while True:
        print("\nExecutando menu principal")  # Debug
        main_action = main_menu.run()
        print(f"Ação do menu principal: {main_action}")  # Debug
        
        if main_action == "game":
            print("Menu de dificuldade selecionado")  # Debug
            difficulty = difficulty_menu.run()
            print(f"Dificuldade selecionada: {difficulty}")  # Debug
            
            if difficulty in ["fácil", "médio", "difícil"]:
                print(f"Iniciando jogo no modo {difficulty}")
                game_screen = GameScreen(screen, difficulty)
                game_screen.run()
            elif difficulty == "back":
                print("Voltando ao menu principal")  # Debug
                continue  # Volta para o menu principal
        elif main_action == "about":
            print("Tela SOBRE selecionada")  # Debug
            about_screen.run()
            print("Retornou da tela SOBRE")  # Debug
        elif main_action == "SAIR":
            print("Saindo do jogo")  # Debug
            pygame.quit()
            return

if __name__ == "__main__":
    print("Iniciando jogo...")  # Debug
    main()

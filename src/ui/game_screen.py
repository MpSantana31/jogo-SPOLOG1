import pygame
from pygame.locals import *
from ..core.game import SudokuGame
from ..core.solver import SudokuSolver

class GameScreen:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty
        self.game = SudokuGame(screen, difficulty)
        self.solver = SudokuSolver(self.game.board.copy())
        self.font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 24)
        self.small_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 16)
        self.lives = 3
        self.heart_img = pygame.image.load('assets/images/heart.png').convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (30, 30))
        
        # Controles
        self.solve_button = pygame.Rect(650, 20, 120, 40)
        self.hint_button = pygame.Rect(650, 70, 120, 40)
        self.speed_buttons = {
            'lento': pygame.Rect(650, 130, 120, 30),
            'normal': pygame.Rect(650, 170, 120, 30),
            'rápido': pygame.Rect(650, 210, 120, 30)
        }
        self.speed = 200
        self.hints_left = {'fácil': 5, 'médio': 3, 'difícil': 1}[difficulty]
        
        # Cores
        self.colors = {
            'bg': (28, 28, 28),
            'grid': (70, 70, 70),
            'selected': (255, 215, 0),
            'text': (255, 255, 255),
            'error': (255, 0, 0),
            'fixed': (100, 100, 255),
            'title': (255, 100, 100),
            'button': (50, 150, 50),
            'button_hover': (70, 170, 70),
            'hint_button': (150, 100, 50),
            'hint_button_hover': (170, 120, 70),
            'speed_button': (80, 80, 80),
            'speed_button_active': (100, 100, 150),
            'speed_button_hover': (90, 90, 90)
        }
        
        # Tamanhos
        self.grid_size = 540
        self.cell_size = self.grid_size // 9
        self.grid_pos = ((800 - self.grid_size) // 2, (600 - self.grid_size) // 2)
        
    def draw(self):
        """Desenha a interface do jogo"""
        self.screen.fill(self.colors['bg'])
        
        # Desenha o tabuleiro
        self.draw_grid()
        self.draw_numbers()
        self.draw_selection()
        self.draw_lives()
        self.draw_buttons()
        
        pygame.display.flip()
    
    def draw_grid(self):
        """Desenha as linhas do tabuleiro"""
        for i in range(10):
            # Linhas grossas para os blocos 3x3
            thickness = 3 if i % 3 == 0 else 1
            
            # Linhas horizontais
            pygame.draw.line(
                self.screen, self.colors['grid'],
                (self.grid_pos[0], self.grid_pos[1] + i * self.cell_size),
                (self.grid_pos[0] + self.grid_size, self.grid_pos[1] + i * self.cell_size),
                thickness
            )
            
            # Linhas verticais
            pygame.draw.line(
                self.screen, self.colors['grid'],
                (self.grid_pos[0] + i * self.cell_size, self.grid_pos[1]),
                (self.grid_pos[0] + i * self.cell_size, self.grid_pos[1] + self.grid_size),
                thickness
            )
    
    def draw_numbers(self):
        """Desenha os números no tabuleiro"""
        for i in range(9):
            for j in range(9):
                num = self.game.board[i][j]
                if num != 0:
                    # Durante resolução automática - todos azuis
                    if hasattr(self, 'solving') and self.solving:
                        color = (100, 100, 255)  # Azul para solver
                    # Células fixas (não editáveis)
                    elif (i,j) not in self.game.hidden_cells:
                        color = (255, 255, 255)  # Branco para fixos
                    # Células editáveis pelo jogador
                    else:
                        # Verifica se o número está correto
                        is_correct = (num == self.game.solution[i][j])
                        color = (100, 100, 255) if is_correct else (255, 100, 100)
                    
                    # Renderiza o número
                    text = self.font.render(str(num), True, color)
                    text_rect = text.get_rect(
                        center=(
                            self.grid_pos[0] + j * self.cell_size + self.cell_size // 2,
                            self.grid_pos[1] + i * self.cell_size + self.cell_size // 2
                        )
                    )
                    self.screen.blit(text, text_rect)
                    
    def draw_selection(self):
        """Destaca a célula selecionada"""
        if hasattr(self, 'selected') and self.selected:
            row, col = self.selected
            pygame.draw.rect(
                self.screen, self.colors['selected'],
                (
                    self.grid_pos[0] + col * self.cell_size,
                    self.grid_pos[1] + row * self.cell_size,
                    self.cell_size, self.cell_size
                ),
                3
            )
    
    def draw_lives(self):
        """Desenha os corações de vida com título"""
        # Título "VIDAS"
        title = self.small_font.render("VIDAS:", True, self.colors['title'])
        self.screen.blit(title, (20, 15))
        
        # Corações
        for i in range(self.lives):
            self.screen.blit(
                self.heart_img,
                (100 + i * 40, 20)
            )
    
    def draw_buttons(self):
        """Desenha os controles"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Botão RESOLVER
        btn_color = self.colors['button_hover'] if self.solve_button.collidepoint(mouse_pos) else self.colors['button']
        pygame.draw.rect(self.screen, btn_color, self.solve_button, border_radius=5)
        text = self.small_font.render("RESOLVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.solve_button.center)
        self.screen.blit(text, text_rect)
        
        # Botão DICA
        hint_color = self.colors['hint_button_hover'] if self.hint_button.collidepoint(mouse_pos) else self.colors['hint_button']
        pygame.draw.rect(self.screen, hint_color, self.hint_button, border_radius=5)
        hint_text = self.small_font.render(f"DICA ({self.hints_left})", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=self.hint_button.center)
        self.screen.blit(hint_text, hint_rect)
        
        # Botões de velocidade
        for speed, rect in self.speed_buttons.items():
            active = self.speed == {'lento': 400, 'normal': 200, 'rápido': 50}[speed]
            btn_color = self.colors['speed_button_active'] if active else (
                self.colors['speed_button_hover'] if rect.collidepoint(mouse_pos) else self.colors['speed_button']
            )
            pygame.draw.rect(self.screen, btn_color, rect, border_radius=3)
            text = self.small_font.render(speed.upper(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Exibe explicação do passo atual
        if hasattr(self, 'current_step'):
            step_text = self.small_font.render(self.current_step, True, (200, 200, 200))
            self.screen.blit(step_text, (20, 550))
    
    def handle_hint_click(self):
        """Fornece uma dica ao jogador"""
        if self.hints_left <= 0:
            return
            
        # Cria novo solver com estado atual do tabuleiro
        self.solver = SudokuSolver(self.game.board.copy())
        hint = self.solver.get_hint()
        
        if hint:
            row, col, num = hint
            # Verifica se a célula ainda está vazia
            if self.game.board[row][col] == 0:
                self.game.board[row][col] = num
                self.hints_left -= 1
                
                # Destaca a dica
                self.draw()
                pygame.draw.rect(
                    self.screen, (0, 200, 200),
                    (
                        self.grid_pos[0] + col * self.cell_size,
                        self.grid_pos[1] + row * self.cell_size,
                        self.cell_size, self.cell_size
                    ),
                    3
                )
                
                # Mostra número da dica
                hint_text = self.font.render(str(num), True, (0, 200, 200))
                text_rect = hint_text.get_rect(
                    center=(
                        self.grid_pos[0] + col * self.cell_size + self.cell_size//2,
                        self.grid_pos[1] + row * self.cell_size + self.cell_size//2
                    )
                )
                self.screen.blit(hint_text, text_rect)
                
                pygame.display.flip()
                pygame.time.delay(1500)
            else:
                # Se a célula já foi preenchida, tenta novamente
                self.handle_hint_click()
    
    def handle_click(self, pos):
        """Processa clique do mouse"""
        if self.hint_button.collidepoint(pos):
            self.handle_hint_click()
            return
            
        if self.solve_button.collidepoint(pos):
            self.run_solver()
            return
            
        # Verifica botões de velocidade
        for speed, rect in self.speed_buttons.items():
            if rect.collidepoint(pos):
                self.speed = {'lento': 400, 'normal': 200, 'rápido': 50}[speed]
                return
        
        # Clique no tabuleiro...
        x, y = pos
        if (self.grid_pos[0] <= x < self.grid_pos[0] + self.grid_size and
            self.grid_pos[1] <= y < self.grid_pos[1] + self.grid_size):
            
            row = (y - self.grid_pos[1]) // self.cell_size
            col = (x - self.grid_pos[0]) // self.cell_size
            
            if (row, col) in self.game.hidden_cells:
                self.selected = (row, col)
            else:
                self.selected = None
        else:
            self.selected = None
    
    def run_solver(self):
        """Executa o solver"""
        self.solver = SudokuSolver(self.game.board.copy())
        
        def update_cell(row, col, num, is_backtrack):
            # Atualiza explicação do passo
            if is_backtrack:
                self.current_step = f"Backtrack: removendo {num} de ({row+1},{col+1})"
            else:
                self.current_step = f"Testando {num} em ({row+1},{col+1})"
            
            # Atualiza visualização
            color = (255, 100, 100) if is_backtrack else (100, 255, 100)
            self.game.board[row][col] = num
            self.draw()
            
            # Destaca célula atual
            pygame.draw.rect(
                self.screen, color,
                (
                    self.grid_pos[0] + col * self.cell_size,
                    self.grid_pos[1] + row * self.cell_size,
                    self.cell_size, self.cell_size
                ),
                3
            )
            pygame.display.flip()
            
            # Delay
            pygame.time.delay(self.speed // 2 if is_backtrack else self.speed)
            
            return True
            
        # Executa a solução
        success = self.solver.solve_visually(update_cell)
        
        # Feedback final
        if success:
            self.current_step = "Sudoku resolvido com sucesso!"
            self.game.board = self.solver.board
        else:
            self.current_step = "Não foi possível encontrar solução!"
        
        self.draw()
        pygame.time.delay(2000)
        
        # Reseta estado
        self.current_step = ""
    
    def handle_key(self, key):
        """Processa teclas pressionadas"""
        if not hasattr(self, 'selected') or not self.selected:
            return
        
        row, col = self.selected
        
        # Números de 1-9
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            self.game.board[row][col] = num
            
            # Verifica se está correto
            if num != self.game.solution[row][col]:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
            else:
                self.game.hidden_cells.remove((row, col))
                if not self.game.hidden_cells:
                    self.victory()
        
        # Backspace ou delete para apagar
        elif key in (pygame.K_BACKSPACE, pygame.K_DELETE):
            self.game.board[row][col] = 0
    
    def show_end_screen(self, victory):
        """Mostra tela de vitória/derrota"""
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        if victory:
            title = self.font.render("VITÓRIA!", True, (0, 255, 0))
            subtitle = self.small_font.render("Parabéns, você completou o Sudoku!", True, (255, 255, 255))
        else:
            title = self.font.render("GAME OVER", True, (255, 0, 0))
            subtitle = self.small_font.render("Tente novamente!", True, (255, 255, 255))
        
        # Centraliza os textos
        title_rect = title.get_rect(center=(400, 250))
        subtitle_rect = subtitle.get_rect(center=(400, 300))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instrução para continuar
        instruction = self.small_font.render("Pressione qualquer tecla para voltar", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(400, 350))
        self.screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
        
        # Espera por qualquer tecla
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN:
                    waiting = False
    
    def game_over(self):
        """Finaliza o jogo quando perde"""
        self.show_end_screen(False)
        self.running = False
    
    def victory(self):
        """Finaliza o jogo quando vence"""
        self.show_end_screen(True)
        self.running = False
    
    def run(self):
        """Loop principal do jogo"""
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    else:
                        self.handle_key(event.key)
            
            self.draw()
            pygame.time.Clock().tick(60)

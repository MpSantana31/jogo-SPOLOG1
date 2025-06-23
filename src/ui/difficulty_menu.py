import pygame
import sys
import random
from .settings import COLORS, FONT_PATH, FONT_SIZE, FONT_FALLBACK, DIFFICULTIES

class DifficultyMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Carrega a fonte
        try:
            self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        except:
            self.font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZE)
            print(f"Fonte {FONT_PATH} não encontrada, usando {FONT_FALLBACK}")
            
        self.options = DIFFICULTIES
        self.selected = 0
        
        # Efeitos de animação
        self.alpha = 0
        self.fade_in = True
        self.glitch_effect = False
        self.glitch_timer = 0
    
    def draw_pixel_border(self, rect, thickness=2):
        """Desenha borda pixelada"""
        for i in range(thickness):
            offset = i
            points = [
                (rect.left-offset, rect.top-offset),
                (rect.right+offset-1, rect.top-offset),
                (rect.right+offset-1, rect.bottom+offset-1),
                (rect.left-offset, rect.bottom+offset-1)
            ]
            pygame.draw.lines(self.screen, COLORS['border'], True, points, 1)
    
    def apply_glitch_effect(self, surface):
        """Aplica efeito glitch"""
        if not self.glitch_effect:
            return surface
            
        glitch_surf = surface.copy()
        for _ in range(5):
            x = random.randint(0, glitch_surf.get_width()//2)
            y = random.randint(0, glitch_surf.get_height())
            w = random.randint(1, 10)
            h = random.randint(1, 3)
            pygame.draw.rect(glitch_surf, (0, 0, 0), (x, y, w, h))
        return glitch_surf
    
    def draw(self):
        # Animação de fade in
        if self.fade_in and self.alpha < 255:
            self.alpha += 5
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255 - self.alpha))
        
        self.screen.fill(COLORS['bg'])
        
        # Título com efeito glitch
        title = self.font.render("ESCOLHA A DIFICULDADE", True, COLORS['text'])
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(self.apply_glitch_effect(title), title_rect)
        
        # Opções do menu com bordas pixeladas
        for i, option in enumerate(self.options):
            color = COLORS['selected'] if i == self.selected else COLORS['text']
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width()//2, 200 + i * 60))
            
            # Background do botão
            btn_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, COLORS['button_bg'], btn_rect)
            self.draw_pixel_border(btn_rect, 3 if i == self.selected else 2)
            
            # Aplica glitch apenas no item selecionado
            if i == self.selected and self.glitch_effect:
                self.screen.blit(self.apply_glitch_effect(text), text_rect)
            else:
                self.screen.blit(text, text_rect)
        
        # Finaliza animação de entrada
        if self.fade_in and self.alpha < 255:
            self.screen.blit(overlay, (0, 0))
            
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                    self.glitch_effect = True
                    self.glitch_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                    self.glitch_effect = True
                    self.glitch_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_RETURN:
                    self.glitch_effect = True
                    return self.options[self.selected]
                elif event.key == pygame.K_ESCAPE:
                    return "back"
        
        # Controla duração do efeito glitch
        if self.glitch_effect and pygame.time.get_ticks() - self.glitch_timer > 200:
            self.glitch_effect = False
        
        return None
    
    def run(self):
        self.fade_in = True
        self.alpha = 0
        
        while True:
            action = self.handle_events()
            if action in self.options:
                # Animação de saída
                for i in range(0, 255, 15):
                    overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, i))
                    self.draw()
                    self.screen.blit(overlay, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(30)
                return action.lower()  # Retorna 'fácil', 'médio' ou 'difícil'
            elif action == "back":
                return "back"
            
            self.draw()
            self.clock.tick(60)

import pygame
import sys
from .settings import COLORS, FONT_PATH, FONT_SIZE, FONT_FALLBACK, ABOUT_INFO

class AboutScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        except:
            self.font = pygame.font.SysFont(FONT_FALLBACK, FONT_SIZE)
        
        # Efeitos de animação
        self.alpha = 0
        self.fade_in = True
    
    def draw(self):
        # Animação de fade in
        if self.fade_in and self.alpha < 255:
            self.alpha += 5
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255 - self.alpha))
        
        self.screen.fill(COLORS['bg'])
        
        # Título
        title = self.font.render(ABOUT_INFO['title'], True, COLORS['selected'])
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 80))
        self.screen.blit(title, title_rect)
        
        # Descrição
        y_pos = 150
        for line in ABOUT_INFO['description']:
            if line:
                text = self.font.render(line, True, COLORS['text'])
                text_rect = text.get_rect(center=(self.screen.get_width()//2, y_pos))
                self.screen.blit(text, text_rect)
            y_pos += 30
        
        # Equipe
        y_pos += 20
        for line in ABOUT_INFO['team']:
            if line:
                text = self.font.render(line, True, COLORS['text'])
                text_rect = text.get_rect(center=(self.screen.get_width()//2, y_pos))
                self.screen.blit(text, text_rect)
            y_pos += 30
        
        # Instrução para voltar
        back_text = self.font.render("Pressione ESC para voltar", True, COLORS['about_text'])
        back_rect = back_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - 50))
        self.screen.blit(back_text, back_rect)
        
        # Finaliza animação de entrada
        if self.fade_in and self.alpha < 255:
            self.screen.blit(overlay, (0, 0))
            
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
        return None
    
    def run(self):
        self.fade_in = True
        self.alpha = 0
        
        while True:
            action = self.handle_events()
            if action == "back":
                return
            
            self.draw()
            self.clock.tick(60)

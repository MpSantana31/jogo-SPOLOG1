import pygame
import random
import numpy as np

class SudokuGame:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.difficulty = difficulty
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)
        self.hidden_cells = set()
        
        # Configurações por dificuldade
        self.difficulty_settings = {
            "fácil": {"hidden_cells": 40, "cells_per_section": 5},
            "médio": {"hidden_cells": 50, "cells_per_section": 6},
            "difícil": {"hidden_cells": 60, "cells_per_section": 7}
        }
        
        self.generate_puzzle()
    
    def generate_puzzle(self):
        """Gera um tabuleiro de Sudoku válido"""
        # Preenche a diagonal de blocos 3x3
        self.fill_diagonal_boxes()
        
        # Resolve o resto do tabuleiro
        self.solve_sudoku()
        self.solution = self.board.copy()
        
        # Remove células para criar o puzzle
        self.remove_cells()
    
    def fill_diagonal_boxes(self):
        """Preenche os blocos diagonais 3x3 com números válidos"""
        for box in range(0, 9, 3):
            self.fill_box(box, box)
    
    def fill_box(self, row, col):
        """Preenche um bloco 3x3 com números válidos"""
        nums = random.sample(range(1, 10), 9)
        index = 0
        for i in range(3):
            for j in range(3):
                self.board[row+i][col+j] = nums[index]
                index += 1
    
    def is_valid(self, num, pos):
        """Verifica se um número é válido em uma posição"""
        # Verifica linha
        if num in self.board[pos[0]]:
            return False
        
        # Verifica coluna
        if num in self.board[:, pos[1]]:
            return False
        
        # Verifica bloco 3x3
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num:
                    return False
        
        return True
    
    def find_empty(self):
        """Encontra a próxima célula vazia"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve_sudoku(self):
        """Resolve o Sudoku usando backtracking"""
        empty = self.find_empty()
        if not empty:
            return True
        
        row, col = empty
        
        for num in random.sample(range(1, 10), 9):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                
                if self.solve_sudoku():
                    return True
                
                self.board[row][col] = 0
        
        return False
    
    def remove_cells(self):
        """Remove células baseado na dificuldade"""
        settings = self.difficulty_settings[self.difficulty]
        hidden = 0
        
        # Garante que cada seção tenha no mínimo X células escondidas
        sections = [(i, j) for i in range(0, 9, 3) for j in range(0, 9, 3)]
        for section in sections:
            cells = [(section[0]+i, section[1]+j) for i in range(3) for j in range(3)]
            to_hide = random.sample(cells, settings["cells_per_section"])
            
            for cell in to_hide:
                if hidden >= settings["hidden_cells"]:
                    break
                self.hidden_cells.add(cell)
                self.board[cell[0]][cell[1]] = 0
                hidden += 1
        
        # Completa o resto aleatoriamente
        while hidden < settings["hidden_cells"]:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if (row, col) not in self.hidden_cells and self.board[row][col] != 0:
                self.hidden_cells.add((row, col))
                self.board[row][col] = 0
                hidden += 1
    
    def is_valid_placement(self, num, pos):
        """Verifica se um número é válido em uma posição"""
        row, col = pos
        
        # Verifica se a posição está nas células editáveis
        if (row, col) not in self.hidden_cells:
            return False
            
        # Verifica linha e coluna
        if num in self.board[row, :] or num in self.board[:, col]:
            return False
            
        # Verifica bloco 3x3
        box_x, box_y = col // 3, row // 3
        if num in self.board[box_y*3:(box_y+1)*3, box_x*3:(box_x+1)*3]:
            return False
            
        return True
    
    def run(self):
        """Loop principal do jogo"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Aqui viria a lógica de renderização e input do usuário
            # Por enquanto apenas para teste
            print("Tabuleiro gerado:")
            print(self.board)
            print("\nSolução:")
            print(self.solution)
            
            pygame.time.delay(2000)  # Pausa para visualização
            running = False

import pygame
import numpy as np
from collections import defaultdict

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.invalid_numbers = defaultdict(set)  # Memoization de números inválidos
        
    def find_empty(self):
        """Encontra a célula vazia com menos opções (heurística MRV)"""
        best = None
        min_options = 10
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    # Conta opções válidas
                    options = [num for num in range(1,10) 
                              if self.is_valid(num, (i,j))]
                    
                    if len(options) < min_options:
                        min_options = len(options)
                        best = (i, j)
                        if min_options == 1:  # Otimização
                            return best
        return best
    
    def is_valid(self, num, pos):
        """Verifica se um número é válido em uma posição"""
        row, col = pos
        
        # Verifica se o número já foi marcado como inválido
        if num in self.invalid_numbers[(row, col)]:
            return False
            
        # Verifica linha e coluna
        if num in self.board[row, :] or num in self.board[:, col]:
            return False
            
        # Verifica bloco 3x3
        box_x, box_y = col // 3, row // 3
        if num in self.board[box_y*3:(box_y+1)*3, box_x*3:(box_x+1)*3]:
            return False
            
        return True
    
    def solve_visually(self, callback=None):
        """
        Resolve com backtracking + MRV + memoization
        callback(row, col, num, is_backtrack)
        """
        empty = self.find_empty()
        if not empty:
            return True
            
        row, col = empty
        
        # Tenta números em ordem aleatória para variar
        for num in np.random.permutation(range(1, 10)):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                
                if callback and not callback(row, col, num, False):
                    return False
                
                if self.solve_visually(callback):
                    return True
                
                # Backtrack
                self.board[row][col] = 0
                self.invalid_numbers[(row, col)].add(num)  # Memoization
                
                if callback and not callback(row, col, 0, True):
                    return False
        
        # Limpa memoization para esta célula
        self.invalid_numbers[(row, col)].clear()
        return False

    def get_hint(self):
        """
        Retorna uma célula e número válido para dica
        Formato: (row, col, num) ou None se não encontrar
        """
        # Lista de células vazias
        empty_cells = [(i,j) for i in range(9) for j in range(9) 
                      if self.board[i][j] == 0]
        
        # Embaralha para evitar padrões
        import random
        random.shuffle(empty_cells)
        
        # Primeiro tenta células com apenas uma possibilidade
        for row, col in empty_cells:
            options = [num for num in range(1,10) 
                      if self.is_valid(num, (row,col))]
            if len(options) == 1:
                return (row, col, options[0])
        
        # Depois tenta qualquer célula válida
        for row, col in empty_cells:
            options = [num for num in range(1,10) 
                      if self.is_valid(num, (row,col))]
            if options:
                return (row, col, random.choice(options))
        
        return None

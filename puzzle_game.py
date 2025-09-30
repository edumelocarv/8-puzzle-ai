"""
Implementação do jogo do 8 (8-puzzle) - Classe Board
Este módulo contém a representação do tabuleiro e lógica básica do jogo.
"""

import random
import copy
from typing import List, Tuple, Optional


class Board:
    """Representa o estado do tabuleiro 3x3 do puzzle 8"""
    
    def __init__(self, state: Optional[List[List[int]]] = None):
        """
        Inicializa o tabuleiro.
        
        Args:
            state: Estado inicial do tabuleiro. Se None, usa o estado final.
        """
        if state is None:
            # Estado final (objetivo)
            self.state = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]  # 0 representa o espaço vazio
            ]
        else:
            self.state = copy.deepcopy(state)
        
        self.empty_pos = self._find_empty_position()
    
    def _find_empty_position(self) -> Tuple[int, int]:
        """Encontra a posição do espaço vazio (0)"""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        raise ValueError("Tabuleiro inválido: espaço vazio não encontrado")
    
    def is_goal_state(self) -> bool:
        """Verifica se o tabuleiro está no estado final"""
        goal = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        return self.state == goal
    
    def get_possible_moves(self) -> List[str]:
        """Retorna lista de movimentos possíveis"""
        moves = []
        row, col = self.empty_pos
        
        if row > 0:
            moves.append('UP')
        if row < 2:
            moves.append('DOWN')
        if col > 0:
            moves.append('LEFT')
        if col < 2:
            moves.append('RIGHT')
        
        return moves
    
    def move(self, direction: str) -> bool:
        """
        Move o espaço vazio na direção especificada.
        
        Args:
            direction: 'UP', 'DOWN', 'LEFT', 'RIGHT'
            
        Returns:
            True se o movimento foi realizado, False caso contrário
        """
        if direction not in self.get_possible_moves():
            return False
        
        row, col = self.empty_pos
        new_row, new_col = row, col
        
        if direction == 'UP':
            new_row = row - 1
        elif direction == 'DOWN':
            new_row = row + 1
        elif direction == 'LEFT':
            new_col = col - 1
        elif direction == 'RIGHT':
            new_col = col + 1
        
        # Troca as posições
        self.state[row][col] = self.state[new_row][new_col]
        self.state[new_row][new_col] = 0
        self.empty_pos = (new_row, new_col)
        
        return True
    
    def move_piece(self, piece_row: int, piece_col: int) -> bool:
        """
        Move uma peça para o espaço vazio (se possível).
        
        Args:
            piece_row, piece_col: Posição da peça a ser movida
            
        Returns:
            True se o movimento foi realizado, False caso contrário
        """
        empty_row, empty_col = self.empty_pos
        
        # Verifica se a peça está adjacente ao espaço vazio
        if (abs(piece_row - empty_row) == 1 and piece_col == empty_col) or \
           (abs(piece_col - empty_col) == 1 and piece_row == empty_row):
            
            # Troca as posições
            self.state[empty_row][empty_col] = self.state[piece_row][piece_col]
            self.state[piece_row][piece_col] = 0
            self.empty_pos = (piece_row, piece_col)
            
            return True
        
        return False
    
    def shuffle(self, moves: int = 100) -> None:
        """
        Embaralha o tabuleiro fazendo movimentos aleatórios válidos.
        
        Args:
            moves: Número de movimentos para embaralhar
        """
        for _ in range(moves):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                self.move(move)
    
    def reset_to_goal(self) -> None:
        """Reseta o tabuleiro para o estado final"""
        self.state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        self.empty_pos = (2, 2)
    
    def set_state(self, new_state: List[List[int]]) -> bool:
        """
        Define um novo estado para o tabuleiro.
        
        Args:
            new_state: Novo estado do tabuleiro
            
        Returns:
            True se o estado é válido, False caso contrário
        """
        if self._is_valid_state(new_state):
            self.state = copy.deepcopy(new_state)
            self.empty_pos = self._find_empty_position()
            return True
        return False
    
    def _is_valid_state(self, state: List[List[int]]) -> bool:
        """Verifica se um estado é válido (contém números 0-8 exatamente uma vez)"""
        if len(state) != 3 or any(len(row) != 3 for row in state):
            return False
        
        numbers = []
        for row in state:
            for num in row:
                numbers.append(num)
        
        return sorted(numbers) == list(range(9))
    
    def is_solvable(self) -> bool:
        """
        Verifica se o estado atual é solvível.
        Um puzzle 8 é solvível se o número de inversões é par.
        """
        # Converte para lista 1D (sem o 0)
        flat = []
        for row in self.state:
            for num in row:
                if num != 0:
                    flat.append(num)
        
        # Conta inversões
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        
        return inversions % 2 == 0
    
    def copy(self) -> 'Board':
        """Retorna uma cópia do tabuleiro"""
        return Board(self.state)
    
    def __str__(self) -> str:
        """Representação string do tabuleiro"""
        result = []
        for row in self.state:
            row_str = []
            for num in row:
                if num == 0:
                    row_str.append(' ')
                else:
                    row_str.append(str(num))
            result.append(' '.join(row_str))
        return '\n'.join(result)
    
    def __eq__(self, other) -> bool:
        """Compara dois tabuleiros"""
        if not isinstance(other, Board):
            return False
        return self.state == other.state
    
    def __hash__(self) -> int:
        """Hash do tabuleiro para uso em sets e dicts"""
        return hash(str(self.state))
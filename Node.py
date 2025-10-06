from puzzle_game import Board
from typing import List, Optional
class Node:
    """
    Representa um nó na árvore de busca para o 8-puzzle.
    
    Atributos:
        state: Board atual
        action: Movimento que levou a este estado ('UP', 'DOWN', etc.)
        parent: Nó pai
        cost: Custo acumulado (profundidade)
    """
    
    def __init__(self, state: Board, action: Optional[str] = None, parent: Optional['Node'] = None):
        self.state = state.copy()  # copia para evitar mutações
        self.action = action
        self.parent = parent
        if parent is not None:
            self.cost = parent.cost + 1
        else:
            self.cost = 0

    def path(self) -> list:
        """Retorna a sequência de nós desde a raiz até este nó"""
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return list(reversed(p))
    
    def __eq__(self, other) -> bool:
        """Verifica igualdade de estados"""
        return isinstance(other, Node) and self.state == other.state
    
    def __hash__(self) -> int:
        """Permite uso em sets/dicionários"""
        return hash(self.state)
  
    def __str__(self):
        return f"Node(cost={self.cost}, action={self.action})\n{self.state}"
    

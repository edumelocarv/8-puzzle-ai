from typing import List, Optional
from puzzle_game import Board
import heapq
import itertools
counter = itertools.count()  # contador global


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
    


def heuristic(board: Board) -> int:
    """Distância de Manhattan — soma das distâncias das peças até suas posições corretas."""
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1)
    }
    
    distance = 0
    for i in range(3):
        for j in range(3):
            value = board.state[i][j]
            if value != 0:  # ignora o espaço vazio
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

# ==================== Busca Gulosa ====================

# ==================== Busca Gulosa ====================
def greedy_best_first_search_with_loop(initial_board: Board) -> Optional[tuple]:
    """
    Resolve o 8-puzzle usando busca gulosa (Greedy Best-First Search).

    Retorna:
        - Se encontrar solução: (movimentos, número de movimentos, nós_visitados, nós_finais)
        - Se entrar em loop: (None, custo_ate_loop, nós_visitados, nós_finais)
        - None se não houver solução.
    """
    root = Node(initial_board)
    if root.state.is_goal_state():
        return [], 0, 1, [root.state]  # já resolvido

    frontier = []
    heapq.heappush(frontier, (heuristic(root.state), next(counter), root))
    explored = set()
    nodes_visited = 0
    final_nodes = []

    while frontier:
        _, _, current_node = heapq.heappop(frontier)
        nodes_visited += 1  # contamos o nó expandido

        state_str = str(current_node.state)
        if state_str in explored:
            # Loop detectado
            return None, current_node.cost, nodes_visited, final_nodes

        explored.add(state_str)

        if current_node.state.is_goal_state():
            path = current_node.path()
            moves = [node.action for node in path if node.action is not None]
            return moves, len(moves), nodes_visited, final_nodes

        possible_moves = current_node.state.get_possible_moves()

        if not possible_moves:
            # Nó sem filhos possíveis (folha)
            final_nodes.append(current_node.state)

        for move in possible_moves:
            new_board = current_node.state.copy()
            new_board.move(move)
            child = Node(new_board, move, current_node)

            child_state_str = str(child.state)
            if child_state_str not in explored:
                heapq.heappush(frontier, (heuristic(child.state), next(counter), child))

    return None  # sem solução
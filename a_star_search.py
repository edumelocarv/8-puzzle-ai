"""
Implementação do algoritmo A* (A-Star) para o quebra-cabeça 8.

O algoritmo A* é uma busca informada que combina:
- g(n): custo real do caminho do estado inicial até o nó n
- h(n): estimativa heurística do custo de n até o objetivo
- f(n) = g(n) + h(n): função de avaliação total

A heurística utilizada é a Distância de Manhattan, que é admissível e consistente.
"""

import heapq
from typing import Optional, Tuple, Dict, Any, List
from Node import Node
from puzzle_game import Board


def manhattan_distance(board: Board) -> int:
    """
    Calcula a distância de Manhattan (heurística h(n)).
    
    A distância de Manhattan é a soma das distâncias de cada peça
    da sua posição atual até sua posição objetivo, considerando
    apenas movimentos horizontais e verticais.
    
    Para cada peça no tabuleiro:
    - Encontra sua posição atual (i_atual, j_atual)
    - Encontra sua posição objetivo (i_objetivo, j_objetivo)
    - Adiciona |i_atual - i_objetivo| + |j_atual - j_objetivo|
    
    Args:
        board (Board): Estado do tabuleiro atual
        
    Returns:
        int: Distância de Manhattan total (valor da heurística)
    """
    distance = 0
    
    # Mapeamento das posições objetivo para cada número
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),  # Linha 1: [1, 2, 3]
        4: (1, 0), 5: (1, 1), 6: (1, 2),  # Linha 2: [4, 5, 6]
        7: (2, 0), 8: (2, 1), 0: (2, 2)   # Linha 3: [7, 8, _]
    }
    
    # Percorre todo o tabuleiro 3x3
    for i in range(3):
        for j in range(3):
            value = board.state[i][j]
            
            # Ignora o espaço vazio (0) no cálculo da heurística
            if value != 0:
                # Posição objetivo da peça atual
                goal_i, goal_j = goal_positions[value]
                
                # Calcula distância Manhattan: |x1-x2| + |y1-y2|
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance


def board_to_list(board: Board) -> List[int]:
    """Converte Board (3x3) para lista 1D"""
    result = []
    for i in range(3):
        for j in range(3):
            result.append(board.state[i][j])
    return result


def list_to_board(state_list: List[int]) -> Board:
    """Converte lista 1D para Board (3x3)"""
    state_2d = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(state_list[i * 3 + j])
        state_2d.append(row)
    return Board(state_2d)


def create_board_successors(board_node) -> List:
    """
    Cria sucessores para nós que contêm objetos Board.
    Adapta entre Board e lista 1D para usar o generate_successors existente.
    """
    from generate_succeessors import create_successors
    
    # Converte Board para lista 1D
    state_list = board_to_list(board_node.state)
    
    # Cria nó temporário com lista 1D
    temp_node = Node(state_list, board_node.action, board_node.parent)
    
    # Gera sucessores usando a função existente
    list_successors = create_successors(temp_node)
    
    # Converte sucessores de volta para Board
    board_successors = []
    for successor in list_successors:
        board_state = list_to_board(successor.state)
        board_successor = Node(board_state, successor.action, board_node)
        board_successors.append(board_successor)
    
    return board_successors


def a_star_search(initial_board: Board) -> Optional[Tuple[Node, Dict[str, Any]]]:
    """
    Implementa o algoritmo A* para encontrar a solução ótima.
    
    O algoritmo mantém uma fronteira (heap) ordenada por f(n) = g(n) + h(n):
    - g(n): profundidade do nó (custo real do caminho)
    - h(n): distância de Manhattan (estimativa heurística)
    - f(n): custo total estimado
    
    Processo:
    1. Inicializa com o estado inicial na fronteira
    2. Remove o nó com menor f(n) da fronteira
    3. Se é o objetivo, retorna a solução
    4. Senão, expande o nó gerando sucessores
    5. Para cada sucessor, calcula f(n) e adiciona à fronteira
    6. Repete até encontrar solução ou esgotar fronteira
    
    Args:
        initial_board (Board): Estado inicial do tabuleiro
        
    Returns:
        Tuple[Node, dict] ou None: (nó solução, métricas) ou None se não encontrar
    """
    # Cria o nó inicial
    initial_node = Node(initial_board, "", None)
    
    # Verifica se já é o estado objetivo
    if initial_board.is_goal_state():
        return initial_node, {
            "visited_nodes": 0,
            "explored_states": 0,
            "max_frontier": 0,
            "solution_depth": 0
        }
    
    # Inicializa estruturas de dados
    frontier = []  # Min-heap: (f_cost, g_cost, counter, node)
    explored = set()  # Estados já explorados
    counter = 1  # Para desempate no heap (ordem FIFO)
    
    # Adiciona nó inicial à fronteira
    h_initial = manhattan_distance(initial_board)
    heapq.heappush(frontier, (h_initial, 0, 0, initial_node))
    
    # Métricas para análise
    visited_nodes = 0
    max_frontier = 1
    
    # Loop principal do A*
    while frontier:
        # Atualiza métrica da fronteira
        max_frontier = max(max_frontier, len(frontier))
        
        # Remove nó com menor f(n) da fronteira
        f_cost, g_cost, _, current_node = heapq.heappop(frontier)
        visited_nodes += 1
        
        # Verifica se já foi explorado (evita ciclos)
        current_state_hash = hash(str(current_node.state.state))
        if current_state_hash in explored:
            continue
        
        # Marca como explorado
        explored.add(current_state_hash)
        
        # Verifica se chegou ao objetivo
        if current_node.state.is_goal_state():
            return current_node, {
                "visited_nodes": visited_nodes,
                "explored_states": len(explored),
                "max_frontier": max_frontier,
                "solution_depth": g_cost
            }
        
        # Gera sucessores do nó atual
        successors = create_board_successors(current_node)
        
        # Processa cada sucessor
        for successor in successors:
            successor_hash = hash(str(successor.state.state))
            
            # Apenas adiciona se não foi explorado
            if successor_hash not in explored:
                # Calcula custos
                g = g_cost + 1  # Custo do caminho (profundidade)
                h = manhattan_distance(successor.state)  # Heurística
                f = g + h  # Custo total f(n) = g(n) + h(n)
                
                # Adiciona à fronteira
                heapq.heappush(frontier, (f, g, counter, successor))
                counter += 1
    
    # Não encontrou solução
    return None, {
        "visited_nodes": visited_nodes,
        "explored_states": len(explored),
        "max_frontier": max_frontier,
        "solution_depth": -1
    }


def print_a_star_step(node: Node, g_cost: int, h_cost: int, f_cost: int):
    """
    Função auxiliar para debug - mostra detalhes de cada passo do A*.
    
    Args:
        node (Node): Nó atual
        g_cost (int): Custo g(n)
        h_cost (int): Custo h(n)  
        f_cost (int): Custo f(n)
    """
    print(f"\n--- Passo A* ---")
    print(f"Ação: {node.action}")
    print(f"g(n) = {g_cost} (profundidade)")
    print(f"h(n) = {h_cost} (Manhattan)")
    print(f"f(n) = {f_cost} (g+h)")
    print("Estado:")
    for row in node.state.state:
        print(f"  {row}")


if __name__ == "__main__":
    # Teste básico do A*
    from puzzle_game import Board
    
    # Cria um estado de teste
    test_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    board = Board(test_state)
    print("Estado inicial:")
    for row in board.state:
        print(f"  {row}")
    
    print(f"\nDistância de Manhattan: {manhattan_distance(board)}")
    print(f"É solvível: {board.is_solvable()}")
    
    if board.is_solvable():
        print("\nExecutando A*...")
        result = a_star_search(board)
        
        if result[0]:
            solution, metrics = result
            path = solution.path()
            print(f"\nSolução encontrada!")
            print(f"Passos: {len(path) - 1}")
            print(f"Nós visitados: {metrics['visited_nodes']}")
            print(f"Estados explorados: {metrics['explored_states']}")
            print(f"Tamanho máximo da fronteira: {metrics['max_frontier']}")
            
            print("\nCaminho da solução:")
            for i, node in enumerate(path):
                if i == 0:
                    print(f"Inicial: {node.action if node.action else 'START'}")
                else:
                    print(f"Passo {i}: {node.action}")
        else:
            print("Nenhuma solução encontrada!")
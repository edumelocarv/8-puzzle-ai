"""
Arquivo principal para executar o jogo do 8 (8-puzzle)
"""

from interface import main
from puzzle_game import Board
from heuristic_search import greedy_best_first_search_with_loop
#['RIGHT', 'DOWN', 'RIGHT']
# Estado inicial embaralhado
initial_state = [



 
        [3, 0, 1],
    [8, 6, 4],
    [5, 2,7]



]


"""
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]

    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]

        [1, 2, 3],
    [0, 4, 6],
    [7, 5, 8]

    [2, 0, 3],
    [1, 4, 6],
    [7, 5, 8]

        [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]

        [2, 3, 0],
    [1, 5, 6],
    [7, 4, 8]

    
        [3, 0, 1],
    [8, 6, 4],
    [5, 2,7]





"""


board = Board(initial_state)

result = greedy_best_first_search_with_loop(board)

if result:
    moves, num_moves, visited, finals = result
    print("Movimentos para resolver:", moves)
    print("Número de movimentos:", num_moves)
    print("Nós visitados:", visited)
    print("Nós finais:", len(finals))
else:
    print("Não foi possível encontrar solução com Greedy BFS.")
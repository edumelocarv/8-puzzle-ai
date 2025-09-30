"""
Testes para validar as funcionalidades da classe Board
"""

from puzzle_game import Board


def test_board_creation():
    """Testa a criação do tabuleiro"""
    print("=== Teste: Criação do Tabuleiro ===")
    
    # Tabuleiro padrão (estado final)
    board = Board()
    print("Tabuleiro inicial (estado final):")
    print(board)
    print(f"É estado final? {board.is_goal_state()}")
    print(f"É solvível? {board.is_solvable()}")
    print()


def test_movements():
    """Testa os movimentos do tabuleiro"""
    print("=== Teste: Movimentos ===")
    
    board = Board()
    print("Estado inicial:")
    print(board)
    print(f"Posição vazia: {board.empty_pos}")
    print(f"Movimentos possíveis: {board.get_possible_moves()}")
    
    # Teste de movimento UP
    print("\nMovendo UP:")
    success = board.move('UP')
    print(f"Movimento realizado: {success}")
    print(board)
    print(f"Nova posição vazia: {board.empty_pos}")
    print()


def test_piece_movement():
    """Testa movimento de peças específicas"""
    print("=== Teste: Movimento de Peças ===")
    
    board = Board()
    print("Estado inicial:")
    print(board)
    
    # Tenta mover a peça 8 (que está ao lado do espaço vazio)
    print("\nTentando mover peça na posição (2,1) - número 8:")
    success = board.move_piece(2, 1)
    print(f"Movimento realizado: {success}")
    print(board)
    print()


def test_shuffle():
    """Testa o embaralhamento"""
    print("=== Teste: Embaralhamento ===")
    
    board = Board()
    print("Estado antes do embaralhamento:")
    print(board)
    
    board.shuffle(20)
    print("\nEstado após embaralhar:")
    print(board)
    print(f"É solvível? {board.is_solvable()}")
    print()


def test_custom_state():
    """Testa definição de estado personalizado"""
    print("=== Teste: Estado Personalizado ===")
    
    # Estado quase resolvido
    custom_state = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
    
    board = Board(custom_state)
    print("Estado personalizado:")
    print(board)
    print(f"É estado final? {board.is_goal_state()}")
    print(f"É solvível? {board.is_solvable()}")
    print(f"Movimentos possíveis: {board.get_possible_moves()}")
    print()


def test_solvability():
    """Testa verificação de solvibilidade"""
    print("=== Teste: Solvibilidade ===")
    
    # Estado solvível
    solvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    # Estado não solvível
    unsolvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    
    board1 = Board(solvable_state)
    board2 = Board(unsolvable_state)
    
    print("Estado solvível:")
    print(board1)
    print(f"É solvível? {board1.is_solvable()}")
    
    print("\nEstado não solvível:")
    print(board2)
    print(f"É solvível? {board2.is_solvable()}")
    print()


def test_copy_and_equality():
    """Testa cópia e igualdade de tabuleiros"""
    print("=== Teste: Cópia e Igualdade ===")
    
    board1 = Board()
    board2 = board1.copy()
    
    print("Tabuleiro original:")
    print(board1)
    print("\nTabuleiro copiado:")
    print(board2)
    print(f"São iguais? {board1 == board2}")
    
    # Modifica a cópia
    board2.move('UP')
    print("\nApós mover a cópia:")
    print("Original:")
    print(board1)
    print("Cópia:")
    print(board2)
    print(f"São iguais? {board1 == board2}")
    print()


def run_all_tests():
    """Executa todos os testes"""
    print("🧪 EXECUTANDO TESTES DO PUZZLE 8 🧪\n")
    
    test_board_creation()
    test_movements()
    test_piece_movement()
    test_shuffle()
    test_custom_state()
    test_solvability()
    test_copy_and_equality()
    
    print("✅ TODOS OS TESTES CONCLUÍDOS!")


if __name__ == "__main__":
    run_all_tests()
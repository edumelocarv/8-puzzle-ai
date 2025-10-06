"""
Arquivo principal para executar o jogo do 8 (8-puzzle)
"""

from interface import main

if __name__ == "__main__":
    print("Iniciando o Puzzle 8...")
    print("Use a interface gráfica para:")
    print("- Clicar nas peças para movê-las")
    print("- Embaralhar o tabuleiro")
    print("- Definir estados personalizados")
    print("- Gerar estados aleatórios solvíveis")
    print("\nObjetivo: Organize as peças na ordem:")
    print("1 2 3")
    print("4 5 6")
    print("7 8  ")
    print("\nAbrindo interface...")
    
    main()
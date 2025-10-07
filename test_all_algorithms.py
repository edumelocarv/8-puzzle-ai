import time
from Node import Node
from breath_first_search import bfs
from deep_first_search import dfs
from a_star_search import a_star_search
from heuristic_search import greedy_best_first_search_with_loop
from puzzle_game import Board

class TestAllAlgorithms:
    def __init__(self):
        # 5 casos de teste com diferentes dificuldades (todos solúveis) - formato matriz 3x3
        self.test_cases = [
            ("Resolvido (0 movimentos)", [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]),
            ("Muito fácil (2 movimentos)", [
                [1, 2, 3],
                [4, 5, 6],
                [0, 7, 8]
            ]),
            ("Médio (6 movimentos)", [
                [1, 2, 3],
                [5, 0, 6],
                [4, 7, 8]
            ]),
            ("Difícil (14 movimentos)", [
                [2, 5, 3],
                [1, 0, 6],
                [4, 7, 8]
            ]),
            ("Muito difícil (31 movimentos)", [
                [8, 6, 7],
                [2, 5, 4],
                [3, 0, 1]
            ])
        ]
        
        # Algoritmos disponíveis
        self.algorithms = {
            "BFS": self.test_bfs,
            "DFS": self.test_dfs,
            "Busca Heurística": self.test_heuristic,
            "A*": self.test_astar
        }
    
    def matrix_to_list(self, matrix):
        """Converte matriz 3x3 para lista 1D"""
        result = []
        for row in matrix:
            for element in row:
                result.append(element)
        return result
    
    def matrix_to_board(self, matrix):
        """Converte matriz 3x3 para objeto Board"""
        board = Board(matrix)
        return board
    
    def test_bfs(self, initial_matrix):
        """Testa o algoritmo BFS"""
        try:
            # Converte matriz para lista 1D para o BFS
            initial_list = self.matrix_to_list(initial_matrix)
            root = Node(initial_list, None, None)
            
            start_time = time.perf_counter()
            result = bfs(root)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if result is None or result[0] is None:
                return {
                    "success": False,
                    "time": execution_time,
                    "error": "Nenhuma solução encontrada"
                }
            
            solve_node, visited_nodes, explored_states_len = result
            path = solve_node.path()
            solution_depth = len(path) - 1
            
            # Extrai movimentos
            moves = [node.action for node in path[1:] if node.action]
            
            return {
                "success": True,
                "time": execution_time,
                "solution_depth": solution_depth,
                "visited_nodes": visited_nodes,
                "explored_states": explored_states_len,
                "moves": moves,
                "path": path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": 0
            }
    
    def test_dfs(self, initial_matrix):
        """Testa o algoritmo DFS"""
        try:
            # Converte matriz para lista 1D para o DFS
            initial_list = self.matrix_to_list(initial_matrix)
            root = Node(initial_list, None, None)
            
            start_time = time.perf_counter()
            result = dfs(root)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if result is None or result[0] is None:
                return {
                    "success": False,
                    "time": execution_time,
                    "error": "Nenhuma solução encontrada"
                }
            
            solve_node, visited_nodes, explored_states_len = result
            path = solve_node.path()
            solution_depth = len(path) - 1
            
            # Extrai movimentos
            moves = [node.action for node in path[1:] if node.action]
            
            return {
                "success": True,
                "time": execution_time,
                "solution_depth": solution_depth,
                "visited_nodes": visited_nodes,
                "explored_states": explored_states_len,
                "moves": moves,
                "path": path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": 0
            }
    
    def test_heuristic(self, initial_matrix):
        """Testa a Busca Heurística"""
        try:
            # Converte matriz para Board para a busca heurística
            board = self.matrix_to_board(initial_matrix)
            
            start_time = time.perf_counter()
            moves, steps = greedy_best_first_search_with_loop(board)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if moves is None:
                return {
                    "success": False,
                    "time": execution_time,
                    "error": f"Algoritmo entrou em loop após {steps} movimentos"
                }
            
            if not moves:  # Já resolvido
                return {
                    "success": True,
                    "time": execution_time,
                    "solution_depth": 0,
                    "visited_nodes": steps,
                    "explored_states": steps,
                    "moves": [],
                    "path": []
                }
            
            return {
                "success": True,
                "time": execution_time,
                "solution_depth": len(moves),
                "visited_nodes": steps,
                "explored_states": steps,  # Aproximação
                "moves": moves,
                "path": []  # Busca heurística não retorna caminho completo
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": 0
            }
    
    def test_astar(self, initial_matrix):
        """Testa o algoritmo A*"""
        try:
            # Converte matriz para Board para o A*
            board = self.matrix_to_board(initial_matrix)
            
            start_time = time.perf_counter()
            result = a_star_search(board)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            if result is None or result[0] is None:
                return {
                    "success": False,
                    "time": execution_time,
                    "error": "Nenhuma solução encontrada"
                }
            
            solution_node, metrics = result
            path = solution_node.path()
            
            # Extrai movimentos
            moves = [node.action for node in path[1:] if node.action]
            solution_depth = len(moves)
            
            return {
                "success": True,
                "time": execution_time,
                "solution_depth": solution_depth,
                "visited_nodes": metrics['visited_nodes'],
                "explored_states": metrics['explored_states'],
                "max_frontier": metrics.get('max_frontier', 0),
                "moves": moves,
                "path": path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": 0
            }
    
    def run_single_test(self, algorithm_name, test_name, initial_matrix):
        """Executa um teste individual"""
        print(f"\n{'='*70}")
        print(f"🧪 TESTE: {algorithm_name} - {test_name}")
        print(f"{'='*70}")
        print(f"Estado inicial:")
        for row in initial_matrix:
            print(f"  {row}")
        
        if algorithm_name not in self.algorithms:
            print(f"❌ Algoritmo '{algorithm_name}' não encontrado!")
            return None
        
        result = self.algorithms[algorithm_name](initial_matrix)
        
        if result["success"]:
            print(f"✅ SUCESSO!")
            print(f"⏱️  Tempo de execução: {result['time']:.4f} segundos")
            print(f"📊 Profundidade da solução: {result['solution_depth']} movimentos")
            print(f"🔍 Nós visitados: {result['visited_nodes']}")
            print(f"💾 Estados explorados: {result['explored_states']}")
            
            if 'max_frontier' in result:
                print(f"🚀 Fronteira máxima: {result['max_frontier']}")
            
            if result['solution_depth'] > 0:
                print(f"📈 Eficiência: {result['visited_nodes']/result['solution_depth']:.2f} nós/movimento")
            
            # Mostra os primeiros movimentos
            if result.get('moves') and len(result['moves']) > 0:
                moves_str = ' → '.join(result['moves'][:10])
                if len(result['moves']) > 10:
                    moves_str += f" ... (+{len(result['moves'])-10} movimentos)"
                print(f"🛤️  Movimentos: {moves_str}")
        else:
            print(f"❌ FALHOU: {result.get('error', 'Erro desconhecido')}")
            if 'time' in result:
                print(f"⏱️  Tempo até falha: {result['time']:.4f} segundos")
        
        return result
    
    def run_algorithm_tests(self, algorithm_name):
        """Testa um algoritmo em todos os casos de teste"""
        print(f"\n{'='*80}")
        print(f"🚀 TESTANDO ALGORITMO: {algorithm_name}")
        print(f"{'='*80}")
        
        results = []
        total_time = 0
        
        for test_name, initial_matrix in self.test_cases:
            result = self.run_single_test(algorithm_name, test_name, initial_matrix)
            results.append((test_name, result))
            
            if result and result["success"]:
                total_time += result["time"]
        
        self.print_algorithm_summary(algorithm_name, results, total_time)
        return results
    
    def run_all_tests(self):
        """Executa todos os algoritmos em todos os casos de teste"""
        all_results = {}
        
        print("🌟 INICIANDO BATERIA COMPLETA DE TESTES")
        print("=" * 80)
        
        for algorithm_name in self.algorithms.keys():
            all_results[algorithm_name] = self.run_algorithm_tests(algorithm_name)
        
        # Imprime comparação final
        self.print_comparison_table(all_results)
        return all_results
    
    def run_comparison_test(self, test_index=2):
        """Compara todos os algoritmos em um caso específico"""
        if test_index >= len(self.test_cases):
            print("❌ Índice de teste inválido!")
            return
        
        test_name, initial_matrix = self.test_cases[test_index]
        print(f"\n{'='*80}")
        print(f"⚔️  COMPARAÇÃO DE ALGORITMOS - {test_name}")
        print(f"Estado inicial:")
        for row in initial_matrix:
            print(f"  {row}")
        print(f"{'='*80}")
        
        results = {}
        for algorithm_name in self.algorithms.keys():
            print(f"\n--- {algorithm_name} ---")
            result = self.algorithms[algorithm_name](initial_matrix)
            results[algorithm_name] = result
            
            if result["success"]:
                efficiency = result['visited_nodes']/max(result['solution_depth'], 1)
                print(f"⏱️ {result['time']:.4f}s | "
                      f"📊 {result['solution_depth']} mov | "
                      f"🔍 {result['visited_nodes']} nós | "
                      f"📈 {efficiency:.1f} nós/mov")
            else:
                print(f"❌ Falhou: {result.get('error', 'Erro desconhecido')}")
        
        # Ordena por tempo para mostrar ranking
        successful_results = [(name, res) for name, res in results.items() if res["success"]]
        successful_results.sort(key=lambda x: x[1]["time"])
        
        if successful_results:
            print(f"\n🏆 RANKING POR TEMPO:")
            for i, (name, res) in enumerate(successful_results, 1):
                print(f"  {i}º {name}: {res['time']:.4f}s")
        
        return results
    
    def print_algorithm_summary(self, algorithm_name, results, total_time):
        """Imprime resumo de um algoritmo"""
        print(f"\n📋 RESUMO - {algorithm_name}")
        print("-" * 60)
        
        successful_tests = 0
        total_moves = 0
        total_nodes = 0
        total_states = 0
        
        for test_name, result in results:
            if result and result["success"]:
                successful_tests += 1
                total_moves += result["solution_depth"]
                total_nodes += result["visited_nodes"]
                total_states += result["explored_states"]
        
        print(f"✅ Testes bem-sucedidos: {successful_tests}/{len(results)}")
        print(f"⏱️  Tempo total: {total_time:.4f} segundos")
        
        if successful_tests > 0:
            print(f"📊 Média de movimentos: {total_moves/successful_tests:.1f}")
            print(f"🔍 Média de nós visitados: {total_nodes/successful_tests:.1f}")
            print(f"💾 Média de estados explorados: {total_states/successful_tests:.1f}")
            print(f"📈 Eficiência média: {(total_nodes/max(total_moves, 1)):.1f} nós/movimento")
    
    def print_comparison_table(self, all_results):
        """Imprime tabela comparativa final"""
        print(f"\n{'='*90}")
        print("📊 TABELA COMPARATIVA COMPLETA")
        print(f"{'='*90}")
        
        # Cabeçalho
        header = f"{'Algoritmo':<18} | {'Caso':<25} | {'Tempo (s)':<10} | {'Movs':<6} | {'Nós':<8} | {'Estados':<8}"
        print(header)
        print("-" * len(header))
        
        for algorithm_name, test_results in all_results.items():
            for test_name, result in test_results:
                if result and result["success"]:
                    print(f"{algorithm_name:<18} | {test_name:<25} | "
                          f"{result['time']:<10.4f} | {result['solution_depth']:<6} | "
                          f"{result['visited_nodes']:<8} | {result['explored_states']:<8}")
                else:
                    error_msg = result.get('error', 'Falhou')[:15] if result else 'Erro'
                    print(f"{algorithm_name:<18} | {test_name:<25} | {'FALHOU':<10} | {'-':<6} | {'-':<8} | {error_msg:<8}")
        
        # Estatísticas gerais por algoritmo
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print("-" * 60)
        
        for algorithm_name, test_results in all_results.items():
            successful = [r for _, r in test_results if r and r["success"]]
            if successful:
                avg_time = sum(r["time"] for r in successful) / len(successful)
                avg_moves = sum(r["solution_depth"] for r in successful) / len(successful)
                avg_nodes = sum(r["visited_nodes"] for r in successful) / len(successful)
                
                print(f"{algorithm_name:<15}: {len(successful)}/5 sucessos | "
                      f"Tempo médio: {avg_time:.4f}s | "
                      f"Movimentos médios: {avg_moves:.1f} | "
                      f"Nós médios: {avg_nodes:.1f}")

def main():
    """Função principal para executar os testes"""
    tester = TestAllAlgorithms()
    
    print("🧩 SISTEMA COMPLETO DE TESTES PARA ALGORITMOS DO 8-PUZZLE")
    print("=" * 70)
    
    while True:
        print("\n📋 OPÇÕES DISPONÍVEIS:")
        print("1. 🚀 Executar TODOS os algoritmos em TODOS os casos")
        print("2. 🎯 Testar algoritmo específico")
        print("3. ⚔️  Comparar algoritmos em caso específico")
        print("4. 📊 Teste rápido (caso médio)")
        print("5. 📋 Listar casos de teste")
        print("6. ❌ Sair")
        
        choice = input("\n👉 Escolha uma opção (1-6): ").strip()
        
        if choice == "1":
            tester.run_all_tests()
            
        elif choice == "2":
            print("\n🔧 ALGORITMOS DISPONÍVEIS:")
            algorithms = list(tester.algorithms.keys())
            for i, algo in enumerate(algorithms):
                print(f"  {i}: {algo}")
            
            try:
                algo_idx = int(input("\n👉 Digite o número do algoritmo (0-3): "))
                if 0 <= algo_idx < len(algorithms):
                    tester.run_algorithm_tests(algorithms[algo_idx])
                else:
                    print("❌ Número inválido!")
            except ValueError:
                print("❌ Por favor, digite um número válido!")
                
        elif choice == "3":
            print("\n📋 CASOS DE TESTE DISPONÍVEIS:")
            for i, (name, matrix) in enumerate(tester.test_cases):
                print(f"  {i}: {name}")
                for row in matrix:
                    print(f"     {row}")
                print()
            
            try:
                test_idx = int(input("\n👉 Digite o número do caso (0-4): "))
                tester.run_comparison_test(test_idx)
            except ValueError:
                print("❌ Por favor, digite um número válido!")
                
        elif choice == "4":
            tester.run_comparison_test(2)  # Caso médio
            
        elif choice == "5":
            print(f"\n📋 CASOS DE TESTE ({len(tester.test_cases)} disponíveis):")
            for i, (name, matrix) in enumerate(tester.test_cases):
                print(f"  {i}: {name}")
                print(f"     Estado:")
                for row in matrix:
                    print(f"       {row}")
                print()
                
        elif choice == "6":
            print("👋 Encerrando testes. Até logo!")
            break
            
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
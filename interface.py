"""
Interface gráfica para o jogo do 8 (8-puzzle)
Permite ao usuário interagir com o tabuleiro e definir estados iniciais.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import List, Optional
import random
from breath_first_search import bfs, backtracking
from Node import Node
from puzzle_game import Board

from a_star_search import a_star_search
from deep_first_search import dfs


class PuzzleGUI:
    """Interface gráfica para o puzzle 8"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Puzzle 8 - Jogo do Quebra-Cabeça")
        self.root.geometry("850x960")
        self.root.resizable(False, False)
        self.current_solution = list()
        # Estado do jogo
        self.board = Board()
        
        
        # Cores
        self.colors = {
            'background': '#f0f0f0',
            'button': "#ffffff",
            'button_hover': '#d0d0d0',
            'empty': '#f8f8f8',
            'piece': '#2c3e50',
            'piece_text': "#000000"
        }
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Jogos dos 8",
            font=("Arial", 18, "bold"),
            bg=self.colors['background'],
            fg="black"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame do tabuleiro
        self.board_frame = tk.Frame(main_frame, bg=self.colors['background'])
        self.board_frame.pack(pady=20)
        
        # Cria os botões do tabuleiro
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    width=8,
                    height=4,
                    font=("Arial", 18, "bold"),
                    command=lambda r=i, c=j: self.on_piece_click(r, c),
                    border=3,
                    relief=tk.RAISED
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.buttons.append(row)
        
        # Frame dos controles
        controls_frame = tk.Frame(main_frame, bg=self.colors['background'])
        controls_frame.pack(pady=20)
        
        # Primeira linha de botões
        btn_shuffle = tk.Button(
            controls_frame,
            text="Embaralhar",
            font=("Arial", 12),
            bg=self.colors['button'],
            command=self.shuffle_board,
            width=18,
            height=2
        )
        btn_shuffle.grid(row=0, column=0, padx=10, pady=8)
        
        btn_reset = tk.Button(
            controls_frame,
            text="Resetar",
            font=("Arial", 12),
            bg=self.colors['button'],
            command=self.reset_board,
            width=18,
            height=2
        )
        btn_reset.grid(row=0, column=1, padx=10, pady=8)
        
        # Segunda linha - botão estado personalizado centralizado
        btn_custom = tk.Button(
            controls_frame,
            text="Estado Personalizado",
            font=("Arial", 12),
            bg=self.colors['button'],
            command=self.set_custom_state,
            width=40,
            height=2
        )
        btn_custom.grid(row=1, column=0, columnspan=2, padx=10, pady=8)
        
        # Terceira linha - label do método de resolução
        method_label = tk.Label(
            controls_frame,
            text="Método de Resolução:",
            font=("Arial", 12),
            bg=self.colors['background']
        )
        method_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0))
        
        # Quarta linha - combobox do método de resolução
        # Lista de métodos disponíveis
        self.solving_methods = [
            "Busca em Largura (BFS)",
            "Busca em Profundidade (DFS)",
            "Busca Heurística",
            "A*"
        ]
        
        self.method_var = tk.StringVar(value=self.solving_methods[0])
        
        self.method_combobox = ttk.Combobox(
            controls_frame,
            textvariable=self.method_var,
            values=self.solving_methods,
            state="readonly",
            width=38,
            font=("Arial", 10)
        )
        self.method_combobox.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10))
        
        # Quinta linha - botão resolver
        btn_solve = tk.Button(
            controls_frame,
            text="Resolver",
            font=("Arial", 12, "bold"),
            bg="#2e7d32",
            fg="black",
            command=self.solve_puzzle,
            width=40,
            height=2
        )
        btn_solve.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # Frame de informações
        info_frame = tk.Frame(main_frame, bg=self.colors['background'])
        info_frame.pack(pady=10)
        
        # Labels de informação
        self.status_label = tk.Label(
            info_frame,
            text="Estado: Jogando",
            font=("Arial", 12),
            bg=self.colors['background']
        )
        self.status_label.pack()
        
        self.moves_label = tk.Label(
            info_frame,
            text="Movimentos: 0",
            font=("Arial", 10),
            bg=self.colors['background']
        )
        self.moves_label.pack()
        
        self.solvable_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            bg=self.colors['background']
        )
        self.solvable_label.pack()
        
        # Contador de movimentos
        self.move_count = 0
    
    def update_display(self):
        """Atualiza a exibição do tabuleiro"""
        for i in range(3):
            for j in range(3):
                value = self.board.state[i][j]
                btn = self.buttons[i][j]
                
                if value == 0:
                    # Espaço vazio
                    btn.config(
                        text="",
                        bg=self.colors['empty'],
                        fg="black",
                        relief=tk.SUNKEN,
                        border=2
                    )
                else:
                    # Peça numerada
                    btn.config(
                        text=str(value),
                        bg=self.colors['piece'],
                        fg=self.colors['piece_text'],
                        relief=tk.RAISED,
                        border=3
                    )
        
        # Atualiza informações
        if self.board.is_goal_state():
            self.status_label.config(text="Estado: RESOLVIDO!", fg="green")
        else:
            self.status_label.config(text="Estado: Jogando", fg="black")
        
        self.moves_label.config(text=f"Movimentos: {self.move_count}")
        
        # Verifica se é solvível
        solvable = self.board.is_solvable()
        solvable_text = "✓ Solvível" if solvable else "✗ Não solvível"
        solvable_color = "green" if solvable else "red"
        self.solvable_label.config(text=solvable_text, fg=solvable_color)
    
    def on_piece_click(self, row: int, col: int):
        """Manipula o clique em uma peça do tabuleiro"""
        if self.board.state[row][col] == 0:
            return  # Não pode clicar no espaço vazio
        
        # Tenta mover a peça
        if self.board.move_piece(row, col):
            self.move_count += 1
            self.update_display()
            
            if self.board.is_goal_state():
                messagebox.showinfo(
                    "Parabéns!", 
                    f"Você resolveu o puzzle em {self.move_count} movimentos!"
                )
    
    def shuffle_board(self):
        """Embaralha o tabuleiro"""
        self.board.shuffle(random.randint(50, 200))
        self.move_count = 0
        self.update_display()
    
    def reset_board(self):
        """Reseta o tabuleiro para o estado final"""
        self.board.reset_to_goal()
        self.move_count = 0
        self.update_display()
    
    def set_custom_state(self):
        """Permite ao usuário definir um estado personalizado"""
        dialog = CustomStateDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            if self.board.set_state(dialog.result):
                self.move_count = 0
                self.update_display()
            else:
                messagebox.showerror("Erro", "Estado inválido! Certifique-se de usar os números 0-8 exatamente uma vez.")
    def play_solution(self, moves, index=0):
        if index >= len(moves):
            return
        self.board.move(moves[index])
        self.move_count += 1  # Incrementa ANTES de update_display
        self.update_display()
        self.root.after(300, lambda: self.play_solution(moves, index + 1))             
    
    def solve_puzzle(self):
        """Resolve o puzzle usando o método selecionado"""
        if self.board.is_goal_state():
            print("\n" + "="*50)
            print("O puzzle já está no estado final!")
            print("="*50)
            return
        
        if not self.board.is_solvable():
            print("\n" + "="*50)
            print("AVISO: Este estado do puzzle não pode ser resolvido!")
            print("="*50)
            return
        
        selected_method = self.solving_methods.index(self.method_var.get()) 
        
        if selected_method == 0:
            state_board_in_list = list()
            self.current_solution = list()
            #PQ IMPLEMENTEI EM FORMATO APENAS DE LISTA N LISTA DE LISTAS
            for i in range(3):
                for j in range(3):
                    state_board_in_list.append(self.board.state[i][j])
            
            root = Node(state_board_in_list, None, None)
            solve_node, node_visited, list_explored_nodes_len = bfs(root)
            if not solve_node:
                print("\n" + "="*50)
                print("ERRO: BFS não encontrou uma solução para esse tabuleiro")
                print("="*50)
                return
            list_backtracking_nodes = solve_node.path()
            for node in list_backtracking_nodes:
                self.current_solution.append(node.action)
            
            # Mostra informações sobre a solução no console
            print("\n" + "="*50)
            print("BFS encontrou solução!")
            print("="*50)
            print(f"Passos da solução: {len(self.current_solution)}")
            print(f"Nós visitados: {node_visited}")
            print(f"Estados explorados: {list_explored_nodes_len}")
            print("\nReproduzindo solução...")
            print("="*50)
            
            self.move_count = 0    
            self.play_solution(self.current_solution)
            messagebox.showinfo("RESULTADOS",f"Passos da solução: {len(self.current_solution)}\nNós visitados: {node_visited}\nEstados explorados: {list_explored_nodes_len}\n")
        if selected_method == 1: # DFS
            state_board_in_list = list()
            self.current_solution = list()
            for i in range(3):
                for j in range(3):
                    state_board_in_list.append(self.board.state[i][j])
            root = Node(state_board_in_list)
            solve_node, visited_nodes, list_explored_nodes_len = dfs(root)
            list_backtracking_nodes = solve_node.path()
            for node in list_backtracking_nodes:
                self.current_solution.append(node.action)
            self.move_count = 0
            self.play_solution(self.current_solution)
            pass
        if selected_method == 2:
            from heuristic_search import greedy_best_first_search_with_loop
            moves, num_moves, visited, finals = greedy_best_first_search_with_loop(self.board)
            if moves is None:
                messagebox.showerror(f"AVISO: Busca Heurística entrou em loop após {num_moves} movimentos.")
                return
            elif not moves:
                print("\n" + "="*50)
                print("O puzzle já estava resolvido!")
                print("="*50)
                return
            self.move_count = 0
            self.play_solution(moves)
            messagebox.showinfo("RESULTADOS",f"Passos da solução: {num_moves}\nNós visitados: {visited}\nEstados explorados: {finals}\n")
            pass
        if selected_method == 3: # A*
            # Executa o algoritmo A*
            result = a_star_search(self.board)
            
            if result is None or result[0] is None:
                print("\n" + "="*50)
                print("ERRO: O algoritmo A* não encontrou uma solução para este tabuleiro!")
                print("="*50)
                return
            
            # Extrai a solução e métricas
            solution_node, metrics = result
            solution_path = solution_node.path()
            
            # Converte o caminho de nós para lista de ações
            moves = []
            for node in solution_path[1:]:  # Pula o estado inicial
                if node.action:
                    moves.append(node.action)
            
            if not moves:
                print("\n" + "="*50)
                print("O puzzle já estava no estado final!")
                print("="*50)
                return
            
            # Reproduz a solução
            self.move_count = 0
            self.play_solution(moves)
            messagebox.showinfo("RESULTADOS",f"Passos da solução: {len(self.current_solution)}\nNós visitados: {metrics['visited_nodes']}\nEstados explorados: {metrics['explored_states']}\n")

class CustomStateDialog:
    """Dialog para definir um estado personalizado do tabuleiro"""
    
    def __init__(self, parent):
        self.result = None
        
        # Cria a janela do dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Estado Personalizado")
        self.dialog.geometry("300x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centraliza o dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Configura o dialog"""
        # Instruções
        instructions = tk.Label(
            self.dialog,
            text="Digite os números 0-8 (0 = espaço vazio):",
            font=("Arial", 12),
            pady=10
        )
        instructions.pack()
        
        # Frame para os campos de entrada
        entries_frame = tk.Frame(self.dialog)
        entries_frame.pack(pady=20)
        
        # Cria os campos de entrada 3x3
        self.entries = []
        for i in range(3):
            row = []
            for j in range(3):
                entry = tk.Entry(
                    entries_frame,
                    width=3,
                    font=("Arial", 14),
                    justify='center'
                )
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.entries.append(row)
        
        # Preenche com o estado atual (exemplo)
        example_state = [
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ]
        
        for i in range(3):
            for j in range(3):
                self.entries[i][j].insert(0, str(example_state[i][j]))
        
        # Botões
        buttons_frame = tk.Frame(self.dialog)
        buttons_frame.pack(pady=20)
        
        ok_button = tk.Button(
            buttons_frame,
            text="OK",
            command=self.ok_clicked,
            width=10
        )
        ok_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.cancel_clicked,
            width=10
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Exemplo
        example_label = tk.Label(
            self.dialog,
            text="Exemplo mostrado: estado quase resolvido",
            font=("Arial", 9),
            fg="gray"
        )
        example_label.pack(pady=(10, 0))
    
    def ok_clicked(self):
        """Manipula o clique no botão OK"""
        try:
            # Coleta os valores dos campos
            state = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = int(self.entries[i][j].get().strip())
                    if value < 0 or value > 8:
                        raise ValueError("Números devem estar entre 0 e 8")
                    row.append(value)
                state.append(row)
            
            # Verifica se todos os números 0-8 estão presentes
            numbers = []
            for row in state:
                numbers.extend(row)
            
            if sorted(numbers) != list(range(9)):
                raise ValueError("Deve conter exatamente os números 0-8")
            
            self.result = state
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")
    
    def cancel_clicked(self):
        """Manipula o clique no botão Cancelar"""
        self.dialog.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
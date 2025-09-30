"""
Interface gráfica para o jogo do 8 (8-puzzle)
Permite ao usuário interagir com o tabuleiro e definir estados iniciais.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Optional
import random

from puzzle_game import Board


class PuzzleGUI:
    """Interface gráfica para o puzzle 8"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Puzzle 8 - Jogo do Quebra-Cabeça")
        self.root.geometry("650x750")
        self.root.resizable(False, False)
        
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
        
        # Terceira linha - botão resolver
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
        btn_solve.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # Frame de informações
        info_frame = tk.Frame(main_frame, bg=self.colors['background'])
        info_frame.pack(pady=20)
        
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
            self.status_label.config(text="Estado: RESOLVIDO! 🎉", fg="green")
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
    

    
    def solve_puzzle(self):
        """Placeholder para função de resolução (será implementada posteriormente)"""
        messagebox.showinfo(
            "Em desenvolvimento"
        )


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
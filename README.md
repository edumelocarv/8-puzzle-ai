# Puzzle 8 - Jogo do Quebra-Cabeça

Este projeto implementa uma solução completa para o jogo do 8 (8-puzzle) em Python, incluindo interface gráfica e algoritmos de busca para resolução automática.

## Descrição do Projeto

O Puzzle 8 é um quebra-cabeça que consiste em um tabuleiro 3x3 com 8 peças numeradas (1-8) e um espaço vazio. O objetivo é reorganizar as peças para alcançar o estado final:

```
1 2 3
4 5 6
7 8  
```

## Estrutura do Projeto

- `main.py` - Arquivo principal para executar o jogo
- `puzzle_game.py` - Classes principais do jogo (Board)
- `interface.py` - Interface gráfica usando tkinter
- `algorithms.py` - Algoritmos de busca (será implementado posteriormente)

## Funcionalidades Implementadas

### Interface Gráfica
- ✅ Visualização do tabuleiro 3x3
- ✅ Clique nas peças para movimentá-las
- ✅ Botão para embaralhar o tabuleiro
- ✅ Botão para resetar ao estado final
- ✅ Definição de estado personalizado
- ✅ Contador de movimentos
- ✅ Verificação se o estado é solvível
- ✅ Detecção do estado final (vitória)

### Classe Board
- ✅ Representação do estado do tabuleiro
- ✅ Validação de movimentos
- ✅ Verificação do estado final
- ✅ Embaralhamento inteligente
- ✅ Verificação de solvibilidade
- ✅ Cópia e comparação de estados

## Como Usar

1. Execute o programa:
```bash
python main.py
```

2. Use a interface para:
   - **Jogar manualmente**: Clique nas peças adjacentes ao espaço vazio para movê-las
   - **Embaralhar**: Clique em "Embaralhar" para gerar um novo puzzle
   - **Resetar**: Clique em "Resetar" para voltar ao estado final
   - **Estado Personalizado**: Defina seu próprio estado inicial
   - **Estado Aleatório**: Gere um estado aleatório solvível

## Algoritmos a Serem Implementados

### Busca Cega
- [ ] Busca em Largura (BFS)
- [ ] Busca em Profundidade (DFS)

### Busca Heurística
- [ ] Busca Gulosa (Greedy Search)
- [ ] A* (A-star)

### Heurísticas Planejadas
- Distância de Manhattan
- Número de peças fora do lugar
- Heurística personalizada da equipe

## Métricas de Comparação

O sistema irá comparar os algoritmos baseado em:
- **Custo do caminho**: Número de movimentos para a solução
- **Custo de espaço**: Número de nós na fronteira
- **Tempo de execução**: Tempo para encontrar a solução
- **Nós gerados**: Total de nós explorados
- **Profundidade da solução**: Profundidade da solução encontrada
- **Profundidade máxima**: Maior profundidade atingida
- **Admissibilidade**: Se a heurística é admissível
- **Otimalidade**: Se encontra a solução ótima
- **Completude**: Se sempre encontra solução quando existe

## Requisitos

- Python 3.6+
- tkinter (geralmente incluído com Python)

## Estrutura da Classe Board

A classe `Board` oferece os seguintes métodos principais:

- `is_goal_state()`: Verifica se está no estado final
- `get_possible_moves()`: Retorna movimentos possíveis
- `move(direction)`: Move o espaço vazio
- `move_piece(row, col)`: Move uma peça específica
- `shuffle(moves)`: Embaralha o tabuleiro
- `is_solvable()`: Verifica se o estado é solvível
- `set_state(state)`: Define um novo estado

## Próximas Etapas

1. Implementação dos algoritmos de busca
2. Interface para visualização passo-a-passo das soluções
3. Métricas e comparação de desempenho
4. Relatório final com análise dos resultados

## Equipe

- Eduardo Melo (e outros membros da equipe - máximo 3 componentes)

## Status do Desenvolvimento

- [x] **Fase 1**: Estrutura básica e interface gráfica ✅
- [ ] **Fase 2**: Algoritmos de busca cega
- [ ] **Fase 3**: Algoritmos de busca heurística
- [ ] **Fase 4**: Comparação e análise de resultados
- [ ] **Fase 5**: Relatório final
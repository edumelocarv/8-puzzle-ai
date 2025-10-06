from Node import Node
from generate_succeessors import create_successors
final_state = [1,2,3,
               4,5,6,
               7,8,0]

def dfs(node: Node):
  visited_nodes = 0
  explored_states = set()
  frontier = list()
  frontier.append(node)
  explored_states.add(tuple(node.state))
  while frontier:
    actual_node = frontier.pop()
    visited_nodes += 1
    if actual_node.state == final_state:
      return (actual_node, visited_nodes, len(explored_states))
    for child in create_successors(actual_node):
      if tuple(child.state) not in explored_states:
        frontier.append(child)  
        explored_states.add(tuple(child.state))
        
if __name__ == "__main__":
  initial_board = [4,5,7,
                  8,0,1,
                  3,6,2]
  root = Node(initial_board, None, None)
  node_solve, visited_nodes, explored_states_len = dfs(root)
  for node in node_solve.path():
    print(node.state, node.action)
  print(f"Nós visitados:{visited_nodes}, \nQuantidade de estados armazenados: {explored_states_len}" )
  

from typing import List, Dict, Tuple, Set
from Node import Node
init_board = [
              1,2,3,
              4,5,6,
              7,0,8
                    ]
root = Node(init_board, None, None)

def create_successors(node: Node):
  list_valid_nodes = list()
  valid_positions = {0:((1,"RIGHT"),(3, "DOWN")), 
                     1:((0,"LEFT"),(2,"RIGHT"),(4,"DOWN")), 
                     2:((1,"LEFT"),(5,"DOWN")), 
                     3:((0,"UP"),(4,"RIGHT"),(6,"DOWN")), 
                     4:((1,"UP"),(3,"LEFT"),(5,"RIGHT"),(7,"DOWN")), 
                     5:((2,"UP"),(4,"LEFT"),(8,"DOWN")), 
                     6:((3,"UP"),(7,"RIGHT")), 
                     7:((4,"UP"),(6,"LEFT"),(8,"RIGHT")), 
                     8:((5,"UP"),(7,"LEFT"))
                     }
  current_pos = node.state.index(0)
  for pos, action in valid_positions[current_pos]:
    new_board = node.state.copy()
    aux = new_board[pos]
    new_board[pos] = new_board[current_pos]
    new_board[current_pos] = aux
    list_valid_nodes.append(Node(new_board, action, node))
  return list_valid_nodes

if __name__ == "__main__":
    for node in create_successors(root):
        print(node.state, node.action, node.cost)
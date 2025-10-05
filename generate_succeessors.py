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
  valid_positions = {0:((1,"right"),(3, "down")), 
                     1:((0,"left"),(2,"right"),(4,"down")), 
                     2:((1,"left"),(5,"down")), 
                     3:((0,"up"),(4,"right"),(6,"down")), 
                     4:((1,"up"),(3,"left"),(5,"right"),(7,"down")), 
                     5:((2,"up"),(4,"left"),(8,"down")), 
                     6:((3,"up"),(7,"right")), 
                     7:((4,"up"),(6,"left"),(8,"right")), 
                     8:((5,"up"),(7,"left"))
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
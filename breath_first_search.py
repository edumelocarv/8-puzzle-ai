from typing import List, Dict, Tuple, Set
from collections import deque
from generate_succeessors import create_successors
from Node import Node

init_board = [8,7,6,
              5,4,3,
              2,1,0]
final_state =  [
              1,2,3,
              4,5,6,
              7,8,0
                    ]

root = Node(init_board, None, None)

def bfs(node: Node):
  visit_nodes = 0
  if node.state == final_state:
    return
  fronteira = deque()
  fronteira.append(node)
  explorados = set(node.state)
  while True:
    actual_level_nodes = list()
    if not fronteira:
      return None
    while fronteira:
      actual_node = fronteira.popleft()
      if actual_node.state == final_state:
        visit_nodes += 1
        return (actual_node, visit_nodes)
      visit_nodes += 1
      actual_level_nodes.append(actual_node)
      #expand nodes
    for explo_node in actual_level_nodes:
       expand_nodes = create_successors(explo_node)
       for nodes in expand_nodes:
         node_state_tuple = tuple(nodes.state)
         if node_state_tuple not in explorados:
           fronteira.append(nodes)
           explorados.add(tuple(nodes.state))


def backtracking(node: Node):
  node_backtracking_list = list()
  if not node.parent:
    return node
  while node:
    if not node.parent:
      return node_backtracking_list
    node_backtracking_list.insert(0, node)
    node = node.parent
  
if __name__ == "__main__":
  node, visit_nodes = bfs(root)
  list_resolve = backtracking(node)
  for node in list_resolve:
    print(node.action)
  print(f"Nós visitados: {visit_nodes}")
    




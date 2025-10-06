from Node import Node
from generate_succeessors import create_successors
final_state = [1,2,3,4,5,6,7,8,0]

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
    for child in create_successors(node):
      if child.state not in explored_states:
        frontier.append(child)  
        explored_states.add(tuple(child.state))

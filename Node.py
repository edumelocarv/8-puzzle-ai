class Node: 
  def __init__(self, state, action, parent):
    self.state = state
    self.action = action
    self.parent = parent
    if parent is not None:
      self.cost = parent.cost + 1
    else:
      self.cost = 0
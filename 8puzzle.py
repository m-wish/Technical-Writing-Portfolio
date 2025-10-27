"""
 3750 Assignment 1
 Sem: Summer I 2024
 Desc: Write a program in Python to implement 8-puzzle problem using iterative
      deepening depth-first search.
 Author: Marisa Wishnowski
 Date: 13/05/2024
"""

# Class to define the state of the 3x3 puzzle.
class Puzzle:
  # Puzzle Constructor.
  # Creates a Puzzle board to the given state, keeps track of the previous state, 
  #   gives it an action to complete, keeps track of the depth.
  def __init__(self, state, parent = None, action = ""):
    self.state = state 
    self.parent = parent
    self.action = action
    self.depth = 0
    if parent:
      self.depth = parent.depth + 1 

  # to_string function to turn the state into a string.
  def to_string(self): 
    return ''.join(map(str, self.state))
  

# Checks whether a given state is valid
def isValid(state):
  if not state.isdigit():
    print(f"Non-digit input.")
    return False
  if len(state) < 9:
    print(f"Not enough numbers entered.")
    return False
  if len(state) > 9:
    print(f"Too many numbers enterted.")
    return False
  stateSet = set(state)
  validState = {'0','1','2','3','4','5','6','7','8'}
  if stateSet != validState:
    print(f"Invalid number set entered.")
    return False
  else:
    return True

# Gets initial state input from user
def getInput():
  initial = []
  inputs = input("Enter the initial state in an unbroken list (ex. 012345678): ")
  while not isValid(inputs):
    inputs = input("Re-enter: ")
  inputs = int(inputs)
  n = 9
  m = 100000000
  for i in range(n):
    initial.append(int(inputs / m))
    inputs = inputs % m
    m = int(m / 10)
  return initial

# Counts number of times the initial state of the puzzle 
#    has a higher number above a lower number (inversions).
# Returns: number of inversions.
def countInversions(puzzle):
  inversions = 0
  for i in range(len(puzzle)):
    if puzzle[i] == 0:
      continue
    for j in range(i + 1, len(puzzle)):
      if puzzle[j] == 0:
        continue 
      if puzzle[i] > puzzle[j]:
        inversions += 1 
  return inversions

# Decides if the given state is solvable or not.
# Returns: True, if num of inversions is even, false
#    if num of inversions is odd.
def isSolvable(puzzle):
  inversions = countInversions(puzzle)
  if inversions % 2 == 0:
    return True
  else:
    return False

# Returns an array of the next possible Puzzle boards given a board.
def getNeighbours(board):
  neighbours = []
  state = board.state
  zeroIndex = state.index(0)
  rows, cols = 3, 3
  lastAction = board.action

  # Helper function to make a new board with the given state, the old state, and the action 
  #  performed to reach said state, then add it to the neighbours of the old state.
  def addNeighbour(newState, action):
    newBoard = Puzzle(newState, board, action)
    neighbours.append(newBoard) 

  # Move up if rational and possible
  if lastAction != "Down" and zeroIndex >= cols:
    newState = state[:]
    newState[zeroIndex], newState[zeroIndex - cols] = newState[zeroIndex - cols], newState[zeroIndex]
    addNeighbour(newState, "Up") 
  # Move down if rational and possible
  if lastAction != "Up" and zeroIndex < len(state) - cols:
    newState = state[:]
    newState[zeroIndex], newState[zeroIndex + cols] = newState[zeroIndex + cols], newState[zeroIndex]
    addNeighbour(newState, "Down")
  # Move left if rational and possible
  if lastAction != "Right" and zeroIndex % cols != 0:
    newState = state[:] 
    newState[zeroIndex], newState[zeroIndex - 1] = newState[zeroIndex - 1], newState[zeroIndex]
    addNeighbour(newState, "Left")
  # Move right if rational and possible
  if lastAction != "Left" and (zeroIndex + 1) % cols != 0:
    newState = state[:]
    newState[zeroIndex], newState[zeroIndex + 1] = newState[zeroIndex + 1], newState[zeroIndex]
    addNeighbour(newState, "Right") 

  return neighbours

# Limited Depth first search function.
# Returns: board if board is already in goal state. If the depth of the Puzzle board has 
#  reached the depthLimit, returns nothing. Otherwise, the function gets all the possible 
#  next moves with getNeighbours, recursively calls dfs() for each neighbour, adds each 
#  neighbour to "visited" vector (if not already visited) and returns the result. If no
#  result is found, returns nothing.
def dls(board, goalState, depthLimit, visited):
  if board.state == goalState: 
    return board
  elif board.depth == depthLimit:
    return None
  else:
    neighbours = getNeighbours(board)
    for neighbour in neighbours:
      stateStr = neighbour.to_string()
      if stateStr not in visited:
        visited.add(stateStr)
        result = dls(neighbour, goalState, depthLimit, visited)
        if result:
          return result 
    return None

# Iterative deepening search.
# Calls dfs to search for the correct path from the initial state to the goal state.
#  If dfs returns nothing, the depthLimit is increased until dfs returns a 
#  result solution path. 
# Returns: Result puzzle board with the correct path from initial to goal states.
def ids(initialState, goalState): 
  depthLimit = 0
  while True:
    visited = set()
    result = dls(Puzzle(initialState), goalState, depthLimit, visited)
    if result:
      return result
    depthLimit += 1

# Prints the solution path of the given puzzle board.
# If the solution is nothing, no solution is found. Otherwise, the function
#  loops through the state and the parents of the states of the solution,
#  pushing the path into a vector and printing that vector to the screen.
def printPath(solution): 
  if not solution:
    print("Solution not found, check input and try again.")
  else:
    path = []
    moves = []
    while solution:
      path.append(solution.state)
      moves.append(solution.action)
      solution = solution.parent
    moves.reverse()
    path.reverse()

    print(f"Solution requires {len(path) - 1} moves: \n")
    for i in range(len(path)):
      if i == 0:
        print(f"Initial State:")
      if i < len(moves) and i > 0:
        print(f"Move:", moves[i])
      for j in range(0, len(path[i]), 3):
        print(" ".join(map(str, path[i][j:j + 3])))
      print()


def main():
  print(f"\n******* 8-Puzzle Solver *******\n")
  goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
  initial = getInput()
  if isSolvable(initial):
    solution = ids(initial, goal) 
    printPath(solution)
  else:
    print("\n**\nPuzzle is in an unsolvable state (odd number of inversions).\n**\n\n")
  print(f"*******************************\n")

if __name__ == "__main__":
  main()

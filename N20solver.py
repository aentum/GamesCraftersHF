import importlib
nim_module = importlib.import_module("N-to-0")

print("Number of pennies:")
N = int(input())
print("Number of pennies can be taken in one move, separated by a space:")
moves = list(map(int, input().split()))
print('Solution:')

game = nim_module.Game(moves)

# key: position, value: one of 'WIN', 'TIE', or 'LOSE'
value_dict = {}
# key: position, value: list of positions that is reachable from current position
game_graph = {}

def solver(position):
    if position in value_dict.keys():
        return value_dict[position]
    else:
        assign_value(position)
        return value_dict[position]

def assign_value(position):
    if position not in game_graph:
        traverse(position)
    if game.PrimitiveValue(position) != 'NOT_PRIMITIVE': 
        # This position is primitive, so update value_dict and we are done
        value_dict[position] = game.PrimitiveValue(position)
    else:
        child_values = []
        for child in game_graph[position]:
            if child not in value_dict:
                assign_value(child)
            if value_dict[child] == 'LOSE':
                # If there exists a losing child, we're in a winning position, and we are done
                value_dict[position] = 'WIN'
                return
            else:
                child_values.append(value_dict[child])
        if 'T' in set(child_values):
            # If there is no losing child but exists a tieing child, we're in a tieing position
            value_dict[position] = 'TIE'
        else:
            # If all children are winning, we're in a losing position
            value_dict[position] = 'LOSE'

# Traverse game graph to position without moves
def traverse(position):
    if position in game_graph:
        return
    game_graph[position] = []
    moves = game.GenerateMoves(position)
    for m in moves:
        newPos = game.DoMove(position, m)
        game_graph[position].append(newPos) 
        traverse(newPos)

for i in range(N, -1, -1):
    print(f"{i}: {solver(i)}")
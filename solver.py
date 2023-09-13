import importlib

print(f'Input the game module to solve:')
module_name = input()
game_module = importlib.import_module(module_name)
game = game_module.Game()
starting_pos = game.startingPos
print(f"Solving game: {module_name}")

primitive_states = {'WIN': 0, 'LOSE': 0, 'TIE': 0}
all_positions = {'WIN': 0, 'LOSE': 0, 'TIE': 0}

# key: position, value: one of 'WIN', 'TIE', or 'LOSE'
value_dict = {}

# We don't need to keep game graph, as we will dynamically find our next moves
# using game.GenerateMoves() function
## key: position, value: list of positions that is reachable from current position
## game_graph = {}

def solver(position):
    if position in value_dict.keys():
        return value_dict[position]
    else:
        assign_value(position)
        #return value_dict[position] -> Don't use this if I want to solve the game fully in one shot

def assign_value(position):
    global primitive_states, all_positions
    if game.PrimitiveValue(position) != 'NOT_PRIMITIVE': 
        # This position is primitive, so update value_dict and we are done
        value_dict[position] = game.PrimitiveValue(position)
        primitive_states[game.PrimitiveValue(position)] += 1
        all_positions[game.PrimitiveValue(position)] += 1
    else:
        child_values = []
        for move in game.GenerateMoves(position):
            child = game.DoMove(position, move)
            if child not in value_dict:
                assign_value(child)
            child_values.append(value_dict[child])
        if 'LOSE' in set(child_values):
            # If there exists a losing child, we're in a winning position, and we are done
            value_dict[position] = 'WIN'
            all_positions['WIN'] += 1
        elif 'TIE' in set(child_values):
            # If there is no losing child but exists a tieing child, we're in a tieing position
            value_dict[position] = 'TIE'
            all_positions['TIE'] += 1
        else:
            # If all children are winning, we're in a losing position
            value_dict[position] = 'LOSE'
            all_positions['LOSE'] += 1

# How do I generalize this to any game? 
#for i in range(N, -1, -1):
    #print(f"{i}: {solver(i)}")

solver(game.startingPos)
print(f'Primitive States: {primitive_states}')
print(f'All Position Values: {all_positions}')
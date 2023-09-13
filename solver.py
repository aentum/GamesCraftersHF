import importlib

print(f'Input the game module to solve:')
module_name = input()
game_module = importlib.import_module(module_name)
game = game_module.Game()
starting_pos = game.startingPos
print(f"Solving game: {module_name}")

primitive_states = {'WIN': 0, 'LOSE': 0, 'TIE': 0}
all_positions = {'WIN': 0, 'LOSE': 0, 'TIE': 0}
by_remoteness = {}

# key: position, value: a tuple,  (one of 'WIN', 'TIE', or 'LOSE' | remoteness)
value_dict = {}

# We don't need to keep game graph, as we will dynamically find our next moves
# using game.GenerateMoves() function
## key: position, value: list of positions that is reachable from current position
## game_graph = {}

def solver(position):
    if game.hasSymmetry and game.Cannonical(position) in value_dict.keys():
        return value_dict[game.Cannonical(position)]
    elif position in value_dict.keys():
        return value_dict[position]
    else:
        assign_value(position)
        #return value_dict[position] -> Don't use this if I want to solve the game fully in one shot

def assign_value(position):
    global primitive_states, all_positions
    if game.PrimitiveValue(position) != 'NOT_PRIMITIVE': 
        # This position is primitive, so update value_dict and we are done
        value = (game.PrimitiveValue(position), 0)
        value_dict[position] = value
        add_analysis(value)
    else:
        child_values = {'WIN': [], 'LOSE': [], 'TIE': []}
        for move in game.GenerateMoves(position):
            child = game.DoMove(position, move)
            if child not in value_dict:
                assign_value(child)
            c_value = value_dict[child]
            child_values[c_value[0]].append(c_value[1])
        if 0 < len(child_values['LOSE']):
            # If there exists a losing child, we're in a winning position, and we are done
            # remoteness = minimum (remoteness of losing children) + 1
            remoteness = min(child_values['LOSE']) + 1
            value = ('WIN', remoteness)
            value_dict[position] = value
            add_analysis(value)
        elif 0 < len(child_values['TIE']):
            # If there is no losing child but exists a tieing child, we're in a tieing position
            # remoteness is calculated to terminate the game as quickly as possible
            remoteness = min(child_values['TIE']) + 1
            value = ('TIE', remoteness)
            value_dict[position] = value
            add_analysis(value)
        else:
            # If all children are winning, we're in a losing position
            remoteness = max(child_values['WIN']) + 1
            value = ('LOSE', remoteness)
            value_dict[position] = value
            add_analysis(value)

def add_analysis(value):
    val, remoteness = value[0], value[1]
    if remoteness == 0:
        primitive_states[val] += 1
        all_positions[val] += 1
    all_positions[val] += 1
    if remoteness in by_remoteness:
        by_remoteness[remoteness][val] += 1
    else:
        by_remoteness[remoteness] = {'WIN': 0, 'LOSE': 0, 'TIE': 0}
        by_remoteness[remoteness][val] += 1


# How do I generalize this to any game? 
#for i in range(N, -1, -1):
    #print(f"{i}: {solver(i)}")

solver(game.startingPos)
# print(f'Primitive States: {primitive_states}')
print(f'All Position Values: {all_positions}')
print(f'Remoteness Analysis:')
print('Remoteness, WIN, LOSE, TIE, TOTAL')
for k in sorted([key for key, _ in by_remoteness.items()], reverse=True):
    w, l, t = by_remoteness[k]['WIN'], by_remoteness[k]['LOSE'], by_remoteness[k]['TIE']
    total = w + l + t
    print(f'{k},  {w},  {l},  {t},  {total}')

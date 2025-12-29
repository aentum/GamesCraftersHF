import importlib
import json

def main():
    global game, solved, positionHistory, value_dict, option, players
    print(f'Input the game module to play:')
    module_name = input()
    game_module = importlib.import_module(module_name)
    game = game_module.Game()
    solved = False # TODO: Check if we have a saved json file with the specified  game configuration

    # Option to solve the game or not
    if ('Y' == input('Solve the Game? (Y/N)').capitalize()):
        solver = importlib.import_module('solver')
        value_dict = solver.main(game, module_name)
        solved = True

    # Play Human vs Human or Human vs Comp
    option = -1
    if solved:
        print('''How do you want to play the game?
                (1) Two-player game
                (2) VS Computer, computer going first
                (3) VS Computer, computer going second''')
        option = int(input())
    else:
        print('There is no solved game. Defaulting to a two-player game.')
        option = 1
    match option:
        case 1:
            players = ['USER', 'USER']
        case 2:
            players = ['COMP', 'USER']
        case 3:
            players = ['USER', 'COMP']

    positionHistory = [game.startingPos]
    while True:
        isover = playGame(positionHistory)
        if isover:
            break
    print('Game Over, Thanks for Playing!')

# On every turn:
# Display the board
# Take in input
# Do the move / Undo a move
# Check if win/lose/tie
def playGame(positionHistory):
    assert len(positionHistory) > 0
    position = positionHistory[-1]
    board = game.decodePosition(position) # TODO: Not game-agnostic
    player = game.setTurn(board) # Player 1 = X , Player 2 = 'O'
    if (game.PrimitiveValue(position) != 'NOT_PRIMITIVE'):
        displayGame(board, gameOver=True)
        print(f"Player {players[player-1]} {game.PrimitiveValue(position)}")
        return True
    
    if players[player-1] == 'COMP':
        position = compDoMove(position)
        positionHistory.append(position)
        return False

    displayGame(board)
    possibleMoves = game.GenerateMoves(position)
    playerMove = (input("Player's move [(u)ndo/1-9]: ")) # TODO: For order and chaos, provide the option to place x or o # TODO: Not game-agnostic
    if (playerMove == "u"):
        if (len(positionHistory) == 1 or (len(positionHistory)==2 and players[1] == 'COMP')): 
            print("Can't Undo!!")
            return False
        positionHistory.pop()
        positionHistory.pop()
        return False
    else:
        playerMove = translateMove(int(playerMove))
        if (playerMove not in possibleMoves):
            print("Invalid Move")
            return False
        else:
            position = game.DoMove(position, playerMove)
            positionHistory.append(position)
            return False

# TODO: Generalize to MxN games
# TODO: Not game-agnostic, Move to game module
def displayGame(board, gameOver=False):
    print("Legend: ", end = '\n')
    print("(1 2 3)", end ='\n') 
    print("(4 5 6)", end ='\n') 
    print("(7 8 9)", end ='\n')

    if game.setTurn(board) == -1 and not game.isOnlyX: 
        # If it is the second player, invert the board for display 
        position = game.encodeBoard(board, invert=True)
        board = game.decodePosition(position)
    board = board.flatten()
    board_str = "Board: \n"
    for i in range(game.m * game.n):
        if board[i] == 1:
            board_str += 'X '
        elif board[i] == -1:
            board_str += 'O '
        else:
            board_str += '- '
        if (i + 1) % game.n == 0:
            board_str += '\n'
    print(board_str)
    if gameOver:
        print('GAME OVER!')
    elif solved:
        position = game.encodeBoard(board, invert=True)
        value, remoteness = value_dict[game.Canonical(position)]
        player = game.setTurn(board)
        print(f"Player {1 if player == 1 else 2} can {value} in {remoteness}")
    
# Generate the best move from POSITION
def compDoMove(position):
    potentialMoves = {'WIN': [], 'LOSE': [], 'TIE': []}
    if (game.PrimitiveValue(position) != 'NOT_PRIMITIVE'):
        displayGame(game.decodePosition(position), gameOver=True)
        print(f"Computer {game.PrimitiveValue(position)}")
        return
    for move in game.GenerateMoves(position):
        child = game.DoMove(position, move)
        value, remoteness = value_dict[game.Canonical(child)]
        potentialMoves[value].append((move, remoteness))
    # Goal is to:
    # Give losing position to child if it exists (minimize remoteness to win ASAP)
    # elif give tieing position to child if it exists
    # else it means all child are winning (maximum remoteness = fight back as hard as you can)
    if (len(potentialMoves['LOSE']) > 0):   
        bestMove = min(potentialMoves['LOSE'], key = lambda x : x[1])[0]
    elif (len(potentialMoves['TIE']) > 0):
        bestMove = min(potentialMoves['TIE'], key = lambda x : x[1])[0]
    else:
        bestMove = max(potentialMoves['WIN'], key = lambda x : x[1])[0]
    position = game.DoMove(position, bestMove) 
    return position

# TODO: Not game-agnostic
def translateMove(n): 
    i = (n-1) // game.m
    j = (n-1) % game.n
    return (i, j, 1) 

if __name__ == "__main__":
    main()

import importlib
import json

def main():
    global game, solved, positionHistory, value_dict
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

    positionHistory = []
    playGame(game.startingPos, option)

# On every turn:
# Display the board
# Take in input
# Do the move / Undo a move
# Check if win/lose/tie
def playGame(position, option):
    #TODO Play with COMP
    if(option == 2):
        position = compDoMove(position)
    board = game.decodePosition(position)
    player = game.setTurn(board) # Player 1 = X , Player 2 = 'O'
    if (game.PrimitiveValue(position) != 'NOT_PRIMITIVE'):
        displayGame(board, gameOver=True)
        print(f"Player {1 if player == 1 else 2} {game.PrimitiveValue(position)}")
        return
    displayGame(board)
    possibleMoves = generatePlayerMoves(position)
    playerMove = (input("Player's move [(u)ndo/1-9]: ")) # TODO: For order and chaos, provide the option to place x or o
    if (playerMove == "u"):
        if (len(positionHistory) == 0): 
            print("Can't Undo!!")
            playGame(position, option)
            return
        oldPosition = len(positionHistory) - 1
        position = positionHistory[oldPosition]
        positionHistory.remove(position)
        playGame(position, option)
    else:
        playerMove = int(playerMove)
        if (playerMove not in possibleMoves):
            print("Invalid Move")
            playGame(position, option)
        else:
            positionHistory.append(position)
            position = game.DoMove(position, translateMove(playerMove))
            if(option == 3):
                position = compDoMove(position)
                if not position: #Game is over on computer's turn
                    return
            playGame(position, option)

def displayGame(board, gameOver=False):
    print("Legend: ", end = '\n')
    print("(1 2 3)", end ='\n') # TODO: Generalize to MxN games
    print("(4 5 6)", end ='\n') # TODO: This function ideally should live in game module
    print("(7 8 9)", end ='\n')

    if game.setTurn(board) == -1 and not game.isOnlyX: 
        # If it is the second player, invert the board for display 
        position = game.encodeBoard(board, True)
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
        position = game.encodeBoard(board, invert=False)
        value, remoteness = value_dict[game.Canonical(position)]
        player = game.setTurn(board)
        # The game values are stored from the first player's perspective,
        # so we reverse it for the second player
        if player == -1: 
            if value == 'WIN':
                value = 'LOSE'
            elif value == 'LOSE':
                value = 'WIN'
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
        bestMove = max(potentialMoves, key= lambda x : x[1])[0]
    position = game.DoMove(position, bestMove) 
    return position

def generatePlayerMoves(position):
    board = game.decodePosition(position).flatten()
    moves = []
    for i in range(len(board)):
        if(board[i] == 0):
            moves.append(i + 1)
    return moves    

def translateMove(n):
    i = (n-1) // game.m
    j = (n-1) % game.n
    return (i, j, 1) 

if __name__ == "__main__":
    main()
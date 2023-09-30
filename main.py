import importlib
import json

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
            (2) VS Computer, going first
            (3) VS Computer, going second''')
    option = int(input().split())
else:
    print('There is no solved game. Defaulting to a two-player game.')
    option = 1

positionHistory = []

# On every turn:
# Display the board
# Take in input
# Do the move / Undo a move
# Check if win/lose/tie
def playGame(position, option):
    #TODO Play with COMP
    board = game.decodePosition(position)
    player = game.setTurn(board) # Player 1 = X , Player 2 = 'O'
    displayGame(board)
    if(game.PrimitiveValue(position) != 'NOT_PRIMITIVE'):
        print(f"Player {player} has {game.PrimitiveValue(position)}")
        return
    possibleMoves = generatePlayerMoves(position)
    playerMove = (input("Player's move [(u)ndo/1-9]: ")) # TODO: Undoing blank board
    if(playerMove == "u"):
        oldPosition = len(positionHistory) - 1
        position = positionHistory[oldPosition]
        positionHistory.remove(position)
        playGame(position, option)
        return 
    else:
        playerMove = int(playerMove)
    if(playerMove in possibleMoves):
        positionHistory.append(position)
        position = game.DoMove(position, translateMove(playerMove))
        playGame(position, option)
    else:
        print("Invalid Move")
        playGame(position, option)

def displayGame(board):
    print("Legend: ", end = '\n')
    print("(1 2 3)", end ='\n')
    print("(4 5 6)", end ='\n')
    print("(7 8 9)", end ='\n')
    if game.setTurn(board) == -1: # If it is the second player, invert the board for display 
        position = game.encodeBoard(board, True)
        board = game.decodePosition(position)
    board = board.flatten()
    board_str = ""
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
    #TODO: Game analysis 
    
def generatePlayerMoves(position):
    board = game.decodePosition(position).flatten()
    moves = []
    for i in range(len(board)):
        if(board[i] == 0):
            moves.append(i + 1)
    return moves    

def translateMove(n):
    i = (n-1) // 3
    j = (n-1) % 3
    return (i, j, 1) 

playGame(0, option)
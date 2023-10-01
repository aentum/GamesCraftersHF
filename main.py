import importlib
import json

def main():
    global game, solved, positionHistory
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
    board = game.decodePosition(position)
    player = game.setTurn(board) # Player 1 = X , Player 2 = 'O'
    displayGame(board)
    if (game.PrimitiveValue(position) != 'NOT_PRIMITIVE'):
        print(f"Player {1 if player == 1 else 2} {game.PrimitiveValue(position)}")
        return
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
        return 
    else:
        playerMove = int(playerMove)
    if (playerMove in possibleMoves):
        positionHistory.append(position)
        position = game.DoMove(position, translateMove(playerMove))
        playGame(position, option)
    else:
        print("Invalid Move")
        playGame(position, option)

def displayGame(board):
    print("Legend: ", end = '\n')
    print("(1 2 3)", end ='\n') # TODO: Generalize to MxN games
    print("(4 5 6)", end ='\n') # TODO: This function ideally should live in game module
    print("(7 8 9)", end ='\n')

    if game.setTurn(board) == -1 and not game.isOnlyX: 
        # If it is the second player, invert the board for display 
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
    if solved:
        pass #TODO: Game analysis 
    
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
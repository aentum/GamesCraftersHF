
class Game():
    hasSymmetry = False
    def __init__(self) -> None:
        self.startingPos = 0

    # Return result of MOVE from POSITION
    # Assumes that POSITION is not a primitive position
    # and that MOVE is valid from current POSITION
    def DoMove(self, position, move):
        board = self.decodePosition(position)
        x, y= move[0], move[1]
        board[x][y] = 1
        # Encode the board for the next player
        position = self.encodeBoard(board)
        return position

    # Return all valid moves from POSITION
    # Assumes POSITION is not primitive
    def GenerateMoves(self, position):
        board = self.decodePosition(position)
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    moves.append((i, j))
        return moves
        
    def PrimitiveValue(self, position):
        board = self.decodePosition(position)
        for i in range(3):
            if sum(board[i]) == -3:
                return 'LOSE'
        # Transpose the 2D matrix
        board = self.transpose(board)
        
        for i in range(3):
            if sum(board[i]) == -3:
                return 'LOSE'
        if board[0][0] + board[1][1] + board[2][2] == -3:
            return 'LOSE'
        if board[0][2] + board[1][1] + board[2][0] == -3:
            return 'LOSE'
        # If there is no winner and there is space left on board,
        # This board is not primitive
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return 'NOT_PRIMITIVE'
        return 'TIE'
    
    # Positions are decoded in base 3
    # 0 means no one made a move there
    # 1 means the move is mine. On the board it is 1
    # 2 means the move is opponent's. On the board it is -1
    def decodePosition(self, position):
        board = []
        if position >=19683:
            return TypeError('Invalid Position')
        while position > 0:
            on_board = position % 3
            if on_board == 1:
                board.append(1)
            elif on_board == 2:
                board.append(-1)
            else:
                board.append(0)
            position = position // 3
        while len(board) < 9:
            board.append(0)
        board = [board[0:3], board[3:6], board[6:9]] # Return the board as a 2D array
        return board
    
    # Encode the board in base 3, but inverting for the next player
    # i.e. My move (1 on board) is not my move (2 base 3) for the next player 
    def encodeBoard(self, board, invert=True):
        board = board[0] + board[1] + board[2]
        if (len(board) != 9):
            return TypeError('Wrong size board')
        position = 0
        for i in range(len(board)-1,-1,-1):
            if invert:
                if board[i] == 1:
                    position += 2
                elif board[i] == -1:
                    position += 1
            else:
                if board[i] == 1:
                    position += 1
                elif board[i] == -1:
                    position += 2
            position *= 3
        return position // 3
    
    # return the canonical 
    def Canonical(self, position):
        board = self.decodePosition(position)
        result = self.encodeBoard(board, False)
        for i in range(2):
            board = self.transpose(board)
            for j in range(4):
                board = self.rotate(board)
                result = min(result, self.encodeBoard(board, False))
        return result
        

    def transpose(self, board):
        for i in range(3):
            for j in range(i):
                board[i][j], board[j][i] = board[j][i], board[i][j]
        return board
    
    def rotate(self, board):
        board = [board[2], board[1], board[0]]
        board = self.transpose(board)
        return board





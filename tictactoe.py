import numpy as np

class Game():
    hasSymmetry = False
    isMisere = False
    isOnlyX = False
    endGameValue = 'LOSE'
    # MxN board with K-in a row to win
    m, n, k= 3, 3, 3
    def __init__(self) -> None:
        self.startingPos = 0
        standard = input('Play Standard (3x3 by 3)? (Y/N)').capitalize()
        if (standard == 'N'):
            m, n , k= map(int, input(("Enter (M N K) for board size and winning condition, "
                                      "each separated by a space:")).split())
            self.m, self.n = m, n
            self.k = k
        misere = input('Play Misere? (Y/N)').capitalize()
        if (misere == 'Y'):
            self.isMisere = True
            self.endGameValue = 'WIN'
        onlyX = input('Play onlyX? (Y/N)').capitalize()
        if (onlyX == 'Y'):
            self.isOnlyX = True
        print('Game configuration complete! \n')
        print(f'Symmetries: {self.hasSymmetry}')

    # Return result of MOVE from POSITION
    # Assumes that POSITION is not a primitive position
    # and that MOVE is valid from current POSITION
    def DoMove(self, position, move):
        board = self.decodePosition(position)
        x, y= move[0], move[1]
        board[x][y] = 1
        # Encode the board for the next player
        # position = self.encodeboard(board, invert = not self.isOnlyX)
        if (self.isOnlyX):
            position = self.encodeBoard(board, invert=False)
        else:
            position = self.encodeBoard(board)
        return position

    # Return all valid moves from POSITION
    # Assumes POSITION is not primitive
    def GenerateMoves(self, position):
        board = self.decodePosition(position)
        moves = []
        for i in range(self.m):
            for j in range(self.n):
                if board[i][j] == 0:
                    moves.append((i, j))
        return moves
        
    def MiserePrimitveValue(self,position):
        default = self.PrimitiveValue(position)
        if(default == 'LOSE'):
            default = 'WIN'
        return default
    
    def PrimitiveValue(self, position):

        board = self.decodePosition(position)
        #Check Rows
        for i in range(self.m):
            rowsum = 0
            for j in range(self.n):
                if(board[i][j] == -1):
                    rowsum -= 1
                else:
                    rowsum = 0
                if(rowsum == -self.k):
                    return self.endGameValue
            
        # Transpose the 2D matrix
        board = np.transpose(board)
        #Check Columns
        for i in range(self.n):
            rowsum = 0
            for j in range(self.m):
                if(board[i][j] == -1):
                    rowsum -= 1
                else:
                    rowsum = 0
                if(rowsum == -self.k):
                    return self.endGameValue
                    
        board = np.transpose(board)
        #Check Diagonal
        for i in range(self.m - self.k + 1):
            for j in range(self.n - self.k + 1):
                diagsum = sum(board[i+r][j+r] for r in range(self.k))
                if (diagsum == -self.k):
                    return self.endGameValue
        for i in range(self.m - self.k + 1):
            for j in range(self.k - 1, self.n):
                diagsum = sum(board[i+r][j-r] for r in range(self.k))
                if (diagsum == -self.k):
                    return self.endGameValue
        # If there is no winner and there is space left on board,
        # This board is not primitive
        for i in range(self.m):
            for j in range(self.n):
                if board[i][j] == 0:
                    return 'NOT_PRIMITIVE'
        return 'TIE'
    
    # Positions are decoded in base 3
    # 0 means no one made a move there
    # 1 means the move is mine. On the board it is 1
    # 2 means the move is opponent's. On the board it is -1
    def decodePosition(self, position):
        board = []
        while position > 0:
            on_board = position % 3
            if on_board == 1:
                board.append(1)
            elif on_board == 2:
                board.append(-1)
            else:
                board.append(0)
            position = position // 3
        while len(board) < (self.m * self.n):
            board.append(0)
        board = np.array(board).reshape((self.m, self.n))
        return board
    
    # Encode the board in base 3, but inverting for the next player
    # i.e. My move (1 on board) is not my move (2 base 3) for the next player 
    def encodeBoard(self, board, invert=True):
        board = board.flatten()
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
        if (self.m == self.n):
            for _ in range(2):
                board = np.transpose(board)
                for _ in range(4):
                    board = np.rot90(board, 1)
                    result = min(result, self.encodeBoard(board, False))
        else:
            for _ in range(2):
                board = np.array(board)
                board = np.flip(board, 0)
                for _ in range(2):
                    board = np.flip(board, 1)
                    result = min(result, self.encodeBoard(board, False))
        return result
        
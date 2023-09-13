
class Game():
    '''
    ALL_MOVES (Int array): ARRAY OF PENNIES THAT CAN BE TAKEN IN ONE MOVE
    '''
    def __init__(self, all_moves) -> None:
        self.all_moves = sorted(all_moves)
    
    def isPrimitive(self, position):
        return position - self.all_moves[0] < 0

    # Return result of MOVE from POSITION
    # Assumes that POSITION is not a primitive position
    # and that MOVE is valid from current POSITION
    def DoMove(self, position, move):
        return position - move

    # Return all valid moves from POSITION
    # Assumes POSITION is not primitive
    def GenerateMoves(self, position):
        result = []
        for m in self.all_moves:
            if position - m >= 0:
                result.append(m)
        return result

    def PrimitiveValue(self, position):
        if not self.isPrimitive(position):
            return 'NOT_PRIMITIVE'
        else:
            # There is no move available, which is a losing position
            return 'LOSE'
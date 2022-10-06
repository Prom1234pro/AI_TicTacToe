import numpy as np

class Hash:
    def __init__(self):
        self.hashList = []

    def getNotation(self, board):
        string = ""
        for i in range(3):
            for j in range(3):
                if board[(i,j)] == 1:
                    string += '8'
                elif board[(i,j)] == 0:
                    string += '0'
                elif board[(i,j)] == -1:
                    string += '5'
        return int(string)
    
    def rrb(self, board):
        b = board
        self.hashList.append(self.getNotation(board))
        rr = np.flip(b, 1)
        self.hashList.append(self.getNotation(rr))
        r = np.flip(b, 0)
        r = np.transpose(r)
        self.hashList.append(self.getNotation(r))
        rr = np.flip(r, 0)
        self.hashList.append(self.getNotation(rr))
        r = np.flip(b, 0)
        r = np.flip(r, 1)
        self.hashList.append(self.getNotation(r))
        rr = np.flip(r, 1)
        self.hashList.append(self.getNotation(rr))
        r = np.flip(b, 0)
        r = np.transpose(r)
        r = np.flip(r, 0)
        r = np.flip(r, 1)
        self.hashList.append(self.getNotation(r))
        rr = np.flip(r, 0)
        self.hashList.append(self.getNotation(rr))
    
    def getSymmetryHash(self, board):
        self.rrb(board)
        self.hashList.sort()
        return str(self.hashList[0])

    def reset(self):
        self.hashList = []
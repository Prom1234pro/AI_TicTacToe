import numpy as np


class State:
    def __init__(self, player1, player2, hash):
        self.p1 = player1
        self.p2 = player2
        self.isEnd = False
        self.board = np.zeros((3, 3))
        self.hash = hash
        # self.boardHashKey = None
        self.player = 1
    
    
    def winner(self):
        for i in range(3):
            if sum(self.board[i, :]) == 3 or sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3 or sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        diag_sum1 = sum([self.board[i, i] for i in range(3)])
        diag_sum2 = sum([self.board[i, 3 - i - 1] for i in range(3)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None

    def availablePositions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions
    
    def updateState(self, position):
        self.board[position] = self.player
        self.player *= -1
    
    def giveReward(self):
        result = self.winner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.5)
            self.p2.feedReward(0.5)
        
    def reset(self):
        self.board = np.zeros((3, 3))
        self.isEnd = False
        self.player = 1
    
    def train(self, rounds):
        for i in range(rounds):
            if rounds > 50000:
                self.p1.exp_rate = 0
                self.p2.exp_rate = 0
            
            if i % 100 ==0:
                print("Rounds {}".format(i))
                print(len(self.p1.q_value))
                print(len(self.p2.q_value))
            while not self.isEnd:
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.player)
                self.updateState(p1_action)
                board_hash = self.hash.getSymmetryHash(self.board)
                self.hash.reset()
                self.p1.addState(board_hash)

                win = self.winner()
                if win is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    position = self.availablePositions()
                    p2_action = self.p2.chooseAction(position, self.board, self.player)
                    self.updateState(p2_action)
                    board_hash = self.hash.getSymmetryHash(self.board)
                    self.hash.reset()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def play(self):
        while not self.isEnd:
            positions = self.availablePositions()

            p1_action = self.p1.chooseAction(positions, self.board, self.player)
            self.updateState(p1_action)
            self.showBoard()

            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions, self.board, self.player)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        for i in range(0, 3):
            print('-------------')
            out = '| '
            for j in range(0, 3):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')


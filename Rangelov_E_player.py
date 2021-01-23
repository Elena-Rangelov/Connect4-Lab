# Name: Elena Rangelov
# Date: 1.20.2021

import random


class RandomAI:
    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move
        # (column num, row num), 0

        moves = list(self.find_moves(board, color))
        if len(moves) == 0:
            return (-1, -1), 0
        index = random.choice(moves)
        best_move = (int(index / 6), int(index % 6))
        self.first_turn = False
        return best_move, 0

    def find_moves(self, board, color):

        self.x_max = 7
        self.y_max = 6

        moves_found = set()
        for c in range(len(board)):
            for r in range(0, 6):
                if r == 5 and board[c][r] == ".":
                    moves_found.add(c * self.y_max + r)
                    break
                if board[c][r] != ".":
                    moves_found.add((c) * self.y_max + r-1)
                    break
        return moves_found


class BestAI:

    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move

        self.x_max = 6
        self.y_max = 7
        return self.alphabeta(board, color, 3, float("inf"), float("-inf"))

    def alphabeta(self, board, color, search_depth, alpha, beta):
        if color == "#ffffff":
            m_color = self.white
        else:
            m_color = self.black
        moves = self.find_moves(board, m_color)
        value = -999
        move = -1
        v = self.max_value(board, m_color, search_depth, alpha, beta)
        for m in moves:
            n_board = self.make_move(board, color, m)
            n_value = self.min_value(n_board, self.opposite_color[m_color], 2, alpha, beta)
            h = self.heuristic(n_board, color, m)
            if h > 1000:
                value = n_value
                move = m
                return (move // self.y_max, move % self.y_max), value
            elif h < -1000:
                break
            elif n_value > value:
                value = n_value
                move = m
        return (move // self.y_max, move % self.y_max), value


    def max_value(self, board, color, search_depth, alpha, beta):

        moves = self.find_moves(board, color)
        if len(moves) == 0: return -1000
        if len(self.find_moves(board, self.opposite_color[color])) == 0: return 1000
        if search_depth == 1:
            return self.evaluate(board, color, moves)
        v = float("-inf")
        for m in moves:
            n_board = self.make_move(board, color, m)
            next = self.min_value(n_board, self.opposite_color[color], search_depth - 1, alpha, beta)
            if max(v, next) != v:
                v = next
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, board, color, search_depth, alpha, beta):

        moves = self.find_moves(board, color)
        if len(moves) == 0: return 1000
        if len(self.find_moves(board, self.opposite_color[color])) == 0: return -1000
        if search_depth == 1:
            return -self.evaluate(board, color, moves)
        v = float("inf")
        for m in moves:
            n_board = self.make_move(board, color, m)
            next = self.max_value(n_board, self.opposite_color[color], search_depth - 1, alpha, beta)
            if min(v, next) != v:
                v = next
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def make_move(self, board, color, move):

        n_board = [row[:] for row in board]
        if color == self.white:
            char = "O"
        else:
            char = "X"
        x_pos, y_pos = int(move / 6), int(move % 6)
        n_board[x_pos][y_pos] = char
        return n_board

    def evaluate(self, board, color, possible_moves):

        mx = 0
        omx = 0
        for m in possible_moves:
            mx = max(self.heuristic(self.make_move(board, color, m), color, m), mx)
        for m in self.find_moves(board, self.opposite_color[color]):
            omx = max(self.heuristic(self.make_move(board, self.opposite_color[color], m), self.opposite_color[color], m), omx)
        return mx - omx

    def heuristic(self, board, color, move):

        x = int(move / 6)
        y = int(move % 6)

        m4 = self.check_streaks(board, color, x, y, 4)
        m3 = self.check_streaks(board, color, x, y, 3)
        m2 = self.check_streaks(board, color, x, y, 2)

        return m4*100000 + m3*100 + m2*10

    def check_streaks(self, board, turn, x, y, s):
        streak = 0
        if turn == self.black:
            color = "X"
        else:
            color = "O"
        for incr in self.directions:
            count = 0
            x_pos = x
            y_pos = y
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max and board[x_pos][y_pos] == color:
                count += 1
                x_pos += incr[0]
                y_pos += incr[1]
                if count == s:
                    streak += 1
                    break
                if x_pos < 0 or x_pos >= self.x_max or y_pos < 0 or y_pos >= self.y_max:
                    x_pos = x
                    y_pos = y
                    if incr == self.directions[0]:
                        incr = self.directions[7]
                    elif incr == self.directions[1]:
                        incr = self.directions[6]
                    elif incr == self.directions[2]:
                        incr = self.directions[5]
                    elif incr == self.directions[3]:
                        incr = self.directions[4]
                    elif incr == self.directions[4]:
                        incr = self.directions[3]
                    elif incr == self.directions[5]:
                        incr = self.directions[2]
                    elif incr == self.directions[6]:
                        incr = self.directions[1]
                    elif incr == self.directions[7]:
                        incr = self.directions[0]
                    x_pos += incr[0]
                    y_pos += incr[1]
                    while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max and board[x_pos][y_pos] == color:
                        count += 1
                        x_pos += incr[0]
                        y_pos += incr[1]
                        if count == s:
                            streak += 1
                            break
                elif board[x_pos][y_pos] != color:
                    x_pos = x
                    y_pos = y
                    if incr == self.directions[0]:
                        incr = self.directions[7]
                    elif incr == self.directions[1]:
                        incr = self.directions[6]
                    elif incr == self.directions[2]:
                        incr = self.directions[5]
                    elif incr == self.directions[3]:
                        incr = self.directions[4]
                    elif incr == self.directions[4]:
                        incr = self.directions[3]
                    elif incr == self.directions[5]:
                        incr = self.directions[2]
                    elif incr == self.directions[6]:
                        incr = self.directions[1]
                    elif incr == self.directions[7]:
                        incr = self.directions[0]
                    x_pos += incr[0]
                    y_pos += incr[1]
                    while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max and board[x_pos][y_pos] == color:
                        count += 1
                        x_pos += incr[0]
                        y_pos += incr[1]
                        if count == s:
                            streak+=1
                            break
        return streak

    def find_moves(self, board, color):
        
        self.x_max = 7
        self.y_max = 6

        moves_found = set()
        for c in range(len(board)):
            for r in range(0, 6):
                if r == 5 and board[c][r] == ".":
                    moves_found.add(c * self.y_max + r)
                    break
                if board[c][r] != ".":
                    moves_found.add((c) * self.y_max + r - 1)
                    break
        return moves_found


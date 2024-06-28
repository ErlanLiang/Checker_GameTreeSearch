import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!
DEPTH = 12

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, cur_turn='r', parent=None, best_child=None):

        self.board = board
        self.turn = cur_turn # the current turn
        self.width = 8
        self.height = 8
        self.parent = parent # the parent state
        self.best_child = best_child # the best child state

    def __eq__(self, other):
        return self.board == other.board and self.turn == other.turn
    
    def __hash__(self):
        return hash(str(self.board) + self.turn)


    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def check_win(self):
        '''
        Check if the game is over
        If one player has no piece, the other player wins
        '''
        r_count = 0
        b_count = 0
        # self.display()
        for i in range(self.height):
            for j in range(self.width):         
                if self.board[i][j] in ['r', 'R']:
                    r_count += 1
                elif self.board[i][j] in ['b', 'B']:
                    b_count += 1
        if r_count == 0:
            return 'b'
        elif b_count == 0:
            return 'r'
        else:
            return None
    

    def get_possible_moves(self):
        '''
        Get all possible moves for based on the current board state
        If a piece can jump, it must jump
        If a multiple jumps are possible, return the longest jump
        Only the king can move backwards
        '''
        # self.display()
        # print("==========================")
        possible_moves = []
        possible_jumps = []
        jump_exists = False
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == self.turn or self.board[i][j] == self.turn.upper():
                    moves, jump_exists = self.get_possible_moves_for_piece(i, j, jump_exists)
                    if moves and jump_exists:
                        possible_jumps += moves
                    elif moves:
                        possible_moves += moves
                # elif self.board[i][j] == self.turn.upper():
                #     possible_moves += self.get_possible_moves_for_king(i, j)
        if possible_jumps:
            possible_moves = possible_jumps
        return possible_moves
    
    def get_possible_moves_for_piece(self, i, j, jump_exists):
        possible_moves = []
        # Check if the piece can jump
        jump_directions = self.can_jump(i, j, self.board)
        if jump_directions:
            jump_exists = True
            for d in jump_directions:
                # check if the piece can be promoted
                if (self.turn == 'r' and i+d[0] == 0) or (self.turn == 'b' and i+d[0] == 7):
                    new_board = copy.deepcopy(self.board)
                    new_board[i+d[0]][j+d[1]] = self.board[i][j].upper()
                    new_board[i][j] = '.'
                    new_board[i+d[0]//2][j+d[1]//2] = '.'
                    possible_moves.append(new_board)
                else:
                    new_board = copy.deepcopy(self.board)
                    new_board[i+d[0]][j+d[1]] = self.board[i][j]
                    new_board[i][j] = '.'
                    new_board[i+d[0]//2][j+d[1]//2] = '.'
                    ni, nj = i+d[0], j+d[1]
                    # Apply a DFS to find all the jump
                    possible_moves += self.DFS_find(new_board, ni, nj)
        elif jump_exists:
            return possible_moves, jump_exists
        else:
            # Check if the piece can move
            move_directions = []
            if jump_exists:
                return possible_moves, jump_exists
            
            if self.turn == 'r':     
                if i >= 1 and j >= 1 and self.board[i-1][j-1] == '.':
                    move_directions.append((-1, -1))
                if i >= 1 and j <= 6 and self.board[i-1][j+1] == '.':
                    move_directions.append((-1, 1))
                if self.board[i][j] == "R":
                    if i <= 6 and j >= 1 and self.board[i+1][j-1] == '.':
                        move_directions.append((1, -1))
                    if i <= 6 and j <= 6 and self.board[i+1][j+1] == '.':
                        move_directions.append((1, 1))
            else:
                if i <= 6 and j >= 1 and self.board[i+1][j-1] == '.':
                    move_directions.append((1, -1))
                if i <= 6 and j <= 6 and self.board[i+1][j+1] == '.':
                    move_directions.append((1, 1))
                if self.board[i][j] == "B":
                    if i >= 1 and j >= 1 and self.board[i-1][j-1] == '.':
                        move_directions.append((-1, -1))
                    if i >= 1 and j <= 6 and self.board[i-1][j+1] == '.':
                        move_directions.append((-1, 1))
            if move_directions:
                for d in move_directions:
                    new_board = copy.deepcopy(self.board)
                    # check if the piece can be promoted
                    if (self.turn == 'r' and i+d[0] == 0) or (self.turn == 'b' and i+d[0] == 7):
                        new_board[i+d[0]][j+d[1]] = self.board[i][j].upper()
                    else:
                        new_board[i+d[0]][j+d[1]] = self.board[i][j]
                    new_board[i][j] = '.'
                    possible_moves.append(new_board)            
        return possible_moves, jump_exists
    
    def DFS_find(self, board, i, j):
        '''
        DFS to find all the possible jumps
        Return all the final board
        '''
        possible_moves = [(board, i, j)]
        final_boards = []
        while possible_moves:
            cur_board, i, j = possible_moves.pop()
            jump_directions = self.can_jump(i, j, cur_board)
            if jump_directions:
                for d in jump_directions:
                    new_board = copy.deepcopy(cur_board)
                    # check if the piece can be promoted
                    if (self.turn == 'r' and i+d[0] == 0) or (self.turn == 'b' and i+d[0] == 7):
                        new_board[i+d[0]][j+d[1]] = cur_board[i][j].upper()
                        new_board[i][j] = '.'
                        new_board[i+d[0]//2][j+d[1]//2] = '.'
                        final_boards.append(new_board)
                    else:
                        new_board[i+d[0]][j+d[1]] = cur_board[i][j]
                        new_board[i][j] = '.'
                        new_board[i+d[0]//2][j+d[1]//2] = '.'
                        ni, nj = i+d[0], j+d[1]
                        possible_moves.append((new_board, ni, nj))
            else:
                final_boards.append(cur_board)
        return final_boards

    def can_jump(self, i, j, board):
        '''
        Check if a piece can jump and return the possible jump directions
        '''
        possible_jump_directions = []
        opp_char = get_opp_char(self.turn)
        if self.turn == 'r':
            # check if the piece can jump to the up right and up left
            if i >= 2 and j >= 2 and board[i-1][j-1] in opp_char and board[i-2][j-2] == '.':
                possible_jump_directions.append((-2, -2))
            if i >= 2 and j <= 5 and board[i-1][j+1] in opp_char and board[i-2][j+2] == '.':
                possible_jump_directions.append((-2, 2))
            if board[i][j] == self.turn.upper():
                if i <= 5 and j >= 2 and board[i+1][j-1] in opp_char and board[i+2][j-2] == '.':
                    possible_jump_directions.append((2, -2))
                if i <= 5 and j <= 5 and board[i+1][j+1] in opp_char and board[i+2][j+2] == '.':
                    possible_jump_directions.append((2, 2))
        else:
            # check if the piece can jump to the down right and down left
            if i <= 5 and j >= 2 and board[i+1][j-1] in opp_char and board[i+2][j-2] == '.':
                possible_jump_directions.append((2, -2))
            if i <= 5 and j <= 5 and board[i+1][j+1] in opp_char and board[i+2][j+2] == '.':
                possible_jump_directions.append((2, 2))
            if board[i][j] == self.turn.upper():
                if i >= 2 and j >= 2 and board[i-1][j-1] in opp_char and board[i-2][j-2] == '.':
                    possible_jump_directions.append((-2, -2))
                if i >= 2 and j <= 5 and board[i-1][j+1] in opp_char and board[i-2][j+2] == '.':
                    possible_jump_directions.append((-2, 2))
        return possible_jump_directions
    
    def max_value(self, state, alpha, beta, depth):
        # Check if already cached
        if state in cache and cache[state]['depth'] >= depth:
            # print("Cache hit")
            return (cache[state]['value'], cache[state]['successor'])
        
        if depth == 0:
            return (self.eval(state), None)
        
        possible_moves = state.get_possible_moves()
        best_move = state
        best_value = -float('inf')

        if not possible_moves:
            cache[state] = {'value': -100000, 'depth': depth, 'successor': None}
            return (-100000, None)
        
        for move in possible_moves:
            temp_value, temp_move = self.min_value(State(move, get_next_turn(state.turn)), alpha, beta, depth-1)
            if temp_value > best_value:
                best_value = temp_value
                best_move = State(move, get_next_turn(state.turn), state)
            if best_value > beta:
                cache[state] = {'value': best_value, 'depth': depth, 'successor': best_move}
                return (best_value, best_move)
            alpha = max(alpha, temp_value)
            cache[state] = {'value': best_value, 'depth': depth, 'successor': best_move}
        return (best_value, best_move)

    def min_value(self, state, alpha, beta, depth):
        # Check if already cached
        if state in cache and cache[state]['depth'] >= depth:
            # print("Cache hit")
            return (cache[state]['value'], cache[state]['successor'])
        
        if depth == 0:
            return (self.eval(state, depth), None)
        
        possible_moves = state.get_possible_moves()
        best_move = state
        best_value = float('inf')

        if not possible_moves:
            cache[state] = {'value': 100000, 'depth': depth, 'successor': None}
            return (100000, None)
        
        for move in possible_moves:
            temp_value, temp_move = self.max_value(State(move, get_next_turn(state.turn)), alpha, beta, depth-1)
            if temp_value < best_value:
                best_value = temp_value
                best_move = State(move, get_next_turn(state.turn), state)
            if best_value < alpha:
                cache[state] = {'value': best_value, 'depth': depth, 'successor': best_move}
                return (best_value, best_move)
            beta = min(beta, temp_value)
            cache[state] = {'value': best_value, 'depth': depth, 'successor': best_move}
        return (best_value, best_move)
            
    
    def eval(self, state, depth=-1):
        num_red_normal_pieces = 0
        num_black_normal_pieces = 0

        num_red_king_pieces = 0
        num_black_king_pieces = 0

        red_piece_positions = 0
        black_piece_positions = 0

        row_counter = 7
        col_counter = 0

        r_row = 0
        r_col = 0
        b_row = 0
        b_col = 0

        total = 0

        for row in range(8):
            for col in range(8):
                if state.board[row][col] == 'r':
                    num_red_normal_pieces += 1
                    r_row += row + 1
                    r_col += col + 1
                    # if the piece is at the edge, add 1
                    if col == 0 or col == 7:
                        total += 1
                    red_piece_positions += 2*(1 + row_counter)
                elif state.board[row][col] == 'b':
                    b_row += row + 1
                    b_col += col + 1
                    if col == 0 or col == 7:
                        total += 1
                    num_black_normal_pieces += 1
                    black_piece_positions += 2*(1 + (7 - row_counter))
                elif state.board[row][col] == 'R':
                    r_row += row + 1
                    r_col += col + 1
                    if col == 0 or col == 7:
                        total += 1
                    num_red_king_pieces += 1
                    total += 2*min(4 - abs(row_counter - 4), 4 - abs(col_counter - 4))
                elif state.board[row][col] == 'B':
                    b_row += row + 1
                    b_col += col + 1
                    if col == 0 or col == 7:
                        total += 1
                    num_black_king_pieces += 1
                    total -= 2*min(4 - abs(row_counter - 4), 4 - abs(col_counter - 4))
                col_counter += 1
            col_counter = 0
            row_counter -= 1

        normal_piece_value = 13
        king_piece_value = 30

        tot_red = num_red_normal_pieces + num_red_king_pieces
        tot_black = num_black_normal_pieces + num_black_king_pieces

        if  tot_black == 0:
            if depth != -1:
                cache[state] = {'value': 10000, 'depth': depth, 'successor': None}
            return 10000
        elif tot_red == 0:
            if depth != -1:
                cache[state] = {'value': -10000, 'depth': depth, 'successor': None}
            return -10000

        total += (num_red_normal_pieces * normal_piece_value +
                    num_red_king_pieces * king_piece_value + red_piece_positions)
        total -= (num_black_normal_pieces * normal_piece_value +
                    num_black_king_pieces * king_piece_value + black_piece_positions)
        
        
        r_avg_row = r_row / tot_red
        r_avg_col = r_col / tot_red
        b_avg_row = b_row / tot_black
        b_avg_col = b_col / tot_black
        # the side with more piece will calculate the average position - the other side
        if tot_red > tot_black:
            # calculate the direct distance between the average position using the Euclidean distance
            total += (6 - ((r_avg_row - b_avg_row)**2 + (r_avg_col - b_avg_col)**2)**0.5) * 5 #* (num_red_king_pieces - num_black_king_pieces)           
        else:
            total -= (6 - ((r_avg_row - b_avg_row)**2 + (r_avg_col - b_avg_col)**2)**0.5) * 5 #* (num_black_king_pieces - num_red_king_pieces)

        if (tot_red + tot_black) < 10:
                total *= 1 + (10 - (tot_red + tot_black))/20 

        if depth != -1:
            cache[state] = {'value': total, 'depth': depth, 'successor': None}
        return total


class Checker:

    def __init__(self, board):
        self.cur_state = State(board)

    def human_play(self):
        '''
        Human player play the game by input the move#
        '''
        
        while self.cur_state.check_win() == None:        
            count = 1
            available_moves = self.cur_state.get_possible_moves()
            for i in available_moves:
                print(count)
                print(" ")
                State(i, get_next_turn(self.cur_state.turn)).display()
                count += 1
            move = int(input("Enter the move: "))
            self.cur_state = State(available_moves[move-1], get_next_turn(self.cur_state.turn))
        
        print("The winner is: ", self.cur_state.check_win())
    
    def alpha_beta_play(self):
        '''
        Alpha-Beta player play the game
        '''
        num_moves = 0
        start = time.time()
        self.cur_state.display()
        print("eval: ", self.cur_state.eval(self.cur_state))
        while self.cur_state and self.cur_state.check_win() == None:
            num_moves += 1
            
            if self.cur_state.turn == 'r':
                value, move = self.cur_state.max_value(self.cur_state, -float('inf'), float('inf'), DEPTH)
            else:
                value, move = self.cur_state.min_value(self.cur_state, -float('inf'), float('inf'), DEPTH)
            
            
            print("value: ", value)
            # print("move: ", move)
            self.cur_state.display()
            print("eval: ", self.cur_state.eval(self.cur_state))
            self.cur_state = move
            # self.cur_state.display()
            # print("eval: ", self.cur_state.eval(self.cur_state))

            # if value == 100000 or value == -100000 or value == 10000 or value == -10000:
            #     while self.cur_state in cache and cache[self.cur_state]['successor'] :
            #         num_moves += 1
            #         self.cur_state = cache[self.cur_state]['successor']
            #         self.cur_state.display()
            #     break
                    

            # print("board: ", self.cur_state.board)
            
            
        # self.cur_state.display()
        print("The winner is: ", self.cur_state.check_win())
        print("Move: ", num_moves)
        print("Time: ", time.time()-start)


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

if __name__ == '__main__':
    # Read the input file
    initial_board = read_from_file("checkers4.txt")
    checker = Checker(initial_board)
    # checker.human_play()
    checker.alpha_beta_play()

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--inputfile",
    #     type=str,
    #     required=True,
    #     help="The input file that contains the puzzles."
    # )
    # parser.add_argument(
    #     "--outputfile",
    #     type=str,
    #     required=True,
    #     help="The output file that contains the solution."
    # )
    # args = parser.parse_args()

    # initial_board = read_from_file(args.inputfile)
    # state = State(initial_board)
    # turn = 'r'
    # ctr = 0

    # sys.stdout = open(args.outputfile, 'w')

    # sys.stdout = sys.__stdout__


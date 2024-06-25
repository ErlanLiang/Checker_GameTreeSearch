import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, cur_turn='r'):

        self.board = board
        self.turn = cur_turn # the current turn
        self.width = 8
        self.height = 8
        # cur_jump_piece = cur_jump_piece # the piece that is currently jumping


    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

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
        jump_exists = False
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == self.turn:
                    jump_move, jump_exists = self.get_possible_moves_for_piece(i, j, jump_exists)
                    if jump_move:
                        possible_moves += jump_move
                # elif self.board[i][j] == self.turn.upper():
                #     possible_moves += self.get_possible_moves_for_king(i, j)
        count = 0
        for move in possible_moves:
            count += 1
            new_state = State(move, get_next_turn(self.turn))
            print("Move", count)
            new_state.display()
        return possible_moves

    def can_jump(self, i, j):
        '''
        Check if a piece can jump and return the possible jump directions
        '''
        possible_jump_directions = []
        opp_char = get_opp_char(self.turn)
        if self.turn == 'r':
            # check if the piece can jump to the up right and up left
            if i >= 2 and j >= 2 and self.board[i-1][j-1] in opp_char and self.board[i-2][j-2] == '.':
                possible_jump_directions.append((-2, -2))
            if i >= 2 and j <= 5 and self.board[i-1][j+1] in opp_char and self.board[i-2][j+2] == '.':
                possible_jump_directions.append((-2, 2))
            if self.board[i][j] == self.turn.upper():
                if i <= 5 and j >= 2 and self.board[i+1][j-1] in opp_char and self.board[i+2][j-2] == '.':
                    possible_jump_directions.append((2, -2))
                if i <= 5 and j <= 5 and self.board[i+1][j+1] in opp_char and self.board[i+2][j+2] == '.':
                    possible_jump_directions.append((2, 2))
        else:
            # check if the piece can jump to the down right and down left
            if i <= 5 and j >= 2 and self.board[i+1][j-1] in opp_char and self.board[i+2][j-2] == '.':
                possible_jump_directions.append((2, -2))
            if i <= 5 and j <= 5 and self.board[i+1][j+1] in opp_char and self.board[i+2][j+2] == '.':
                possible_jump_directions.append((2, 2))
            if self.board[i][j] == self.turn.upper():
                if i >= 2 and j >= 2 and self.board[i-1][j-1] in opp_char and self.board[i-2][j-2] == '.':
                    possible_jump_directions.append((-2, -2))
                if i >= 2 and j <= 5 and self.board[i-1][j+1] in opp_char and self.board[i-2][j+2] == '.':
                    possible_jump_directions.append((-2, 2))
        return possible_jump_directions
    
    def get_possible_moves_for_piece(self, i, j, jump_exists):
        possible_moves = []
        # Check if the piece can jump
        jump_directions = self.can_jump(i, j)
        if jump_directions:
            jump_exists = True
            for d in jump_directions:
                new_board = copy.deepcopy(self.board)
                new_board[i+d[0]][j+d[1]] = self.board[i][j]
                new_board[i][j] = '.'
                new_board[i+d[0]//2][j+d[1]//2] = '.'
                ni, nj = i+d[0], j+d[1]
                possible_moves.append(new_board)
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
                if self.board[i][j] == self.turn.upper():
                    if i <= 6 and j >= 1 and self.board[i+1][j-1] == '.':
                        move_directions.append((1, -1))
                    if i <= 6 and j <= 6 and self.board[i+1][j+1] == '.':
                        move_directions.append((1, 1))
            else:
                if i <= 6 and j >= 1 and self.board[i+1][j-1] == '.':
                    move_directions.append((1, -1))
                if i <= 6 and j <= 6 and self.board[i+1][j+1] == '.':
                    move_directions.append((1, 1))
                if self.board[i][j] == self.turn.upper():
                    if i >= 1 and j >= 1 and self.board[i-1][j-1] == '.':
                        move_directions.append((-1, -1))
                    if i >= 1 and j <= 6 and self.board[i-1][j+1] == '.':
                        move_directions.append((-1, 1))
            if move_directions:
                for d in move_directions:
                    new_board = copy.deepcopy(self.board)
                    new_board[i+d[0]][j+d[1]] = self.board[i][j]
                    new_board[i][j] = '.'
                    possible_moves.append(new_board)            
        return possible_moves, jump_exists
    
class Checker:

    def __init__(self, board):
        self.cur_state = State(board)

    def human_play(self):
        '''
        Human player play the game by input the move#
        '''
        
        while True:        
            available_moves = self.cur_state.get_possible_moves()
            move = int(input("Enter the move: "))
            self.cur_state = State(available_moves[move-1], get_next_turn(self.cur_state.turn))
            




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
    initial_board = read_from_file("checkers1.txt")
    checker = Checker(initial_board)
    checker.human_play()

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


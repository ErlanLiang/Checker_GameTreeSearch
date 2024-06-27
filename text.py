# def evaluation_function(state):
#     player_score, opponent_score = 0, 0
#     mid = 4
#     board = state.board
#     for y in range(state.height):
#         for x in range(state.width):
#             piece = board[y][x]
#             if piece == 'r':
#                 player_score += 5 - abs(mid - y) * 0.5
#             elif piece == 'R':
#                 player_score += 10 - abs(mid - y) * 0.5
#             elif piece == 'b':
#                 opponent_score += 5 - abs(mid - y) * 0.5
#             elif piece == 'B':
#                 opponent_score += 10 - abs(mid - y) * 0.5
#     if player_score == 0:
#         return NEGATIVE_LARGE_NUMBER
#     elif opponent_score == 0:
#         return POSITIVE_LARGE_NUMBER
#     return player_score - opponent_score

def evaluation_function(self.state):
    num_red_normal_pieces = 0
    num_black_normal_pieces = 0

    num_red_king_pieces = 0
    num_black_king_pieces = 0

    red_piece_positions = 0
    black_piece_positions = 0

    row_counter = 7
    col_counter = 0

    for row in state.board:
        for piece in row:
            if piece == 'r':
                num_red_normal_pieces += 1
                red_piece_positions += (1 + row_counter)
            elif piece == 'b':
                num_black_normal_pieces += 1
                black_piece_positions += (1 + (7 - row_counter))
            elif piece == 'R':
                num_red_king_pieces += 1
            elif piece == 'B':
                num_black_king_pieces += 1
            col_counter += 1
        col_counter = 0
        row_counter -= 1

    normal_piece_value = 1
    king_piece_value = 20

    red_total = (num_red_normal_pieces * normal_piece_value +
                 num_red_king_pieces * king_piece_value + red_piece_positions)
    black_total = (num_black_normal_pieces * normal_piece_value +
                   num_black_king_pieces * king_piece_value + black_piece_positions)
    if  num_black_normal_pieces + num_black_king_pieces == 0:
        return NEGATIVE_LARGE_NUMBER
    elif num_red_normal_pieces + num_red_king_pieces == 0:
        return POSITIVE_LARGE_NUMBER
    eval = red_total - black_total

    return eval

def evaluation_function(state):
    red_score = 0
    black_score = 0

    center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}
    double_corners = {(0, 0), (0, 7), (7, 0), (7, 7)}

    num_red_normal_pieces = 0
    num_red_king_pieces = 0
    num_black_normal_pieces = 0
    num_black_king_pieces = 0

    board = state.board
    for i in range(8):
        for j in range(8):
            cell = board[i][j]
            if cell == 'r':
                num_red_normal_pieces += 1
                red_score += 1  # 普通红棋子得1分
                red_score += 0.2 * (7 - i)  # 行数越高，分数越高
                if (i, j) in center_squares:
                    red_score += 0.5  # 中心位置加分
                if (i, j) in double_corners:
                    red_score += 0.5  # 双角位置加分
                if j == 0 or j == 7:
                    red_score += 0.3  # 边缘位置加分
            elif cell == 'R':
                num_red_king_pieces += 1
                red_score += 3  # 红王得3分
                if (i, j) in center_squares:
                    red_score += 0.5
                if (i, j) in double_corners:
                    red_score += 0.5
                if j == 0 or j == 7:
                    red_score += 0.3
            elif cell == 'b':
                num_black_normal_pieces += 1
                black_score += 1
                black_score += 0.2 * i  # 行数越低，分数越高
                if (i, j) in center_squares:
                    black_score += 0.5
                if (i, j) in double_corners:
                    black_score += 0.5
                if j == 0 or j == 7:
                    black_score += 0.3
            elif cell == 'B':
                num_black_king_pieces += 1
                black_score += 3
                if (i, j) in center_squares:
                    black_score += 0.5
                if (i, j) in double_corners:
                    black_score += 0.5
                if j == 0 or j == 7:
                    black_score += 0.3

    # 处理场上没有黑棋或红棋的情况
    if num_black_normal_pieces + num_black_king_pieces == 0:
        return POSITIVE_LARGE_NUMBER
    elif num_red_normal_pieces + num_red_king_pieces == 0:
        return NEGATIVE_LARGE_NUMBER

    # 计算最终分数
    total_score = red_score - black_score

    return total_score
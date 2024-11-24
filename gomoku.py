"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""
#=============================================================================

def is_empty(board):
    for r in board:
        for x in r:
            if x != " ":
                return False
    return True
    
#=============================================================================
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    tmp = 0 #count the open sides

    #check the cell placed before the sequence
    pos_x = x_end - (d_x * length)
    pos_y = y_end - (d_y * length)
    if 0 <= pos_y < len(board) and 0 <= pos_x < len(board):
        if board[pos_y][pos_x] == " ":
            tmp += 1
    
    #check the cell placed after the sequence
    pos_x = x_end + d_x
    pos_y = y_end + d_y
    if 0 <= pos_y < len(board) and 0 <= pos_x < len(board):
        if board[pos_y][pos_x] == " ":
            tmp += 1
    
    if tmp == 0:
        return "CLOSED"
    elif tmp == 1:
        return "SEMIOPEN"
    else:
        return "OPEN"

#=============================================================================
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    
    open_seq_count = 0
    semi_open_seq_count = 0

    #stx, std and edx, edy = start and end for a potential sequence of color col.
    sty = y_start
    stx = x_start
    edx = stx + (length - 1) * d_x
    edy = sty + (length - 1) * d_y

    while sty < len(board) and stx < len(board) and sty >= 0 and stx >= 0 and edy < len(board) and edx < len(board) and edy >= 0 and edx >= 0:
        seq = True #is this a maximal sequence of color col?

        i = sty
        j = stx
        for _ in range(length): #check all "length" cells to be the same color as col
            if board[i][j] != col:
                    seq = False
                    break
            i += d_y
            j += d_x
        

        #check if the sequence is maximal (previous and following cells should be empty or the opposite color)
        prex = stx - d_x
        prey = sty - d_y
        follx = edx + d_x
        folly = edy + d_y
        if prex >= 0 and prex < len(board) and prey >= 0 and prey < len(board):
            if board[prey][prex] == col:
                seq = False
        if follx >= 0 and follx < len(board) and folly >= 0 and folly < len(board):
            if board[folly][follx] == col:
                seq = False

        
        if seq: #a maximal sequence is found
            tmp = is_bounded(board, edy, edx, length, d_y, d_x)
            if tmp=="SEMIOPEN":
                semi_open_seq_count+= 1
            elif tmp=="OPEN":
                open_seq_count+= 1

        #next potential sequence (move one cell in the d_y,d_x direction)
        stx += d_x
        sty += d_y
        edx = stx + (length - 1) * d_x
        edy = sty + (length - 1) * d_y


    return open_seq_count, semi_open_seq_count

#=============================================================================
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    ds = [(1,0), (0,1), (1,1)] #sequences in these directions are counted starting from the first row and the first column.

    for d_x, d_y in ds:
        for stx in range(len(board)): #first row
            opens, semis = detect_row(board, col, 0, stx, length, d_y, d_x)
            open_seq_count += opens
            semi_open_seq_count += semis
        for sty in range(1, len(board)): #first column
            opens, semis = detect_row(board, col, sty, 0, length, d_y, d_x)
            open_seq_count += opens
            semi_open_seq_count += semis
    

    d_y, d_x = 1, -1 #sequences in this direction are counted starting from the right-most column.
    for sty in range(len(board)):
        opens, semis = detect_row(board, col, sty, len(board)-1, length, d_y, d_x)
        open_seq_count += opens
        semi_open_seq_count += semis

    return open_seq_count, semi_open_seq_count

#=============================================================================
    
def search_max(board):
    scores = []
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] != ' ':
                continue
            #put a 'b' on each empty cell and calculate the resulting score
            b = board.copy()
            b[y][x] = 'b'
            scores.append((score(b), y, x))
            b[y][x] = ' '
    
    scores.sort(key=lambda item: item[0], reverse=True)
    return scores[0][1:] #y, x that gives maximum score

#=============================================================================
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

#=============================================================================
   
def is_win(board):
    ds = [(1,0), (0,1), (1,1), (-1,1)] #directions
    for col in ["w", "b"]:
        for d_x, d_y in ds:
            for stx in range(len(board)):
                for sty in range(len(board)): #check every possible 5 adjacent cells on the board
                    x = stx
                    y = sty
                    flag = True #its true iff all 5 cells are the same color
                    for _ in range(5):
                        if x < 0 or x >= len(board) or y < 0 or y >= len(board):
                            flag = False
                            break
                        if board[y][x] != col:
                            flag = False
                            break
                        x += d_x
                        y += d_y
                    if flag:
                        if col == "b":
                            return "Black won"
                        else:
                            return "White won"
                        
    for r in board:
        for x in r:
            if x == " ":
                return "Continue playing"
    
    return "Draw"

#=============================================================================

def print_board(board): 
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

#=============================================================================

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

#=============================================================================
                
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

#=============================================================================
        
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

#=============================================================================
                
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

#=============================================================================

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

#============================================================================= 

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

#============================================================================= 

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print(detect_row(board, "w", 0,x,length,d_y,d_x))
        print("TEST CASE for detect_row FAILED")

#=============================================================================

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print(detect_rows(board, col,length))
        print("TEST CASE for detect_rows FAILED")

#============================================================================= 

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

#============================================================================= 

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

#============================================================================= 

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

#=============================================================================

if __name__ == '__main__':
    print(play_gomoku(8))
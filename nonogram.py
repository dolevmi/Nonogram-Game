#################################################################
# FILE : ex8.py
# WRITER : Dolev Mizrahi , dolevm , 205671738
# EXERCISE : intro2cs2 ex7 2020
# DESCRIPTION: Nonogram Game
#################################################################
import copy
import ex8_helper as help

WHITE = 0
BLACK = 1
EMPTY = -1


# if it's ambivalent, it's unknown

def is_row_okay(lst, chunk):  # TODO: Refactor
    """This function checks if a row perm
     meets the requirements of the blocks"""
    total = 0
    count = []
    k = 0
    for i in lst[0]:
        # counts how many 1's are in a row
        if i == 1:
            if len(count) >= len(chunk):
                return False
            total += i
        else:
            if k >= len(chunk):
                if count == chunk:
                    return True
                return False
            elif total == chunk[k]:
                count.append(total)
                k += 1
                total = 0
            elif total:
                return False
    if k < len(chunk):
        if total == chunk[k]:
            count.append(total)
    if count == chunk:
        return True
    return False


def row_helper(row, blocks, step=0, chunk=0, count=0):
    """This function gets a row and its constraints
    :returns list of lists of all permutations"""
    # Base Case: if program reaches to end of permutation
    if len(row[:step]) >= len(row):
        if is_row_okay([row], blocks):
            return [row]
        return []

    # Recursive Case
    if row[step] == 0:
        ans = row_helper(row, blocks, step + 1, chunk, count)
    elif row[step] == 1:
        ans = row_helper(row[:step] + [1] + row[step + 1:],
                         blocks, step + 1, chunk, count)
    elif row[step] == -1:
        if count >= sum(blocks):
            ans = row_helper(row[:step] + [0] + row[step + 1:],
                             blocks, step + 1, chunk, count)
            return ans
        ans = row_helper(row[:step] + [1] + row[step + 1:],
                         blocks, step + 1, chunk, count + 1)
        ans += row_helper(row[:step] + [0] + row[step + 1:],
                          blocks, step + 1, chunk, count)
    return ans


def get_row_variations(row, blocks):
    return row_helper(row, blocks)


def get_intersection_row(rows):
    """This function checks the board intersection
     :returns list of lists"""
    result = []
    rows_lst = list(zip(*rows))
    for i in range(len(rows_lst)):
        if all(j == rows_lst[i][0] for j in rows_lst[i]):
            result.append(rows_lst[i][0])
        else:
            result.append(-1)
    return result


def build_board(constraints):
    """This function builds the board according to constraints
    :returns list of lists"""
    board = [[-1] * len(constraints[1])] * len(constraints[0])
    cp_board = [row[:] for row in board]
    return cp_board


def is_board_full(board):
    """This function checks if board is full
    :returns bool"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:
                return False
    return True


def scan_horizontal(board, consts):
    """This function scans the board horizontally
    :returns list of lists"""
    for block, row in enumerate(board):
        board[block] = get_intersection_row(get_row_variations
                                            (row, consts[block]))
    return board


def scan_vertical(board, consts):
    """This function scans the board horizontally
    :returns list of lists"""
    columns = list(zip(*board))
    for block, column in enumerate(columns):
        columns[block] = get_intersection_row(get_row_variations
                                              (column, consts[block]))
    return board


def solve_easy_nonogram(constraints):
    """This function solves an easy board"""
    board = build_board(constraints)
    while not is_board_full(board):
        board = scan_horizontal(board, constraints[0])
        board = scan_vertical(board, constraints[1])
    return board


constraints = [[[], [4], [6], [2, 2], [1, 3]], [[], [2], [1], [2, 2], [2, 2]]]
print(solve_easy_nonogram(constraints))

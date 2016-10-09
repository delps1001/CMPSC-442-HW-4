############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import math

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    possible_cells =[]
    for x in range(0, 9):
        for y in range(0, 9):
            possible_cells.append((tuple([x, y])))
    return possible_cells

def sudoku_arcs(regions):

    # First do all arcs that are in the same row or column (easy)
    arcs = []
    # same row
    """
    for z in range(0, 9):
        for x in range(0, 9):
            for y in range(x + 1, 9):
                arcs.append(tuple([tuple([z, x]), tuple([z, y])]))
            # left upper corner
            if (x == 0 and (z == 0 or z == 3 or z == 6)) or (x == 3 and (z == 0 or z == 3 or z == 6)) or (x == 6 and (z == 0 or z == 3 or z == 6)):
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x + 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 2, x + 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x + 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 2, x + 1])]))
            # right upper corner
            if (x == 2 and (z == 0 or z == 3 or z == 6)) or (x == 5 and (z == 0 or z == 3 or z == 6)) or (x == 8 and (z == 0 or z == 3 or z == 6)):
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x - 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 2, x - 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x - 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 2, x - 1])]))
            # left lower corner
            if (x == 0 and (z == 2 or z == 5 or z == 8)) or (x == 3 and (z == 2 or z == 5 or z == 8)) or (x == 6 and (z == 2 or z == 5 or z == 8)):
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x + 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 2, x + 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x + 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 2, x + 1])]))
            # lower right corner
            if (x == 2 and (z == 2 or z == 5 or z == 8)) or (x == 5 and (z == 2 or z == 5 or z == 8)) or (x == 8 and (z == 2 or z == 5 or z == 8)):
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x - 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 2, x - 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x - 2])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 2, x - 1])]))
            # center
            if (x == 1 and (z == 1 or z == 4 or z == 7)) or (x == 4 and (z == 1 or z == 4 or z == 7)) or (x == 7 and (z == 1 or z == 4 or z == 7)):
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x - 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x - 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z - 1, x + 1])]))
                arcs.append(tuple([tuple([z, x]), tuple([z + 1, x + 1])]))

    # same column
    for z in range(0, 9):
        for x in range(0, 9):
            for y in range(x + 1, 9):
                arcs.append(tuple([tuple([x, z]), tuple([y, z])]))
                arcs.append(tuple([tuple([y, z]), tuple([x, z])]))"""
    for x in range(9):
        for y in range(9):
            for r in range(9):
                if (r, y) != (x, y):
                    arcs.append(tuple([(x, y), (r, y)]))
                    if (r, y) not in regions[0][r]:
                        regions[0][r].append((r, y))
            for c in range(9):
                if (x, c) != (x, y):
                    arcs.append(((x, y), (x, c)))
                    if (x, c) not in regions[1][c]:
                        regions[1][c].append((x, c))
            sr = int(math.floor(x/3) * 3)
            sc = int(math.floor(y/3) * 3)

            for r in range(3):
                for c in range(3):
                    if (sr+r, sc+c) != (x, y):
                        arcs.append(((x, y), (sr+r, sc+c)))
                        if (sr+r, sc+c) not in regions[2][sr + (sc/3)]:
                            regions[2][sr + (sc/3)].append((sr+r, sc+c))


    return arcs

def read_board(path):
    file_object = open(path, 'r')
    board = {}
    for x in range(0, 9):
        current_string = file_object.readline()
        for y in range(0, 9):
            if current_string[y] != '*':
                board[tuple([x, y])] = set([int(current_string[y])])
            else:
                board[tuple([x, y])] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    file_object.close()
    return board


class Sudoku(object):

    REGIONS = [[[] for x in range(9)]for y in range(3)]
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs(REGIONS)
    print len(REGIONS[2][0])
    for x in sorted(REGIONS[1][1]):
        print x,

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        values_removed = False
        cell2values = self.board[cell2]
        if len(cell2values) == 1:
            for x in cell2values:
                if x in self.board[cell1]:
                    self.board[cell1].remove(x)
                    values_removed = True
        return values_removed

    def infer_ac3(self):
        queue = self.ARCS[:]

        while len(queue) != 0:
            cell1, cell2 = queue.pop()
            if self.remove_inconsistent_values(cell1, cell2):
                temp = self.ARCS
                for x, y in temp:
                    if x == cell1:
                        queue.append(tuple([y, cell1]))

    def infer_improved(self):
        changed = True
        while changed:
            self.infer_ac3()
            changed = False
            for r in range(len(self.REGIONS)):
                for r_c_b in range(len(self.REGIONS[r])):
                    domain = range(0, 9)
                    current = self.REGIONS[r][r_c_b]
                    print r, r_c_b
                    for i in current:
                        if len(self.board[i]) == 1 and list(self.board[i])[0] in domain:
                            print i, self.board[i]
                            print "REMOVING :" + str(list(self.board[i])[0])
                            domain.remove(list(self.board[i])[0])
                    for d in domain:
                        if sum(list(self.board[k]).count(d) for k in current) == 1:
                            self.board[[k for k in current if list(self.board[k]).count(d) > 0][0]] = set([d])
                            print "CHANGED _________________________ TRUE"
                            changed = True
#TESt for change


    def infer_with_guessing(self):
        print "Here"
        pass

b = read_board('hw4-hard1.txt')
print ""
sudoku = Sudoku(b)
sudoku.infer_improved()
count = 0
for x in sorted(sudoku.board):
    if count % 9 == 0:
        print ""
    print list(sudoku.board[x])[0],
    count = count + 1

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

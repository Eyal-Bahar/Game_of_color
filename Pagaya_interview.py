import copy
import json
from typing import List
from typing import NamedTuple
from typing import Set
from typing import Tuple
from typing import Union

# DO NOT MODIFY THIS CODE

EMPTY = 0


class Insert(NamedTuple):
    column: int
    value: int


class Undo(NamedTuple):
    pass




Move = Union[Insert, Undo]

DEBUG = False
PRINT_TEST_CASE = False


# DO NOT MODIFY THIS CODE

def solution(initial_board_repr: str, moves_strings: List[str], use_extra_patterns: bool):
    if PRINT_TEST_CASE:
        print(json.dumps(initial_board_repr), ",", json.dumps(moves_strings), ",", json.dumps(use_extra_patterns))
    # For simplicity, width is constant.
    initial_board = [[int(c) for c in row.strip()] for row in initial_board_repr.splitlines(keepends=False)]
    # Validate all rows are the same length
    assert len(set(len(row) for row in initial_board)) == 1
    moves = []
    for move_string in moves_strings:
        if move_string[0] == "i":
            moves.append(Insert(int(move_string[1]), int(move_string[2])))
        elif move_string == "u":
            moves.append(Undo())
    return simulate_game(initial_board, moves, use_extra_patterns)


# DO NOT MODIFY THIS CODE
def board_repr(board: List[List[int]]) -> str:
    return "\n".join(map(lambda row: "".join(map(str, row)), board))


# DO NOT MODIFY THIS CODE
def simulate_game(initial_board: List[List[int]], moves: List[Move], use_extra_patterns: bool) -> str:
    game = Game(initial_board, use_extra_patterns)
    for move in moves:
        game.apply_move(move)
        # print(game.board)
    result = board_repr(game.get_board_state())
    if DEBUG:
        print(result)
    return result


# Example test cases
def run_tests():
    # Basic tests for your convenience.
    # Please make sure your code does not crash before submitting it.
    print("Basic Game:: A few insertion steps")
    assert (solution(
        "00000\n"
        "00000\n"
        "00000",
        ["i01", "i02", "i13", "i24"], False
    ) ==
            "00000\n"
            "20000\n"
            "13400")

    print("Basic Game:: insert (-> basic pattern consolidation with column drop)")
    assert (solution(
        "60000\n"
        "70000\n"
        "80800",
        ["i18"], False
    ) ==
            "00000\n"
            "60000\n"
            "70000")
    print("Bonus 2 - Extra Patterns:: insert (-> diagonal pattern search with column consolidation)")
    assert (solution(
        "09000\n"
        "28000\n"
        "13800",
        ["i08"], True
    ) ==
            "00000\n"
            "29000\n"
            "13000")
    print("Bonus 3 - Undo:: insert, undo, insert")
    assert (solution(
        "000\n"
        "000",
        ["i01", "u", "i02"], False
    ) == "000\n"
         "200")


# Your implementation goes here
class Game:
    def __init__(self, initial_board_state: List[List[int]], use_extra_patterns: bool):
        """
        :param initial_board_state: list of table in rows
        :param use_extra_patterns: checking horizontal or diagonal - #todo
        """
        self.board = initial_board_state
        self.extra_patterns = use_extra_patterns


    def get_board_state(self) -> List[List[int]]:
        return self.board# old: [[0] * 3 for _ in range(3)]

    def apply_move(self, move: Move):
        """
        apply users move, check for patterns, destroy patters, and check again to make sure no new ones emerge

        :param move:
        :return:
        """
        # Update user's move
        col = move[0] # which col to update to
        value_to_update_to = move[1] # value to update the col to to
        self.update_board(col, value_to_update_to)

        while patterns_to_destroy is not []:
            # Check for patterns
            patterns_to_destroy = []
            row_patterns = self.check_for_patterns(digonal=False) # Check for row patterns
            patterns_to_destroy = row_patterns
            # Check for diagonal patterns
            if self.extra_patterns:
                diag_patterns = self.check_for_patterns(self.extra_patterns)
                patterns_to_destroy.append(diag_patterns)

            # Destroy patterns # turn patterns to zero
            for place in patterns_to_destroy:
                self.board[place[0]][place[1]]
            if patterns_to_destroy == []:
                break
            # Update board (by pulling down to fill the zeros)
            self.drop_down_on_zeros()


        # # Destroy patterns # turn patterns to zero
        # while patterns_to_destroy != []:
        #     if len(self.where_to_destory) > 2: # minimum chain to destroy is 3 by game rules
        #         while len(self.where_to_destory) > 0:
        #             self.remove_pattern(self.where_to_destory.pop())
        #         self.check_for_patterns()
        #     else:
        #         self.where_to_destory = [] # check this place
        # # Update board (by pulling down to fill the zeros

        # if self.extra_patterns: # check diagonals
        #     self.check_for_patterns(diagonal = self.extra_patterns)  # updates:  self.where_to_destory
        #     if len(self.where_to_destory) > 2:  # minimum chain to destroy is 3 by game rules
        #         while len(self.where_to_destory) > 0:
        #             # for patterns_index in self.where_to_destory: # todo change to pop when can debug here
        #             self.remove_pattern(self.where_to_destory.pop())
        #         self.check_for_patterns(diagonal = self.extra_patterns)

    def update_board(self, col_to_update, value):
        row_to_update = self.find_where_empty(col_to_update)
        if row_to_update !=-1: # update only if row is not full
            self.board[row_to_update][col_to_update] = value

    def find_where_empty(self, col_to_update):
        """
        Checking all rows to see if they are zero, and returning where its firsly not

        :param col_to_update:
        :return:
        """
        for rows in range(len(self.board)):
            if self.board[rows][col_to_update] == 0:
                pass # keep checking next rows until hitting the enc
            else:
                if rows == 0:
                    return -1
                else:
                    return rows-1
        return (len(self.board)-1)

    def check_for_patterns(self, diagonal=False):
        """
        Check for patterns, filter if patterns is not big enough.
        Find pattern by going over each pixel in the chart and check its neighbours for identical neighbours.
        Neighbours are defined by either only row or only diagonal, according to the rules of the game
        """
        self.patterns = []
        # Check for patterns, is diagonal is False then it looks for rows
        for r in range(len(self.board)): # go over rows
            for c in range(len(self.board[0])): # go over colomubs
                self.dsf(r, c, diagonal) # search by depth-search-first (dsf)
        # Filter according to minimali connected rules of the game
        return self.keep_only_minimaly_connected_places(self.patterns)

    def dsf(self, r,c, diagonal):
            """ Based on the Depth-search-first approach, go pixel by pixel, inqueryt about neighbours and write that down
            updates to self.where_to_destory"""
            for s, t in self.neighbours(r, c, diagonal):
                if self.board[s][t] == self.board[r][c] and [s, t] not in self.where_to_destory and self.board[r][c] != 0:
                    self.patterns.append([s, t])
                    self.dsf(s, t, method)

    def neighbours(self, x, y, diagonal):
        """find neighbours, make sure not to step outside array"""
        neighbours_list = []
        if not diagonal: # todo change to bonus
            if y > 0:
                neighbours_list.append([x, y - 1])
            if y < (len(self.board[0]) - 1):
                neighbours_list.append([x, y + 1])
            return neighbours_list
        if diagonal:
            a = 1 #check _diagonals


    def remove_pattern(self, where_to_remove):
        r = where_to_remove[0]
        c = where_to_remove[1]
        if r > 0:
            for i in range(r,0, -1):
                self.board[i][c] = self.board[i-1][c] #todo update all!!
                if self.board[r][c] == 0: # no need to update all the zeros since zero means empty.
                    break
        self.board[0][c] = 0

    def keep_only_minimaly_connected_places(self, patterns):
        patterns.sort(key=lambda x: x[0]) # sort by coloumb
        # split into sub lists to check if sublist has minimal 3 entrys as the game rules require.
        sublists = {}
        for sub in patterns:
            key = sub[0]
            if key not in sublists:
                sublists[key] = []
            sublists[key].append(sub)
        # deleting sublists with less then 3 entries
        for key in sublists.copy().keys():
            if len(sublists[key]) < 3:
                del sublists[key]
        return sublists

    def drop_down_on_zeros(self):
        """
        Go over each row, and check coloum by coloum if there is a zero.
        If there is then collapse the col above it on its self.
        make sure to keeps checking the same row
        """
        for row in range(len(self.board), 1, -1):
            check_this_row = 1
            while check_this_row:
                check_this_row = 0 # dont check this row more than once unless updating
                for col in range(0, len(self.board[0])):
                    if self.board[row][col] == 0:
                        check_this_row = 1  #  check this row again since the board was collapesd and change
                        for collapsing_rows in range(row, 1, -1):
                            self.board[collapsing_rows][col] = self.board[collapsing_rows-1][col]
                        self.board[0][col] = 0





def complexity_analysis():
    # Bonus 1 - write the answer, an explanation is not required.
    return "O(K ** 10 * M ** 2 * N ** 3)"



# Basic tests for your convenience.
# Please make sure your code does not crash before submitting it.
# run_tests()
if __name__ == "__main__":
    run_tests()


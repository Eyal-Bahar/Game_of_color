import numpy as np
import random
import matplotlib.pyplot as plt


class Game:

    def __init__(self, rows, columns, starting_point):
        self.r = rows
        self.c = columns
        self.starting_point = starting_point
        self.complete = 0
        self.color_code_dict = {0: 'y', 1: 'r', 2: 'g', 3: 'b'}
        self.color_code_dict_inverse = {value: key for (key, value) in self.color_code_dict.items()}

    def play(self):
        """ Creates a board (random for now). While the game is not complete,
        its shows the user the board and asks for input how to change the batch.
        Limited to 21 moves """
        moves_counter = 0
        self.create_board()
        while self.complete != 1 and moves_counter < 21:  # todo this!
            self.show_board()
            self.make_move()
            moves_counter += 1

        if moves_counter >= 21:
            print('wha wha wha... Good luck next time')
        if self.complete == 1:
            print('Good job! You ROCK!')

    def create_board(self):
        """ Create the board by randomly assigning numbers to each location in the matrix
        Note that numbers correspont to colors through self.color_code("color") which return a number"""
        self.board = np.empty([self.r, self.c], dtype=int)
        for i in range(self.r):
            for j in range(self.c):
                self.board[i, j] = random.choice(range(4))  # todo maybe enable to have more colors

    def show_board_in_letters(self):
        """ initialize an empty board and write to it the colors accoring to the color_code method"""
        board_in_letters = np.empty([self.r, self.c], dtype=object)
        for i in range(self.r):
            for j in range(self.c):
                board_in_letters[i, j] = self.color_code(self.board[i, j])

    def color_code(self, param):
        """
        Takes paramter number/letter and return the color code letter/number
        """
        ans = -1
        if type(param) == str:
            while ans == -1:
                try:
                    ans = self.color_code_dict_inverse[param]
                except:
                    print('No such color, try again! or quit by writing quit')
                    param = input("Choose from y,r,g,b,:")
                    if param == 'quit':
                        print('Thanks for trying! Good bye!')
                        exit()
            return ans

        if type(param) == int:
            return self.color_code_dict[param]

    def show_board(self):
        plt.figure(1)
        plt.axis('off')  # how to plot image without axis
        plt.imshow(self.coloring(self.board))
        plt.pause(0.000001)
        # plt.show(block=False)


    def make_move(self):
        """
        Take user input as letter, convert to number and then convert connected numbers to that number(color)
        """
        user_input_int = int(self.color_code(input("Choose a color ['b','s','g','y'] : ")))
        self.convert_connected_number(user_input_int)

    def convert_connected_number(self, user_input_int):
        self.where_to_color = [self.starting_point]
        self.find_neighbours_with_same_color_as_starting_point(self.starting_point[0],self.starting_point[1])
        self.set_point_to_color(self.where_to_color, user_input_int)
        # check if after update the game is complete
        self.find_neighbours_with_same_color_as_starting_point(self.starting_point[0], self.starting_point[1])
        checking_game_after_move = np.array(self.where_to_color)
        if checking_game_after_move.size == (self.r * self.c):
            self.complete = 1

    def find_neighbours_with_same_color_as_starting_point(self, pixel_s, pixel_t):
        """go pixel by pixel, inqueryt about neighbours and write that down
        updates to self.where_to_color"""
        for s,t in self.neighbours(pixel_s, pixel_t):
            if self.board[s,t] == self.board[pixel_s,pixel_t] and [s,t] not in self.where_to_color:
                self.where_to_color.append([s,t])
                self.find_neighbours_with_same_color_as_starting_point(s, t)


    def neighbours(self, x, y):
        """find neighbours, make sure not to step outside array"""
        neighbours_list = []
        if x > 0:
            neighbours_list.append([x - 1, y])
        if x < (self.r-1):
            neighbours_list.append([x + 1, y])
        if y > 0:
            neighbours_list.append([x, y - 1])
        if y < (self.c-1):
            neighbours_list.append([x, y + 1])
        return neighbours_list

    def set_point_to_color(self, where_to_color, user_input_int):
        for s, t in where_to_color:
            self.board[s, t] = user_input_int

    def coloring(self, map):
        map2 = map.copy()
        color_map = {0: np.array([255, 255, 0]),  # yellow
                     1: np.array([255, 0, 0]),  # red
                     2: np.array([0, 255, 0]),  # green
                     3: np.array([0, 0, 255])}  # blue
        map_3d = np.ndarray(shape=(map2.shape[0], map2.shape[1], 3), dtype=int)
        for i in range(0, map2.shape[0]):
            for j in range(0, map2.shape[1]):
                map_3d[i][j] = color_map[map[i][j]]
        return map_3d


        for k in color_map:
            map2[map2 == k] = color_map[k]
        return map2


if __name__ == "__main__":
    ## Board defitions
    rows = 10  # todo : make these user input values
    columns = 10
    starting_point = [0, 0]
    ## run game
    h = Game(rows, columns, starting_point)  # todo: 1.option for input board 2.option for more colors
    h.play()
    plt.show()
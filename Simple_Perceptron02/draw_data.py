import sys, random
import pygame
import dill as pickle

DARKGREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 55, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

"""
===================================================
                class Element
===================================================
"""

class Element:
    def __init__(self, x, y, answer):
        ## -0.4547358416942422 -0.5802417851269618 1 -1
        self.input_x = x
        self.input_y = y
        self.coord_x = -10
        self.coord_y = -10
        self.answer = answer
        self.color = (0, 0, 0)

    def __repr__(self):
        return "(coord_x, coord_y: {}, {}), (input_x, input_y: {}, {}), answer: {}".format(
            self.coord_x, self.coord_y, self.input_x, self.input_y, self.answer)

    def read_fileline(self, fileline):
        # x y  width height color         contents
        # 0 13 20    20     255 0 255     m
        mylist = []
        try:
            mylist = fileline.split(" ")
        except:
            return []
        # ['49', '43', '20', '20', '255', '0', '255', 'm']
        self.input_x = int(mylist[0])
        self.input_y = int(mylist[1])
        self.width = int(mylist[2])
        self.height = int(mylist[3])
        color_list = [0, 0, 0]
        color_list[0] = int(mylist[4])
        color_list[1] = int(mylist[5])
        color_list[2] = int(mylist[6])
        self.color = tuple(color_list)
        self.contents = mylist[7]

    def datapoint_parse_fileline(self, fileline):
        #"-0.10963565633547623 -0.9693369582057646 1 -1"
        mylist = fileline.split(" ")
        self.input_x = float(mylist[0])
        self.input_y = float(mylist[1])
        # line is skipped because we're not using the bias
        self.answer = int(mylist[3])

    # def tile_color(self):
    #     temp = constants.GOLD
    #     if self.contents == "m":
    #         temp = constants.DARKGREY
    #     if self.contents == ".":
    #         temp = constants.GREEN
    #     if self.contents == "p":
    #         temp = constants.BLACK
    #     if self.contents == "n":
    #         temp = constants.RED
    #     if self.contents == "c":
    #         temp = self.color
    #         print(temp)
    #         # if self.activation():
    #         #     temp = constants.UGLY_PINK
    #         # else:
    #         #     temp = constants.BROWN
    #     return temp

    def get_rect(self):
        return pygame.Rect(self.x + self.width, self.y + self.height, self.width, self.height)

    def _change_color_helper(self):
        color_list = [0, 0, 0]
        for i in range(0, 3):
            if self.color[i] in [0, 1, 2, 3, 4, 5]:
                color_list[i] = 6
            elif self.color[i] in [250, 251, 252, 253, 254, 255]:
                color_list[i] = 249
            else:
                color_list[i] = self.color[i]
        return color_list

    def change_color(self):
        # --------------------
        change_color_up = random.randint(0, 1)  # true and false
        the_change = random.randint(0, 3)
        axis = random.randint(0, 2)  # 0, 1, or 2
        # --------------------
        new_color_list = self._change_color_helper()
        if change_color_up == 1:
            new_color_list[axis] = new_color_list[axis] + the_change
        else:
            new_color_list[axis] = new_color_list[axis] - the_change
        self.color = tuple(new_color_list)
        if ((self.color[0] < 0 or self.color[0] > 255) or
                (self.color[1] < 0 or self.color[1] > 255) or
                (self.color[2] < 0 or self.color[2] > 255)):
            print("{}".format(new_color_list))
            print("Element.change_color: contains an illegal value.")
            breakpoint()

    def transform_data_for_display(self, width, height):
        # This assumes that input_x and input_y are
        # between -0.999 and 0.999
        print("data before transform: {},{}".format(self.input_x, self.input_y))
        x = (self.input_x + 1) * width
        y = (self.input_y + 1) * height
        print("data after transform: {},{}".format(x, y))
        return x, y

    def draw(self, surface, width, height):
        x, y = self.transform_data_for_display(width, height)
        # --------------------------------------------------
        print("draw: {},{}".format(x, y))
        myrect = pygame.Rect(x * width, y * height, width, height)
        pygame.draw.rect(surface, self.color, myrect)

    def debug_draw_tile(self, surface, x_coord, y_coord, width, height, color):
        # print("draw: {},{}".format(x_coord, y_coord))
        print("draw * width/height: {},{}".format(x_coord * width, y_coord * height))
        # myrect1 = pygame.Rect(x_coord, y_coord, width, height)
        myrect2 = pygame.Rect(x_coord * width, y_coord * height, width, height)
        # pygame.draw.rect(surface, color, myrect1)
        pygame.draw.rect(surface, color, myrect2)

    def print_fileline(self):
        # x  y  w  h  color        contents
        # 0 13 20 20 255 0 255     m
        return "{} {} {} {} {} {} {} {}".format(self.x, self.y, self.width, self.height,
                                                self.color[0], self.color[1], self.color[2], self.contents)



"""
===================================================
                class Critter
===================================================
"""


class Critter(Element):
    def __init__(self, x, y, width, height, color, contents):
        Element.__init__(self, x, y, width, height, color, contents)
        self.guessed_correctly = False

    def guess(self):
        """Guessing whether a particular point is above or below the line."""
        # At the moment, the quess is going to be random.
        myran = random.randint(0, 1)
        if myran == 0:
            return True
        return False

    def color_calculated(self, myPerceptron):
        """Determins whether the critter made a correct guess."""
        # let the critter guess whether they are
        # under the line
        critter_guess = self.guess()
        # is their guess correct?
        answer = myPerceptron.under_the_line(self.x, self.y)
        if answer != critter_guess:
            self.color = RED
        else:
            self.color = BLUE


"""
===================================================
                class World
===================================================
"""


class World:
    def __init__(self, datapoints_file, tiles_wide=50, tiles_high=50, tile_width=10, tile_height=10):
        self.number_of_tiles_wide = tiles_wide
        self.number_of_tiles_high = tiles_high
        self.world = []
        self.element_width = tile_width
        self.element_height = tile_height
        self.datapoints_file = datapoints_file
        # self.scale = scale
        self.screenwidth = (self.number_of_tiles_wide * self.element_width)
        self.screenheight = (self.number_of_tiles_high * self.element_height)
        self.slope_of_the_line = None

    def initialize_game(self, title="Drawing Data"):
        pygame.init()
        self.surface = pygame.display.set_mode((self.screenwidth, self.screenheight))
        print("screenwidth: {}, screenheight: {}".format(self.screenwidth, self.screenheight))
        pygame.display.set_caption(title)
        self.surface.fill(WHITE)

    def _get_contents(self, i, j):
        contents = ""
        if i == 0 or j == 0:
            contents = "m"
        elif i == (self.number_of_tiles_wide - 1) or i == (self.number_of_tiles_high - 1):
            contents = "m"
        elif j == (self.number_of_tiles_wide - 1) or j == (self.number_of_tiles_high - 1):
            contents = "m"
        else:
            rannum = random.randint(1, 10)
            if rannum == 1:
                contents = "c"
            else:
                contents = "."
        return contents

    # ------------- doing stuff (top) ------------------

    def move_critters_random(self):
        for row in self.world:
            for elem in row:
                if elem.contents == "c":
                    elem.move_randomly()

    def change_color_critters_random(self):
        for row in self.world:
            for elem in row:
                if elem.contents == "c":
                    elem.change_color()
                    if elem.under_the_line():
                        elem.color = (0, 0, 0)

    def do_stuff(self):
        for datapoint in self.data:
            if datapoint.answer == 1:
                datapoint.color = RED

    def debug_do_stuff(self):
        pass

    # ------------- doing stuff (bottom) ------------------

    def _get_slope(self):
        x = 0
        y = self.slope_of_the_line(x)
        x1 = 10
        y1 = self.slope_of_the_line(x1)
        b = self.slope_of_the_line(0)
        m = (y-y1)/(x-x1)
        return "{}x + {}".format(m, b)

    def draw_line(self):
        x = 0
        x1 = self.screenwidth
        y = self.slope_of_the_line(x)
        y1 = self.slope_of_the_line(x1)
        print("slope of the line: {}".format(self.slope_of_the_line))
        pygame.draw.line(self.surface, BLACK, (x, y), (x1, y1), 4)

    def debug_draw_line(self, slope_line, x):
        x1 = self.screenwidth
        y = slope_line(x)
        y1 = slope_line(x1)
        print("x,y: {},{} || x1,y1: {},{}".format(x, y, x1, y1))
        pygame.draw.line(self.surface, BLACK, (x, y), (x1, y1), 4)

    def draw_grid(self):
        for i in range(self.screenwidth):
            new_height = round(i * self.element_height)
            new_width = round(i * self.element_width)
            pygame.draw.line(self.surface, BLACK, (0, new_height), (self.screenwidth, new_height), 1)
            pygame.draw.line(self.surface, BLACK, (new_width, 0), (new_width, self.screenheight), 1)

    def draw_world(self):
        """
        The datapoints, natively, range between -0.999 and 8.999. But that is difficult to display
        in Pygame, so I transform them before I display them, but that is ONLY to make them
        easier to display.
        """
        print("------------------------------------------")
        print("data len: {}".format(len(self.data)))
        for dataelem in self.data:
            dataelem.draw(self.surface, self.element_width, self.element_height)
        self.draw_grid()
        self.draw_line()
        # --------- debugging -----------
        # x = 0
        # y = 38
        # width = constants.BLOCK_WIDTH
        # height = constants.BLOCK_HEIGHT
        # temprect = pygame.Rect(x * width, y * height, width, height)
        # pygame.draw.rect(self.surface, (25, 25, 255), temprect)

    def debug_draw_tile(self, x_coord, y_coord, slope_line, color):
        my_tile = Element(x_coord, y_coord, 0)
        my_tile.debug_draw_tile(self.surface, x_coord, y_coord, self.element_width, self.element_height, color)
        self.draw_grid()
        self.debug_draw_line(slope_line, 0)

    def write_map(self, mapfile):
        with open(mapfile, "w") as f:
            for row in self.world:
                for elem in row:
                    f.write(elem.print_fileline() + "\n")
                f.write("=\n")

    def _generate_data_point(self):
        # generate random number between -1.0 and 1.0
        mycoin = random.randint(0, 1)
        x = random.random()
        if mycoin == 0:
            x = x * -1
        return x

    # def convert_input_to_map_coords(self):
    #     for datapoint in self.data:
    #         datapoint.coord_x = round(datapoint.input_x * self.scale)
    #         datapoint.coord_y = round(datapoint.input_y * self.scale)


    # def read_mapfile(self, filepath, slope_of_the_line):
    #     new_data = []
    #     with open(filepath, "r") as f:
    #         mylist = f.readlines()
    #     mylist = [i.strip() for i in mylist]
    #     self.file_metadata = [i for i in mylist if i[0] == "#"]
    #     mylist = [i for i in mylist if i[0] != "#"]
    #     # [print(i) for i in self.file_metadata]
    #     # [print(i) for i in mylist]
    #     for i in range(50):
    #         for j in range(50):
    #             x = self._generate_data_point()
    #             y = self._generate_data_point()
    #             # new_datapoint = Datapoint(x, y, self.bias, self.slope_of_the_line)
    #             new_datapoint = Element(i, j, x, y, WHITE, slope_of_the_line)
    #             new_data.append(new_datapoint)
    #     self.data = new_data
    #     # # ------------------------
    #     # with open(mapfile, "r") as f:
    #     #     mylist = f.readlines()
    #     # mylist = [i.strip() for i in mylist]
    #     # # [print(i) for i in mylist]
    #     # if len(mylist) == 0:
    #     #     print("Error. Tried to read data from file but received an empty list.")
    #     #     breakpoint()
    #     # row = []
    #     # for line in mylist:
    #     #     # print(line)
    #     #     if line != "=":
    #     #         elem = Element(-1, -1, -1, -1, constants.UGLY_PINK, "")
    #     #         elem.read_fileline(line)
    #     #         # elem.debug_print()
    #     #         row.append(elem)
    #     #         # [i.debug_print() for i in row]
    #     #     else:
    #     #         self.world.append(row)
    #     #         row = []

    def read_datapoints(self):
        # get slope of the line
        # ----------------------------------
        # self.slope_of_the_line = pickle.load(open("save.p", "rb"))
        self.slope_of_the_line = pickle.load(open("slope_of_the_line.p", "rb"))
        print("slope of the line in read_datapoints():")
        x = 0
        y = self.slope_of_the_line(x)
        x1 = 10
        y1 = self.slope_of_the_line(x1)
        b = self.slope_of_the_line(0)
        m = (y-y1)/(x-x1)
        print("{}x + {}".format(m, b))
        # for i in range(0, 10, 2):
        #     print("x, y: {}, {}".format(i, self.slope_of_the_line(i)))
        # ----------------------------------
        new_data = []
        with open(self.datapoints_file, "r") as f:
            mylist = f.readlines()
        mylist = [i.strip() for i in mylist]
        if len(mylist) == 0:
            sys.exit("Error in World.read_datapoints(). len(mylist) == 0.")
        # separate metadata from data
        self.file_metadata = [i for i in mylist if i[0] == "#"]
        # ----------------------------------
        mylist = [i for i in mylist if i[0] != "#"]
        bias = int(mylist[0])
        mylist = mylist[1:]
        # ----------------------------------
        # [print(i) for i in self.file_metadata]
        # [print(i) for i in mylist]
        if len(mylist) == 0:
            sys.exit("Error in World.read_datapoints(). len(mylist) == 0.")
        for aline in mylist:
            my_element = Element(-1, -1, -10)
            my_element.datapoint_parse_fileline(aline)
            new_data.append(my_element)
        self.data = new_data

    # def debug_read_datapoint(self, x, y, slope_of_line):
    #     new_data = []
    #     my_element = Element(x, y, -10)
    #     new_data.append(my_element)
    #     self.data = new_data
    #
    # def debug_draw_datapoints(self):
    #     if len(self.data) == 0:
    #         sys.exit("Error in World.debug_draw_datapoints(). There are no datapoints to draw!")
    #     for datapoint in self.data:
    #         print(datapoint)

    # def debug_draw_world(self):
    #     if len(self.world) == 0:
    #         sys.exit("Error in World.debug_draw_world(). There is no world to draw!")
    #     # print(self.world)
    #     for row in self.data:
    #         rowstring = ""
    #         for elem in row:
    #             rowstring = "{}{}".format(rowstring, elem.contents)
    #         print(rowstring)

    def datapoints_debug_print(self):
        for item in self.data:
            print(item)

    def debug_print(self):
        if len(self.world) == 0:
            print("Error in World.debug_print. len(self.world) == 0")
        for row in self.world:
            if len(row) == 0:
                print("Error in World.debug_print. len(row) == 0.")
            for elem in row:
                elem.debug_print()


"""
===================================================
===================================================
"""

def game_loop(game_world):
    FPS = 1
    fpsClock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # game_world.write_map()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # game_world.write_map()
                    pygame.quit()
                    sys.exit()

        # 1. do stuff
        # --------------------------------------------
        game_world.do_stuff()
        # game_world.debug_do_stuff()

        # 2. draw stuff
        # --------------------------------------------
        game_world.draw_world()
        pygame.display.update()
        fpsClock.tick(FPS)
        # sys.exit("--- end in draw_data.py game_loop() ---")

# def debug_testing():
#     scale = 10 # scale is used for transforming points between -1 and 1 into screen coords.
#     datapoints_file = ""
#     game_world = World(datapoints_file, scale, tiles_wide=41, tiles_high=41, tile_width=20, tile_height=20)
#
#     # game_world.debug_print()
#     # my_slope = lambda x: x
#     # game_world.debug_read_datapoint(1, 1, my_slope)
#     # game_world.datapoints_debug_print()
#     game_world.initialize_game("Debugging")
#     # game_world.draw_world()
#
#     # game_world.convert_input_to_map_coords()
#
#     game_loop(game_world)


def main():
    print("--- Begin Program: draw_data.py ---")
    datapoints_file = "/Users/BigBlue/Documents/Programming/Python/neural_networks/perceptron_hello_world/second_try/datapoints.txt"
    output_file = "/Users/BigBlue/Documents/Programming/Python/neural_networks/perceptron_hello_world/second_try/draw_data_log01.txt"
    # scale = 10 # scale is used for transforming points between -1 and 1 into screen coords.
    game_world = World(datapoints_file, tiles_wide=41, tiles_high=41, tile_width=20, tile_height=20)

    # game_world.debug_print()
    game_world.read_datapoints()
    # game_world.datapoints_debug_print()
    game_world.initialize_game()
    game_world.draw_world()

    # game_world.convert_input_to_map_coords()
    # game_world.debug_draw_datapoints()

    # game_world.write_map(output_file)
    game_loop(game_world)

if __name__=="__main__":
    if len(sys.argv) == 1:
        main()
        # debug_testing()
    elif len(sys.argv) == 2:
        arg = sys.argv(1)
        if arg == "debug":
            pass
            # debug_testing()

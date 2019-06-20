import tkinter as tk
import sys, random

# ==================================================================
#                         WorldMap
# ==================================================================

class WorldMap:
    def __init__(self, tiles_wide):
        self.tiles_wide = tiles_wide
        self.world_map = self.initialize_world()
        self.player_x = -1
        self.player_y = -1
        self.food_x = -1
        self.food_y = -1

    def __repr__(self):
        self.build_world_map()
        s = ""
        # s += "player: {},{}\n".format(self.player_x, self.player_y)
        # s += "food: {},{}\n".format(self.food_x, self.food_y)
        for row in self.world_map:
            r = ""
            for elem in row:
                if elem == "player":
                    r += "[P]"
                elif elem == "food":
                    r += "[F]"
                elif elem == "grass":
                    r += "[.]"
                else:
                    print("Input not recognized: {}".format(elem))
                    print("Error in WorldMap.__repr__")
                    sys.exit()
            s += r + "\n"
        return s

    def build_world_map(self):
        filled = False
        for i in range(self.tiles_wide):
            for j in range(self.tiles_wide):
                if i == self.player_x:
                    if j == self.player_y:
                        self.world_map[i][j] = "player"
                        filled = True
                if i == self.food_x:
                    if j == self.food_y:
                        self.world_map[i][j] = "food"
                        filled = True
                if filled == False:
                    self.world_map[i][j] = "grass"
                filled = False

    def new_food_position(self, x, y):
        self.food_x = y
        self.food_y = x

    def new_player_position(self, x, y):
        self.player_x = y
        self.player_y = x

    def initialize_world(self):
        temp_array = []
        for i in range(self.tiles_wide):
            row_array = []
            for j in range(self.tiles_wide):
                row_array.append("grass")
            temp_array.append(row_array)
        return temp_array

# ==================================================================
#                         Food
# ==================================================================

class Food:
    def __init__(self, canvas, x, y, food_size, world_map):
        self.x = x
        self.y = y
        self.food_size = food_size
        self.world_map = world_map
        self.canvas = canvas
        # self.body = self.canvas.create_rectangle(self.x, self.y, self.food_size, self.food_size, fill="#B20404")
        x = self.x * self.food_size
        y = self.y * self.food_size
        self.body = self.canvas.create_rectangle(x, y, x + self.food_size, y + self.food_size, fill="#B20404")
        # self.x += 1
        # self.canvas.move(self.body, 20, 0) # right
        # self.y += 1
        # self.canvas.move(self.body, 0, 20) # down
        self.world_map.new_food_position(self.x, self.y)
        # print("food position: {},{}".format(self.x, self.y))

# ==================================================================
#                         Player
# ==================================================================

class Player:
    def __init__(self, canvas, x, y, player_size, board_size, world_map):
        # myObject.__init__(self, canvas, x, y, player_size)
        self.x = x
        self.y = y
        self.player_size = player_size
        self.canvas = canvas
        self.board_size = board_size
        self.world_map = world_map
        self.body = self.canvas.create_rectangle(self.x, self.y, self.player_size, self.player_size, fill="#476042")
        self.world_map.new_player_position(self.x, self.y)
        # print("player position: {},{}".format(self.x, self.y))
        # print("In move_player_old: {}".format(myexp))
        # myexp[0] = 20
        # print("In move_player_new: {}".format(myexp))

    # def draw(self):
    #     self.canvas.create_rectangle(self.x, self.y, self.player_size, self.player_size, fill="#476042")

    def move_player(self, event):
        key = event.keysym
        # print("self.x: {}, self.y: {}".format(self.x, self.y))
        if key == "Left":
            if self.x > 0:
                self.x -= 1
                self.canvas.move(self.body, -20, 0)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Right":
            if (self.x * self.player_size) < self.board_size-self.player_size:
                self.x += 1
                self.canvas.move(self.body, 20, 0)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Up":
            if self.y > 0:
                self.y -= 1
                self.canvas.move(self.body, 0, -20)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Down":
            if (self.y * self.player_size) < self.board_size - self.player_size:
                self.y += 1
                self.canvas.move(self.body, 0, 20)
                self.world_map.new_player_position(self.x, self.y)

# ==================================================================
#                         Game
# ==================================================================

class Game(tk.Tk):
    def __init__(self, player_x, player_y, player_size, food_x, food_y, tiles_wide):
        tk.Tk.__init__(self)
        self.center(self)
        player_size = player_size
        self.tiles_wide = tiles_wide
        self.board_width = self.tiles_wide * player_size
        self.canvas = tk.Canvas(self, width=self.board_width, height=self.board_width)
        self.canvas.pack(fill="both", expand=True)
        self.world_map = WorldMap(self.tiles_wide)
        self.player = Player(self.canvas, player_x, player_y, player_size, self.board_width, self.world_map)
        self.food = Food(self.canvas, food_x, food_y, player_size, self.world_map)
        # self.world = self.initialize_world()
        self.bind("<Key>", self.player.move_player)
        self.bind('<Escape>', self.program_close)

    # def __repr__(self):
    #     s = ""
    #     for row in self.world:
    #         s += " ".join(row) + "\n"
    #     return s

    # def debug_print(self):
    #     for row in self.world:
    #         # for elem in row:
    #         print(row)

    def program_close(self, event):
        print(self.world_map)
        # master.withdraw() # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing

    def center(self, myroot):
        # from:
        # https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        # print("Width", windowWidth, "Height", windowHeight)
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

# ==================================================================
# ==================================================================

def generate_random_weights():
    filepath = "weights.txt"
    weight_array = []
    for _ in range(32):
        temp = [random.random(), random.random(), random.random(), random.random(), random.random()]
        weight_array.append(temp)
    # print(weight_array)

if __name__ == "__main__":
    generate_random_weights()
    player_x = 0
    player_y = 0
    player_size = 20
    food_x = 0
    food_y = 1
    tiles_wide = 10
    game = Game(player_x, player_y, player_size, food_x, food_y, tiles_wide)
    game.mainloop()

# master = Tk()
#
# cell_size = 20
# x = 0
# y = 0
#
# w = Canvas(master, width=500, height=500)
# w.pack()


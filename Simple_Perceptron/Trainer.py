import random

"""
================================================================
                     class Trainer
================================================================
"""

class Trainer():
    def __init__(self, width, height):
        x = random.uniform((-1 * width)/2, width/2)
        y = random.uniform((-1 * height)/2, height/2)
        self.inputs = [x, y, 1]
        self.answer = self._activate(x, y)

    def create_from_file(self, x, y, bias, answer):
        self.inputs = [x, y, bias]
        self.answer = answer

    # def create_input(self):
    #     x = random.uniform(-1, 1)
    #     y = random.uniform(-1, 1)
    #     self.inputs = [x, y, 1]
    #     self.answer = self._activate(x, y)

    def _activate(self, x, y):
        the_line = self._f(x)
        if y < the_line:
            return -1
        return 1

    def _f(self, x):
        return (2*x)+1

    def file_line(self):
        return "{} {} {} {}\n".format(self.inputs[0], self.inputs[1], self.inputs[2], self.answer)

    def debug_print(self):
        print("inputs: {}, answer: {}".format(self.inputs, self.answer))
"""
================================================================
                     class Training
================================================================
"""

class Training():
    def __init__(self, number_items_in_array, width, height):
        self.training_array = []
        for i in range(number_items_in_array):
            temp = Trainer(width, height)
            self.training_array.append(temp)

    def write_to_file(self, filepath, weights):
        mystring = ""
        for item in weights:
            mystring = "{} {}".format(mystring, str(item))
        mystring = "{}{}".format(mystring, "\n")
        with open(filepath, "w") as f:
            f.write(mystring)
            for item in self.training_array:
                f.write(item.file_line())

    def read_from_file(self, filepath):
        mylist = []
        with open(filepath, "r") as f:
            filelist = f.readlines()
        filelist = [i.strip() for i in filelist]
        # print(filelist)
        # training_data = ''.join(filelist)

        # [print(i) for i in training_data]
        # The weights are thrown away here because they are read in
        # and used by the perceptron, elsewhere.
        self.training_array = []
        weights = filelist[0:1]
        for fileline in filelist[1:]:
            # print(fileline)
            mylist = fileline.split(' ')
            # print("This is the list: {}".format(mylist))
            x = float(mylist[0])
            y = float(mylist[1])
            bias = int(mylist[2])
            answer = int(mylist[3])
            # print("x: {}, y: {}, bias: {}, answer: {}".format(x, y, bias, answer))
            temp = Trainer(-1, -1)
            temp.create_from_file(x, y, bias, answer)
            self.training_array.append(temp)

    def get_x_list_correct(self):
        x_list = []
        for item in self.training_array:
            if item.answer == 1:
                x_list.append(item.inputs[0])
        return x_list

    def get_y_list_correct(self):
        y_list = []
        for item in self.training_array:
            if item.answer == 1:
                y_list.append(item.inputs[1])
        return y_list

    def get_x_list_incorrect(self):
        x_list = []
        for item in self.training_array:
            if item.answer == -1:
                x_list.append(item.inputs[0])
        return x_list

    def get_y_list_incorrect(self):
        y_list = []
        for item in self.training_array:
            if item.answer == -1:
                y_list.append(item.inputs[1])
        return y_list

def main():
    # print("x,y: {},{} answer: {}, f(x): {}".format(x, y, answer, (2*x)+1))
    filepath = "data.txt"
    screenwidth = 400
    screenheight = 400
    number_of_items_in_array = 20
    mytrainer = Training(number_of_items_in_array, screenwidth, screenheight)
    mytrainer.read_from_file(filepath)
    # mytrainer.write_to_file(filepath)
    print(mytrainer.get_x_list())
    print(mytrainer.get_y_list())

if __name__ == "__main__":
        main()

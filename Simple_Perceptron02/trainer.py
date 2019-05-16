import random, sys
import dill as pickle
import draw_data

"""
================================================================
                     class Datapoint
================================================================
"""

class Datapoint:

    def __init__(self, bias):
        self.bias = bias
        self.x = -10
        self.y = -10
        self.answer = -10

    def create_datapoint(self, x, y, answer):
        self.x = x
        self.y = y
        self.answer = answer

    def inputs(self):
        return [self.x, self.y, self.bias]

    def get_as_fileline(self):
        return "{} {} {} {}\n".format(self.x, self.y, self.bias, self.answer)

    def parse_as_fileline(self, fileline):
        "-0.10963565633547623 -0.9693369582057646 1 -1"
        mylist = fileline.split(" ")
        self.x = float(mylist[0])
        self.y = float(mylist[1])
        self.bias = int(mylist[2])
        self.answer = int(mylist[3])

    def debug_print(self):
        print("(x,y: {},{} bias: {}), answer: {}".format(self.x, self.y, self.bias, self.answer))
"""
================================================================
                     class Trainer
================================================================
"""

class Trainer():

    def __init__(self, number_of_datapoints, bias, slope_of_the_line, metadata=["#There is no metadata."]):
        self.number_of_datapoints = number_of_datapoints
        self.bias = bias
        self.file_metadata = metadata
        self.slope_of_the_line = slope_of_the_line
        self.data = []

    def _generate_data_point(self):
        # generate random number between -1.0 and 1.0
        mycoin = random.randint(0, 1)
        x = random.random()
        if mycoin == 0:
            x = x * -1
        return x

    def _get_slope(self):
        x = 0
        print("slope of the line: {}".format(self.slope_of_the_line))
        y = self.slope_of_the_line(x)
        x1 = 10
        y1 = self.slope_of_the_line(x1)
        b = self.slope_of_the_line(0)
        m = (y-y1)/(x-x1)
        return "{}x + {}".format(m, b)

    def generate_data(self, bias):
        # generate random numbers between -1.0 and 1.0
        print("in trainer.py -> Trainer.generate_data()")
        print("slope of the line: {}".format(self._get_slope()))
        new_data = []
        for i in range(self.number_of_datapoints):
            x = self._generate_data_point()
            y = self._generate_data_point()
            answer = self._activate(x, y)
            new_datapoint = Datapoint(bias)
            new_datapoint.create_datapoint(x, y, answer)
            new_data.append(new_datapoint)
        self.data = new_data

    # --------------------------------------------------
    # These two defs used to be in Datapoint.

    def _activate(self, x, y):
        print("=======================")
        print("slope of the line in trainer.py Trainer._activate: {}".format(self._get_slope()))
        y1 = self._f(x)
        if y < y1:
            return -1
        return 1

    def _f(self, x):
        """The function for the lope of the line."""
        return self.slope_of_the_line(x)

    # --------------------------------------------------

    def draw_datapoints(self):
        draw_data.main()

    def read_datapoints_from_file(self, filepath):
        # unpickle our lambda expression, slope_of_the_line
        self.slope_of_the_line = pickle.load(open("slope_of_the_line.p", "rb"))
        # get the rest of our data.
        new_data = []
        with open(filepath, "r") as f:
            mylist = f.readlines()
        mylist = [i.strip() for i in mylist]
        # separate metadata from data
        self.file_metadata = [i for i in mylist if i[0] == "#"]
        # ----------------------------------
        mylist = [i for i in mylist if i[0] != "#"]
        bias = int(mylist[0])
        mylist = mylist[1:]
        # ----------------------------------
        # [print(i) for i in self.file_metadata]
        # [print(i) for i in mylist]
        for aline in mylist:
            # print("line: {}".format(aline))
            new_datapoint = Datapoint(bias)
            new_datapoint.parse_as_fileline(aline)
            new_data.append(new_datapoint)
        self.data = new_data

    def write_datapoints_to_file(self, filepath):
        # pickle the formula for the slope of the line
        # print("in trainer.py -> write_datapoints_to_file(). slope: {}".format(self._get_slope()))
        pickle.dump(self.slope_of_the_line, open("slope_of_the_line.p", "wb"))
        with open(filepath, "w") as f:
            for aline in self.file_metadata:
                f.write(aline)
            f.write("\n{}\n".format(self.bias))
            for datapoint in self.data:
                f.write(datapoint.get_as_fileline())
        # sys.exit("write_datapoints_to_file. sys.exit()")

    def file_line(self):
        return "{} {} {} {}\n".format(self.inputs[0], self.inputs[1], self.inputs[2], self.answer)

    def debug_print(self):
        print("Printing {} records from class Trainer.".format(len(self.data)))
        if len(self.data) == 0:
            sys.exit("Error in Trainer.debug_print(). len(self.data) == 0.")
        print("slope of the line: {}".format(self.slope_of_the_line))
        print("bias: {}".format(self.bias))
        for aline in self.file_metadata:
            print(aline)
        for datapoint in self.data:
            datapoint.debug_print()

"""
================================================================
================================================================
"""

def main():
    # print("x,y: {},{} answer: {}, f(x): {}".format(x, y, answer, (2*x)+1))
    filepath = "datapoints.txt"
    screenwidth = 400
    screenheight = 400
    bias = 1
    number_of_items_in_array = 20
    metadata = []
    slope_of_the_line = lambda x: x
    metadata.append("#data from trainer.py")
    # -------------------------------------
    mytrainer = Trainer(number_of_items_in_array, bias, slope_of_the_line, metadata)
    mytrainer.generate_data(bias)
    # mytrainer.read_datapoints_from_file(filepath)
    mytrainer.slope_of_the_line = slope_of_the_line
    mytrainer.write_datapoints_to_file(filepath)
    # mytrainer.debug_print()
    mytrainer.draw_datapoints()

if __name__ == "__main__":
    main()
    # exp01_dump()
    # exp01_load()

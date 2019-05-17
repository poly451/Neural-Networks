import sys
import trainer
import perceptron
import dill as pickle

def help():
    # training_data = "datapoints.txt" # training data
    # # testing_data = "testing_data.txt" # testing data
    # # generate_training_data(1000, training_data)
    # input_data = read_data(training_data)
    # test_neural_network(input_data)
    print("")
    print("====================================================")
    print("Welcome to FirstPerceptron!")
    print("-----------------------------")
    print("I'm the, Hello world!, of neural network programs.")
    print("I can generate a training set of data, train myself to")
    print("accurately classify the data, and then test myself to ")
    print("make sure I really do know what I'm doing.")
    print("")
    print("Here are the commands I understand:")
    print("")
    print("generate_data:")
    print("Generates BOTH training and testing datasets.")
    print("")
    print("train_perceptron:")
    print("Trains the perceptron on a data set.")
    print("")
    print("test_perceptron:")
    print("Tests the perceptron on new data to make sure it really is a good classifier.")
    print("")
    print("view_training_data:")
    print("Displays the training data.")
    print("")
    print("set_slope_of_line:")
    print("Input equation of the form: mx+1")
    print("")
    print("view_slope_of_line:")
    print("Tells you what formula (of the form mx + b) I'm using.")
    print("")
    print("--help and -h:")
    print("Presents this information.")
    print("====================================================")
    print("")

"""
Training/Testing
"""
def generate_training_data(number_of_items_in_population, filepath, slope_of_the_line):
    bias = 1
    metadata = []
    metadata.append("#data from FirstPerceptron.py")
    # -------------------------------------
    mytrainer = trainer.Trainer(number_of_items_in_population, bias, slope_of_the_line, metadata)
    mytrainer.generate_data(bias)
    mytrainer.slope_of_the_line = slope_of_the_line
    mytrainer.write_datapoints_to_file(filepath)

def read_data(filepath):
    number_of_datapoints = -10
    bias = -10
    slope_of_the_line = None
    metadata = []
    mytrainer = trainer.Trainer(number_of_datapoints, bias, slope_of_the_line, metadata)
    mytrainer.read_datapoints_from_file(filepath)
    # mytrainer.draw_datapoints()
    return mytrainer.get_input_data()

def view_training_data(filepath):
    number_of_items_in_population = -10
    bias = -10
    slope_of_the_line = None
    metadata = []
    mytrainer = trainer.Trainer(number_of_items_in_population, bias, slope_of_the_line, metadata)
    # -------------------------------------
    mytrainer.read_datapoints_from_file(filepath)
    mytrainer.draw_datapoints()

def generate_testing_data(number_of_items_in_population, filepath, slope):
    generate_training_data(number_of_items_in_population, filepath, slope)

# ------------------------------------

def train_neural_network(input_data):
    number_of_inputs = 3
    learning_rate = 0.00001
    brain_cell = perceptron.Perceptron(number_of_inputs, learning_rate)
    print("--------------------------------")
    memory = []
    max_gens = 1000
    gen = 0
    correct = 0
    for i in range(max_gens):
        correct = 0
        for item in input_data:
            inputs = [item[0][0], item[0][1], item[0][2]]
            # a correct guess = 0, incorrect = 2 or -2
            error = brain_cell.train(inputs, item[0][3])
            # print(error)
            if error == 0:
                correct += 1
        gen += 1
        cor_per = (correct / len(input_data)) * 100
        if gen == 1:
            memory.append(cor_per)
        if gen == max_gens - 1:
            memory.append(cor_per)
        print("gen: {}, accuracy: {}".format(gen, cor_per))
        if correct == len(input_data):
            print("Got it!!! :-) Number of generations: {}".format(gen))
            brain_cell.write_weights_to_file()
            sys.exit()
    print("first: {}, last: {}".format(memory[0], memory[1]))

def test_neural_network(input_data):
    number_of_inputs = 3  # we're not going to be using this
    learning_rate = -100  # we're not going to be using this
    load_data = True
    brain_cell = perceptron.Perceptron(number_of_inputs, learning_rate, load_data)
    print("--------------------------------")
    correct = 0
    for item in input_data:
        inputs = [item[0][0], item[0][1], item[0][2]]
        # a correct guess = 0, incorrect = 2 or -2
        correct_guess = brain_cell.test(inputs, item[0][3])
        if correct_guess == True:
            correct += 1
        #     print("Correct guess! :-)")
        # else:
        #     print("Incorecct guess.")
    cor_per = (correct / len(input_data)) * 100
    print("accuracy: {}".format(cor_per))


# ------------------------------------

def _get_slope(slope_of_the_line):
    x = 0
    y = slope_of_the_line(x)
    x1 = 10
    y1 = slope_of_the_line(x1)
    b = slope_of_the_line(0)
    m = (y - y1) / (x - x1)
    return "{}x + {}".format(m, b)

# ------------------------------------

def main():
    help()

if __name__ == "__main__":
    command_list = ["generate_data", "train_perceptron", "test_perceptron",
                    "view_training_data", "set_slope_of_line", "view_slope_of_line", "--help", "-h"]
    print(" ")
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if not arg in command_list:
            print("")
            print("=== FirstPerceptron.py ======================================================")
            print("Sorry! I don't recognize that command! Here are the commands I do recognize:")
            print("-----------------------------------------------------------------------------")
            mystring = ""
            for command in command_list:
                mystring = "{}{}||".format(mystring, command)
            print(mystring)
            print("=============================================================================")
            print("")
        if arg == "generate_data":
            print("-------------------------")
            print("----- Generate Data -----")
            # slope_of_the_line = lambda x: x
            filepath = "slope_of_the_line.p"
            slope_of_the_line = pickle.load(open(filepath, "rb"))
            # --- generate training data ---
            training_data = "datapoints.txt"  # training data
            number_of_training_records = 1000
            generate_training_data(number_of_training_records, training_data, slope_of_the_line)
            print("{} training records were successfully created.")
            # --- generate testing data ---
            testing_data = "testing_data.txt"
            number_of_testing_records = 1000
            generate_testing_data(number_of_testing_records, testing_data, slope_of_the_line)
            print("{} testing records were successfully created.")
            print("-------------------------")
            print("-------------------------")
        if arg == "train_perceptron":
            training_data = "datapoints.txt"  # training data
            input_data = read_data(training_data)
            train_neural_network(input_data)
        if arg == "test_perceptron":
            print("---------------------------")
            print("----- Test Perceptron -----")
            testing_data = "testing_data.txt"  # training data
            input_data = read_data(testing_data)
            print("Testing the perceptron on {} data points read from the file: {}.".format(len(input_data), testing_data))
            test_neural_network(input_data)
            print("---------------------------")
            print("---------------------------")
            print("")
        if arg == "set_slope_of_line":
            print("-----------------------------")
            print("----- Set Slope of Line -----")
            slope_of_the_line = input("Please enter a lambda formula of the form: mx+b. For example, lambda x: 2x + 1.\n: ")
            user_input = input("The following will be used: {}. Okay? (y/n)\n: ".format())
            print("You entered: {}".format(slope_of_the_line))
            if slope_of_the_line == "quit" or slope_of_the_line == "exit":
                sys.exit()
            slope = eval(slope_of_the_line)
            print(slope)
            pickle.dump(slope, open("slope_of_the_line.p", "wb"))
            print("-----------------------------")
            print("-----------------------------")
        if arg == "view_slope_of_line":
            print("------------------------------")
            print("----- View Slope of Line -----")
            slope_of_the_line = pickle.load(open("slope_of_the_line.p", "rb"))
            slope = _get_slope(slope_of_the_line)
            print("Slope of the line: {}".format(slope))
            print("------------------------------")
            print("------------------------------")
        if arg == "view_training_data":
            print("---------------------------------")
            print("----- Viewing Training Data -----")
            training_data = "datapoints.txt"
            view_training_data(training_data)
            print("---------------------------------")
            print("---------------------------------")
        if arg == "--help":
            help()
        if arg == "-h":
            help()
    else:
        print("That's too many arguments! Here are the commands I recognize:\n {}"
              .format(command_list))
    print("")

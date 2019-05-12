import trainer, perceptron, format_logfile
import sys
import draw_exp01_01

screenwidth = 400
screenheight = 400
number_of_training_elements = 200
read_data_from_file = False
save_data_to_file = False
filepath = "data.txt"
logfile = "logfile.txt"
logfile_formatted = "formatted_logfile.txt"
x1y1x2y2_file = "x1y1x2y2_data.txt"
training_data = trainer.Training(number_of_training_elements, screenwidth, screenheight)

def setup_random_numbers():
    # generate weights randomly
    # training_data = trainer.Training(number_of_training_elements, screenwidth, screenheight)
    p = perceptron.Perceptron(3, 0.01)
    return training_data, p

def setup_from_file(filepath):
    # generate weights randomly
    # training_data = trainer.Training(number_of_training_elements, screenwidth, screenheight)
    # read the weights in from a file
    training_data.read_from_file(filepath)
    p = perceptron.Perceptron(3, 0.001)
    p.read_weights_from_file(filepath)
    return training_data, p

def main():
    # clear the logfile.
    open(logfile, "w").close()
    if read_data_from_file == False:
        training_data, p = setup_random_numbers()
    else:
        training_data, p = setup_from_file(filepath)
    total_data = len(training_data.training_array)
    i = 0
    stop_program = False
    filestring = ""
    while (i < 10000) and (stop_program == False):
        correct_guesses = 0
        for input in training_data.training_array:
            # print("input: {}, answer: {}".format(input.inputs, input.answer))
            guess = p.train(input.inputs, input.answer)
            if guess == 0:
                correct_guesses += 1
            filestring += "{} {} {}\n".format(input.inputs[0], input.inputs[1], guess)
        print("==============================================")
        print("Total data points: {}, correct guesses: {}".format(total_data, correct_guesses))
        print("Percentage of correct guesses: {}".format(correct_guesses / total_data))
        if correct_guesses == len(training_data.training_array):
            stop_program = True
            print("stop_program == True after {} loops.".format(i))
            print("weights: {}".format(p.weights))
            if save_data_to_file == True:
                training_data.write_to_file("data.txt", p.weights)
            sys.exit()
        with open(logfile, "a") as f:
            f.write(filestring)
            f.write("==================================================================\n")
        filestring = ""
        i += 1
    print("SOLUTION NOT FOUND: Exiting program with i = {}".format(i))
    print("weights: {}".format(p.weights))
    if save_data_to_file == True:
        training_data.write_to_file("data.txt", p.weights)

def formatlogfile():
    format_logfile.format_file(logfile, logfile_formatted)
    format_logfile.format_x1y1x2y2_data_file(logfile_formatted, x1y1x2y2_file)

if __name__ == "__main__":
    command_list = ["justrun", "formatlogfile", "readfromfile", "savetofile", "drawdata"]
    if len(sys.argv) == 1:
        # no arguments have been given.
        print("----------------------------------")
        print("Hi! I am SimplePerceptron.py. Here are the arguments I understand:")
        print(' | '.join(command_list))
        print("----------------------------------")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "formatlogfile":
            # DO NOT call main()
            formatlogfile()
        elif sys.argv[1] == "justrun":
            main()
        elif sys.argv[1] == "readfromfile":
            # don't randomly generate the values, get them from a file
            read_data_from_file = True
            main()
        elif sys.argv[1] == "savetofile":
            save_data_to_file = True
            main()
        elif sys.argv[1] == "drawdata":
            mydraw = draw_exp01_01.Draw(x1y1x2y2_file)
            mydraw.draw_figure()
        else:
            print("I'm sorry, I didn't understand what you typed ({})".format(sys.argv[1]))
            print("I understand the following commands:")
            [print(i) for i in command_list]

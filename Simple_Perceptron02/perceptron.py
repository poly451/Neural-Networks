import random, sys

class Perceptron:
    def __init__(self, number_of_inputs, learning_constant, load_weights=False):
        self.perceptron_weights_filename = "perceptron_weights.txt"
        self.learning_constant = learning_constant
        if load_weights == False:
            self.weights = []
            for i in range(number_of_inputs):
                self.weights.append(random.uniform(-1, 1))
            print("weights: {}".format(self.weights))
        else:
            self.read_weights_from_file()

    def _feedforward(self, inputs):
        # thinking || guess
        sum = 0.0
        for i in range(len(self.weights)):
            # print("sum: {}, inputs {}: {}, weights {}: {}".format(sum, i, inputs[i], i, self.weights[i]))
            sum += inputs[i] * self.weights[i]
        # print("sum: {}".format(sum))
        return self._activate(sum)

    # def _activate(self, sum):
    #     if (sum > 0): return 1
    #     return -1

    def _activate(self, sum):
        # sign; the activation function
        # print("=======================")
        # print("slope of the line in trainer.py Trainer._activate: {}".format(self._get_slope()))
        if 0 > sum:
            # if 0 < sum:
            return -1
        return 1

    def train(self, inputs, desired):
        # doing + memory of what was done
        # print("---- Perceptron.train BEGIN ----")
        # print("inputs: {}".format(inputs))
        # print("desired: {}".format(desired))
        guess = self._feedforward(inputs)
        error = desired - guess
        for i in range(len(self.weights)):
            # gradient descent -- tune all the weights
            self.weights[i] += self.learning_constant * error * inputs[i]
        # print("weights: {}".format(self.weights))
        # self._debug_print(inputs, desired, guess, error)
        # print("---- Perceptron.train END ----")
        return error

    def test(self, inputs, desired):
        """For any points x and y identifies whether x > y."""
        # Note: This won't work unless the weights have been
        # loaded from the file.
        guess = self._feedforward(inputs)
        if guess == desired: return True
        return False

    # ================================================

    # def set_weights(self, x, y, z):
    #     self.weights = [x, y, z]

    def write_weights_to_file(self):
        mystring = ' '.join([str(i) for i in self.weights])
        with open(self.perceptron_weights_filename, "w") as f:
            f.write (mystring)

    def read_weights_from_file(self):
        mylist = []
        with open(self.perceptron_weights_filename, "r") as f:
            mylist = f.readlines()
        use_weights = mylist[0].strip()
        list_weights = use_weights.split(" ")
        self.weights = []
        for item in list_weights:
            self.weights.append(float(item))
        print("Read weights from file ({}):\n{}".format(self.perceptron_weights_filename, self.weights))

    # ================================================

    def _debug_print(self, inputs, desired, guess, error):
        print("---- PRIVATE debug print BEGIN----")
        print("inputs: {} || weights: {}".format(inputs, self.weights))
        print("error ({}) = desired ({}) - guess ({})".format(error, desired, guess))
        print("---- PRIVATE debug print END----")

    def debug_print(self):
        print("---- PUBLIC debug print BEGIN ----")
        print("weights: {}".format(self.weights))
        print("---- PUBLIC debug print END ----")
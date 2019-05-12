import random, sys

class Perceptron:
    def __init__(self, n, c):
        self.weights = []
        for i in range(n):
            self.weights.append(random.uniform(-1, 1))
        self.c = c

    def _feedforward(self, inputs):
        # thinking
        sum = 0.0
        for i in range(len(self.weights)):
            # print("sum: {}, inputs {}: {}, weights {}: {}".format(sum, i, inputs[i], i, self.weights[i]))
            sum += inputs[i] * self.weights[i]
        return self._activate(sum)

    def _activate(self, sum):
        if (sum > 0): return 1
        return -1

    def train(self, inputs, desired):
        # doing + memory of what was done
        # print("---- Perceptron.train BEGIN ----")
        # print("inputs: {}".format(inputs))
        # print("desired: {}".format(desired))
        guess = self._feedforward(inputs)
        error = desired - guess
        for i in range(len(self.weights)):
            self.weights[i] += self.c * error * inputs[i]
        # print("weights: {}".format(self.weights))
        # self._debug_print(inputs, desired, guess, error)
        # print("---- Perceptron.train END ----")
        return error

    def set_weights(self, x, y, z):
        self.weights = [x, y, z]

    def read_weights_from_file(self, filepath):
        mylist = []
        with open(filepath, "r") as f:
            mylist = f.readlines()
        use_weights = mylist[0].strip()
        list_weights = use_weights.split(" ")
        self.weights = []
        for item in list_weights:
            self.weights.append(float(item))
        # print(self.weights)

    def _debug_print(self, inputs, desired, guess, error):
        print("---- PRIVATE debug print BEGIN----")
        print("inputs: {} || weights: {}".format(inputs, self.weights))
        print("error ({}) = desired ({}) - guess ({})".format(error, desired, guess))
        print("---- PRIVATE debug print END----")

    def debug_print(self):
        print("---- PUBLIC debug print BEGIN ----")
        print("weights: {}".format(self.weights))
        print("---- PUBLIC debug print END ----")

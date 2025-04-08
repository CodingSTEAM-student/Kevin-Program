import math
import random
import matplotlib
import matplotlib.pyplot
import display
import statistics


def sigmoid(x):
    return 1 / (1+math.e ** (-x))


def linear(x):
    y = x
    return y


def relu(x):
    y = x
    if y > 1:
        y == 1
    elif y < -1:
        y == -1
    return y


def step(x):
    if x < 0:
        return 0
    else:
        return 1


class Neuron:
    def __init__(self) -> None:
        self.weights = []
        self.inputs = None
        self.activation = linear

    def activate(self):
        intermediates = []
        try:
            for n in range(len(self.inputs)):
                # print(self.weights)
                intermediates.append(self.inputs[n] * self.weights[n])
        except IndexError:
            print("Number of inputs and Weights are not the same ")
        output = sum(intermediates)
        return output

    def activation_funtion(self):
        return self.activation(self.activate())


class Layer:

    def __init__(self, size, inputSize=1, chosenWeights=None):

        self.DEBUGGER = True
        self.neurons = []

        self.weights = []

        for i in range(size):
            neuron = Neuron()
            self.neurons.append(neuron)
        print("Created", size, "neurons")

        if chosenWeights is None:
            for neuron in self.neurons:
                # assign a random weight to each neuron
                for i in range(inputSize):
                    neuron.weights.append(random.uniform(-1, 1))
            print("Assigned", size, "random weights")
        elif type(chosenWeights) is list:
            # assign the chosen weights to the neurons
            # for neuron, weight in zip(self.neurons, chosenWeights):
            for i in range(size):
                self.neurons[i].weights = chosenWeights

                # print(chosenWeights[i])
                print("Assigned", size, "chosen weights")

        else:
            raise Exception("Chosen weights are not in list form.")
        # print(self.neurons)
        # print(self.neurons[0].weight)

    def set_inputs(self, inputs: list):
        for neuron in self.neurons:
            neuron.inputs = inputs

    def forward_propagation(self) -> list:
        outputs = []
        for neuron in self.neurons:
            activation_value = neuron.activation_funtion()
            outputs.append(activation_value)

        return outputs


weights = [1, 0.01]  # unused
hiddenLayer = Layer(size=2, inputSize=2)
hiddenLayer.activation = linear
outputWeight = [1]
outputLayer = Layer(size=1, chosenWeights=outputWeight)
outputLayer.activation = linear
numberOfInputs = 1000
savedWeights = []
errors = []
line = [
    (1, 0),
    (-1, 0)
]
points = []
for i in range(numberOfInputs):
    inputs = [random.uniform(-1, 1),
              random.uniform(-1, 1)]
    points.append(inputs)
training_rounds = 1000
predictions = []
for _ in range(training_rounds):
    predictionSet = []
    for i in range(numberOfInputs):
        inputs = points[i]
        hiddenLayer.set_inputs(inputs)
        hiddenActivation = hiddenLayer.forward_propagation()
        # print("gegknewhwekhkelw", hiddenActivation)
        outputLayer.set_inputs(hiddenActivation)
        prediction = outputLayer.forward_propagation()[0]
        correct = display.classify(line, inputs)
        # calculate error
        error = correct - prediction
        # invert activation

        # print(correct, prediction)
        ...
        # preform gradient descent
        learningRate = 0.0001

        hiddenLayer.neurons[0].weights[0] += error * \
            inputs[0] * learningRate
        hiddenLayer.neurons[0].weights[1] += error * \
            inputs[1] * learningRate

        savedWeights. append(
            (hiddenLayer.neurons[0].weights[0],
             hiddenLayer.neurons[0].weights[1])
        )
        errors.append((error))

        # print(prediction, "correct:", correct)

        # inputs.append(prediction)
        predictionSet.append([inputs[0], inputs[1], prediction])
        # print(points)
    predictions.append(predictionSet)

display.display(*predictions, line=line, interval=1)
matplotlib.pyplot.plot(savedWeights)
matplotlib.pyplot.show()
matplotlib.pyplot.plot(errors)
matplotlib.pyplot.show()

correctpredictions = [
    [*point, display.classify(line, point)] for point in points]
display.display(correctpredictions, line=line)

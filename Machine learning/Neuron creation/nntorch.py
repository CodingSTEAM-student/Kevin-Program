import matplotlib.pyplot as plt
import torch
import numpy as np
from PIL import Image
import torch.utils.data.dataloader
import torchvision
import time

repeats = 3
displayErrors = True
learningRate = 0.001
batch = 10
train = torchvision.datasets.MNIST(
    "data", train=True, download=True,
    transform=torchvision.transforms.ToTensor()
)
test = torchvision.datasets.MNIST(
    "data", train=False, download=True,
    transform=torchvision.transforms.ToTensor()
)
mnist = torch.utils.data.DataLoader(train,batch_size=batch,shuffle=True)
mnistTest = torch.utils.data.DataLoader(test)


print(torch.backends.cudnn.enabled)
print(torch.cuda.is_available())

class Network(torch.nn.Module):
    def __init__(self):
        print("Initialising network")
        super().__init__() # Tell pytorch to initialise the Module we have borrowed

        print("Creating layer 1 and 2")
        self.brain = torch.nn.Sequential(
            # torch.nn.Con,
            torch.nn.Flatten(),
            torch.nn.Linear(784, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512,10),
            torch.nn.ReLU(),
            torch.nn.Softmax(dim=1)

        )



    def forward(self, data):
        output = self.brain(data)
        return output

    # def output(self, result):
    #     # print(result)
    #     prediction = torch.nn.functional.softmax(result, dim=1)
    #     return prediction.argmax()
    
    def optimise(self, prediction, correct):
        CEL = torch.nn.CrossEntropyLoss()
        optimiser = torch.optim.SGD(self.parameters())
        # tensor = torch.tensor([correct], dtype=torch.float)
        error = CEL(prediction, correct)
        # print(error)
        error.backward()
        optimiser.step()
        optimiser.zero_grad()
        # print("optimsed: Done")
        return error
    def train(self,mnist,repeats:int, displayCorrect = False):
        errors = np.zeros(((60000*repeats)//batch, 1))
        totalIter = 60000 *repeats
        for epoch in range(repeats):
            for i, (data, label) in enumerate(mnist):
                idx = i * batch
                offset = i + epoch * (60000//batch)
                prediction = self(data)
                

                error = self.optimise(prediction,label)
                errors[offset] = error.detach().numpy()

                if idx % 491 == 0:
                    print("     Iteration:", idx + epoch * 60000, "/", totalIter, end = "\r" ) 
                    if displayCorrect: 
                        print("Prediction is:", prediction, "Correct Label was:", label)
        return errors

nn = Network()



# data = torch.rand((28, 28))
def saveToImage(data):
    array = data.numpy()[0] * 255
    array = np.array(array, dtype=np.uint8)
    # print(array)
    image = Image.fromarray(array, mode="L")
    # print(image)
    image.save("image.png")

iterator = iter(mnist)

print("Training...")

errors = nn.train(mnist, repeats, displayCorrect= False)

print("Training Errors: ")
if displayErrors:
    for i in range(0,(60000 * repeats)//batch ,6000//batch ):
        values = errors[i:i+6000]
        mean = values.mean()
        median = np.median(values)
        std = np.std(values)


        print("Error block", i ,"to", i + 6000)
        print("mean:", mean, "median:", median, "std:", std)
    plt.plot(errors)
    plt.show()
correctness = 0
correctTable = {index: 0 for index in range(10)}


for testData, testLabel in mnistTest:
    prediction = nn(testData)
    isCorrect = prediction.argmax() == testLabel
    if isCorrect:
        correctness += 1
        intLabel = int(testLabel)

        if intLabel not in correctTable:
            correctTable[intLabel] = 0 
        correctTable[intLabel] += 1 

print(correctTable)

print("{} {:.2%}".format(correctness,correctness/60000))
plt.bar(range(10), correctTable.values())
plt.show()
from torchvision import datasets #datasets used to load the mnist dataset
from torchvision.transforms import ToTensor #makes the data a tensor, 
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

train_data = datasets.MNIST(
    root='data',
    train=True,
    download=True, 
    transform=ToTensor())

test_data = datasets.MNIST(
    root='data',
    train=False,
    download=True, 
    transform=ToTensor())

loaders = { 
    'train': DataLoader(train_data, batch_size=100, shuffle=True, num_workers=0 ),
    'test': DataLoader(test_data, batch_size=100, shuffle=True, num_workers= 0 )
}

print("loaders created")
#Used ai to comment the code 

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv1 = nn.Conv2d(1, 10, kernel_size=5) # 1 input channel, 10 output channels, 5x5 kernel
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5) # 10 input channels, 20 output channels, 5x5 kernel
        self.conv2_drop = nn.Dropout2d() # Dropout layer to prevent overfitting
        self.fc1 = nn.Linear(320, 50) # 320 input features, 50 output features
        self.fc2 = nn.Linear(50, 10) # 50 input features, 10 output features (10 classes for MNIST)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2)) # Apply ReLU activation and max pooling to the first convolutional layer
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2)) # Apply ReLU activation, dropout, and max pooling to the second convolutional layer
        x = x.view(-1, 320) # Flatten the output from the convolutional layers 
        x = F.relu(self.fc1(x)) # Apply ReLU activation to the first fully connected layer 
        x = self.fc2(x) # Apply the second fully connected layer

        return F.softmax(x, dim=1) # Apply softmax activation to the output layer
        
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNN().to(device)
optimiser = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss() 

print("cuda available" if torch.cuda.is_available() else "cuda not available")
print(f'Using device: {device}')
print("model created")

def train(epoch):
    model.train()

    for batch_idx, (data, target) in enumerate(loaders['train']):
        data, target = data.to(device), target.to(device)
        # print("sending data to device")
        optimiser.zero_grad() 
        output = model(data)
        loss = loss_fn(output, target)
        loss.backward()
        optimiser.step()

        if batch_idx % 20 == 0:
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(loaders["train"].dataset)} ({100. * batch_idx / len(loaders["train"]):.0f}%)]\tLoss: {loss.item():.6f}')

def test():
    model.eval() 

    test_loss = 0 
    correct = 0 

    with torch.no_grad():
        for data, target in loaders['test']:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += loss_fn(output, target).item()  # Accumulate batch loss
            pred = output.argmax(dim=1, keepdim=True) 
            correct += pred.eq(target.view_as(pred)).sum().item()

    # Divide test_loss by the number of batches, not the dataset size
    test_loss /= len(loaders['test'].dataset)  
    print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(loaders["test"].dataset)} ({100. * correct / len(loaders["test"].dataset):.0f}%)\n')

print("Training started")
for epoch in range(1, 11):
    print(f'Starting Training epoch: {epoch}')
    train(epoch)
    print(f'Starting testing epoch: {epoch}')
    test()

model.eval()

data, target = test_data[0]

data = data.unsqueeze(0).to(device)  # Add batch dimension and send to device

output = model(data)

prediction = output.argmax(dim=1, keepdim=True).item()  # Get the predicted class

print(f'Prediction: {prediction}')
image = data.squeeze(0).cpu().numpy()  # Remove only the batch dimension
plt.imshow(image[0], cmap='gray')  # Use the first channel for grayscale
plt.show()
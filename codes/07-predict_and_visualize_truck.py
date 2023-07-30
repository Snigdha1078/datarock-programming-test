import numpy as np
import torch
from torchvision.utils import make_grid
import matplotlib.pyplot as plt
from models.cnn_model import Net

# Load the model
net = Net()
net.load_state_dict(torch.load('./codes/models/deer_truck_net.pth'))

# Load the test data
testloader = torch.load('./data/interim/testloader.pt')

# Get some random images from the test loader
dataiter = iter(testloader)
images, labels = next(dataiter)

# Get predictions
outputs = net(images)
_, predicted = torch.max(outputs, 1)

# Function for plotting images
from PIL import Image

# Function for plotting images
def imshow(img, title):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    npimg = np.transpose(npimg, (1, 2, 0))
    
    # Convert to PIL Image for better resizing
    pil_img = Image.fromarray(np.uint8(npimg*255))
    
    # Resize the image using PIL's resize function with LANCZOS filter (interpolation)
    pil_img = pil_img.resize((128,128), Image.LANCZOS)
    
    plt.imshow(pil_img)
    plt.title(title)
    plt.show()

# Get class names
classes = ('deer', 'truck')

# Identify correctly and incorrectly classified 'truck' images
correct_truck_indices = (labels == predicted) & (labels == 1)
incorrect_truck_indices = (labels != predicted) & (labels == 1)

# Plot two images labeled 'truck' that the model predicts correctly
correct_truck_images = images[correct_truck_indices][:2]
correct_truck_labels = predicted[correct_truck_indices][:2]
imshow(make_grid(correct_truck_images), ' '.join('%5s' % classes[correct_truck_labels[j]] for j in range(2)))

# Plot two images labeled 'truck' that the model predicts incorrectly
incorrect_truck_images = images[incorrect_truck_indices][:2]
incorrect_truck_labels = predicted[incorrect_truck_indices][:2]
imshow(make_grid(incorrect_truck_images), ' '.join('%5s' % classes[incorrect_truck_labels[j]] for j in range(2)))

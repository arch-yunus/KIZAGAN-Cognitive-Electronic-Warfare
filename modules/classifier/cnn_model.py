import torch
import torch.nn as nn
import torch.nn.functional as F

class ModulationCNN(nn.Module):
    """
    1D CNN for Modulation Classification on RadioML Dataset.
    Input shape: (Batch, 2, 128) - I/Q components
    """
    def __init__(self, num_classes=11):
        super(ModulationCNN, self).__init__()
        
        # Convolutional Layers
        # (2, 128) -> (64, 126)
        self.conv1 = nn.Conv1d(2, 64, kernel_size=3)
        # (64, 126) -> (64, 63)
        self.pool1 = nn.MaxPool1d(2)
        
        # (64, 63) -> (128, 61)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3)
        # (128, 61) -> (128, 30)
        self.pool2 = nn.MaxPool1d(2)
        
        # Fully Connected Layers
        self.fc1 = nn.Linear(128 * 30, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        # x expected shape: (Batch, 2, 128)
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

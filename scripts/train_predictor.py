import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import sys

# Import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.predictor.hop_predictor import HopTransformer

MODEL_SAVE_PATH = "models/hop_transformer.pt"

def generate_hop_data(num_samples=5000, seq_len=16):
    """Generates synthetic frequency hopping sequences."""
    X = []
    y = []
    
    # Patterns: Linear, Alternative, Random Walk
    for _ in range(num_samples):
        pattern_type = np.random.choice(['linear', 'alternating', 'random_walk'])
        base_freq = np.random.uniform(100, 1000)
        step = np.random.uniform(5, 50)
        
        seq = []
        if pattern_type == 'linear':
            for i in range(seq_len + 1):
                seq.append(base_freq + i * step)
        elif pattern_type == 'alternating':
            for i in range(seq_len + 1):
                seq.append(base_freq + (i % 2) * step)
        else: # random walk
            curr = base_freq
            for i in range(seq_len + 1):
                seq.append(curr)
                curr += np.random.uniform(-step, step)
        
        # Add noise
        seq = np.array(seq) + np.random.normal(0, 0.5, seq_len + 1)
        
        X.append(seq[:-1].reshape(seq_len, 1))
        y.append(seq[-1].reshape(1))
        
    return torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(np.array(y), dtype=torch.float32)

def train():
    X, y = generate_hop_data()
    
    # Split
    n_train = int(len(X) * 0.8)
    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = HopTransformer().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 20
    print(f"[*] HopTransformer eğitimi başlıyor ({epochs} epoch)...")
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train.to(device))
        loss = criterion(outputs, y_train.to(device))
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 5 == 0:
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_test.to(device))
                val_loss = criterion(val_outputs, y_test.to(device))
                print(f"Epoch {epoch+1}/{epochs} - Train Loss: {loss.item():.4f} - Val Loss: {val_loss.item():.4f}")
                
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"[+] Model kaydedildi: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()

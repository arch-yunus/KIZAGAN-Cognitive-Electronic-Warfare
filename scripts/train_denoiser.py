import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import sys

# Import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.denoiser.neural_denoiser import SpectralAutoencoder

MODEL_SAVE_PATH = "models/spectral_autoencoder.pt"

def generate_denoise_data(num_samples=2000, dim=512):
    """Generates synthetic PSD signals with noise."""
    X_noisy = []
    X_clean = []
    
    for _ in range(num_samples):
        # Base signal (some peaks)
        clean = np.zeros(dim)
        num_peaks = np.random.randint(1, 5)
        for _ in range(num_peaks):
            center = np.random.randint(0, dim)
            width = np.random.randint(5, 20)
            clean += np.exp(-0.5 * ((np.arange(dim) - center) / width)**2)
            
        clean = (clean - clean.min()) / (clean.max() - clean.min() + 1e-6)
        
        # Add noise
        noise = np.random.normal(0, 0.2, dim)
        noisy = clean + noise
        noisy = np.clip(noisy, 0, 1)
        
        X_clean.append(clean.reshape(1, dim))
        X_noisy.append(noisy.reshape(1, dim))
        
    return torch.tensor(np.array(X_noisy), dtype=torch.float32), torch.tensor(np.array(X_clean), dtype=torch.float32)

def train():
    X_noisy, X_clean = generate_denoise_data()
    
    n_train = int(len(X_noisy) * 0.8)
    X_train_noisy, X_test_noisy = X_noisy[:n_train], X_noisy[n_train:]
    X_train_clean, X_test_clean = X_clean[:n_train], X_clean[n_train:]
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SpectralAutoencoder().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 30
    print(f"[*] SpectralAutoencoder eğitimi başlıyor ({epochs} epoch)...")
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train_noisy.to(device))
        loss = criterion(outputs, X_train_clean.to(device))
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_test_noisy.to(device))
                val_loss = criterion(val_outputs, X_test_clean.to(device))
                print(f"Epoch {epoch+1}/{epochs} - Train Loss: {loss.item():.6f} - Val Loss: {val_loss.item():.6f}")
                
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"[+] Model kaydedildi: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()

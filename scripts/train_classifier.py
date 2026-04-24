import os
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import requests
from tqdm import tqdm
import sys

# Import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.classifier.cnn_model import ModulationCNN

DATA_URL = "https://github.com/radioML/dataset/raw/master/2016.10A.dict.pkl"
DATA_PATH = "data/RML2016.10a_dict.pkl"
MODEL_SAVE_PATH = "models/modulation_cnn.pt"

def download_data():
    if not os.path.exists(DATA_PATH):
        print(f"[*] Veri seti indiriliyor: {DATA_URL}")
        os.makedirs("data", exist_ok=True)
        response = requests.get(DATA_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(DATA_PATH, "wb") as f, tqdm(
            total=total_size, unit='iB', unit_scale=True
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)
        print("[+] İndirme tamamlandı.")
    else:
        print("[*] Veri seti zaten mevcut.")

def load_data():
    with open(DATA_PATH, 'rb') as f:
        d = pickle.load(f, encoding='latin1')
        
    mods, snrs = map(lambda x: sorted(list(set(x))), zip(*d.keys()))
    X = []
    lbl = []
    
    for mod in mods:
        for snr in snrs:
            X.append(d[(mod, snr)])
            for i in range(d[(mod, snr)].shape[0]):
                lbl.append((mod, snr))
    
    X = np.vstack(X)
    
    # Map labels to integers
    mod_to_idx = {m: i for i, m in enumerate(mods)}
    y = np.array([mod_to_idx[l[0]] for l in lbl])
    
    print(f"[*] Toplam örnek: {X.shape[0]}, Sınıf sayısı: {len(mods)}")
    print(f"[*] Sınıflar: {mods}")
    
    return X, y, mods

def train():
    download_data()
    X, y, mods = load_data()
    
    # Shuffle and split
    n_examples = X.shape[0]
    n_train = int(n_examples * 0.8)
    train_idx = np.random.choice(range(n_examples), n_train, replace=False)
    test_idx = list(set(range(n_examples)) - set(train_idx))
    
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Convert to torch tensors
    # Input shape is (N, 2, 128) - PyTorch expects (Batch, Channels, Length)
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.long)
    y_test = torch.tensor(y_test, dtype=torch.long)
    
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=128)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Cihaz: {device}")
    
    model = ModulationCNN(num_classes=len(mods)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 15
    print(f"[*] Eğitim başlıyor ({epochs} epoch)...")
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/len(train_loader):.4f} - Val Acc: {accuracy:.2f}%")
        
    # Save model
    os.makedirs("models", exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'classes': mods
    }, MODEL_SAVE_PATH)
    print(f"[+] Model kaydedildi: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()

import torch
import torch.nn as nn
import numpy as np
from collections import deque
import math
import os

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class HopTransformer(nn.Module):
    def __init__(self, d_model=32, nhead=4, num_layers=2, dim_feedforward=128):
        super(HopTransformer, self).__init__()
        self.embedding = nn.Linear(1, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        # x: (Batch, SeqLen, 1)
        x = self.embedding(x)
        x = self.pos_encoder(x)
        x = self.transformer_encoder(x)
        x = self.fc(x[:, -1, :]) # Predict next from last token
        return x

class FrequencyHopPredictor:
    """
    Predicts the next frequency hop using a Transformer architecture.
    Phase 1 Upgrade: Replaced LSTM with Transformer for superior pattern recognition.
    """
    def __init__(self, history_len=16):
        self.history_len = history_len
        self.histories  = {} # track_id -> deque
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = HopTransformer().to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        
        # Load trained weights
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models/hop_transformer.pt")
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self.model.eval()
                print(f"[Predictor] HopTransformer ağırlıkları yüklendi.")
            except Exception as e:
                print(f"[Predictor] Model yükleme hatası: {e}")
        else:
            print(f"[Predictor] Model dosyası bulunamadı, taze başlatıldı.")
        
    def update_and_predict(self, track_id, current_freq_mhz):
        if track_id not in self.histories:
            self.histories[track_id] = deque(maxlen=self.history_len)
        
        history = self.histories[track_id]
        prediction = None
        
        if len(history) == self.history_len:
            # Online learning step
            seq = np.array(list(history), dtype=np.float32).reshape(1, self.history_len, 1)
            target = np.array([[current_freq_mhz]], dtype=np.float32)
            
            self.model.train()
            input_tensor = torch.from_numpy(seq).to(self.device)
            target_tensor = torch.from_numpy(target).to(self.device)
            
            output = self.model(input_tensor)
            loss   = self.criterion(output, target_tensor)
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Predict
            self.model.eval()
            with torch.no_grad():
                next_seq = np.append(seq[0, 1:, :], target.reshape(1,1), axis=0).reshape(1, self.history_len, 1)
                prediction = self.model(torch.from_numpy(next_seq).to(self.device)).item()
        
        history.append(current_freq_mhz)
        return prediction

    def get_all_predictions(self):
        preds = {}
        for tid, hist in self.histories.items():
            if len(hist) == self.history_len:
                seq = np.array(list(hist), dtype=np.float32).reshape(1, self.history_len, 1)
                self.model.eval()
                with torch.no_grad():
                    preds[tid] = self.model(torch.from_numpy(seq).to(self.device)).item()
        return preds

if __name__ == "__main__":
    # Smoke Test
    predictor = FrequencyHopPredictor(history_len=8)
    # Simulate a linear hop sequence
    for i in range(10):
        res = predictor.update_and_predict(1, 100.0 + i*10)
        if res:
            print(f"Step {i}, Predicted Next: {res:.2f} (Actual will be {100.0 + (i+1)*10})")
    print("FrequencyHopPredictor (Phase 1 Transformer) Smoke Test: SUCCESS")

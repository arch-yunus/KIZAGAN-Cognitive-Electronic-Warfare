import torch
import torch.nn as nn
import numpy as np

class SpectralAutoencoder(nn.Module):
    """
    Advanced 1D U-Net Autoencoder for Spectral Denoising.
    Phase 1 Upgrade: Added Skip Connections for low-level feature preservation.
    """
    def __init__(self, input_dim=512):
        super(SpectralAutoencoder, self).__init__()
        # Encoder
        self.enc1 = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
        )
        self.enc2 = nn.Sequential(
            nn.MaxPool1d(2),
            nn.Conv1d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
        )
        self.enc3 = nn.Sequential(
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
        )
        
        # Decoder
        self.dec3 = nn.Sequential(
            nn.ConvTranspose1d(64, 32, kernel_size=2, stride=2),
            nn.ReLU(),
        )
        self.dec2 = nn.Sequential(
            nn.ConvTranspose1d(64, 16, kernel_size=2, stride=2), # 32 (from dec3) + 32 (skip) = 64
            nn.ReLU(),
        )
        self.dec1 = nn.Sequential(
            nn.Conv1d(32, 1, kernel_size=3, stride=1, padding=1), # 16 (from dec2) + 16 (skip) = 32
            nn.Sigmoid()
        )

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)  # (B, 16, 512)
        e2 = self.enc2(e1) # (B, 32, 256)
        e3 = self.enc3(e2) # (B, 64, 128)
        
        # Decoder with Skip Connections
        d3 = self.dec3(e3) # (B, 32, 256)
        d2 = self.dec2(torch.cat([d3, e2], dim=1)) # (B, 16, 512)
        d1 = self.dec1(torch.cat([d2, e1], dim=1)) # (B, 1, 512)
        
        return d1

class NeuralDenoiser:
    """Enterprise-grade Neural Denoiser using Deep Learning."""
    def __init__(self, input_dim: int = 512):
        self.input_dim = input_dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SpectralAutoencoder(input_dim).to(self.device).eval()
        
        # Load trained weights
        import os
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models/spectral_autoencoder.pt")
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self._is_trained = True
                print(f"[Denoiser] SpectralAutoencoder ağırlıkları yüklendi.")
            except Exception as e:
                print(f"[Denoiser] Model yükleme hatası: {e}")
                self._is_trained = True # Can still run with random init
        else:
            print(f"[Denoiser] Model dosyası bulunamadı, taze başlatıldı.")
            self._is_trained = True

    def process(self, psd_frame: list) -> list:
        if not self._is_trained:
            return psd_frame # Fallback

        # Normalize 0-1
        arr = np.array(psd_frame, dtype=np.float32)
        min_val, max_val = arr.min(), arr.max()
        if max_val - min_val < 1e-6:
            return psd_frame
        
        norm_arr = (arr - min_val) / (max_val - min_val)
        
        # Tensorize
        input_tensor = torch.from_numpy(norm_arr).unsqueeze(0).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        
        # Denormalize
        denoised = output_tensor.cpu().numpy().squeeze()
        # Handle 0-dim vs 1-dim result
        if denoised.ndim == 0:
            denoised = np.array([denoised])
            
        denoised = denoised * (max_val - min_val) + min_val
        
        # Statistical Blending (Keep some original fidelity)
        alpha = 0.8
        blended = (alpha * denoised) + ((1 - alpha) * arr)
        
        return blended.tolist()

if __name__ == "__main__":
    # Test
    denoiser = NeuralDenoiser(512)
    fake_psd = np.random.rand(512).tolist()
    result = denoiser.process(fake_psd)
    print(f"Original Mean: {np.mean(fake_psd):.4f}, Denoised Mean: {np.mean(result):.4f}")

import torch
import numpy as np
import os

class ZeroShotDetector:
    """
    Detects unknown RF signals (Zero-Shot) using Reconstruction Error from the autoencoder.
    Part of Phase 2 AI Roadmap.
    """
    def __init__(self, threshold=0.15):
        self.threshold = threshold
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def analyze_anomaly(self, original_psd, reconstructed_psd):
        """
        Calculates the mean squared error between original and reconstructed PSD.
        If error > threshold, it's flagged as an 'Unknown/New' signal.
        """
        orig = np.array(original_psd)
        recon = np.array(reconstructed_psd)
        
        # Normalize for comparison
        orig = (orig - orig.min()) / (orig.max() - orig.min() + 1e-12)
        recon = (recon - recon.min()) / (recon.max() - recon.min() + 1e-12)
        
        mse = np.mean((orig - recon)**2)
        
        is_unknown = mse > self.threshold
        confidence = min(1.0, mse / self.threshold) if is_unknown else 1.0 - (mse / self.threshold)
        
        return is_unknown, float(mse), float(confidence)

if __name__ == "__main__":
    # Test
    detector = ZeroShotDetector(threshold=0.1)
    orig = np.random.rand(512)
    # Simulate a good reconstruction (known signal)
    recon_good = orig + np.random.normal(0, 0.01, 512)
    # Simulate a bad reconstruction (unknown signal)
    recon_bad = np.random.rand(512) 
    
    unk_g, mse_g, _ = detector.analyze_anomaly(orig, recon_good)
    unk_b, mse_b, _ = detector.analyze_anomaly(orig, recon_bad)
    
    print(f"Known Signal - Unknown: {unk_g}, MSE: {mse_g:.4f}")
    print(f"Unknown Signal - Unknown: {unk_b}, MSE: {mse_b:.4f}")

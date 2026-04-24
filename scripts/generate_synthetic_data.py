import pickle
import numpy as np
import os

def generate_synthetic_rml(output_path="data/RML2016.10a_dict.pkl"):
    """
    Generates a synthetic dataset mimicking the structure of RadioML 2016.10A.
    Classes: 11
    SNR: -20 to 18 dB (2 dB step)
    Samples: 100 per (Mod, SNR) for speed, 128 IQ points
    """
    mods = ["8PSK", "AM-DSB", "AM-SSB", "BPSK", "CPFSK", "GFSK", "PAM4", "16QAM", "64QAM", "QPSK", "WBFM"]
    snrs = range(-20, 20, 2)
    
    dataset = {}
    
    print(f"[*] Sentetik veri üretiliyor: {output_path}")
    
    for mod in mods:
        for snr in snrs:
            # Generate noisy IQ samples (N, 2, 128)
            num_samples = 100
            
            # Simple modulation simulation:
            # Different mods have different "shapes" in IQ plane
            iq = np.random.randn(num_samples, 2, 128) * 0.1
            
            # Add some "signal" based on mod type
            t = np.linspace(0, 1, 128)
            if mod == "BPSK":
                signal = np.sign(np.random.randn(num_samples, 1, 1)) * np.cos(2 * np.pi * 5 * t)
                iq[:, 0, :] += signal.squeeze()
            elif mod == "QPSK":
                iq[:, 0, :] += np.cos(2 * np.pi * 5 * t)
                iq[:, 1, :] += np.sin(2 * np.pi * 5 * t)
            # (Simplified for other mods)
            
            # Apply SNR
            noise_std = 10**(-snr / 20.0)
            noise = np.random.randn(num_samples, 2, 128) * noise_std
            iq += noise
            
            dataset[(mod, snr)] = iq.astype(np.float32)
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(dataset, f)
        
    print(f"[+] Veri seti oluşturuldu: {len(dataset.keys())} mod/snr kombinasyonu.")

if __name__ == "__main__":
    generate_synthetic_rml()

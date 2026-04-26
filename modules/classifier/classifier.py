import numpy as np
import torch
import os
import sys
from core.config import THREAT_MAP

# Add current directory to path to import cnn_model
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from cnn_model import ModulationCNN
    from zero_shot_detector import ZeroShotDetector
except ImportError:
    ModulationCNN = None
    ZeroShotDetector = None

class ModulationClassifier:
    """Classifies RF signal modulation type using CNN and advanced spectral features."""

    def __init__(self):
        self.classes = ["8PSK", "AM-DSB", "AM-SSB", "BPSK", "CPFSK", "GFSK", "PAM4", "16QAM", "64QAM", "QPSK", "WBFM"]
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load the trained CNN model
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models/modulation_cnn.pt")
        if ModulationCNN is not None:
            self.model = ModulationCNN(num_classes=len(self.classes))
            self.model.to(self.device)
            self.model.eval()
            
            if os.path.exists(model_path):
                try:
                    checkpoint = torch.load(model_path, map_location=self.device)
                    # Use non-strict loading to handle Minor architecture changes if possible, 
                    # but here we mostly care about catching the mismatch error.
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                    self.classes = checkpoint.get('classes', self.classes)
                    print(f"[Classifier] CNN Modeli yüklendi: {len(self.classes)} sınıf.")
                except Exception as e:
                    print(f"[Classifier] Model ağırlıkları yüklenemedi (Mimari uyuşmazlığı olabilir): {e}")
                    print(f"[Classifier] Faz 1 mimarisi ile taze başlatma (Fresh Initialization) yapılıyor.")
            else:
                print(f"[Classifier] Model dosyası bulunamadı, rastgele ağırlıklarla başlatıldı.")
        
        self.zs_detector = ZeroShotDetector() if ZeroShotDetector is not None else None

    def _calculate_spectral_moments(self, psd_slice):
        """Calculates 1st-4th order spectral moments and flatness."""
        if psd_slice is None or len(psd_slice) < 5:
            return 0.0, 3.0, 0.5, 0.0
        
        arr = np.array(psd_slice, dtype=float)
        # Normalize PSD to linear scale for moment calculation
        lin_psd = 10**(arr / 10.0)
        norm_psd = lin_psd / (np.sum(lin_psd) + 1e-12)
        
        bins = np.arange(len(norm_psd))
        mean = np.sum(bins * norm_psd)
        std  = np.sqrt(np.sum(((bins - mean)**2) * norm_psd) + 1e-12)
        
        # Skewness (3rd moment) & Kurtosis (4th moment)
        skewness = np.sum(((bins - mean)**3) * norm_psd) / (std**3 + 1e-12)
        kurtosis = np.sum(((bins - mean)**4) * norm_psd) / (std**4 + 1e-12)
        
        # Spectral Flatness (Wiener entropy)
        geometric_mean = np.exp(np.mean(np.log(lin_psd + 1e-12)))
        arithmetic_mean = np.mean(lin_psd)
        flatness = geometric_mean / (arithmetic_mean + 1e-12)
        
        return round(float(skewness), 3), round(float(kurtosis), 3), round(float(flatness), 4), round(float(std), 2)

    def _psd_to_iq_proxy(self, psd_slice):
        """
        Creates a synthetic IQ proxy (128 samples) based on PSD slice for CNN input.
        This is used when raw IQ is not available (SIMULATED mode).
        """
        # Interpolate PSD to 128 bins if needed
        psd = np.array(psd_slice)
        if len(psd) != 128:
            psd = np.interp(np.linspace(0, len(psd)-1, 128), np.arange(len(psd)), psd)
        
        # Linear scale
        mag = np.sqrt(10**(psd / 10.0))
        # Random phase
        phase = np.random.uniform(0, 2*np.pi, 128)
        
        # Complex signal
        iq = mag * np.exp(1j * phase)
        
        # Format as (2, 128)
        x = np.zeros((2, 128), dtype=np.float32)
        x[0, :] = np.real(iq)
        x[1, :] = np.imag(iq)
        return x

    def classify(self, signal_data, psd_slice=None):
        snr = float(signal_data.get('snr', 0))
        if snr < 6:
            return "Noise", 0.98, "LOW"

        # 1. Try CNN Classification if model is available
        if self.model is not None and psd_slice is not None:
            try:
                iq_proxy = self._psd_to_iq_proxy(psd_slice)
                input_tensor = torch.tensor(iq_proxy, dtype=torch.float32).unsqueeze(0).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(input_tensor)
                    probs = torch.softmax(outputs, dim=1)
                    conf, pred = torch.max(probs, 1)
                    
                # 1.1 Zero-Shot Check (Phase 2)
                if self.zs_detector and 'denoised_psd' in signal_data:
                    is_unknown, mse, zs_conf = self.zs_detector.analyze_anomaly(psd_slice, signal_data['denoised_psd'])
                    if is_unknown:
                        return "Unknown (Zero-Shot)", zs_conf, "CRITICAL"

                mod_type = self.classes[pred.item()]
                confidence = conf.item()
                threat_level = THREAT_MAP.get(mod_type, "MEDIUM")
                
                # Attach for RFI
                _, kurt, _, _ = self._calculate_spectral_moments(psd_slice)
                signal_data['kurtosis'] = kurt
                
                return mod_type, confidence, threat_level
            except Exception as e:
                print(f"[Classifier] CNN Inference hatası: {e}")

        # 2. Fallback to Rule-Based System
        bw  = float(signal_data.get('bandwidth_idx', 0))
        skew, kurt, flat, std = self._calculate_spectral_moments(psd_slice)
        
        if kurt > 4.5 and snr > 35:
            mod_type = "Radar"
            conf = 0.94
        elif (bw > 25 if flat > 0.5 else bw > 40):
            mod_type = "LoRa" if flat > 0.5 else "QPSK"
            conf = 0.88
        elif 2.0 < kurt < 3.8 and bw > 10:
            mod_type = "QPSK" if bw > 15 else "BPSK"
            conf = 0.85
        elif bw < 12:
            mod_type = "WBFM" if std > 2.5 else "AM-DSB"
            conf = 0.82
        else:
            mod_type = "16QAM"
            conf = 0.70

        threat_level = THREAT_MAP.get(mod_type, "MEDIUM")
        signal_data['kurtosis'] = kurt
        signal_data['skewness'] = skew
        
        return mod_type, conf, threat_level

    def extract_rfi_signature(self, signal_data):
        """Generates a stable RFI fingerprint based on spectral moments."""
        kurt = signal_data.get('kurtosis', 3.0)
        skew = signal_data.get('skewness', 0.0)
        snr  = signal_data.get('snr', 10.0)
        
        val = abs(kurt * 1337) + abs(skew * 777) + (snr * 6.6)
        return f"0x{(int(val * 42) % 0xFFFFF):05X}"

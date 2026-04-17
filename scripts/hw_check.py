import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.real_sdr import RealSDR

def test_environment():
    print("--- [Otonom-EHS] System & Hardware Diagnostic Tool ---")
    
    # 1. AI Stack Check
    print("\n[1/3] AI Stack Diagnostics:")
    try:
        import torch
        print(f"  - PyTorch version: {torch.__version__}")
        cuda_avail = torch.cuda.is_available()
        print(f"  - CUDA Available: {'YES' if cuda_avail else 'NO'}")
        if cuda_avail:
            print(f"  - GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("  - FAILURE: PyTorch not installed.")

    # 2. SDR connectivity
    print("\n[2/3] SDR Connectivity (HAL):")
    try:
        sdr = RealSDR()
        if sdr.is_active():
            print(f"  - SDR found and active at {sdr.center_freq/1e6} MHz")
            print("  - Capturing test frame...")
            frame = sdr.generate_spectrum_frame()
            print(f"  - Capture successful. Spectral bins: {len(frame)}")
            print(f"  - Avg Power: {sum(frame)/len(frame):.2f} dB")
            sdr.close()
        else:
            print("  - FAILURE: SDR detected but not responding correctly.")
    except Exception as e:
        print(f"  - FAILURE: {e}")
        print("    Check USB connection and drivers (librtlsdr/UHD/HackRF).")

    # 3. Memory & System
    print("\n[3/3] System Resources:")
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"  - Total RAM: {mem.total / (1024**3):.1f} GB")
        print(f"  - Available: {mem.available / (1024**3):.1f} GB")
    except ImportError:
        print("  - psutil not installed, skipping memory check.")

    print("\n--- Diagnostic Finished ---")

if __name__ == "__main__":
    test_environment()

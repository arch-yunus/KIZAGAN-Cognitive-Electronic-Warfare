import numpy as np
import random
import time

class AIAdversary:
    """
    Electronic Warfare Adversary AI.
    Simulates a smart enemy that detects jamming and adapts its strategy.
    """
    def __init__(self, center_freq=433e6, fs=2e6):
        self.center_freq = center_freq
        self.fs = fs
        self.current_freq = center_freq
        self.state = "TRANSMITTING" # TRANSMITTING, HOPPING, STEALTH
        self.integrity = 100.0 # Signal quality (0-100)
        
        # Simple Q-Learning for frequency selection
        self.freq_options = [center_freq + (i * 200e3) for i in range(-4, 5)]
        self.q_table = {f: 0.0 for f in self.freq_options}
        
    def detect_jamming(self, jamming_type, jam_freq=None):
        """Simulates the adversary's detection of being jammed."""
        if jamming_type == "STANDBY":
            self.integrity = min(100.0, self.integrity + 5.0)
            return False
            
        is_jammed = False
        if jamming_type == "JAM_BARRAGE":
            is_jammed = True
            self.integrity -= 15.0
        elif jamming_type == "JAM_SPOT" and jam_freq is not None:
            if abs(self.current_freq - jam_freq) < 50e3:
                is_jammed = True
                self.integrity -= 25.0
        
        if self.integrity < 0: self.integrity = 0
        return is_jammed

    def act(self, is_jammed):
        """Adversary decides what to do next."""
        decision = "STAY"
        
        if is_jammed or self.integrity < 40:
            # AI decides to hop if integrity is low or actively jammed
            decision = "HOP"
            old_freq = self.current_freq
            self.current_freq = random.choice([f for f in self.freq_options if f != old_freq])
            self.state = "HOPPING"
        else:
            self.state = "TRANSMITTING"
            
        return decision, self.current_freq

    def get_signal_params(self):
        """Returns the signal parameters for the RF environment."""
        return {
            "freq": self.current_freq,
            "bw": 25e3 if self.state == "TRANSMITTING" else 5e3,
            "amplitude": 50.0 if self.state == "TRANSMITTING" else 10.0,
            "type": "Radar" if random.random() > 0.5 else "QPSK",
            "duration": 5.0,
            "is_adversary": True
        }

if __name__ == "__main__":
    adv = AIAdversary()
    print(f"Adversary Initialized at {adv.current_freq/1e6} MHz")
    jammed = adv.detect_jamming("JAM_SPOT", adv.current_freq)
    dec, new_f = adv.act(jammed)
    print(f"Jamming Detected: {jammed} | Decision: {dec} | New Freq: {new_f/1e6} MHz")

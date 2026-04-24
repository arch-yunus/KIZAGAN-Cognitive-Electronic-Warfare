import time
import numpy as np
from core.orchestrator import SystemOrchestrator
from sim.ai_adversary import AIAdversary
from modules.ai_specialist.explainability import AIExplainer

class AIDuelEngine:
    """
    Runs a high-fidelity AI-vs-AI electronic warfare duel.
    """
    def __init__(self):
        self.orchestrator = SystemOrchestrator()
        self.adversary = AIAdversary()
        self.explainer = AIExplainer()
        self.is_running = False
        self.battle_log = []

    def start_duel(self, duration_sec=60):
        self.is_running = True
        start_time = time.time()
        print("\n=== AI vs AI DÜELLO BAŞLADI ===")
        
        while time.time() - start_time < duration_sec and self.is_running:
            # 1. Adversary Action
            jamming_type = self.orchestrator.latest_results.get("ea_status", {}).get("action", "STANDBY")
            jam_freq = None # For simplicity in this demo loop
            
            is_jammed = self.adversary.detect_jamming(jamming_type, jam_freq)
            adv_decision, adv_freq = self.adversary.act(is_jammed)
            
            # Inject adversary signal into environment
            adv_sig = self.adversary.get_signal_params()
            self.orchestrator.env.active_signals = [adv_sig] # Clear others for focus
            
            # 2. System Orchestrator Cycle
            results = self.orchestrator.run_cycle()
            
            # 3. Explainability & Analysis
            msg_dqn = self.explainer.explain_dqn(results.get("ea_status", {}))
            msg_adv = self.explainer.explain_adversary(self.adversary.state, self.adversary.integrity)
            
            log_entry = {
                "t": int(time.time() - start_time),
                "adv_f": round(adv_freq / 1e6, 2),
                "adv_integrity": round(self.adversary.integrity, 1),
                "sys_action": jamming_type,
                "msg_dqn": msg_dqn,
                "msg_adv": msg_adv
            }
            self.battle_log.append(log_entry)
            
            # Output to terminal
            print(f"[{log_entry['t']}s] Düşman: {log_entry['adv_f']}MHz | Durum: {self.adversary.state} | Integrity: {log_entry['adv_integrity']}%")
            print(f"       Savunma: {log_entry['sys_action']} | {msg_dqn}")
            print(f"       {msg_adv}")
            print("-" * 40)
            
            if self.adversary.integrity <= 0:
                print("\n[!] DÜŞMAN ETKİSİZ HALE GETİRİLDİ. AI ZAFERİ!")
                break
                
            time.sleep(1.0) # Simulation tick

    def stop_duel(self):
        self.is_running = False

if __name__ == "__main__":
    engine = AIDuelEngine()
    try:
        engine.start_duel(duration_sec=30)
    except KeyboardInterrupt:
        engine.stop_duel()

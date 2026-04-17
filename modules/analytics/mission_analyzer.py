import time
from collections import deque

class MissionAnalyzer:
    """
    Cognitive Mission Intelligence Analyzer.
    Analyzes live system telemetry to generate human-readable strategic insights.
    """
    def __init__(self):
        self.history = deque(maxlen=50) # Last 50 cycles
        self.strategy_log = []
        self.last_report_time = 0
        self.report_interval = 5.0 # Seconds
        self.total_engaged_targets = set()
        self.successful_bda_count = 0

    def update(self, latest_results):
        """Adds latest cycle data to history."""
        self.history.append(latest_results)

    def generate_strategic_summary(self):
        """Generates a high-density strategic summary of the mission."""
        if not self.history:
            return "SİSTEM BAŞLATILIYOR: Bilişsel Spektrum Gözlem Modu Aktif."

        now = time.time()
        last_5 = list(self.history)[-5:]
        avg_threats = sum(len(h.get("signals", [])) for h in last_5) / len(last_5)
        
        # Advanced Pattern Detection
        jamming_active = any(h.get("ea_status", {}).get("action") != "STANDBY" for h in last_5)
        heavy_threats = any(any(s.get("threat_level") in ["HIGH", "CRITICAL"] for s in h.get("signals", [])) for h in last_5)
        ep_hops = last_5[-1].get("ep_status", {}).get("total_hops", 0)
        security_idx = last_5[-1].get("ep_status", {}).get("security_index", 100.0)

        # Strategic Pattern Logic (v10.0)
        # 1. Saturation Attack (Doygunluk Taarruzu)
        saturation_threat = avg_threats > 5
        
        # 2. Evasive LPI Pattern (Gizlenme Girişimi)
        evasion_detected = any(
            s.get('snr', 0) < 8 and s.get('threat_level') in ['HIGH', 'CRITICAL'] 
            for h in last_5 for s in h.get('signals', [])
        )

        # 3. Dynamic RFI Signature Analysis (RF Parmak İzi)
        unknown_rfi = any(s.get('rfi_hash') == 'UNKNOWN' for h in last_5 for s in h.get('signals', []))
        
        report = []
        
        # Priority 1: Critical Saturation or Evasion
        if saturation_threat:
            report.append("KRİTİK: Doygunluk Taarruzu tespit edildi! EA-Master çoklu angajman moduna geçti.")
        if evasion_detected:
            report.append("İSTİHBARAT: Evasive LPI (Düşük Yakalanma Olasılığı) taktikleri denendiği öngörülüyor. Neural Denoiser hassasiyeti maksimize edildi.")

        # Priority 2: Operational Status
        if avg_threats == 0:
            report.append("SPEKTRUM TEMİZ: Spektral Güvenlik Endeksi stabil.")
        elif not saturation_threat:
            report.append(f"OPERASYONEL: {int(avg_threats)} aktif hedef otonom takip döngüsünde.")

        # Priority 3: Electronic Defense/Attack
        if ep_hops > 3:
            report.append(f"EP AJANI: Düşman karıştırması tespit edildi; {ep_hops} adet başarılı otonom frekans atlaması gerçekleştirildi.")
        
        if jamming_active:
            action = last_5[-1].get("ea_status", {}).get("action", "JAM")
            report.append(f"ET AKTİF: DQN Optimizer {action} politikasıyla domine ediyor.")

        if unknown_rfi and avg_threats > 0:
            report.append("UYARI: Bilinmeyen RF imzası tespit edildi. İstihbarat veri tabanı güncelleniyor.")

        summary = " | ".join(report[:4]) # Keep it high-density but readable
        self.strategy_log.append(summary)
        self.last_report_time = now
        
        return summary

    def get_mission_metrics(self):
        """Calculates high-level mission KPIs."""
        if not self.history:
            return {"effectiveness": 0, "security": 100}
            
        success_count = sum(1 for h in self.history if h.get("ea_status", {}).get("reward", 0) > 0)
        effectiveness = (success_count / len(self.history)) * 100
        
        security = self.history[-1].get("ep_status", {}).get("security_index", 100.0)
        
        return {
            "effectiveness": round(effectiveness, 1),
            "security": round(security, 1)
        }

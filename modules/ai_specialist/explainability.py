class AIExplainer:
    """
    Translates AI metrics (DQN, CNN, Q-Learning) into Turkish explanations
    for the AI Lead (User).
    """
    @staticmethod
    def explain_dqn(last_result):
        """Explains DQN jamming decision."""
        action = last_result.get("action", "STANDBY")
        reward = last_result.get("reward", 0)
        epsilon = last_result.get("epsilon", 0.1)
        
        explanation = f"DQN AJANI: '{action}' stratejisini seçti. "
        if reward > 0:
            explanation += f"Ödül (+{reward}) son aksiyonun etkili olduğunu gösteriyor. "
        else:
            explanation += f"Ödül ({reward}) stratejinin optimize edilmesi gerektiğini işaret ediyor. "
            
        if epsilon > 0.5:
            explanation += "Ajan şu an keşif (exploration) modunda, yeni taktikler deniyor."
        else:
            explanation += "Ajan şu an sömürü (exploitation) modunda, öğrenilen en iyi taktikleri uyguluyor."
            
        return explanation

    @staticmethod
    def explain_denoiser(original_psd, denoised_psd):
        """Explains CNN Denoiser performance."""
        import numpy as np
        orig = np.array(original_psd)
        denoised = np.array(denoised_psd)
        # Calculate spectral noise reduction
        noise_red = (np.std(orig) - np.std(denoised)) / np.std(orig) * 100
        
        if noise_red > 10:
            return f"EVRIŞIMSEL SİNYAL TEMİZLEME: Gürültü oranı %{noise_red:.1f} azaltıldı. Sinyal-Gürültü oranı (SNR) iyileştirildi."
        return "EVRIŞIMSEL SİNYAL TEMİZLEME: Spektrum halihazırda temiz, minimal işlem uygulandı."

    @staticmethod
    def explain_adversary(adv_state, adv_integrity):
        """Explains Adversary AI status."""
        if adv_integrity < 30:
            return f"DÜŞMAN ANALİZİ: Düşman sinyal bütünlüğü kritik (%{adv_integrity:.1f}). Mağlubiyete yakın."
        elif adv_state == "HOPPING":
            return "DÜŞMAN ANALİZİ: Düşman jamming tespit etti ve frekans atlıyor (Autonomous Evading)."
        return f"DÜŞMAN ANALİZİ: Düşman stabil yayın yapıyor, bütünlük: %{adv_integrity:.1f}."

# 🛰️ Aegis-AI OMEGA v10.0 | Cognitive Electronic Warfare Suite

![Aegis-AI Banner](banner.png)

[![Version](https://img.shields.io/badge/version-10.0.0-gold.svg)](https://github.com/bahattinyunus/Otonom-Elektronik-Harp-Sistemi)
[![TEKNOFEST](https://img.shields.io/badge/TEKNOFEST-2026-red.svg)](https://www.teknofest.org/)
[![Status](https://img.shields.io/badge/TRL-9.5-success.svg)](#)
[![AI Level](https://img.shields.io/badge/Cognitive_AI-Superiority-gold.svg)](#)

**Aegis-AI OMEGA**, modern elektromanyetik spektrum operasyonlarında (EMSO) Derin Öğrenme (DL) ve Pekiştirmeli Öğrenme (RL) metodolojilerini merkezileştiren, otonom bir **Bilişsel Elektronik Harp (Cognitive EW)** platformudur. Sistem, LPI radarları ve frekans atlamalı haberleşme sistemlerine karşı proaktif üstünlük kurmak üzere tasarlanmıştır.

---

## 🏛️ Mimari Katmanlar (v10.0)

Sistem, donanım bağımsızlığı ve yüksek performans için 4 kritik katmanda mimarize edilmiştir:

### 1. SDR Hardware Abstraction Layer (HAL)
- **HW-Agnostic:** USRP, HackRF, RTLSDR ve `RFEnvironment` (Simülasyon) katmanları arasında kesintisiz geçiş.
- **MIMO Senkronizasyonu:** Çoklu alıcı nodları (ES-Nod) arasında faz senkronizasyonu ve TDOA optimizasyonu.

### 2. Cognitive Detection & Sensing (v4.5)
- **CA-CFAR Logic:** Dinamik gürültü zeminine (Noise Floor) uyumlu otonom eşikleme.
- **Neural Denoising:** 1D-CNN Autoencoder ile sinyal saflığının stokastik gürültü altında korunması.
- **UKF Tracking:** Non-lineer hedef manevralarını takip edebilen **Unscented Kalman Filter** mimarisi.

### 3. Artificial Intelligence & Decision (Cognitive Engine)
- **DQN EA Optimizer:** Deep Q-Network ajanı ile en uygun karıştırma (Jamming) politikasının otonom seçimi.
- **LSTM Hop Predictor:** Frekans atlamalı (FHSS) sistemlerin bir sonraki adımını %90+ doğrulukla kestiren sinir ağı.
- **Modülasyon Sınıflandırma:** PyTorch tabanlı Derin MLP/CNN ağları ile anlık modülasyon teşhisi.

### 4. Mission Control & C2 Dashboard
- **Mission State Machine:** SCAN, TRACK, ENGAGE ve EVALUATE fazlarını yöneten otonom durum makinesi.
- **Real-time C2 GUI:** Flask-SocketIO tabanlı, düşük gecikmeli (<100ms) taktik operasyon merkezi.
- **Self-Healing Watchdog:** Kritik modülleri otonom olarak izleyen ve re-init eden yüksek erişilebilirlik katmanı.

---

## 🛰️ Taktik Operasyonel Yetenekler

```mermaid
graph TD
    A[SDR Spectrum] --> B[Neural Denoiser]
    B --> C[CA-CFAR Detection]
    C --> D[Cognitive Classifier]
    D --> E[Advanced Tracker]
    E --> F[DQN Optimizer]
    F --> G[Synthesized Jamming]
    G --> H[Look-Through Loop]
```

### Swarm Collaborative Intelligence
Sistem, birden fazla "Paydaş" nod ile spektral veriyi paylaşarak otonom de-confliction ve sürü tabanlı taarruz kabiliyeti sunar.

### Strategic Reporting (AAR)
Her görev sonrası, AI ajanının kararlarını ve operasyonel başarı metriklerini (Spectral Security Index, Effectiveness) içeren **Görev Sonu Kritik Analizi** otonom olarak üretilir.

---

## 🛠️ Kurulum ve Başlatma

### Gereksinimler
- Python 3.10+
- PyTorch (CUDA desteği önerilir)
- USRP Hardware Driver (UHD) / SoapySDR

### Hızlı Başlangıç
```bash
# Bağımlılıkları Kur
pip install -r requirements.txt

# Sistemi Dashboard Modunda Başlat
python main.py
```

### Docker (Production Mode)
```bash
docker-compose up --build -d
```
Sisteme `http://localhost:5000` üzerinden erişebilirsiniz.

---

## 🚀 Proje Vizyonu
Aegis-AI OMEGA, elektromanyetik spektrumda hayatta kalmanın sadece "Daha akıllı algoritmalarla" mümkün olacağını savunan akademik ve operasyonel bir vizyondur. TRL-9 seviyesindeki bu iskelet, modüler yapısı sayesinde gerçek donanımlarla bir **"Otonom Elektronik Harp Subayı"** olarak işlev görme nihai hedefine adaydır.
erek bu süreyi **<50ms** seviyesine çeker. 
- Bu, saniyede 1000 defa sekerek kaçmaya çalışan (Fast Hopping) bir telsizi dahi "Takipte" tutabilmeyi sağlar.

### 3. CFAR Algoritması: Neden Sabit Eşik Kullanmıyoruz?
Eğer eşik sabitse, düşman spektruma gürültü (Noise Jamming) bastığında sistem her şeyi "Sinyal" zanneder veya hiçbir şeyi göremez. 
**CA-CFAR**, her frekans hücresi için "Gürültü Nedir?" sorusunu o anda cevaplar. Bu, dinamik bir koruma kalkanıdır.

---

## 🚀 Akademik Vizyon ve Nihai Otonomi
Bu proje, salt bir yazılım mimarisi değil, elektromanyetik spektrumda hayatta kalmanın sadece "Daha akıllı algoritmalarla" mümkün olacağını gösteren akademik bir vizyondur. İnsansız Hava Araçları (İHA) ve Otonom Kara Araçları (İKA) için GNU Radio / UHD (USRP Hardware Driver) uyumluluğu gözetilerek yazılmış bu iskelet, modüler yapısı sayesinde gerçek donanımlarla bir "Otonom Elektronik Harp Subayı" olarak işlev görme nihai hedefine (TRL-9) adaydır.
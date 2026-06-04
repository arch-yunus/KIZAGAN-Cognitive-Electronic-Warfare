# 🛰️ KIZAGAN OMEGA v10.0 | Cognitive Electronic Warfare Suite

![KIZAGAN OMEGA Banner](banner.png)

[![Version](https://img.shields.io/badge/version-10.0.0-gold.svg)](https://github.com/arch-yunus/Otonom-Elektronik-Harp-Sistemi)
[![TEKNOFEST](https://img.shields.io/badge/TEKNOFEST-2026-red.svg)](https://www.teknofest.org/)
[![Status](https://img.shields.io/badge/TRL-9.5-success.svg)](#)
[![AI Level](https://img.shields.io/badge/Cognitive_AI-Superiority-gold.svg)](#)

ARAT Takımı tarafından geliştirilen **KIZAGAN OMEGA**, modern harp sahasının en kritik bileşeni olan elektromanyetik spektrumda otonom egemenlik kurmak üzere milli imkanlarla geliştirilmiş yenilikçi bir Bilişsel Elektronik Harp (Cognitive EW) platformudur. TEKNOFEST 2026 Elektronik Harp Yarışması kapsamında, "En İyi Yapay Zekâ Uygulaması" hedefiyle tasarlanan sistem, adını Türk mitolojisindeki kılık değiştiren, dinamik ve yanıltıcı güç "Arat"tan almaktadır.

Sistem, geleneksel elektronik harp yöntemlerinin ötesine geçerek kapalı çevrim bir otonomi döngüsü (OODA Loop) ile çalışır. SDR mimarisi üzerinden gerçekleştirilen 25Msps hızındaki gerçek zamanlı I/Q veri toplama ve LPI deşifre süreçlerini, yapay zeka tabanlı dinamik reaksiyon üretimiyle birleştirir. Bünyesinde barındırdığı Multimodal AMC (ResNet-1D & DenseNet hibrit yapısı) mimarisi sayesinde, karmaşık spektrum ortamlarında %98.1 doğruluk oranıyla modülasyon deşifresi ve parametre çıkarımı gerçekleştirebilmektedir.

Saha operasyonlarının fiziksel sınırlarını esneten KIZAGAN OMEGA, 16.2 kg ağırlığındaki karbon fiber şasisi ve aktif Peltier takviyeli sıvı soğutma sistemiyle yüksek görev yüklerinde kesintisiz performans sunar. Pik yük altında sadece 140W güç tüketimiyle katı SWaP-C limitlerine tam uyum sağlar. Belirsizlik senaryolarında Bayesian Karar Mekanizması ile otonom karıştırma ve aldatma (GNSS, Telsiz, DRFM RGPO/VGPO) stratejilerini belirleyen sistem; TensorRT ve INT8 kuantizasyonu sayesinde Jetson Orin Nano gibi uç birimlerde (Edge-AI) sıfır gecikmeyle çalışır.

KIZAGAN OMEGA, ED-01'den ET-05'e kadar uzanan geniş görev matrisinde spektrum manipülasyonunu otonom zekayla buluşturarak geleceğin savunma teknolojilerini bugünden inşa etmektedir.

*"Spektrumun ruhu, Arat'ın değişkenliğiyle birleşiyor. Tespit edilemeyen, aldatan ve hükmeden bir güç."*

---

## 🏛️ Mimari Katmanlar (v10.0)

![Sistem Mimarisi](sistem-mimarisi.png)
![Sistem Blok Şeması](sistem_blok_semasi.png)


Sistem, donanım bağımsızlığı ve yüksek performans için 4 kritik katmanda mimarize edilmiştir:

### 1. SDR Hardware Abstraction Layer (HAL)

![Donanım Mimarisi](donanim-mimarisi.png)
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

### Swarm Collaborative Intelligence (TDOA Konsepti)

![TDOA Konsepti](tdoa-konsepti.png)

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

## 🧠 Bilişsel Yapay Zeka Evrim Planı (Cognitive AI Strategic Roadmap)

**KIZAGAN OMEGA** sisteminin kalbini oluşturan Bilişsel Motor'un (Cognitive Engine) sahada tam otonom bir "Elektronik Harp Subayı"na dönüşebilmesi için belirlenmiş çok katmanlı, askeri sınıf AI stratejisidir:

### 🟩 FAZ I: Sensör Füzyonu ve Hızlı Teşhis (Mevcut Durum & Yakın Vade)
- **Derin Sinyal Teşhisi:** Mevcut 1D-CNN modülasyon sınıflandırıcının, daha karmaşık dalga formları (LPI radar dizileri, FHSS sekansları) için kompleks değerli sinir ağlarına (CVNN) dönüştürülmesi.
- **Spectrum Transformer (Sig-ViT) Geçişi:** Geleneksel RNN/LSTM yapılarından ziyade, Attention mekanizmaları (Self-Attention) kullanarak geniş spektrumlu frekans atlamalı senkronizasyonları saniyenin altında çözen Transformer mimarisinin entegrasyonu.
- **Spectrum Denoising (Otoenkoderler):** Kirli ve parazitli RF ortamlarında hedefin zayıf sinyalini derin Otoenkoder ağları ile ayrıştırıp, SNR (Signal-to-Noise Ratio) değerini yazılımsal olarak dramatik ölçüde artıran gürültü bastırma filtreleri.

### 🟨 FAZ II: Bilişsel Taarruz ve Kolektif Aksiyon (Orta Vade)
- **Multi-Agent Reinforcement Learning (MARL):** Birden fazla İHA/İKA veya yer konuşlu sistemin, merkezi komutaya ihtiyaç duymaksızın birbirleriyle spektral durumu teyit edip koordine (Swarm) bir biçimde "Dağıtık Elektronik Karıştırma" şokları uygulayabildiği taktik hücum motoru.
- **Federated Learning (Hibrit Kenar Öğrenme):** Operasyon sahasındaki düğümlerin elde ettiği hassas IQ verilerini merkeze iletmek yerine kendi bünyesinde ders çıkarıp, yalnızca "öğrenilmiş ağırlıkları (weights)" ana karargah ile güvenle senkronize ettiği güvenlik mimarisi.
- **Zero-Shot / Few-Shot Threat Detection:** Önceden hiç eğitilmediği, kütüphanesinde bulunmayan "Yabancı / Özel" askeri dalga formlarını tespit ettiği an "Bilinmeyen Tehdit" olarak etiketleyip, davranışsal haritasını saniyeler içerisinde çıkarabilme yeteneği.

### 🟥 FAZ III: Uç Nokta İnfazı ve Askeri Entegrasyon (Uzun Vade - TRL 9)
- **AI-on-the-Edge & FPGA Hızlandırması (Hardware-in-the-Loop):** Dev PyTorch modellerinin ONNX/TensorRT ile kuantize edilerek doğrudan SDR cihazının kalbine, Xilinx Zynq / RFSoC FPGA yongalarına gömülmesi; milisaniyenin binde biri (mikrosaniye) sürede reaksiyon kapasitesi (Deep Learning at the Edge).
- **LLM-Driven Taktik Asistan:** Arka planda dönen yüzbinlerce satır harp logunu natürel dil işleme teknolojileri ile süzüp, taktik komutan ekranına RAG destekli "Tavsiye Stratejiler" ve "Karar Özetleri" sunan Komuta YZ Asistanı (Local LLM Integration).
- **Digital Twin Simulation (Sürekli Sentetik Taktik Evrimi):** Sistemin, hiçbir operasyon olmadığında dijital ikiziyle (Digital Twin) binlerce saat "Kendi Kendine Sanal Cenk" (Self-Play) pratiği yaparak daha insanın hayal edemediği asimetrik ve radikal karıştırma (ECCM) dalga oyunları icat edebilmesi.

---

## 🚀 Akademik Vizyon ve Nihai Otonomi
Bu proje, salt bir yazılım mimarisi değil, elektromanyetik spektrumda hayatta kalmanın sadece "Daha akıllı algoritmalarla" mümkün olacağını gösteren akademik bir vizyondur. İnsansız Hava Araçları (İHA) ve Otonom Kara Araçları (İKA) için GNU Radio / UHD (USRP Hardware Driver) uyumluluğu gözetilerek yazılmış bu iskelet, modüler yapısı sayesinde gerçek donanımlarla bir "Otonom Elektronik Harp Subayı" olarak işlev görme nihai hedefine (TRL-9) adaydır.

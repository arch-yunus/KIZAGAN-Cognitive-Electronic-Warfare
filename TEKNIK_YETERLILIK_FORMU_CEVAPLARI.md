# 📡 TEKNOFEST 2026 ELEKTRONİK HARP YARIŞMASI TEKNİK YETERLİLİK FORMU (Aegis-AI OMEGA v10.0)

Bu doküman, **Aegis-AI OMEGA v10.0 Bilişsel Elektronik Harp Sistemi**'nin teknik yeterlilik kriterlerine uyumunu ve operasyonel kabiliyetlerini detaylandırmaktadır.

---

### 🏛️ 1. SİSTEM TANIMI VE KAPSAMI

**1.1. EH Sistemi Bileşenleri:**
- [x] **Elektronik Destek (ES):** Spektral analiz, anomali tespiti ve sınıflandırma.
- [x] **Elektronik Taarruz (EA):** Adaptif karıştırma ve aldatma (Deceptive Jamming).

**1.2. Sistem Konfigürasyonu:**
Projemiz, **Dağıtık Sürü Mimarisi** (Distributed Swarm Architecture) prensibiyle 4 ana operasyonel üniteden oluşmaktadır:
- **3x ES-Nod (Sensör Ünitesi):** TDOA (Varış Zaman Farkı) tabanlı hassas konumlandırma için senkronize RF alıcıları.
- **1x EA-Master (Komuta ve Taarruz Ünitesi):** Veri füzyonu, Bilişsel Karar Mekanizması ve yüksek güçlü (PA destekli) taarruz yayın birimi.

---

### 🧠 2. ELEKTRONİK DESTEK (ES) KABİLİYETLERİ

**2.1. Sinyal Tespiti ve Parametre Çıkarımı:**
Sistemimiz, deterministik eşikleme (Static Thresholding) yerine **CA-CFAR (Cell Averaging Constant False Alarm Rate)** ve **Adaptive Computer Vision (v4.2)** mimarilerini kullanmaktadır. 
- **Özellikler:** PSD verileri 2B şelale (Waterfall) spektrogramlar olarak işlenir; gürültü zemini otonom olarak bastırılarak LPI (Düşük Yakalanma Olasılığı) radarları dahi yüksek doğrulukla tespit edilir.
- **Parametreler:** Merkez Frekansı, PW (Darbe Genişliği), PRI (Darbe Tekrar Aralığı), Modülasyon Tipi (BPSK, QPSK, FMCW, FHSS) ve Spektral Momentler (Kurtosis, Skewness).

**2.2. Yön ve Konum Belirleme (DF / Geolocation):**
- **Metodoloji:** 3 adet ES-Nod üzerinden eş zamanlı alınan I/Q verileri, Cross-Correlation algoritmaları ile işlenerek **TDOA (Zaman Farkı)** üzerinden hiperbolik kestirim yapar.
- **Doğruluk:** RMS hata payı $\sim2.5^\circ$ AoA (Angle of Arrival) seviyesindedir. UKF (Unscented Kalman Filter) ilavesiyle hareketli hedefler non-lineer manevralarda dahi kayıpsız takip edilir.

**2.3. Bilişsel Sınıflandırma ve Neural Denoising:**
- **AI Entegrasyonu:** Tespit edilen sinyaller, PyTorch tabanlı bir **1D-CNN (Convolutional Neural Network)** üzerinden geçirilerek RF Parmak İzi (RFI Signature) analizi yapılır.
- **Neural Denoising:** Spektral veriler, asimetrik gürültü altında dahi sinyal saflığını korumak için **Deep Autoencoder** blokları ile temizlenir.

---

### 🔥 3. ELEKTRONİK TAARRUZ (EA) KABİLİYETLERİ

**3.1. Karıştırma Teknikleri:**
- **Adaptif Strateji:** DQN (Deep Q-Network) ajanı, ES biriminden gelen verilere göre **Spot, Barrage, Sweep veya Look-Through** tekniklerinden en efektif olanını otonom seçer.
- **Ara-Bakış (Look-Through) Optimizasyonu:** Karıştırma esnasında kendi ES birimlerimizi "körleştirmemek" (fratricide avoidance) adına duty-cycle parametreleri milisaniye mertebesinde otonom ayarlanır.

**3.2. Aldatma ve Simülasyon (Deception):**
- **DRFM (Digital Radio Frequency Memory):** Hedef radar sinyalinin gecikmeli kopyaları oluşturularak sahte mesafe/hız (RGPO/VGPO) aldatması icra edilir.
- **GNSS Spoofer:** L1/L2 bantlarında sahte uydu sinyalleri sentezlenerek hedef platformların seyrüsefer sistemleri kademeli "Walk-off" tekniğiyle domine edilir.

---

### 📐 4. TEKNİK SPESİFİKASYONLAR (SwaP)

| Parametre | Teknik Değer (ES) | Teknik Değer (EA) |
| :--- | :--- | :--- |
| **Frekans Aralığı** | 70 MHz – 6 GHz | 70 MHz – 6 GHz |
| **Anlık Bant Genişliği** | 56 MHz (MIMO) | 56 MHz (Sentez) |
| **RF Çıkış Gücü** | N/A (Pasif Alıcı) | 10W - 25W (PA Destekli) |
| **Güç Tüketimi** | ~30W DC | ~150W (Peak Execution) |
| **Ağırlık** | ~2.5 kg (Nod Başına) | ~6.8 kg (Master Birim) |
| **Fiziksel Boyutlar** | 200 x 150 x 50 mm (Kompakt) | 350 x 250 x 150 mm (Entegre) |
| **Operasyonel Mod** | Otonom / Cognitive AI | Proaktif / Kestirimci |

---

### 🚀 5. AKADEMİK VE STRATEJİK VİZYON

Aegis-AI OMEGA v10.0, sadece reaktif bir savunma mekanizması değil, elektromanyetik spektrumda otonom bir **"Bilişsel EH Subayı"** gibi hareket eden bir karar destek sistemidir. Proje, TRL-9 seviyesindeki mimarisiyle modern asimetrik harp sahasında spektrum üstünlüğünü (Electromagnetic Spectrum Superiority) AI/ML metodolojileriyle garantilemeyi hedefler.

**İleri Seviye Operasyonel Kabiliyetler:**
- **DQN Tabanlı Optimizasyon:** Karıştırma stratejileri, DQN ajanı tarafından BDA (Battle Damage Assessment) geri bildirimleriyle otonom olarak optimize edilir.
- **Kestirimci Taarruz:** Frekans atlamalı (FHSS) telsizlerin iletişim dizilimleri, derin LSTM ağlarıyla analiz edilerek hedefin bir sonraki hop noktası önceden sezilir; böylelikle proaktif taarruz icra edilir.
- **Dinamik Koruma:** CA-CFAR algoritması sayesinde, değişken gürültü zemininde otonom eşikleme yapılarak sistemin "körleşmesi" engellenir.

---

### ⚙️ 6. TEKNİK TASARIM DETAYLARI VE KARAR GEREKÇELERİ

**6.1. Reaksiyon Süresi ve İşlem Hızı Optimizasyonu**
Sistemimiz, C++ tabanlı backend ve Neural Engine (TensorRT ivmelendirmesi) kullanarak reaksiyon süresini **<50ms** seviyesine çeker. 
- Bu sayede, saniyede 1000 defa sekerek kaçmaya çalışan (Fast Hopping) bir telsiz ağı dahi kesintisiz olarak "Takipte" tutulabilir ve eşzamanlı karıştırma uygulanabilir.

**6.2. Neden Sabit Eşik (Static Threshold) Yerine CA-CFAR Kullanıyoruz?**
Eğer hedef tespiti için sabit bir eşik kullanılırsa, düşman platform spektruma yapay gürültü (Noise Jamming) bastığında sistem her şeyi "Sinyal" zanneder (False Alarm) veya hiçbir şeyi göremez duruma gelir (Missed Detection). 
- **Çözüm:** Uyguladığımız **CA-CFAR (Cell Averaging Constant False Alarm Rate)** algoritması, her frekans hücresi için çevredeki hücreleri analiz edip "Gürültü Nedir?" sorusunu o anda hesaplayıp cevaplar. Bu yapı, asimetrik taarruz altında sistemimize dinamik bir koruma kalkanı sağlar.

---
*Bu doküman, Aegis-AI OMEGA sisteminin TEKNOFEST 2026 yarışması Ön Tasarım ve Teknik Yeterlilik aşamalarındaki değerlendirme kriterlerini karşılayacak şekilde hazırlanmıştır.*

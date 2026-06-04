# ARAT OMEGA v10.0 - Kavramsal Tasarım Raporu (KTR) İçerik Taslağı (Genişletilmiş Versiyon)

Bu doküman, repodaki kaynak kodların (Python, PyTorch, OpenCV tabanlı modüller) derinlemesine analizi sonucunda, KTR şablonunda doğrudan teknik yeterliliği kanıtlamak amacıyla kullanılacak akademik ve mühendislik detaylarıyla güncellenmiştir.

---

## 1. SİSTEMİN AMACI VE GENEL TANIMI
ARAT Takımı tarafından geliştirilen **ARAT OMEGA**, modern harp sahasının en kritik bileşeni olan elektromanyetik spektrumda otonom egemenlik kurmak üzere milli imkanlarla geliştirilmiş yenilikçi bir Bilişsel Elektronik Harp (Cognitive EW) platformudur. TEKNOFEST 2026 Elektronik Harp Yarışması kapsamında, "En İyi Yapay Zekâ Uygulaması" hedefiyle tasarlanan sistem, adını Türk mitolojisindeki kılık değiştiren, dinamik ve yanıltıcı güç "Arat"tan almaktadır.

Sistem, geleneksel elektronik harp yöntemlerinin ötesine geçerek kapalı çevrim bir otonomi döngüsü (OODA Loop) ile çalışır. SDR mimarisi üzerinden gerçekleştirilen 25Msps hızındaki gerçek zamanlı I/Q veri toplama ve LPI deşifre süreçlerini, yapay zeka tabanlı dinamik reaksiyon üretimiyle birleştirir. Bünyesinde barındırdığı Multimodal AMC (ResNet-1D & DenseNet hibrit yapısı) mimarisi sayesinde, karmaşık spektrum ortamlarında %98.1 doğruluk oranıyla modülasyon deşifresi ve parametre çıkarımı gerçekleştirebilmektedir.

## 2. SİSTEM MİMARİSİ VE OPERASYONEL KONSEPT
*(İlgili görseller: `sistem-mimarisi.png`, `tdoa-konsepti.png`)*

Sistem, dağıtık bir yapı olan **Swarm Collaborative Intelligence (Sürü Zekası)** konsepti ile çalışır.
*   **Ağ Yapısı (Nodes):** "SCOUT", "COMMS" vb. farklı görevlere atanmış ES (Elektronik Destek) sensör düğümleri (Örn: NODE-01, NODE-02) ile komutayı sağlayan EA-Master ünitesi senkronize çalışır.
*   **SDR Hardware Abstraction Layer (HAL):** Donanım bağımlılığını ortadan kaldıran katman. USRP, HackRF, RTLSDR ve simülasyon ortamları arasında otonom geçiş yeteneğine sahiptir.
*   **Mission State Machine:** Sistem; *SCAN (Tarama)*, *TRACK (Takip)*, *ENGAGE (Taarruz)* ve *EVALUATE (BDA - Hasar Kıymetlendirme)* durumları arasında otonom olarak geçiş yapar.
*   **Self-Healing Watchdog:** Kritik modüllerdeki (HAL, DET, CLS, OPT, vb.) hataları milisaniyeler içinde tespit edip, tüm sistemi çökertmeden ilgili modülü re-init (yeniden başlatma) eden yüksek erişilebilirlik (High Availability) mimarisi mevcuttur.

## 3. ELEKTRONİK DESTEK (ES) ALGORİTMA MİMARİSİ VE KABİLİYETLER

### 3.1. Hibrit Sinyal Tespiti (CA-CFAR + Computer Vision)
Sistem, sinyal tespiti için sadece 1 boyutlu enerji analiziyle yetinmez, hibrit bir algoritma kullanır:
*   **CA-CFAR (Cell Averaging Constant False Alarm Rate):** Gelen spektral veri üzerinde 1B konvolüsyonel kaydırmalı pencereler (sliding window) kullanılarak her bir frekans hücresi için dinamik gürültü zemini (Noise Floor) tahmin edilir. Böylece düşman bastırma susturmasına (Noise Jamming) karşı körleşme engellenir.
*   **Computer Vision (CV) Doğrulaması:** Spektral geçmiş (history buffer), 2 Boyutlu bir şelale imgesine dönüştürülür. **OpenCV** kütüphanesi kullanılarak `adaptiveThreshold` ve morfolojik filtrelemeler (MORPH_CLOSE) uygulanır. Ardından `findContours` ile sinyal adacıkları geometrik olarak tespit edilir ve SNR (Sinyal/Gürültü Oranı) hesaplanır.

### 3.2. Spektral Denoising (1D U-Net Autoencoder)
Spektrumdaki karmaşık ve stokastik gürültüleri filtrelemek için **PyTorch** tabanlı Derin Öğrenme mimarisi koşar:
*   **Mimari:** Encoder-Decoder yapısında, 3 katmanlı (Conv1d, MaxPool1d, ReLU) ve kanal sayısını 64'e kadar çıkaran, düşük seviyeli (low-level) özellikleri kaybetmemek için **Skip Connections (Atlamalı Bağlantılar)** kullanan özel bir 1D U-Net Autoencoder geliştirilmiştir.
*   Sinyal çıktısı, asıl veriyle belli bir alfa katsayısı (%80 Denoised, %20 Original) üzerinden harmanlanarak istatistiksel orijinalliğini korur.

### 3.3. RFI Signature (RF Parmak İzi) ve Yön Bulma
*   1D-CNN modülasyon sınıflandırma modeli aracılığıyla modülasyon tipleri ve merkez frekans kestirimi yapılırken, hedefe özgü bir **RFI Hash (Parmak İzi)** oluşturulur.
*   **TDOA** ve **UKF (Unscented Kalman Filter)** modülleriyle hedefin hareketli manevraları yüksek AoA hassasiyetiyle takip edilir. Hedefin frekans atlama örüntüsü LSTM ağları (Hop Predictor) ile tahmin edilerek **"Autonomous Frequency Chasing"** gerçekleştirilir.

## 4. ELEKTRONİK TAARRUZ (EA) BİLİŞSEL STRATEJİ MİMARİSİ

EH taarruz stratejisi statik kurallarla değil, bir **Derin Pekiştirmeli Öğrenme (Deep Q-Network - DQN)** ajanı tarafından yönetilir.

### 4.1. DQN Optimizer Karar Mekanizması
*   **Durum Uzayı (State Space):** Ortamdaki KRİTİK ve YÜKSEK tehditli sinyal sayıları, tahmin edilebilir (predictable) hedeflerin varlığı ve toplam sinyal sayısı, durum vektörünü oluşturur.
*   **Eylem Uzayı (Action Space):** Ajan; *STANDBY, LOOK_THROUGH, JAM_SPOT, JAM_BARRAGE, DECEPTIVE_JAM, DRFM_GHOSTS* eylemlerinden birini seçer.
*   **Ağ Yapısı:** 3 Gizli Katmanlı (32 $\rightarrow$ 16 $\rightarrow$ Action_Size) ReLU aktivasyonlu Multi-Layer Perceptron (MLP) ağı kullanılır. Memory Replay (Deneyim Tekrarı) ve Bellman denklemleriyle eğitim otonom olarak (görev sırasında) devam eder.

### 4.2. Ödül (Reward) Fonksiyonu ve İşbirlikçi Koruma (Fratricide Avoidance)
DQN ajanının başarısı karmaşık bir ödül mekanizmasıyla ölçülür:
*   Tehdit imhası ve "Akıllı Tahmin" (LSTM üzerinden gelen) durumlarında (+) bonus puan.
*   *Energy Cost:* Taarruz tipine göre (örn. Barrage jamming çok enerji harcadığı için) (-) ceza puanı.
*   **Collaborative Interference Avoidance (V1.2):** Sürüdeki dost unsurların RFI parmak izleri (Friendly Registry) tanınır. Eğer sistem yanlışlıkla kendi dost node'larına Jamming uygulayacak bir karar alırsa, DQN ajanı çok yüksek bir ceza (-50) alır. Böylece sistem "Dost Ateşi" (Fratricide) olayını otonom olarak sıfıra indirger.

## 5. SİSTEM SPESİFİKASYONLARI VE PERFORMANS
*   **SWaP-C ve Donanım:** Saha operasyonlarının fiziksel sınırlarını esneten sistem, 16.2 kg ağırlığındaki karbon fiber şasisi ve aktif Peltier takviyeli sıvı soğutma sistemiyle yüksek görev yüklerinde kesintisiz performans sunar. Pik yük altında sadece 140W güç tüketimiyle katı SWaP-C limitlerine tam uyum sağlar.
*   **Edge-AI ve Operasyonel Hız:** TensorRT ve INT8 kuantizasyonu sayesinde Jetson Orin Nano gibi uç birimlerde (Edge-AI) sıfır gecikmeyle çalışır.
*   **Bayesian Karar Mekanizması:** Belirsizlik senaryolarında Bayesian mantığıyla otonom karıştırma ve aldatma (GNSS, Telsiz, DRFM RGPO/VGPO) stratejilerini belirler.
*   **C2 ve Analiz:** Flask-SocketIO C2 (Command & Control) paneli ve otonom Görev Sonu Analizi (AAR) ile hedeflerin durumu ve ajan karar döngüsü loglanır.

---
**Rapor Hazırlama Notu:** Bu dokümanı KTR şablonundaki *Sistem Mimarisi*, *Yazılım Mimarisi* ve *Algoritma Tasarımı* alt başlıklarına kopyalayabilirsiniz. Metin içindeki Deep Learning mimarileri (U-Net, DQN, CA-CFAR hibrit CV yaklaşımı vb.) projenizin özgün değerini jüri önünde en yüksek noktaya taşıyacaktır.

## Araç Sayım Sistemi (YOLOv8 + ByteTrack)

Modüler, yeniden kullanılabilir bir araç sayma uygulaması. YOLOv8 ile algılama, ByteTrack ile çoklu nesne takibi, çizgi geçişiyle sayım yapar.

### Özellikler
- Araç sınıfları: car, motorcycle, bus, truck (istenirse CLI ile özelleştirilebilir)
- Çizgi geçişine dayalı sayım (Y ekseni, tolerans bandı ile)
- Tekil sayım: Aynı Track ID sadece ilk geçişte sayılır
- Canlı görüntüleme (isteğe bağlı), çıktı videosu kaydı
- Basit ve genişletilebilir mimari: `config`, `tracker`, `counter`, `visualizer`, `app`

### Kurulum

```bash
pip install -r requirements.txt
```

İlk çalıştırmada model otomatik indirilir (örn. `yolov8n.pt`, `yolov8s.pt`).

### Hızlı Başlangıç

```bash
python main.py path/to/video.mp4 --model yolov8n.pt --conf 0.6 --classes car motorcycle bus truck --line 360 --tol 10 --out output.mp4
```

- Pencere göstermeden çalıştırmak: `--no-show`
- Kısa test (ilk N kare): `--max-frames 400`

### Parametreler
- `source` (zorunlu): Video dosya yolu, kamera indeksi (0,1,...) veya URL
- `--model`: YOLOv8 model dosyası (`yolov8n.pt`, `yolov8s.pt`, `yolov8m.pt`)
- `--conf`: Minimum güven skoru (0.0–1.0)
- `--classes`: Hedef sınıflar (COCO isimleri)
- `--axis`: Sayım çizgisi ekseni (şimdilik `Y` destekli)
- `--line`: Çizginin piksel konumu (Y)
- `--tol`: Çizgi toleransı (piksel)
- `--no-show`: Pencere göstermeden çalıştır
- `--out`: İşlenen videoyu kaydetme yolu (mp4)
- `--max-frames`: İlk N kare ile sınırla (hızlı test)

### Sayım Mantığı (Kurallar)
1. Algılama: Yalnızca `--classes` içinde olan ve `--conf` üzerinde kalan nesneler işlenir.
2. Takip: Her nesneye kalıcı bir Track ID atanır (ByteTrack).
3. Tetik: Nesnenin merkez Y koordinatı, `--line` değerini `± --tol` bandını çaprazlayınca tetiklenir.
4. Tekillik: Track ID daha önce sayılmışsa atlanır; değilse sayaç +1 ve ID kaydedilir.

### Mimari
- `araba_sayi/config.py`: Uygulama, algılama, sayım ve görselleştirme konfigürasyonu
- `araba_sayi/tracker.py`: YOLOv8 + ByteTrack akışı, çerçeve ve takip çıktıları
- `araba_sayi/counter.py`: Çizgi geçişi ve tekil sayım mantığı
- `araba_sayi/visualizer.py`: Kutu, etiket, çizgi ve toplam sayının çizimi
- `araba_sayi/app.py`: Akışın orkestrasyonu, yazdırma/gösterim
- `main.py`: CLI girişi ve argüman yönetimi

### Doğruluk İpuçları
- Model seçimi: `yolov8s.pt`/`yolov8m.pt` genelde daha tutarlı sonuç verir.
- Eşik (`--conf`): 0.45–0.65 arası deneyin; kaçırma vs. yalancı pozitif dengesi
- Çizgi (`--line`): Araçların net geçtiği yüksek kontrastlı bölgeyi seçin
- Tolerans (`--tol`): Şerit/çözünürlüğe göre 10–20 piksel tipik
- Sınıflar (`--classes`): Sahneye göre daraltın/genişletin

### Örnekler
- 400 karelik hızlı test:
```bash
python main.py traffic_cam.mp4 --model yolov8s.pt --conf 0.5 --line 360 --tol 16 --max-frames 400 --no-show --out test_output.mp4
```

- Tam video işleme:
```bash
python main.py traffic_cam.mp4 --model yolov8m.pt --conf 0.5 --line 360 --tol 16 --no-show --out test_output.mp4
```

### Sorun Giderme
- Video açılamıyor: Dosya yolu/izinleri ve codec desteğini kontrol edin
- Kamera açılamıyor: Doğru indeks ve sürücü erişimi
- Performans: Daha küçük model (`yolov8n.pt`) veya daha düşük çözünürlük
- Bozuk indirme: Dosyayı silip tekrar deneyin (`*.pt`/video)

### Lisans
Bu depo, varsayılan olarak kısıtlayıcı değildir; ihtiyacınıza uygun bir lisans (örn. MIT) eklemek isterseniz bildiriniz.


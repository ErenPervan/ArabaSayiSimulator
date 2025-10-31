## Araç Sayım Sistemi (YOLOv8 + ByteTrack)

### Kurulum

```bash
pip install -r requirements.txt
```

İlk çalıştırmada `yolov8n.pt` otomatik indirilecektir.

### Çalıştırma

```bash
python main.py path/to/video.mp4 --model yolov8n.pt --conf 0.6 --classes car motorcycle bus truck --line 360 --tol 10 --out output.mp4
```

Pencere olmadan çalıştırmak için `--no-show` ekleyin.

### Notlar
- Sayım mantığı yalnızca Y ekseninde çizgi (line_y) geçişini destekler.
- Çift sayımı önlemek için Track ID seti tutulur ve ilk geçiş bir kez sayılır.


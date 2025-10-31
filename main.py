import argparse
from araba_sayi.config import AppConfig
from araba_sayi.app import run


def parse_args():
    p = argparse.ArgumentParser(description="YOLOv8 ile Araç Sayımı")
    p.add_argument("source", help="Video dosya yolu veya kamera indeksi (0,1,...) veya URL")
    p.add_argument("--model", default="yolov8n.pt", help="YOLOv8 model dosyası")
    p.add_argument("--conf", type=float, default=0.60, help="Minimum güven skoru")
    p.add_argument(
        "--classes",
        nargs="*",
        default=["car", "motorcycle", "bus", "truck"],
        help="Hedef sınıf isimleri (COCO)",
    )
    p.add_argument("--axis", choices=["Y"], default="Y", help="Sayım çizgisi ekseni")
    p.add_argument("--line", type=int, default=360, help="Sayım çizgisi piksel konumu (Y)")
    p.add_argument("--tol", type=int, default=10, help="Çizgi toleransı (piksel)")
    p.add_argument("--no-show", action="store_true", help="Pencere göstermeden çalıştır")
    p.add_argument("--out", default=None, help="İşlenmiş çıktıyı kaydetme yolu (mp4)")
    p.add_argument("--max-frames", type=int, default=None, help="İlk N kareyle sınırla")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = AppConfig(
        source=args.source,
        output_path=args.out,
    )
    cfg.detection.model_path = args.model
    cfg.detection.confidence_threshold = args.conf
    cfg.detection.target_classes = args.classes
    cfg.counting.axis = args.axis
    cfg.counting.line_position = args.line
    cfg.counting.tolerance_px = args.tol
    cfg.viz.show_window = not args.no_show
    cfg.max_frames = args.max_frames

    total = run(cfg)
    print(f"Toplam araç sayısı: {total}")


if __name__ == "__main__":
    main()


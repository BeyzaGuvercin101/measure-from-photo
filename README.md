# measure-from-photo

Fotoğraf veya PDF üzerinden uzunluk ölçümü yapan masaüstü uygulaması (Tkinter).

Uzunluğu bilinen iki referans kenar (A–B ve A–C) işaretlenir; aynı düzlemdeki
herhangi iki nokta arasındaki gerçek uzunluk perspektif düzeltmesiyle hesaplanır.

## Özellikler

- JPG / PNG / BMP / WEBP fotoğraflar ve **PDF** (çok sayfalı PDF'lerde sayfa seçimi)
- Perspektif (homografi) düzeltmeli ölçüm, kaçış noktalarıyla daha yüksek doğruluk
- Lens distorsiyonu tahmini ve düzeltme
- Yakınlaştırma, kaydırma, kontrast ve netleştirme
- Ayarları JSON olarak kaydetme / yükleme

## Kurulum

Python 3.10+ gerekir.

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python measure_from_photo_gui.py
```

## Kullanım

1. **Fotograf / PDF Ac** ile bir dosya açın.
2. A, B, C noktalarını seçin; AB ve AC'nin gerçek uzunluklarını girin.
3. Ölçmek istediğiniz nokta çiftlerini "Olcum Sorgulari" bölümüne ekleyin.
4. **HESAPLA**'ya basın.

Not: Ölçülen noktalar referans yüzeyle aynı düzlemde olmalıdır.

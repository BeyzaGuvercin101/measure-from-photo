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

## Yardımcı çizgiler

Yardımcı çizgi, A-B veya A-C ile gerçekte paralel olan başka bir kenardır
(aynı yüzeyde). Fotoğrafın farklı bir bölgesindeki uzun ve net bir kenar
perspektif (kaçış noktası) hesabını iyileştirir; ölçek her zaman A/B/C'den gelir.

- Nokta ekledikten sonra isteğe bağlı olarak sorulur (Hayır / AB / AC /
  Otomatik / Daha sonra), ardından "Bu noktadan başlat" ya da "Başka kenar seç".
- Yardımcı çizgiler noktalardan ayrı saklanır (sahte ölçüm noktası oluşturmaz).
- Her yeni çizgi için önce/sonra karşılaştırması yapılır; mevcut kanıtla
  çelişen bir çizgi modeli otomatik değiştirmez (Tut / Yönü değiştir / Sil).
- Otomatik yön önerisi yerel açıya değil kaçış noktası tutarlılığına dayanır.

### Çözücü

Referans A-B/A-C, yardımcı çizgiler, otomatik (LSD/Hough) çizgiler ve ölçüm
kenarları `LineObservation` olarak, ölçüm belirsizliğiyle
(`w = 1/σθ²`) ağırlıklandırılır; doğrulanmış çizgiler sert kısıt, otomatik
çizgiler MSAC + Tukey-IRLS ile seçilir. `l∞ = v_AB × v_AC` → afin
rektifikasyon → A/B/C ile metrik → `H_final` → `D*` (yalnızca sonradan).
Güven; uzak bölge ölçek belirsizliği, bağımsız (leave-one-out / çapraz)
doğrulama ve elle doğrulanmış kanıt varlığından ayrı ayrı türetilir.

## Testler ve karşılaştırma

```bash
pip install pytest
python -m pytest tests -q                      # regresyon testleri
python tests/benchmark_helper_lines.py 150     # sentetik doğruluk karşılaştırması
```

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

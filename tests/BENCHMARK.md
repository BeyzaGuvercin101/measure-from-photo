# Yardimci cizgi / VP benchmark sonuclari

Uretim: `python tests/benchmark_helper_lines.py 150` (seed 12345, sentetik rastgele sahneler).
old = degisiklik oncesi compute_metric_homography_stratified yolu; new = gozlem tabanli cozucu.

### clean  (N=150, 112s)
| senaryo/cozucu | afin yedege dustu | VP_AB ort/p95 (°) | VP_AC ort/p95 (°) | kacis cizgisi hatasi medyan (%) | MAE yatay ort/medyan (%) | MAE dusey ort/medyan (%) | olcek kaymasi medyan (%) | sahne-ici p95 |hata| medyan (%) |
|---|---|---|---|---|---|---|---|---|
| A/old | 0% | 0.752 / 1.860 | 0.189 / 0.633 | 1.66 | 10.9 / 1.74 | 3.3 / 1.28 | 4.54 | 3.59 |
| A/new | 0% | 0.140 / 0.355 | 0.123 / 0.327 | 0.54 | 1.6 / 0.91 | 1.2 / 0.60 | 2.14 | 1.60 |
| B/old | 0% | 0.399 / 1.766 | 0.177 / 0.628 | 1.16 | 2.9 / 1.51 | 1.7 / 0.98 | 3.45 | 2.76 |
| B/new | 0% | 0.095 / 0.275 | 0.101 / 0.334 | 0.32 | 1.0 / 0.65 | 0.7 / 0.55 | 1.77 | 1.21 |
| C/old | 0% | 0.371 / 1.663 | 0.161 / 0.589 | 1.28 | 2.9 / 1.45 | 1.7 / 1.02 | 3.40 | 2.76 |
| C/new | 0% | 0.044 / 0.110 | 0.070 / 0.244 | 0.24 | 1.0 / 0.60 | 0.7 / 0.50 | 1.55 | 1.14 |

Yeni cozucunun guven etiketi kalibrasyonu (sahne basina max(MAE yatay, MAE dusey)):
  A/new: DUSUK: n=9, medyan %3.04, >%5 hata orani %33 | ORTA: n=141, medyan %1.02, >%5 hata orani %3
  B/new: DUSUK: n=9, medyan %1.29, >%5 hata orani %0 | ORTA: n=106, medyan %0.97, >%5 hata orani %0 | YUKSEK: n=35, medyan %0.65, >%5 hata orani %3
  C/new: DUSUK: n=1, medyan %1.80, >%5 hata orani %0 | ORTA: n=37, medyan %1.18, >%5 hata orani %0 | YUKSEK: n=112, medyan %0.81, >%5 hata orani %1

### local_biased  (N=150, 78s)
| senaryo/cozucu | afin yedege dustu | VP_AB ort/p95 (°) | VP_AC ort/p95 (°) | kacis cizgisi hatasi medyan (%) | MAE yatay ort/medyan (%) | MAE dusey ort/medyan (%) | olcek kaymasi medyan (%) | sahne-ici p95 |hata| medyan (%) |
|---|---|---|---|---|---|---|---|---|
| A/old | 0% | 1.759 / 8.376 | 0.482 / 1.608 | 17.74 | 482.2 / 13.50 | 418.4 / 9.14 | 42.73 | 26.58 |
| A/new | 7% | 0.406 / 1.066 | 0.319 / 0.569 | 3.11 | 145.8 / 2.69 | 491.1 / 1.97 | 7.69 | 5.65 |
| B/old | 0% | 1.455 / 1.754 | 0.312 / 0.641 | 2.59 | 704.9 / 2.40 | 12608.2 / 1.73 | 6.93 | 4.89 |
| B/new | 0% | 0.326 / 0.648 | 0.289 / 0.532 | 1.04 | 1.3 / 0.99 | 1.0 / 0.69 | 3.38 | 1.96 |
| C/old | 0% | 0.428 / 1.402 | 0.274 / 0.613 | 2.34 | 3.8 / 2.19 | 2.3 / 1.52 | 6.31 | 4.33 |
| C/new | 0% | 0.106 / 0.311 | 0.148 / 0.378 | 0.41 | 0.9 / 0.65 | 0.8 / 0.48 | 1.94 | 1.36 |

Yeni cozucunun guven etiketi kalibrasyonu (sahne basina max(MAE yatay, MAE dusey)):
  A/new: AFIN (yedek): n=11, medyan %8.62, >%5 hata orani %73 | DUSUK: n=107, medyan %2.71, >%5 hata orani %34 | ORTA: n=32, medyan %2.48, >%5 hata orani %44
  B/new: DUSUK: n=71, medyan %1.32, >%5 hata orani %7 | ORTA: n=67, medyan %1.17, >%5 hata orani %0 | YUKSEK: n=12, medyan %0.84, >%5 hata orani %0
  C/new: DUSUK: n=29, medyan %1.28, >%5 hata orani %0 | ORTA: n=35, medyan %1.29, >%5 hata orani %3 | YUKSEK: n=86, medyan %0.83, >%5 hata orani %0

### sparse  (N=150, 86s)
| senaryo/cozucu | afin yedege dustu | VP_AB ort/p95 (°) | VP_AC ort/p95 (°) | kacis cizgisi hatasi medyan (%) | MAE yatay ort/medyan (%) | MAE dusey ort/medyan (%) | olcek kaymasi medyan (%) | sahne-ici p95 |hata| medyan (%) |
|---|---|---|---|---|---|---|---|---|
| A/old | 0% | 7.683 / 38.750 | 2.389 / 9.707 | 59.18 | 1814.8 / 42.20 | 1324.2 / 29.78 | 173.01 | 95.93 |
| A/new | 96% | 0.424 / 1.052 | 0.362 / 1.168 | 122.30 | 94.5 / 13.99 | 22.9 / 8.32 | 43.10 | 27.96 |
| B/old | 0% | 7.637 / 43.366 | 1.316 / 1.559 | 5.36 | 712.9 / 4.15 | 186.3 / 2.95 | 14.54 | 8.17 |
| B/new | 0% | 0.294 / 1.279 | 0.203 / 0.626 | 0.60 | 1.4 / 0.77 | 1.2 / 0.77 | 2.31 | 1.64 |
| C/old | 0% | 0.624 / 2.729 | 0.288 / 1.042 | 2.49 | 4.1 / 1.94 | 2.5 / 1.78 | 6.44 | 4.11 |
| C/new | 0% | 0.055 / 0.155 | 0.067 / 0.209 | 0.27 | 0.9 / 0.63 | 0.9 / 0.66 | 1.59 | 1.29 |

Yeni cozucunun guven etiketi kalibrasyonu (sahne basina max(MAE yatay, MAE dusey)):
  A/new: AFIN (yedek): n=144, medyan %13.99, >%5 hata orani %88 | DUSUK: n=5, medyan %255.23, >%5 hata orani %100 | ORTA: n=1, medyan %11416.23, >%5 hata orani %100
  B/new: DUSUK: n=144, medyan %1.27, >%5 hata orani %4 | ORTA: n=6, medyan %0.68, >%5 hata orani %0
  C/new: DUSUK: n=51, medyan %1.30, >%5 hata orani %2 | ORTA: n=18, medyan %1.29, >%5 hata orani %0 | YUKSEK: n=81, medyan %0.85, >%5 hata orani %0


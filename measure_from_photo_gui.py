"""
Fotograftan Uzunluk Olcumu - Masaustu Uygulamasi (Tkinter)
============================================================

REFERANS OLUSTURMA (sag panelde tek akis - "Referans Olustur"):

  A, B, C olmak uzere UC nokta secilir (A ortak kose; AB ve AC iki
  referans kenari olur), bu iki kenarin GERCEK uzunluklari girilir.
  DORDUNCU KOSE (D) OTOMATIK olusturulur - elle isaretlenmez:

    - Fotografta AB ve AC yonlerinde, baska bir yerde GERCEKTEN gorunen
      birer paralel kenar ("Daha Yuksek Dogruluk" bolumunde) belirtilirse,
      D GERCEK kacis noktalarindan (tam projektif, perspektif dogru
      modellenerek) hesaplanir.
    - Belirtilmezse (bu bilgi olmadan D'nin gercek konumu matematiksel
      olarak TEK ve DOGRU sekilde belirlenemez), sistem sahte kesinlik
      uretmez: yaklasik (afin) sonuca ACIKCA belirterek doner ve durum
      mesajinda "Daha Yuksek Dogruluk" bolumunu doldurmanizi onerir.

  A'daki aci bilinmiyorsa 90 derece (dikdortgen) varsayilir; degilse
  gercek aciyi girebilirsiniz.

  Uc nokta secilir secilmez, uzunluklari HENUZ girmeseniz bile canli bir
  onizleme (turuncu-sari izgara) gorursunuz.

  Adimlar:
  1) A, B, C secin; AB ve AC uzunluklarini girin (D otomatik olusur).
  2) "Olcum Sorgulari" bolumune, referans yuzey uzerindeki (referans
     noktalarinin disinda olsa bile) uzunlugunu merak ettiginiz nokta
     ciftlerini ekleyin.
  3) "HESAPLA" -> sonuclar ve isaretli/izgarali gorsel gosterilir.

  (Eski afin/4-kose/N-nokta hesaplama yollari kod icinde regresyon
  testleri icin korunuyor ama kullanici arayuzunde gosterilmiyor.)

YARDIMCI CIZGILER (istege bagli, perspektifi iyilestirir):

  Yardimci cizgi, A-B veya A-C ile gercekte paralel olan baska bir
  kenardir. Fotografin farkli bir bolgesindeki uzun ve net bir kenar
  secmek perspektif hesabini iyilestirir. Kenar A/B/C ile AYNI yuzeyde
  olmali (zemin, yan duvar, balkon onu, pencere girintisi DEGIL).

  - Nokta ekledikten sonra kucuk bir pencere sorar: Hayir (Enter) /
    AB yonu / AC yonu / Otomatik / Yonu daha sonra belirle. Ardindan
    "Bu noktadan baslat" (nokta kenarin bir ucu olur) ya da "Baska
    kenar sec" (fotografin herhangi bir yerinde iki uc). Istemiyorsaniz
    arac cubugundaki "Noktadan sonra yardimci cizgi oner" kutusunu kapatin.
  - Yakalama sirasinda Esc ya da sag tik (surukleme olmadan) iptal eder.
  - "Kenara oturt" acikken cizgi gercek goruntu kenarina subpixel
    hassasiyetle oturtulur (dusuk kontrastli/belirsiz kenarda zorlanmaz).
  - Her yeni cizgi icin once/sonra karsilastirmasi gosterilir (yon
    belirsizligi, bagimsiz kalinti, uzamsal kapsama). Cizgi mevcut
    kanitla celisiyorsa model OTOMATIK degismez; Tut / Yonu degistir /
    Sil secersiniz.
  - "Daha Yuksek Dogruluk" listesinde tum yardimci cizgiler (eski
    nokta-cifti secimleri dahil) gorunur: sil, AB/AC yap, yon oner.

Not: Olcum, sorgu noktalarinin referans yuzeyle AYNI DUZLEMDE (es-
duzlemsel) oldugunu varsayar - farkli bir yuzeydeki (ornek: cati disina
cikan bir dormer) bir uzunluk icin o yuzeyin kendi referans
noktalariyla ayri bir olcum kurmaniz gerekir.

Diger ozellikler:
  - Fare tekerlegi: yakinlastir/uzaklastir (nokta secimini hassaslastirir)
  - Sag tik + surukle: goruntude gezinme
  - Kontrast kaydirici: sadece ekran gorunumu icin (kenarlari netlestirir)
  - Netlestirme: fotograf acildiginda sorulur, istendiginde ac/kapat

DOGRULUK ICIN IKI ONEMLI NOKTA (ozellikle genis/uzun bir yuzeyi TEK bir
kucuk referans koseden hesaplarken "farkli yerlerde farkli uzunluk cikmasi"
sikayetinin en sik iki nedeni):

  1) LENS DISTORSIYONU: telefonlarin genis acili (ör. 0.5x) lensleri, gercekte
     duz olan kenarlari fotografta hafifce kavisli gosterir - bu, homografinin
     dayandigi "duz cizgiler duz kalir" varsayimini bozar. Kaydiriciyi gozle
     ayarlamak yerine "Duz Kenar Modu"nu acip GERCEKTE DUZ olan bir kenar
     (ör. bir pencere sirasi, cati hatti) boyunca 3+ nokta tiklayip "Otomatik
     k Tahmin Et"e basin - k, o noktalari en duz hale getirecek sekilde
     hesaplanir. Bunu noktalari isaretlemeden ONCE yapip "Uygula (Kaydet)"
     ile kalici hale getirmeniz onerilir.

  2) EKSTRAPOLASYON: referans nokta(lar)iniz fotografin kucuk bir bolgesinde
     toplanmisken, olcmek istediginiz nokta o bolgeden UZAKTAYSA, kucuk bir
     tiklama/model hatasi bile orantisiz buyuyebilir (projektif/afin
     donusumlerin dogasi geregi). "HESAPLA" sonuclarinda bunun icin bir
     uyari gorursunuz ([!] ... uzakta). Cozum: referans nokta(lar)inizi,
     olcmek istediginiz alana MUMKUN OLDUGUNCA YAKIN/YAYILMIS secin - ör.
     uzak bir pencereyi olcuyorsaniz, o pencereye yakin (biliniyorsa kendi
     boyutuyla) ayri bir "Kayitli Duzlem" kurun, tek bir kucuk referansi
     tum fotograf icin kullanmak yerine.

Birim: Sag ust kosede metre/santimetre/milimetre/feet/inc secebilirsiniz;
tum girdiler ve sonuclar bu birimde gosterilir.

Bagimliliklar: pip install pillow numpy opencv-python
"""

import json
import math
import os
from dataclasses import dataclass, field
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext

import numpy as np
import cv2
from scipy.optimize import least_squares
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter, ImageEnhance

try:
    import pymupdf  # PDF destegi (pip install pymupdf)
except ImportError:
    pymupdf = None

MAX_CANVAS_W = 1000
MAX_CANVAS_H = 700

# PDF sayfasi goruntuye cevrilirken kullanilan cozunurluk: uzun kenar
# yaklasik PDF_TARGET_LONG_SIDE piksel olacak sekilde, PDF_MAX_DPI ile
# sinirli. Deterministik oldugu icin ayni PDF/sayfa her acilista ayni
# boyutta goruntu verir (config'teki piksel koordinatlari gecerli kalir).
PDF_TARGET_LONG_SIDE = 5000
PDF_MAX_DPI = 400

IMAGE_FILETYPES = [
    ("Gorseller ve PDF", "*.jpg *.jpeg *.png *.bmp *.webp *.pdf"),
    ("PDF", "*.pdf"),
    ("Gorseller", "*.jpg *.jpeg *.png *.bmp *.webp"),
    ("Tum dosyalar", "*.*"),
]


def render_pdf_page(path, page_index):
    """PDF'in verilen sayfasini (0 tabanli) RGB PIL goruntusune cevirir."""
    if pymupdf is None:
        raise RuntimeError("PDF destegi icin 'pymupdf' kurulu degil.\n"
                           "Kurmak icin: python -m pip install pymupdf")
    with pymupdf.open(path) as doc:
        page = doc[page_index]
        long_pt = max(page.rect.width, page.rect.height)
        zoom = min(PDF_TARGET_LONG_SIDE / long_pt, PDF_MAX_DPI / 72.0)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def pdf_page_count(path):
    if pymupdf is None:
        raise RuntimeError("PDF destegi icin 'pymupdf' kurulu degil.\n"
                           "Kurmak icin: python -m pip install pymupdf")
    with pymupdf.open(path) as doc:
        return doc.page_count

POINT_COLOR = (255, 140, 0)
EDGE_ROUGH_COLOR = (255, 60, 60)
EDGE_REFINED_COLOR = (60, 255, 255)
QUERY_COLOR = (34, 160, 34)
PLANE_COLOR = (255, 40, 40)
GRID_COLOR = (255, 215, 0)
PREVIEW_GRID_COLOR = (255, 170, 40)
LINE_CALIB_COLOR = (0, 200, 255)
LINE_CALIB_ACTIVE_COLOR = (255, 0, 220)
# Yardimci cizgiler KESIKLI cizilir (referans/sorgu/lens/kenar cizgileri
# duz cizilir) ve aileye gore renklenir.
HELPER_COLORS = {"ab": (40, 120, 255), "ac": (190, 80, 255), "auto": (190, 190, 190)}
HELPER_WARN_COLOR = (255, 60, 60)


def _draw_dashed_line(draw, p, q, fill, width=2, dash=10, gap=6):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    if L < 1e-6:
        return
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    t = 0.0
    while t < L:
        t2 = min(L, t + dash)
        draw.line([(p[0] + ux * t, p[1] + uy * t), (p[0] + ux * t2, p[1] + uy * t2)], fill=fill, width=width)
        t = t2 + gap

UNITS = {"m": 1.0, "cm": 0.01, "mm": 0.001, "ft": 0.3048, "inc": 0.0254}


def to_meters(value, unit):
    return value * UNITS[unit]


def from_meters(value_m, unit):
    return value_m / UNITS[unit]


def load_font(size):
    for name in ("arial.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def _normalize_points(pts):
    """Hartley normalizasyonu: agirlik merkezini orijine tasir, ortalama
    uzakligi sqrt(2) yapacak sekilde olcekler. DLT (dogrudan lineer
    donusum) ile homografi tahmininde sayisal kararliligi onemli olcude
    artirdigi bilinen standart bir on-isleme adimidir (Hartley, "In
    Defense of the Eight-Point Algorithm", 1997). BUNUN OLMADAN: piksel
    (yuzlerce/binlerce) ve metre (0-birkac) gibi COK FARKLI olcekteki
    koordinatlar dogrudan ayni SVD matrisine (A) girince matris kotu
    kosullanir (ill-conditioned) - kucuk tiklama/yuvarlama hatalari,
    ozellikle referans noktalarindan uzak sorgularda, orantisiz buyuk
    homografi hatasina donusebilir. Donen T, normalize noktalari geri
    orijinal olcege tasiyan 3x3 donusumdur (H = T_dst^-1 @ H_norm @ T_src)."""
    pts = np.asarray(pts, dtype=np.float64)
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    mean_dist = float(np.mean(np.hypot(centered[:, 0], centered[:, 1])))
    scale = (math.sqrt(2) / mean_dist) if mean_dist > 1e-12 else 1.0
    T = np.array([
        [scale, 0.0, -scale * centroid[0]],
        [0.0, scale, -scale * centroid[1]],
        [0.0, 0.0, 1.0],
    ])
    homog = np.hstack([pts, np.ones((pts.shape[0], 1))])
    normed = (T @ homog.T).T
    return normed[:, :2], T


def compute_homography(src_pts, dst_pts):
    """DLT ile homografi (n>=4 nokta; n==4 icin tam cozum, n>4 icin en
    kucuk kareler). Hartley normalizasyonu kullanilir (bkz.
    _normalize_points) - piksel/metre gibi cok farkli olcekli noktalarda
    dogrudan (normalizasyonsuz) SVD'ye gore belirgin sekilde daha
    kararli/dogru sonuc verir, ozellikle n>4 (en kucuk kareler) durumunda
    ya da referans noktalari fotografin sadece kucuk bir bolgesinde
    toplanmissa."""
    src = np.asarray(src_pts, dtype=np.float64)
    dst = np.asarray(dst_pts, dtype=np.float64)
    n = len(src)
    if n < 4:
        raise ValueError("Homografi icin en az 4 nokta gerekli.")

    src_n, T_src = _normalize_points(src)
    dst_n, T_dst = _normalize_points(dst)

    A = np.zeros((2 * n, 9))
    for i in range(n):
        x, y = src_n[i]
        u, v = dst_n[i]
        A[2 * i] = [x, y, 1, 0, 0, 0, -u * x, -u * y, -u]
        A[2 * i + 1] = [0, 0, 0, x, y, 1, -v * x, -v * y, -v]
    _, _, Vt = np.linalg.svd(A)
    H_n = Vt[-1].reshape(3, 3)

    H = np.linalg.inv(T_dst) @ H_n @ T_src
    if abs(H[2, 2]) < 1e-12:
        raise ValueError("Homografi hesaplanamadi (noktalar dogrusal/gecersiz olabilir).")
    return H / H[2, 2]


# ---------------------------------------------------------------------
# DOGRUDAN KISITLI HOMOGRAFI: nokta + kacis-yonu kisitlarini AYNI ANDA
# cozer (D ARA DEGISKENI OLMADAN).
#
# ESKI mimari: A,B,C -> kacis noktalari -> D (sentetik nokta) -> 4-nokta
# homografi. Sorun: D, VP'lerin KENDISINDEN turetiliyor - VP biraz
# yanlissa D yanlis olur, SONRA 4-noktali DLT bu yanlis D'yi sanki
# BAGIMSIZ dorduncu bir gozlemmis gibi kullanir. Bu "self-confirming"
# (kendi kendini dogrulayan) bir model kurar - D, H'nin kalitesi
# hakkinda HICBIR BAGIMSIZ bilgi tasimaz, cunku zaten H'yi kuracak ayni
# kanittan (VP) hesaplanmisti.
#
# YENI mimari: A,B,C (gercek nokta gozlemleri) VE V_AB,V_AC (kacis
# noktasi -> dunya YONU kisitlari) TEK bir asiri-belirlenmis (3 nokta x
# 2 denklem + 2 yon x 2 denklem = 10 denklem, 8 serbestlik derecesi)
# en-kucuk-kareler sisteminde BIRLIKTE cozulur. D, SADECE EN SONDA,
# H_final'den GERIYE turetilir (bkz. compute_global_homography) - bir
# GIRDI degil bir CIKTIdir.
# ---------------------------------------------------------------------

def _dlt_rows_full(p_hom, q_hom):
    """Genel homojen DLT aday satirlari - p (goruntu) ve q (dunya)
    HER IKISI de ya SONLU bir nokta (w=1) ya da bir YON/ideal nokta
    (w=0, ör. kacis noktasi sonsuzda VEYA dunya tarafinda saf bir yon
    kisiti) olabilir, ayni formul DEGISMEDEN calisir (capraz-carpim
    q x (Hp) = 0'in 3 bileseni). Bu 3 aday satirdan, p,q'nun sonlu/ideal
    olma durumuna gore HANGI 2'sinin bagimsiz oldugu DEGISIR (ör. q ideal
    -w=0- ise klasik (row1,row2) cifti BIRBIRINE ORANTILI/bagimli hale
    gelir, gercek ikinci kisit row3'tedir) - bu yuzden GUVENLI ve GENEL
    olmasi icin UCU DE eklenip SVD'nin dogal olarak bagimli/sifir
    satirlari yok saymasina birakiliyor (redundant bir satir null-space'i
    DEGISTIRMEZ, sadece zarasizca goz ardi edilir)."""
    p1, p2, p3 = p_hom
    q1, q2, q3 = q_hom
    return [
        [0.0, 0.0, 0.0, -q3 * p1, -q3 * p2, -q3 * p3, q2 * p1, q2 * p2, q2 * p3],
        [q3 * p1, q3 * p2, q3 * p3, 0.0, 0.0, 0.0, -q1 * p1, -q1 * p2, -q1 * p3],
        [-q2 * p1, -q2 * p2, -q2 * p3, q1 * p1, q1 * p2, q1 * p3, 0.0, 0.0, 0.0],
    ]


def compute_constrained_homography(point_pairs, direction_pairs):
    """A,B,C (+varsa GERCEK ek kontrol noktalari) VE V_AB/V_AC (kacis
    noktasi -> dunya yonu) kisitlarinin HEPSINI TEK bir en-kucuk-kareler
    SVD cozumunde BIRLIKTE kullanarak H'yi (goruntu->dunya) DOGRUDAN
    kurar - bkz. modul dokumantasyonu (D ARA DEGISKENI YOK).

    point_pairs: [(img_pt(x,y), world_pt(X,Y)), ...] - EN AZ 3 GERCEK
        nokta gozlemi (A,B,C; + varsa kamera-pozu adayi D ya da baska
        gercek kontrol noktalari).
    direction_pairs: [(img_hom(px,py,pw), world_dir(dx,dy)), ...] - pw=1
        ise goruntude SONLU bir kacis noktasi (px,py); pw=0 ise goruntude
        cizgiler zaten (neredeyse) PARALEL - kacis noktasi pratikte
        goruntude de sonsuzda (bkz. _direction_constraint_for_kind).

    Sistem KASITLI OLARAK asiri-belirlenmis: 3 nokta+2 yon = 10 denklem,
    8 serbestlik derecesi icin. TUM kanitlar AYNI ANDA agirliklandirilir -
    sadece 4 kisit secip digerlerini atan bir yaklasim DEGIL."""
    n_pts = len(point_pairs)
    n_dirs = len(direction_pairs)
    if n_pts < 3:
        raise ValueError("En az 3 gercek nokta eslesmesi (A,B,C) gerekli.")
    if n_pts + n_dirs < 4:
        raise ValueError("Toplam en az 4 kisit (nokta+yon) gerekli.")

    img_finite = np.array([p for p, _ in point_pairs], dtype=np.float64)
    world_finite = np.array([w for _, w in point_pairs], dtype=np.float64)
    _, T_img = _normalize_points(img_finite)
    _, T_world = _normalize_points(world_finite)

    rows = []
    for (x, y), (X, Y) in point_pairs:
        pv = T_img @ np.array([x, y, 1.0])
        qv = T_world @ np.array([X, Y, 1.0])
        r = _dlt_rows_full(tuple(pv), tuple(qv))
        rows.append(r[0])
        rows.append(r[1])  # sadece standart 2 satir (compute_homography ile AYNI denklemler - dogrulandi)

    for p_hom, (dx, dy) in direction_pairs:
        # AYNI (nokta kumesinden hesaplanan, SABIT) T_img/T_world
        # donusumleri kacis noktasina/yonune de uygulanir - boylece TUM
        # sistem AYNI normalize koordinat cercevesinde kurulur. p_hom'un
        # 3. bileseni (pw) 0 ya da 1 olabilir - T_img homojen carpimi
        # HER IKI durumda da doğru calisir (pw=0 ise oteleme etkisiz
        # kalir, SADECE olceklenir - bir YONUN oteleme altinda degismemesi
        # gerektigi icin bu MATEMATIKSEL OLARAK dogru davranistir).
        pv = T_img @ np.array(p_hom)
        qv = T_world @ np.array([dx, dy, 0.0])
        norm_q = math.hypot(qv[0], qv[1])
        if norm_q < 1e-12:
            continue
        qv = (qv[0] / norm_q, qv[1] / norm_q, 0.0)
        rows.extend(_dlt_rows_full(tuple(pv), qv))  # HER UCU de ekle - bkz. _dlt_rows_full notu

    Amat = np.array(rows, dtype=np.float64)
    _, _, Vt = np.linalg.svd(Amat)
    H_n = Vt[-1].reshape(3, 3)
    H = np.linalg.inv(T_world) @ H_n @ T_img
    if abs(H[2, 2]) < 1e-12:
        raise ValueError("Kisitli homografi hesaplanamadi (kisitlar dejenere/tutarsiz olabilir).")
    return H / H[2, 2]


def _direction_constraint_for_kind(kind, vp, A, B):
    """(kind, vp) -> goruntu tarafi homojen temsil (px,py,pw).

    Kacis noktasi SONLU ise (finite_strong/finite_weak): kendisi (pw=1).
    "near_infinity" ise (goruntude bu yondeki cizgiler ZATEN neredeyse
    paralel - sayisal olarak kanitlanmis): kacis noktasinin KENDI PIKSEL
    KONUMU degil, referans cizgisinin (A->B) GORUNTUDEKI YONU kullanilir
    (pw=0, ideal/sonsuzdaki bir goruntu noktasi) - cunku bu durumda en iyi
    kanit, cizgilerin fiilen hangi acida goruldugudur, uydurma bir
    'sonsuzdaki piksel konumu' degil.
    "invalid"/"None" ise: bu yon icin HICBIR kisit eklenemez (None doner)."""
    if kind in _FINITE_KINDS and vp is not None:
        return (vp[0], vp[1], 1.0)
    if kind == "near_infinity":
        return (B[0] - A[0], B[1] - A[1], 0.0)
    return None


def apply_transform(H, point):
    v = H @ np.array([point[0], point[1], 1.0])
    if abs(v[2]) < 1e-12:
        raise ValueError("Donusum gecersiz (sonsuzdaki nokta).")
    return float(v[0] / v[2]), float(v[1] / v[2])


def fit_affine(src_pts, dst_pts):
    """3 (tam cozum) veya daha fazla (en kucuk kareler) nokta ciftinden
    afin donusum (6 serbestlik derecesi: donme+olcek+kayma+oteleme,
    ACI KORUNUMU VARSAYIMI YOK) fit eder. Homografiden farkli olarak
    perspektif (kacis noktasi) yakalayamaz - dogrular paralel kalir."""
    src = np.asarray(src_pts, dtype=np.float64)
    dst = np.asarray(dst_pts, dtype=np.float64)
    n = len(src)
    A = np.zeros((2 * n, 6))
    b = np.zeros(2 * n)
    for i in range(n):
        x, y = src[i]
        u, v = dst[i]
        A[2 * i] = [x, y, 1, 0, 0, 0]
        A[2 * i + 1] = [0, 0, 0, x, y, 1]
        b[2 * i] = u
        b[2 * i + 1] = v
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    a, bb, c, d, e, f = sol
    return np.array([[a, bb, c], [d, e, f], [0.0, 0.0, 1.0]])


# --------------------------------------------------------------------------
# Nokta kaynagi / piksel belirsizligi. Her nokta NASIL yerlestirildiyse
# (kaba tiklama, buyutecli hassas tiklama, subpixel kenar hizalama...) o
# kadar farkli bir konum belirsizligine sahiptir - Monte Carlo tabanli
# olcum belirsizligi (bkz. monte_carlo_uncertainty) bunu KULLANIR. Bu
# degerler kesin fiziksel gercekler degil, baslangic varsayimlaridir -
# gerekirse degistirin.
# --------------------------------------------------------------------------
POINT_SOURCE_SIGMA_PX = {
    "manual": 1.0,             # dogrudan tek tiklama
    "manual_magnifier": 0.5,   # buyutecli, yon oklariyla hassaslastirilmis tiklama
    "subpixel_edge": 0.25,     # Sobel gradyan + parabolik pik ile kenar hizalama
    "line_intersection": 0.2,  # iki TLS-fit dogrunun kesisimi (bkz. Bolum 8)
    # D noktasi gercek bir tiklama DEGIL - A,B,C VE yardimci cizgi
    # noktalarinin kacis-noktasi kesisiminden TUREYEN sentetik bir
    # konumdur. Bu noktalarin gurultusu VP kesisiminde GENELDE
    # BUYUTULEREK yansir (bkz. Monte Carlo testleri - D hatasi, girdi
    # nokta gurultusunden buyuk cikabiliyor). Kesin bir hata yayilim
    # turevi yerine, TEK bir noktaya (D) gore muhafazakar/buyutulmus bir
    # sigma kullaniyoruz - bu bir YAKLASIKLIKTIR, D'nin GERCEK
    # belirsizligi A,B,C VE yardimci cizginin BIRLESIK belirsizliginden
    # gelir (bkz. Bolum 14 notu, gelecekteki dogru hata yayilimi icin).
    "derived_projective": 2.0,
}
DEFAULT_POINT_SIGMA_PX = 1.0


def point_sigma_px(source):
    """Bir noktanin KAYNAGINA (source alani) gore varsayilan piksel
    belirsizligini (1-sigma, Gauss) doner. Bilinmeyen/eksik source icin
    en muhafazakar (en buyuk) varsayilan olan 'manual' degerine duser."""
    return POINT_SOURCE_SIGMA_PX.get(source, DEFAULT_POINT_SIGMA_PX)


# --------------------------------------------------------------------------
# Homografi/afin KOSULLULUK (conditioning) olcumu. MIN_TRIANGLE_ANGLE_DEG
# ve MIN_VANISHING_ANGLE_DEG gibi sabit acisal esikler kaba, hizli bir
# on-kontrol saglar ama referans noktalarinin GERCEKTE ne kadar "iyi
# yerlestirilmis" oldugunu olcmez. Bunun yerine, DLT/afin en-kucuk-kareler
# sisteminin (Hartley-normalize edilmis A matrisi) tekil deger ayrisimindan
# STANDART matris KOSUL SAYISINI (en buyuk/en kucuk tekil deger orani)
# kullaniyoruz - kucuk tiklama hatalarinin cozume ne kadar buyutulerek
# yansiyacagini dogrudan olcen, klasik bir sayisal analiz metrigidir.
#
# ESIKLER, ASAGIDAKI SENTETIK KALIBRASYONLA belirlendi (bkz. proje
# gecmisindeki calibrate_condition3.py): gercek bir kamera projeksiyonuyla
# uretilmis, KARE-BENZERI referanslar (buyuk ya da kucuk, ama makul en/boy
# oraninda) kosul sayisi ~3-19 veriyor; ince bir serit (0.15x0.02 m gibi
# asiri uzun/dar) ~19; NEREDEYSE DOGRUSAL (dejenere) 4 nokta ise ~12000-
# 29000 - yani "iyi" ve "dejenere" arasinda ÇOK BUYUK bir bosluk var ve
# esikler bu bosluga yerlestirildi (keyfi degil, olculmus).
# --------------------------------------------------------------------------
CONDITION_EXCELLENT_MAX = 15.0
CONDITION_GOOD_MAX = 50.0
CONDITION_WEAK_MAX = 300.0


def homography_condition_number(img_pts, world_pts):
    """4+ nokta homografisi icin, Hartley-normalize DLT matrisinin
    (2n x 9) STANDART kosul sayisi (sigma_max/sigma_min). Referans
    noktalari neredeyse dogrusalsa ya da cok carpik bir sekil olusturuyorsa
    bu sayi hizla buyur - kucuk tiklama hatalarinin homografiye ne kadar
    orantisiz yansiyacaginin dogrudan bir olcusudur."""
    src = np.asarray(img_pts, dtype=np.float64)
    dst = np.asarray(world_pts, dtype=np.float64)
    n = len(src)
    if n < 4:
        return None
    src_n, _ = _normalize_points(src)
    dst_n, _ = _normalize_points(dst)
    A = np.zeros((2 * n, 9))
    for i in range(n):
        x, y = src_n[i]
        u, v = dst_n[i]
        A[2 * i] = [x, y, 1, 0, 0, 0, -u * x, -u * y, -u]
        A[2 * i + 1] = [0, 0, 0, x, y, 1, -v * x, -v * y, -v]
    s = np.linalg.svd(A, compute_uv=False)
    if s[-1] < 1e-14:
        return float("inf")
    return float(s[0] / s[-1])


def affine_condition_number(img_pts, world_pts):
    """3+ nokta afin fit'i icin ayni fikrin afin karsiligi (fit_affine'in
    kendi en-kucuk-kareler A matrisinin kosul sayisi). Noktalar neredeyse
    ayni dogru uzerindeyse (bkz. MIN_TRIANGLE_ANGLE_DEG kontrolu) bu sayi
    hizla buyur."""
    src = np.asarray(img_pts, dtype=np.float64)
    n = len(src)
    if n < 3:
        return None
    A = np.zeros((2 * n, 6))
    for i in range(n):
        x, y = src[i]
        A[2 * i] = [x, y, 1, 0, 0, 0]
        A[2 * i + 1] = [0, 0, 0, x, y, 1]
    s = np.linalg.svd(A, compute_uv=False)
    if s[-1] < 1e-14:
        return float("inf")
    return float(s[0] / s[-1])


def classify_condition_quality(condition_number):
    """Kosul sayisini (bkz. yukaridaki kalibrasyon notu) 4 seviyeli,
    olculebilir bir kalite etiketine cevirir."""
    if condition_number is None:
        return "N/A"
    if condition_number <= CONDITION_EXCELLENT_MAX:
        return "Mukemmel"
    if condition_number <= CONDITION_GOOD_MAX:
        return "Iyi"
    if condition_number <= CONDITION_WEAK_MAX:
        return "Zayif"
    return "Kararsiz"


def loocv_reprojection_stats(img_pts, world_pts, is_affine):
    """Leave-One-Out Cross Validation: N>=5 (homografi) ya da N>=4 (afin)
    referans noktasi varsa, HER noktayi sirayla DISARIDA birakip kalan
    noktalarla modeli yeniden kurar, cikarilan noktayi tahmin eder ve
    GERCEK (girilen) konumuyla karsilastirir. ONEMLI: 4 noktalik tam
    homografi ya da 3 noktalik tam afin fit'in kendi noktalarindaki hatasi
    HER ZAMAN ~0'dir (model o noktalara TAM oturacak sekilde kurulur) -
    bu, modelin GORULMEMIS noktalarda da dogru calisacagini KANITLAMAZ.
    LOOCV, her noktayi sirayla 'gorulmemis' varsayarak daha durust bir
    dogruluk tahmini verir. Doner: dict(rmse, median, max, per_point) ya
    da yetersiz nokta sayisinda None."""
    src = np.asarray(img_pts, dtype=np.float64)
    dst = np.asarray(world_pts, dtype=np.float64)
    n = len(src)
    min_n = 4 if is_affine else 5
    if n < min_n:
        return None
    errors = []
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        try:
            if is_affine:
                H_loo = fit_affine(src[mask], dst[mask])
            else:
                H_loo = compute_homography(src[mask], dst[mask])
            est = apply_transform(H_loo, src[i])
        except (ValueError, np.linalg.LinAlgError):
            continue
        errors.append(float(np.hypot(est[0] - dst[i][0], est[1] - dst[i][1])))
    if not errors:
        return None
    errors = np.array(errors)
    return {
        "rmse": float(np.sqrt(np.mean(errors ** 2))),
        "median": float(np.median(errors)),
        "max": float(np.max(errors)),
        "n": len(errors),
    }


def monte_carlo_uncertainty(img_pts, world_pts, query_img_pts, is_affine,
                             point_sigmas_px=None, n_iter=400, seed=None):
    """Referans (ve sorgu) noktalarini, KAYNAKLARINA gore Gauss gurultuyle
    (bkz. point_sigma_px) tekrar tekrar (Monte Carlo) perturbe edip
    homografi/afini YENIDEN kurarak, sorgu mesafesinin olasi DAGILIMINI
    kestirir. Bu, tek bir sayi (ör. '2.341 m') yerine, o sayinin ne kadar
    GUVENILIR oldugunu (tiklama/kalibrasyon hassasiyeti verildiginde) da
    gosterir. Doner: dict(mean, std, ci95_low, ci95_high, n_success) ya
    da tum denemeler basarisiz olursa None.

    query_img_pts: [(A,B)] ya da [(A,B,C)] (kirikli/koseli olcum) formunda
    tek bir sorgu icin piksel nokta listesi.
    point_sigmas_px: img_pts ile AYNI uzunlukta, her referans noktasi icin
    1-sigma piksel belirsizligi listesi (bkz. point_sigma_px)."""
    src = np.asarray(img_pts, dtype=np.float64)
    dst = np.asarray(world_pts, dtype=np.float64)
    n = len(src)
    if point_sigmas_px is None:
        point_sigmas_px = [DEFAULT_POINT_SIGMA_PX] * n
    rng = np.random.default_rng(seed)
    results = []
    for _ in range(n_iter):
        noise = rng.normal(0.0, 1.0, size=(n, 2)) * np.array(point_sigmas_px).reshape(-1, 1)
        src_noisy = src + noise
        try:
            H_mc = fit_affine(src_noisy, dst) if is_affine else compute_homography(src_noisy, dst)
            pts_w = [apply_transform(H_mc, p) for p in query_img_pts]
        except (ValueError, np.linalg.LinAlgError):
            continue
        if len(pts_w) == 3:
            length = dist(pts_w[0], pts_w[1]) + dist(pts_w[1], pts_w[2])
        else:
            length = dist(pts_w[0], pts_w[1])
        results.append(length)
    if not results:
        return None
    arr = np.array(results)
    return {
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "ci95_low": float(np.percentile(arr, 2.5)),
        "ci95_high": float(np.percentile(arr, 97.5)),
        "n_success": len(arr),
        "n_total": n_iter,
    }


def _convex_hull_2d(points):
    """Monotone chain (Andrew) algoritmasiyla 2B dis-bukey govde (convex
    hull) - saf numpy, harici bagimlilik gerektirmez. Nokta listesini,
    hull'un cevresi boyunca SIRALI donerek verir."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _point_in_polygon(pt, poly):
    """Ray-casting: pt, poly (sirali kose listesi) icinde mi?"""
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-15) + x1):
            inside = not inside
    return inside


def _dist_point_to_polygon(pt, poly):
    """pt'nin poly kenarlarina olan en kisa (Oklid) mesafesi."""
    pt = np.asarray(pt, dtype=np.float64)
    best = float("inf")
    n = len(poly)
    for i in range(n):
        p1 = np.asarray(poly[i], dtype=np.float64)
        p2 = np.asarray(poly[(i + 1) % n], dtype=np.float64)
        seg = p2 - p1
        seg_len2 = seg @ seg
        if seg_len2 < 1e-9:
            d = np.linalg.norm(pt - p1)
        else:
            t = np.clip(((pt - p1) @ seg) / seg_len2, 0.0, 1.0)
            proj = p1 + t * seg
            d = float(np.linalg.norm(pt - proj))
        best = min(best, d)
    return best


def _polygon_area(poly):
    n = len(poly)
    a = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


def reference_coverage_report(ref_img_pts, query_img_pts):
    """extrapolation_ratio'nun (bounding-box tabanli, halen korunuyor)
    tamamlayicisi: referans noktalarinin CONVEX HULL'unu kullanarak sorgu
    noktalarinin bu bolgenin GERCEKTEN icinde mi (interpolasyon - en
    guvenilir durum) yoksa disinda mi (ekstrapolasyon) oldugunu, ve ne
    kadar disinda oldugunu (hull kenarina goreli uzaklik) hesaplar.
    Bounding-box'tan farkli olarak, ucgen/dortgen olmayan (ör. L-seklinde
    yayilmis) referans noktalarinda kose bosluklarini yanlislikla
    'iceride' saymaz. Doner: (durum, goreli_mesafe) - durum:
    'interpolasyon' / 'hafif ekstrapolasyon' / 'guclu ekstrapolasyon'."""
    ref = [tuple(p) for p in ref_img_pts]
    if len(ref) < 3:
        return extrapolation_ratio(ref_img_pts, query_img_pts), None
    hull = _convex_hull_2d(ref)
    if len(hull) < 3:
        return extrapolation_ratio(ref_img_pts, query_img_pts), None
    area = _polygon_area(hull)
    span = math.sqrt(max(area, 1e-6))

    def dist_outside(pt):
        return 0.0 if _point_in_polygon(pt, hull) else _dist_point_to_polygon(pt, hull)

    max_d = max(dist_outside(p) for p in query_img_pts)
    rel = max_d / max(span, 1e-6)
    if rel <= 1e-9:
        durum = "interpolasyon"
    elif rel <= 0.5:
        durum = "hafif ekstrapolasyon"
    else:
        durum = "guclu ekstrapolasyon"
    return durum, rel


def triangle_from_sides(d12, d23, d13):
    """3 kenar uzunlugundan (SSS - Side-Side-Side), HICBIR ACI VARSAYIMI
    OLMADAN, ucgenin dunya koordinatlarini kurar: P1=(0,0), P2=(d12,0),
    P3=(x,y). Bu, dikdortgen/90-derece varsayimina hic ihtiyac
    duymadan, sadece 3 gercek uzunluk olcumunden tam bir referans
    cercevesi kurmayi saglar (kosinus teoremi)."""
    if d12 <= 0:
        raise ValueError("1-2 uzunlugu pozitif olmali.")
    x3 = (d13 ** 2 + d12 ** 2 - d23 ** 2) / (2 * d12)
    y3_sq = d13 ** 2 - x3 ** 2
    if y3_sq <= 0:
        raise ValueError("Bu 3 uzunluk gecerli bir ucgen olusturmuyor "
                          "(ucgen esitsizligini kontrol edin).")
    y3 = math.sqrt(y3_sq)
    return [(0.0, 0.0), (float(d12), 0.0), (float(x3), float(y3))]


def _line_through(p, q):
    return np.cross(np.array([p[0], p[1], 1.0]), np.array([q[0], q[1], 1.0]))


def _intersect_lines(l1, l2):
    pt = np.cross(l1, l2)
    if abs(pt[2]) < 1e-9:
        return None  # cizgiler goruntude paralel -> kacis noktasi sonsuzda
    return (pt[0] / pt[2], pt[1] / pt[2])


def _angle_between_dirs(v1, v2):
    """Iki DOGRUNUN (yonsuz) goruntudeki acisal farkini derece cinsinden
    doner (0-90 derece)."""
    a = math.atan2(v1[1], v1[0])
    b = math.atan2(v2[1], v2[0])
    d = abs(a - b)
    if d > math.pi:
        d = 2 * math.pi - d
    if d > math.pi / 2:
        d = math.pi - d
    return math.degrees(d)


def _angular_residual_deg(p, q, vp):
    """Bir (p,q) cizgi parcasinin GERCEK yonu ile, parcanin ORTA
    NOKTASINDAN aday kacis noktasina (vp) giden yon arasindaki farki
    (derece, 0-90 arasi) hesaplar.

    ONEMLI - NEDEN PIKSEL MESAFESI DEGIL ACI: bir kacis noktasi COK UZAKTA
    olabilir (zayif perspektif - bu SIK karsilasilan, gecerli bir durum).
    'residual = |a*vx+b*vy+c|' (dogruya OLAN PIKSEL uzakligi) kullanan
    eski kriter, sabit bir piksel toleransiyla karsilastirildiginda,
    mesafe * sin(aci_hatasi) seklinde OLCEKLENIR - yani VP ne kadar
    uzaktaysa, GERCEK dunyada dogru olan ama elle tiklamadan kaynaklanan
    KUCUCUK (alt-derece) bir aci sapmasi bile ORANTISIZ BUYUK bir kalinti
    uretir. Bu, bu oturumda sentetik "click noise" testiyle SOMUT olarak
    dogrulanan GERCEK bir bug: referans noktalarina SADECE 0.5 piksellik
    Gauss gurultusu eklendiginde bile, tum otomatik kacis noktasi
    pipeline'i (RANSAC dahil) referans cizgisinin KENDISINI 'aykiri deger'
    sayip reddediyor ve sessizce afin moda duşuyordu - sentetik, sifir
    gurultulu testler bunu MASKELEMISTI. Aci-tabanli kriter OLCEK-
    BAGIMSIZDIR (VP ne kadar uzakta olursa olsun ayni kalir) ve gercekci
    tiklama gurultusune karsi dayanikli - bkz. VP_RANSAC_ANGLE_TOL_DEG ve
    tests/test_click_noise_robustness.py."""
    mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
    seg_dir = (q[0] - p[0], q[1] - p[1])
    to_vp_dir = (vp[0] - mx, vp[1] - my)
    return _angle_between_dirs(seg_dir, to_vp_dir)


def _angular_residual_to_vp_hom(p, q, vp_hom, eps=1e-9):
    """_angular_residual_deg'in HOMOJEN genellemesi (Bolum 4/19/39): aday
    kacis noktasi vp_hom=(vx,vy,vz) SONLU (|vz| yeterince buyuk) ise
    Oklid'e cevrilip _angular_residual_deg ile AYNI hesap yapilir; ANCAK
    |vz|~0 ise (kacis noktasi TAM SONSUZDA - GECERLI bir durum, ozel-
    durum/hata DEGIL), (vx,vy) DOGRUDAN bir YON olarak kullanilir - cunku
    sonsuzdaki bir nokta zaten SADECE bir yon temsil eder, ve o yone
    'giden' cizginin KENDI acisi budur (herhangi bir 'orta nokta -> nokta'
    vektoru hesaplamaya GEREK YOK, cunku sonsuzda TUM boyle vektorler
    zaten AYNI yone yakinsar). Bu ayrim, near-infinite bir VP'yi ASLA
    devasa/sayisal olarak kararsiz bir Oklid koordinatina ZORLAMADAN
    calismayi saglar."""
    vx, vy, vz = vp_hom
    if abs(vz) > eps:
        return _angular_residual_deg(p, q, (vx / vz, vy / vz))
    seg_ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
    inf_ang = math.degrees(math.atan2(vy, vx))
    diff = abs(seg_ang - inf_ang) % 180.0
    return 180.0 - diff if diff > 90.0 else diff


MIN_VANISHING_ANGLE_DEG = 4.0
MIN_TRIANGLE_ANGLE_DEG = 8.0


def _orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_intersect(p1, p2, p3, p4):
    """p1-p2 dogru parcasi ile p3-p4 dogru parcasi kesisiyor mu?"""
    d1 = _orient(p3, p4, p1)
    d2 = _orient(p3, p4, p2)
    d3 = _orient(p1, p2, p3)
    d4 = _orient(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def quad_is_self_intersecting(p1, p2, p3, p4):
    """4 kosenin 1->2->3->4 sirasiyla GECERLI (kendi kendini kesmeyen)
    bir dortgen olusturup olusturmadigini kontrol eder. Kullanici
    koseleri yanlis sirada (ör. kosegen atlayarak) tiklarsa, "Genislik"
    ve "Yukseklik" artik gercek kenarlara degil kosegenlere karsilik
    gelir ve sonuc anlamsizlasir - bu, boyle bir "kelebek" sekli
    tespit eder."""
    return _segments_intersect(p1, p2, p3, p4) or _segments_intersect(p2, p3, p4, p1)


def triangle_min_angle_deg(p1, p2, p3):
    """Ucgenin (fotografta tiklanan 3 nokta) en kucuk ic acisi. Bu aci
    cok kucukse (noktalar neredeyse ayni dogru uzerinde), afin fit
    sayisal olarak COK KARARSIZ hale gelir - kucuk bir tiklama hatasi
    bile sonucu tamamen degistirebilir. Bu, kacis noktasi yontemindeki
    'neredeyse paralel kenar' guvenlik kontrolunun ucgen icin karsiligidir."""
    def angle_at(a, b, c):
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - a[0], c[1] - a[1])
        n1, n2 = math.hypot(*v1), math.hypot(*v2)
        if n1 < 1e-9 or n2 < 1e-9:
            return 0.0
        cos_a = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        return math.degrees(math.acos(cos_a))

    a1 = angle_at(p1, p2, p3)
    a2 = angle_at(p2, p1, p3)
    a3 = 180.0 - a1 - a2
    return min(a1, a2, a3)


MIN_HELPER_LINE_ANGLE_DEG = 3.0   # geriye-donuk uyumluluk icin tutuluyor (artik SADECE bilgi amacli)

# Dereceli kacis noktasi guven siniflandirmasi icin esikler. Eskiden TEK bir
# aci esigiyle ("< 3 derece ise sonsuzda") ikili (parallel/finite) karar
# veriliyordu - bu KABA bir kisayoldu: iki cizgi goruntude 2 derece farkli
# gorunuyor diye kacis noktasi GERCEKTEN sonsuzda olmak ZORUNDA degildir,
# sadece COK UZAKTA olabilir. Simdi GERCEK homojen kesisimi (SVD null
# vektoru) hesaplayip, kacis noktasinin REFERANS OLCEGINE GORE ne kadar
# uzakta oldugunu (dist_ratio - OLCEK-BAGIMSIZ bir oran) dogrudan olcuyoruz.
# (NOT: kesisimin ham 'sonsuzluk bileseni' pz, piksel koordinatlarinin
# buyuklugune bagli OLCEK-BAGIMLI bir degerdir - sabit bir esikle
# karsilastirmak yanlis olceklendirme hatasina yol acar; bu yuzden pz
# SADECE tam/neredeyse-tam sifir oldugu - Oklid donusumunun sayisal olarak
# imkansiz oldugu - ozel durumda kullanilir, ana kriter dist_ratio'dur.)
VP_MAX_DIST_RATIO = 100.0    # vp, referans olceginin bu kadar (kati) uzagindaysa "sonsuzda" sayilir
VP_STRONG_SINGULAR_RATIO = 0.3  # (3+ cizgi) en kucuk iki tekil deger orani bunun altindaysa "finite_strong"


def _svd_line_intersection(lines):
    """Birden fazla (homojen, (a,b,c) formunda) dogrunun, EN KUCUK KARELER
    anlaminda ORTAK kesisimini SVD ile bulur ve HAM HOMOJEN 3-vektoru
    (p_hom) dondurur - Oklid'e ZORLA CEVRİLMEZ. p_hom[2] (pz) sifira
    YAKINSA bu GECERLI bir sonuctur (kesisim tam SONSUZDADIR - GERCEKTEN
    paralel bir dogru ailesi icin BEKLENEN, dogru sonuc) - None DONMEZ;
    cagiran taraf pz'yi KENDI ihtiyacina gore yorumlar (bkz. Bolum 4/19:
    'near_infinity -> None' YANLIS bir tasarimdir, sonsuzdaki bir nokta
    da GECERLI bir projektif nesnedir).

    Her dogru ONCE (a,b) bileseni birim-norm olacak sekilde normalize
    edilir (homojen dogru normalizasyonu) - boylece farkli olcekte/farkli
    sayida temsil edilen dogrular SVD'de esit agirlikla degerlendirilir.

    Doner: (p_hom (3,) ndarray ya da None, singular_ratio ya da None).
    singular_ratio (sadece n>=3 dogru icin) en kucuk iki tekil degerin
    orani (kucukse cozum daha 'net/tekil', yani daha guvenilir)."""
    L = np.array(lines, dtype=np.float64)
    if len(L) < 2:
        return None, None
    norms = np.linalg.norm(L[:, :2], axis=1, keepdims=True)
    if np.any(norms < 1e-12):
        return None, None
    L = L / norms
    s, Vt = np.linalg.svd(L, full_matrices=True)[1:]
    p_hom = Vt[-1]
    singular_ratio = None
    if len(L) >= 3 and len(s) >= 2:
        singular_ratio = float(s[-1] / s[-2]) if s[-2] > 1e-14 else 0.0
    return p_hom, singular_ratio


def _vanishing_point_from_lines(lines, return_diagnostics=False):
    """Birden fazla (homojen, (a,b,c) formunda) dogrudan, EN KUCUK KARELER
    anlaminda ORTAK kesisim noktasini SVD ile bulur (bkz. _svd_line_
    intersection - bu fonksiyon onun Oklid-donusumlu SARMALAYICISIDIR,
    ESKI/mevcut cagiran kodla TAM geriye-uyumluluk icin korunmustur).

    2 dogru icin klasik iki-dogru kesisimiyle ozdestir; 3+ dogru icin ise
    tek bir (gurultulu olabilecek) yardimci cizgiye bagimli kalmak yerine,
    TUM mevcut kanitlari birlikte kullanarak tiklama hatasina karsi COK
    daha dayanikli bir tahmin verir - single-view metrology literaturunde
    (Criminisi ve ark., 2000) standart yontemdir.

    return_diagnostics=True ise (vp_euclidean_or_None, pz, singular_ratio)
    doner - pz kacis noktasinin 'sonsuzluk bileseni' (kucukse nokta cok
    uzakta), singular_ratio (sadece n>=3 dogru icin, yoksa None) en kucuk
    iki tekil degerin orani (kucukse cozum daha 'net/tekil', yani daha
    guvenilir)."""
    p_hom, singular_ratio = _svd_line_intersection(lines)
    if p_hom is None:
        return (None, None, None) if return_diagnostics else None
    pz = float(p_hom[2])
    if abs(pz) < 1e-12:
        vp = None
    else:
        vp = (p_hom[0] / pz, p_hom[1] / pz)
    if return_diagnostics:
        return vp, pz, singular_ratio
    return vp


def _resolve_vanishing_point(A, B, helper, extra_lines=None, ref_scale=None, auto_lines=None):
    """A-B yonu icin, helper=(P,Q) yardimci cizgisinden (ve varsa extra_lines'tan)
    bir kacis noktasi kestirir ve GERCEK sayisal kanitlarla (aci esigi
    DEGIL) 4 seviyeli bir guven sinifina ayirir:

      "finite_strong": 3+ cizgi (referans+yardimci+ekstralar) var VE
          bunlarin SVD tekil deger orani kucuk (cozum net/tekil - cizgiler
          gercekten tutarli bir noktada birlesiyor). D hesaplamak ve grid'i
          TUM fotografa yaymak icin guvenilir.
      "finite_weak": sonlu bir kacis noktasi bulundu ama ya sadece 2 cizgi
          var (kendi kendini dogrulayamaz) ya da 3+ cizginin tekil deger
          orani yuksek (cizgiler birbiriyle tam tutarli degil). Kullanilir
          ama dusuk guvenle isaretlenir.
      "near_infinity": kesisimin 'sonsuzluk bileseni' (pz) cok kucuk YA DA
          bulunan nokta referanstan asiri uzakta - bu, o yonde kacis
          noktasinin PRATIKTE sonsuzda oldugunun (kameranin bu yonde onemli
          bir egimi olmadiginin) sayisal kanitidir (bir aci esigi degil).
      "invalid": yardimci cizgi yok, ya da kesisim hesaplanamiyor (dejenere,
          ör. tum cizgiler tam paralel/cakisik).

    auto_lines: (opsiyonel) fotograftan OTOMATIK tespit edilmis (detect_
    line_segments), henuz DOGRULANMAMIS aday (p,q) cizgi ciftleri. Bunlar
    dogrudan guvenilmez - RANSAC ile, GUVENILIR (referans+yardimci+extra)
    cizgilerin ZATEN belirledigi kacis noktasiyla TUTARLI olanlari
    (inlier'lar) secilip, SADECE onlar nihai tahmine katilir. Boylece
    kullanici manuel yardimci cizgi vermese bile (Bolum 46: basit akis),
    sistem fotografin kendisinden GERCEK ek kanit bulup TAM PROJEKTIF
    cozume ulasma sansini artirir - kullanicidan ekstra tiklama istemeden.

    Doner: (kind, vp_or_None)."""
    user_verified = helper is not None
    trusted_segments = [(A, B)]
    if user_verified:
        trusted_segments.append((helper[0], helper[1]))
        for p, q in (extra_lines or []):
            trusted_segments.append((p, q))

    if not user_verified and not auto_lines:
        return "invalid", None  # ne yardimci cizgi ne otomatik kanit - hicbir sey bilinmiyor

    if ref_scale is None or ref_scale < 1e-6:
        ref_scale = math.hypot(B[0] - A[0], B[1] - A[1]) or 1.0

    segments = trusted_segments
    auto_capped_confidence = False
    if auto_lines:
        all_segments = trusted_segments + list(auto_lines)
        vp_ransac, inlier_idx = _ransac_vanishing_point(all_segments)
        if vp_ransac is not None:
            n_trusted_inliers = sum(1 for i in inlier_idx if i < len(trusted_segments))
            n_auto_inliers = len(inlier_idx) - n_trusted_inliers
            if user_verified:
                # GUVENLIK: otomatik tespit edilen cizgiler TEK BASINA bir VP
                # dayatamaz - kesisimin en az 2 GUVENILIR (kullanici
                # kaynakli) cizgiyle tutarli cikmasi SART (aksi halde,
                # fotografta rastgele baska bir yondeki guclu bir cizgi
                # kumesi, YANLIS bir kacis noktasini "dogrulanmis" gibi
                # gosterebilirdi).
                if n_trusted_inliers >= min(2, len(trusted_segments)):
                    segments = [all_segments[i] for i in inlier_idx]
            else:
                # HIC kullanici yardimci cizgisi/dogrulamasi YOK (Bolum 46:
                # tam otomatik akis). Bu durumda TEK BASINA referans
                # kenarina (1 cizgi) guvenemeyiz - en az 3 BAGIMSIZ otomatik
                # cizginin AYNI noktada birlestigini GORMEMIZ gerekir. Bu
                # da bulunsa bile, sonuc INSAN TARAFINDAN DOGRULANMAMIS
                # oldugu icin en fazla "finite_weak" olarak isaretlenir
                # (asla "finite_strong" - grid'i tum fotografa yaymak icin
                # kullanilan en yuksek guven, hep en az bir GERCEK kullanici
                # dogrulamasi gerektirir).
                if n_auto_inliers >= 3 and n_trusted_inliers >= 1:
                    segments = [all_segments[i] for i in inlier_idx]
                    auto_capped_confidence = True

    if len(segments) < 2:
        return "invalid", None

    lines = [_line_through(p, q) for p, q in segments]
    vp, pz, singular_ratio = _vanishing_point_from_lines(lines, return_diagnostics=True)
    if pz is None:
        return "invalid", None  # SVD basarisiz (dejenere/cakisik cizgiler)
    if abs(pz) < 1e-9 or vp is None:
        # pz TAM/neredeyse tam 0 - Oklid kacis noktasina donusum sayisal
        # olarak imkansiz (bolme patlar). Kesisim GERCEKTEN sonsuzda -
        # bu bir hata degil, gecerli/kullanilabilir bir sonuctur.
        #
        # ONEMLI (kalibrasyon notu): pz'nin KENDISI, goruntu piksel
        # koordinatlarinin buyuklugune (coz unurluk, ana nokta ofseti)
        # bagli olcek-BAGIMLI bir buyukluktur - bu yuzden pz'yi sabit bir
        # esikle (ör. 0.02) karsilastirmak YANLIS OLCEKLENDIRME hatasina
        # yol acar (bir 4000x3000 fotografta makul bir kacis noktasi bile
        # pz~0.0004 verebilir). Bunun yerine, ASAGIDAKI dist_ratio
        # (kacis noktasinin REFERANS OLCEGINE gore uzakligi) kullaniliyor -
        # bu olcek-BAGIMSIZ, dogru kriterdir.
        return "near_infinity", None
    if ref_scale is None or ref_scale < 1e-6:
        ref_scale = math.hypot(B[0] - A[0], B[1] - A[1]) or 1.0
    dist_ratio = math.hypot(vp[0] - A[0], vp[1] - A[1]) / ref_scale
    if dist_ratio > VP_MAX_DIST_RATIO:
        return "near_infinity", None
    if singular_ratio is not None and singular_ratio < VP_STRONG_SINGULAR_RATIO and not auto_capped_confidence:
        return "finite_strong", vp
    return "finite_weak", vp


_FINITE_KINDS = ("finite_strong", "finite_weak")


def detect_line_segments(gray, max_segments=250, min_length_px=25):
    """Fotograftaki BELIRGIN dogru parcalarini OTOMATIK bulur - kullanicinin
    manuel olarak yardimci cizgi secmesine GEREK KALMADAN, kacis noktasi
    tahminine ek gercek kanit saglamak icin (bkz. _ransac_vanishing_point).

    OpenCV'nin Line Segment Detector'ini (LSD) dener; bazi OpenCV
    derlemelerinde (eski patent kisitlamasi nedeniyle) bulunmayabilir - bu
    durumda HoughLinesP'ye GERI DUSER. Ikisi de basarisiz olursa bos liste
    doner (cagiran taraf, otomatik kanit olmadan sadece kullanicinin
    yardimci cizgileriyle devam eder - sistem CALISMAYI DURDURMAZ).

    Performans: buyuk fotograflarda hizli olmasi icin, gerekirse once
    kucuk bir olcege indirgenir, sonuc koordinatlari geri buyutulur."""
    h, w = gray.shape[:2]
    scale = 1.0
    max_dim = 1600
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        small = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    else:
        small = gray

    # ONEMLI: cv2 surumune gore lsd.detect()/HoughLinesP sonucu (N,4) ya da
    # (N,1,4) sekilli olabilir (OpenCV 5.x'te LSD artik (N,4) donuyor, eski
    # surumlerde (N,1,4) idi). reshape(-1,4) HER IKI durumda da dogru
    # calisir - sabit bir sekil varsaymak (ör. lines[:,0]) surume gore
    # SESSIZCE 0 sonuc donmesine yol acabilir (gelistirme sirasinda
    # bulunan gercek bir bug).
    segments = []
    try:
        lsd = cv2.createLineSegmentDetector(0)
        lines, *_ = lsd.detect(small)
        if lines is not None:
            for l in lines.reshape(-1, 4):
                segments.append((float(l[0]), float(l[1]), float(l[2]), float(l[3])))
    except Exception:
        segments = []

    if not segments:
        try:
            edges = cv2.Canny(small, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, math.pi / 180, threshold=40,
                                     minLineLength=min_length_px * scale, maxLineGap=8)
            if lines is not None:
                for l in lines.reshape(-1, 4):
                    segments.append((float(l[0]), float(l[1]), float(l[2]), float(l[3])))
        except Exception:
            segments = []

    out = []
    for x1, y1, x2, y2 in segments:
        length = math.hypot(x2 - x1, y2 - y1) / scale
        if length < min_length_px:
            continue
        out.append(((x1 / scale, y1 / scale), (x2 / scale, y2 / scale)))
    out.sort(key=lambda pq: -math.hypot(pq[1][0] - pq[0][0], pq[1][1] - pq[0][1]))
    return out[:max_segments]


VP_RANSAC_ANGLE_TOL_DEG = 3.0  # RANSAC ic-nokta (inlier) ACI toleransi (bkz. _angular_residual_deg)


def _ransac_vanishing_point(segments, angle_tol_deg=VP_RANSAC_ANGLE_TOL_DEG, n_iter=300, seed=0, min_inliers=2):
    """Bir cizgi-parcasi (nokta cifti) havuzundan (ör. kullanicinin
    yardimci cizgisi + otomatik tespit edilen adaylar KARISIK), RANSAC ile
    GURULTUYE/AYKIRI DEGERLERE dayanikli bir kacis noktasi bulur.

    Yontem: rastgele iki parca sec, tam kesisimlerini adayin VP'si say,
    TUM havuzdaki parcalarin bu adaya olan ACISAL kalintisini
    (_angular_residual_deg - PIKSEL mesafesi DEGIL, bkz. o fonksiyonun
    dokumantasyonu) hesapla, angle_tol_deg icinde kalanlari 'inlier' say.
    En YUKSEK AGIRLIKLI (ham SAYI degil - bkz. asagi) inlier kumesini olan
    adayi tut, sonunda TUM inlier parcalarla SVD ile (bkz.
    _vanishing_point_from_lines) son bir kez hassas kesisim hesapla
    (klasik RANSAC + refinement paterni).

    AGIRLIK = parca UZUNLUGU (piksel): daha UZUN bir cizgi parcasi, kacis
    noktasi yonu hakkinda daha AZ acisal belirsizlik tasir (kisa bir
    parcanin ucundaki ayni piksel-tiklama hatasi, UZUN bir parcadakinden
    cok daha buyuk bir ACI hatasina karsilik gelir) - bu yuzden ham SAYI
    yerine TOPLAM UZUNLUK kullanmak, GERCEKTEN ait olmayan ama SAYICA
    rakip cizgi ailesine (ör. baska bir duzlemden - balkon/zemin -
    gelen, KISA cizgiler) karsi daha dayaniklidir. Bu, sentetik bir
    'yabanci duzlem' testiyle (bkz. tests/test_bad_vp.py) DOGRULANDI:
    ham-sayi oylamasi, sayica rakip olabilen KISA yabanci bir cizgi
    kumesine kanabiliyordu; uzunluk-agirlikli oylama bunu duzeltti.

    segments: [(p,q), ...] nokta-cifti listesi (homojen katsayi DEGIL).

    Doner: (vp, inlier_indices) ya da yeterli inlier bulunamazsa (None, [])."""
    n = len(segments)
    if n < 2:
        return None, []
    homs = [_line_through(p, q) for p, q in segments]
    L = np.array(homs, dtype=np.float64)
    norms = np.linalg.norm(L[:, :2], axis=1, keepdims=True)
    valid = (norms[:, 0] > 1e-12)
    if valid.sum() < 2:
        return None, []
    Ln = np.where(norms > 1e-12, L / np.where(norms > 1e-12, norms, 1.0), 0.0)
    lengths = np.array([math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in segments])

    def _refine_from(vx, vy):
        """Bir HAM 2-cizgi hipotez kesisiminden baslayip, IRLS-benzeri birkac
        tur ile (inlier kumesini ORTAK SVD kesisimine gore YENIDEN hesapla,
        degismeyi birakana kadar tekrarla) kararli bir (inliers, vp) cifti
        bulur. ONEMLI: bu, HER hipotez icin (sadece EN SONDAKI kazanan icin
        degil) yapilir - cunku HAM bir 2-cizgi kesisimi, GERCEKTE iki farkli
        aileden (ör. farkli bir duzlemden gelen KISA cizgiler - bkz.
        tests/test_bad_vp.py) KIRLENMIS bir inlier kumesini 'yanlislikla'
        tatmin edebilecek rastgele bir noktada olabilir; SADECE kazanani
        inceltmek bu KIRLENMIS kumeyi degistirmeyebilir (kendi kendini
        dogrulayan kararli ama YANLIS bir sabit nokta olabilir). Her
        hipotezi BASTAN inceltmek, kirlenmis kumelerin GERCEK bir aileye
        (daha yuksek toplam agirlikli) COKMESINI/kucul mesini saglar."""
        inliers = [k for k in valid_idx
                   if _angular_residual_deg(segments[k][0], segments[k][1], (vx, vy)) <= angle_tol_deg]
        vp = (vx, vy)
        for _ in range(4):
            if len(inliers) < 2:
                break
            refined_vp = _vanishing_point_from_lines([homs[i] for i in inliers])
            if refined_vp is None:
                break
            new_inliers = [k for k in valid_idx
                           if _angular_residual_deg(segments[k][0], segments[k][1], refined_vp) <= angle_tol_deg]
            vp = refined_vp
            if set(new_inliers) == set(inliers):
                break
            inliers = new_inliers
        return inliers, vp

    rng = np.random.default_rng(seed)
    valid_idx = np.where(valid)[0]
    best_inliers = []
    best_weight = -1.0
    best_vp = None
    n_iter = min(n_iter, max(50, len(valid_idx) * (len(valid_idx) - 1) // 2))
    for _ in range(n_iter):
        i, j = rng.choice(valid_idx, size=2, replace=False)
        cand = np.cross(Ln[i], Ln[j])
        if abs(cand[2]) < 1e-12:
            continue  # neredeyse paralel cift -> aday VP sonsuzda, bu fonksiyon SONLU VP arar
        vx0, vy0 = cand[0] / cand[2], cand[1] / cand[2]
        inliers, vp = _refine_from(vx0, vy0)
        weight = float(lengths[inliers].sum()) if inliers else 0.0
        if weight > best_weight and len(inliers) >= min_inliers:
            best_inliers = inliers
            best_weight = weight
            best_vp = vp
    if best_vp is None:
        return None, []

    refined = _vanishing_point_from_lines([homs[i] for i in best_inliers])
    return (refined if refined is not None else best_vp), best_inliers


VP_BOOTSTRAP_N = 40  # bootstrap tekrar sayisi (bkz. bootstrap_vp_uncertainty)


def bootstrap_vp_uncertainty(segments, ref_scale, n_bootstrap=VP_BOOTSTRAP_N, seed=0):
    """Bir kacis noktasi tahmininin NE KADAR KARARLI oldugunu, RANSAC'in
    ZATEN dogruladigi inlier cizgi kumesinden TEKRARLI ORNEKLEME
    (bootstrap - klasik istatistiksel yeniden-ornekleme, N. YERINE KOYARAK
    orneklenen alt-kumeler) ile olcer.

    NEDEN GEREKLI: dikey (ya da herhangi bir) kacis noktasi, cizgiler
    goruntude neredeyse PARALEL oldugunda (kamera o yonde az egimliyse)
    COK UZAKTA olabilir - bu durumda, hangi cizgilerin dahil edildigine
    bagli olarak VP tahmini SERT bicimde sicrayabilir (bazen isaret bile
    degistirebilir). Mevcut kod HER iki kacis noktasi kisitina (yatay ve
    dikey) optimizasyonda ESIT agirlik veriyordu - bu, KARARSIZ bir
    kisitin GUCLU/SAGLAM bir kisitla AYNI sozu soylemesine izin verir ve
    H'yi o kararsiz yonde YANLIS bir yere cekebilir (bkz. final rapor,
    Bolum 16 - kullanicinin bildirdigi dikeye-ozel sapma icin en olasi
    ANCAK bu oturumda dogrudan sentetik olarak dogrulanamayan aday).

    Her bootstrap turunde, segments'ten (AYNI boyutta, yerine koyarak)
    bir alt-kume orneklenir, o alt-kumeden SVD ile bir VP tahmini uretilir
    (_vanishing_point_from_lines). NIHAI RAPOR:
      - vp_std_ratio: sonlu VP tahminlerinin piksel STD'sinin ref_scale'e
        orani (OLCEK-BAGIMSIZ - kucukse KARARLI, buyukse KARARSIZ).
      - finite_fraction: bootstrap orneklerinin ne kadari SONLU bir VP
        uretti (dusukse cogu ornek 'sonsuza kacti' - COK kararsiz demektir).

    segments < 2 ise ya da hicbir ornek sonlu VP uretmezse None doner
    (belirsizlik olcusuz - cagiran taraf varsayilan/dusuk guven
    kullanmali)."""
    n = len(segments)
    if n < 2 or ref_scale < 1e-9:
        return None
    rng = np.random.default_rng(seed)
    finite_vps = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)  # bootstrap: yerine koyarak, AYNI boyutta yeniden ornekleme
        subset = [segments[i] for i in idx]
        homs = [_line_through(p, q) for p, q in subset]
        vp, pz, _sr = _vanishing_point_from_lines(homs, return_diagnostics=True)
        if vp is not None and pz is not None and abs(pz) > 1e-9:
            finite_vps.append(vp)
    finite_fraction = len(finite_vps) / n_bootstrap
    if len(finite_vps) < 3:
        return {"vp_std_ratio": None, "finite_fraction": finite_fraction, "n_bootstrap": n_bootstrap}
    arr = np.array(finite_vps)
    vp_std_px = float(np.mean(np.std(arr, axis=0)))
    return {"vp_std_ratio": vp_std_px / ref_scale, "finite_fraction": finite_fraction, "n_bootstrap": n_bootstrap}


def direction_weight_from_uncertainty(bootstrap_result):
    """bootstrap_vp_uncertainty sonucunu, nonlineer inceltmede kullanilacak
    TEK bir agirlik katsayisina (0-1 arasi) cevirir. Belirsizlik olcusuz
    (None) ise ya da orneklerin COGU sonsuza kaciyorsa (finite_fraction
    dusuk) TAM guven (1.0) varsayilir - cunku bu, VP'nin zaten (ayri bir
    mekanizma - bkz. _resolve_vanishing_point) 'near_infinity' olarak
    siniflandirilip FARKLI (ideal nokta) bir kisit turune donusturuldugu
    durumdur, bu fonksiyonun ilgilendigi 'sonlu ama kararsiz' durum
    DEGILDIR. vp_std_ratio buyudukce agirlik 1/(1+oran) ile azalir - bu,
    hicbir 'esik' KEYFI olmadan, SUREKLI/yumusak bir gecis saglar."""
    if bootstrap_result is None or bootstrap_result.get("vp_std_ratio") is None:
        return 1.0
    ratio = bootstrap_result["vp_std_ratio"]
    return 1.0 / (1.0 + ratio)


# =======================================================================
# STRATIFIED (KADEMELI) DUZLEM REKTIFIKASYONU - Hartley&Zisserman "Multiple
# View Geometry" Bol.2 klasik iki-asamali yontemi: PROJEKTIF->AFIN
# (kacis cizgisi ile) sonra AFIN->METRIK (A/B/C ile). D, hicbir asamada
# GIRDI olarak KULLANILMAZ; SADECE H_final KURULDUKTAN SONRA turetilir.
#
# ESKI mimariden (compute_global_homography - A,B,C VE yon kisitlarini
# TEK bir en-kucuk-kareler sisteminde BIRLIKTE cozer) FARKI: metrik olcek
# (A,B,C'den) ve projektif duzeltme (kacis cizgisinden) ARTIK ASLA AYNI
# optimizasyon degiskenini PAYLASMAZ - biri digerini KIRLETEMEZ. T_metric,
# A,B,C'den TAM (en kucuk kareler DEGIL, 3 nokta = 6 serbestlik derecesi
# icin TAM belirlenmis) olarak kurulur; bu yuzden AB_recovered/AC_recovered
# HER ZAMAN girdiyle (sayisal hassasiyete kadar) TAM eslesir - bu,
# mimarinin doğruluğunun otomatik bir sertifikasidir (bkz. Bolum 33 testi).
# =======================================================================

def estimate_vanishing_direction_robust(segments, angle_tol_deg=VP_RANSAC_ANGLE_TOL_DEG,
                                         n_iter=300, seed=0, min_inliers=2):
    """segments (nokta-cifti listesi) icinden, HOMOJEN bir kacis YONU/
    NOKTASI (v_hom=(vx,vy,vz), SONLU YA DA SONSUZDA - HER IKISI de GECERLI
    ve ESIT ONCELIKLE ele alinir) saglam sekilde tahmin eder.

    _ransac_vanishing_point ile AYNI RANSAC+IRLS+uzunluk-agirlikli iskelet
    kullanilir (rastgele 2-cizgi hipotezi -> _angular_residual_to_vp_hom
    ile ACISAL ic-nokta sayimi -> IRLS yeniden-suzme -> uzunluk-agirlikli
    en iyi adayi sec), TEK ONEMLI FARKLA: near-infinite hipotezler ASLA
    atlanmaz/Oklid'e zorlanmaz - cunku GERCEKTEN paralel bir cizgi ailesi
    icin (vx,vy,0) TAM OLARAK dogru/beklenen sonuctur, bir ozel durum ya
    da hata DEGILDIR (bkz. Bolum 4/19).

    Doner: (v_hom (3,) birim-normalize ndarray ya da None, inlier_indices)."""
    n = len(segments)
    if n < 2:
        return None, []
    homs = [_line_through(p, q) for p, q in segments]
    L = np.array(homs, dtype=np.float64)
    norms = np.linalg.norm(L[:, :2], axis=1, keepdims=True)
    valid = (norms[:, 0] > 1e-12)
    if valid.sum() < 2:
        return None, []
    Ln = np.where(norms > 1e-12, L / np.where(norms > 1e-12, norms, 1.0), 0.0)
    lengths = np.array([math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in segments])
    valid_idx = np.where(valid)[0]

    def _refine_from(vp_hom):
        inliers = [k for k in valid_idx
                   if _angular_residual_to_vp_hom(segments[k][0], segments[k][1], vp_hom) <= angle_tol_deg]
        cur = vp_hom
        for _ in range(4):
            if len(inliers) < 2:
                break
            p_hom, _sr = _svd_line_intersection([homs[i] for i in inliers])
            if p_hom is None:
                break
            new_inliers = [k for k in valid_idx
                           if _angular_residual_to_vp_hom(segments[k][0], segments[k][1], p_hom) <= angle_tol_deg]
            cur = p_hom
            if set(new_inliers) == set(inliers):
                break
            inliers = new_inliers
        return inliers, cur

    rng = np.random.default_rng(seed)
    best_inliers, best_weight, best_vp = [], -1.0, None
    n_iter_eff = min(n_iter, max(50, len(valid_idx) * (len(valid_idx) - 1) // 2))
    for _ in range(n_iter_eff):
        i, j = rng.choice(valid_idx, size=2, replace=False)
        cand = np.cross(Ln[i], Ln[j])
        cn = np.linalg.norm(cand)
        if cn < 1e-12:
            continue  # iki cizgi TAM CAKISIK/ozdes - GERCEK dejenerasyon (near-infinity DEGIL - bkz. docstring)
        cand = cand / cn
        inliers, vp_hom = _refine_from(cand)
        weight = float(lengths[inliers].sum()) if inliers else 0.0
        if weight > best_weight and len(inliers) >= min_inliers:
            best_inliers, best_weight, best_vp = inliers, weight, vp_hom
    if best_vp is None:
        return None, []

    final_hom, _sr = _svd_line_intersection([homs[i] for i in best_inliers])
    final = final_hom if final_hom is not None else best_vp
    norm = np.linalg.norm(final)
    if norm > 1e-12:
        final = final / norm
    return final, best_inliers


def bootstrap_vanishing_direction_uncertainty(segments, n_bootstrap=VP_BOOTSTRAP_N, seed=0):
    """bootstrap_vp_uncertainty'nin ACISAL versiyonu (Bolum 14/27):
    kullanicinin ACIKCA belirttigi gibi, Oklid VP koordinatinin piksel
    STD'si YANILTICI olabilir - kacis noktasi sonsuza yakinken KUCUK bir
    ACI belirsizligi bile DEVASA bir piksel-STD'sine karsilik gelebilir
    (bu SOMUT olarak dogrulandi - bkz. final rapor).

    Bunun yerine, her bootstrap orneginin (segments'ten YERINE KOYARAK
    yeniden ornekleme) HOMOJEN yonunun (vx,vy) KENDI ACISINI olcer - bu
    aci, pz'DEN TAMAMEN BAGIMSIZDIR (bir YON, sonlu ya da sonsuz bir
    noktadan gelsin, HER ZAMAN atan2(vy,vx)'in tanimladigi acidir). Bir
    DOGRU YONU YONSUZDUR (pi-periyodiktir, 0 derece ile 180 derece AYNI
    yondur) - bu yuzden standart dairesel istatistik yerine 'aciyi 2 ile
    carp, dairesel ortalama/varyansi hesapla, sonucu 2'ye bol' KLASIK
    yontemi kullanilir (yon istatistiginde standart teknik).

    Doner: {"angular_std_deg": ... ya da None, "n_success", "n_bootstrap"}."""
    n = len(segments)
    if n < 2:
        return None
    homs = [_line_through(p, q) for p, q in segments]
    rng = np.random.default_rng(seed)
    angles = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        p_hom, _sr = _svd_line_intersection([homs[i] for i in idx])
        if p_hom is not None and math.hypot(p_hom[0], p_hom[1]) > 1e-12:
            angles.append(math.atan2(p_hom[1], p_hom[0]) % math.pi)
    if len(angles) < 3:
        return {"angular_std_deg": None, "n_success": len(angles), "n_bootstrap": n_bootstrap}
    two_ang = np.array(angles) * 2.0
    C, S = float(np.mean(np.cos(two_ang))), float(np.mean(np.sin(two_ang)))
    R = min(max(math.hypot(C, S), 1e-12), 1.0)
    circ_std = math.sqrt(-2.0 * math.log(R)) / 2.0
    return {"angular_std_deg": math.degrees(circ_std), "n_success": len(angles), "n_bootstrap": n_bootstrap}


def estimate_vanishing_line(v_ab_hom, v_ac_hom):
    """Iki BAGIMSIZ dunya yonunun (AB, AC) HOMOJEN kacis noktalarindan/
    yonlerinden, duzlemin goruntudeki SONSUZLUK CIZGISINI (l_inf) hesaplar:

        l_inf = v_AB x v_AC

    (capraz carpim - iki nokta arasindan gecen DOGRUNUN homojen katsayilari).
    Bu, Bolum 39'daki KRITIK ayrimdir: kacis NOKTASI ile kacis CIZGISI
    (vanishing line) FARKLI seylerdir - duzlemin TUM projektif bozulmasi,
    l_inf ile tek bir cizgi olarak temsil edilir, iki ayri VP koordinati
    DEGIL. (a,b) bileseni birim-norm olacak sekilde normalize edilir."""
    l_inf = np.cross(np.asarray(v_ab_hom, dtype=np.float64), np.asarray(v_ac_hom, dtype=np.float64))
    norm = math.hypot(l_inf[0], l_inf[1])
    if norm < 1e-12:
        return None  # v_AB ve v_AC AYNI yon/nokta - dejenere (AB//AC gibi imkansiz bir durum)
    return l_inf / norm


def affine_rectification_from_vanishing_line(l_inf):
    """l_inf'i (goruntudeki sonsuzluk cizgisi) kanonik sonsuzluk cizgisine
    (0,0,1)^T tasiyan PROJEKTIF->AFIN rektifikasyon homografisini kurar
    (Hartley&Zisserman, 'Multiple View Geometry', Sonuc 2.2 - standart
    'affine rectification' insaasi):

        H_p = [[1,0,0],
               [0,1,0],
               [l1,l2,l3]]

    Dogrulama: x'=H_p*x seklinde NOKTALARA uygulandiginda, cizgiler
    l'=H_p^-T*l kuraliyla donusur; H_p^-T*l_inf = (0,0,1)^T olmasi icin
    GEREK VE YETER sart, H_p'nin UCUNCU SATIRININ TAM OLARAK l_inf olmasidir
    - yukaridaki insaa budur. Bu asamadan SONRA, l_inf uzerindeki (yani
    dunyada sonsuzdaki) tum noktalar goruntude de sonsuzda kalir - yani
    AB-ailesi ve AC-ailesi cizgiler ARTIK KENDI ICINDE PARALEL gorunur
    (perspektif yakinsama ORTADAN KALKAR) - bkz. Bolum 8/32 testi."""
    l1, l2, l3 = float(l_inf[0]), float(l_inf[1]), float(l_inf[2])
    return np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [l1, l2, l3]])


def _rectified_orientation_std_deg(H_p, segments):
    """AFIN rektifikasyon KALITESININ dogrudan olcumu (Bolum 32): bir
    cizgi ailesindeki TUM segmentler H_p ile donusturuldukten SONRA,
    hepsinin GORUNTU ACISI (yonsuz, 0-180 derece) NE KADAR ORTAK/tutarli?
    Dairesel (pi-periyodik) standart sapma olarak doner - rektifikasyon
    MUKEMMELSE bu deger ~0 olmalidir (TUM aile artik TAM paralel)."""
    if len(segments) < 2:
        return None
    angles = []
    for p, q in segments:
        try:
            pr, qr = apply_transform(H_p, p), apply_transform(H_p, q)
        except ValueError:
            continue
        angles.append(math.atan2(qr[1] - pr[1], qr[0] - pr[0]) % math.pi)
    if len(angles) < 2:
        return None
    two_ang = np.array(angles) * 2.0
    C, S = float(np.mean(np.cos(two_ang))), float(np.mean(np.sin(two_ang)))
    R = min(max(math.hypot(C, S), 1e-12), 1.0)
    return math.degrees(math.sqrt(-2.0 * math.log(R)) / 2.0)


def compute_metric_homography_stratified(A, B, C, ab_m, ac_m, angle_deg,
                                          helper_ab=None, helper_ac=None,
                                          extra_ab=None, extra_ac=None,
                                          auto_ab=None, auto_ac=None):
    """YENI (Bolum 3-13, 39): klasik IKI-ASAMALI projektif duzlem
    rektifikasyonu (Hartley&Zisserman Bol.2) - compute_global_homography'nin
    (A,B,C VE yon kisitlarini TEK bir en-kucuk-kareler sisteminde BIRLIKTE
    cozen) YERINE GECMEK UZERE tasarlanmis AYRI/BAGIMSIZ bir cozucu
    (bkz. Bolum 37 - eski yontem karsilastirma icin KORUNUR).

    1) v_AB, v_AC: HOMOJEN (sonlu ya da sonsuzda - HER IKISI GECERLI)
       kacis yonleri, RANSAC+IRLS+uzunluk-agirlikli olarak saglam bicimde
       tahmin edilir (bkz. estimate_vanishing_direction_robust).
    2) l_inf = v_AB x v_AC: duzlemin goruntudeki SONSUZLUK CIZGISI
       (Bolum 39 - kacis NOKTASI degil kacis CIZGISI kullanilir).
    3) H_p: l_inf'i kanonik sonsuzluk cizgisine tasiyan PROJEKTIF->AFIN
       rektifikasyon (bkz. affine_rectification_from_vanishing_line).
    4) A,B,C H_p ile afin-rektifiye uzaya tasinir (A',B',C' - ARTIK
       SADECE afin, perspektif YOK).
    5) T_metric: A',B',C' -> A_w,B_w,C_w AFIN donusumu (fit_affine ile
       TAM/kesin cozum - 3 nokta, 6 serbestlik derecesi).
    6) H_final = T_metric @ H_p.

    KRITIK MIMARI FARK (Bolum 13): metrik olcek (A,B,C'den, T_metric
    asamasinda TAM/kesin olarak) VE projektif duzeltme (kacis cizgisinden,
    H_p asamasinda) ARTIK AYNI optimizasyon degiskenini PAYLASMIYOR - biri
    digerini KIRLETEMEZ. D, HICBIR ASAMADA GIRDI olarak KULLANILMAZ.

    Basarili olursa zengin bir sonuc sozlugu (H, Hinv, D_img, teshis
    alanlari - bkz. Bolum 30-33), degilse (yeterli kacis yonu kaniti yoksa)
    None doner."""
    angle_rad = math.radians(angle_deg)
    world_A = (0.0, 0.0)
    world_B = (ab_m, 0.0)
    world_C = (ac_m * math.cos(angle_rad), ac_m * math.sin(angle_rad))
    world_D = (world_B[0] + world_C[0], world_B[1] + world_C[1])

    all_ab = [(A, B)] + ([helper_ab] if helper_ab else []) + list(extra_ab or []) + list(auto_ab or [])
    all_ac = [(A, C)] + ([helper_ac] if helper_ac else []) + list(extra_ac or []) + list(auto_ac or [])
    if len(all_ab) < 2 or len(all_ac) < 2:
        return None  # kacis yonu icin en az 2 bagimsiz cizgi sart (klasik VP kesisimi tanimi geregi)

    v_ab_hom, inliers_ab = estimate_vanishing_direction_robust(all_ab)
    v_ac_hom, inliers_ac = estimate_vanishing_direction_robust(all_ac)
    if v_ab_hom is None or v_ac_hom is None:
        return None

    core = _stratified_metric_from_vps(A, B, C, ab_m, ac_m, angle_deg, v_ab_hom, v_ac_hom)
    if core is None:
        return None
    H_p, l_inf = core["H_p"], core["l_inf"]
    H_final, Hinv_final, D_img = core["H"], core["Hinv"], core["D_img"]

    # BOLUM 32/33 TESHIS: iki asamayi AYRI AYRI dogrula - hangisi
    # basarisiz olursa hatanin KAYNAGINI (VP/rektifikasyon mu, yoksa
    # metrik/referans geometrisi mi) ACIKCA ayirir.
    ab_inlier_segs = [all_ab[i] for i in inliers_ab]
    ac_inlier_segs = [all_ac[i] for i in inliers_ac]
    affine_residual_ab_deg = _rectified_orientation_std_deg(H_p, ab_inlier_segs)
    affine_residual_ac_deg = _rectified_orientation_std_deg(H_p, ac_inlier_segs)
    ab_recovered = dist(apply_transform(H_final, A), apply_transform(H_final, B))
    ac_recovered = dist(apply_transform(H_final, A), apply_transform(H_final, C))
    v1 = (apply_transform(H_final, B)[0] - apply_transform(H_final, A)[0],
          apply_transform(H_final, B)[1] - apply_transform(H_final, A)[1])
    v2 = (apply_transform(H_final, C)[0] - apply_transform(H_final, A)[0],
          apply_transform(H_final, C)[1] - apply_transform(H_final, A)[1])
    angle_recovered_deg = _angle_between_dirs(v1, v2)
    # T_metric TAM/kesin oldugu icin bunlar (sayisal hassasiyete kadar)
    # GIRDIYLE (ab_m, ac_m, angle_deg) TAM eslesmelidir - bkz. Bolum 33.

    ref_scale = (math.hypot(B[0] - A[0], B[1] - A[1]) + math.hypot(C[0] - A[0], C[1] - A[1])) / 2.0

    return {
        "H": H_final, "Hinv": Hinv_final,
        "D_img": D_img, "world_D": world_D,
        "world_A": world_A, "world_B": world_B, "world_C": world_C,
        "H_p": H_p, "l_inf": l_inf,
        "v_ab_hom": v_ab_hom, "v_ac_hom": v_ac_hom,
        "n_inliers_ab": len(inliers_ab), "n_inliers_ac": len(inliers_ac),
        "v_ab_uncertainty": bootstrap_vanishing_direction_uncertainty(ab_inlier_segs),
        "v_ac_uncertainty": bootstrap_vanishing_direction_uncertainty(ac_inlier_segs),
        "affine_residual_ab_deg": affine_residual_ab_deg,
        "affine_residual_ac_deg": affine_residual_ac_deg,
        "ab_recovered": ab_recovered, "ac_recovered": ac_recovered,
        "ab_input": ab_m, "ac_input": ac_m,
        "angle_recovered_deg": angle_recovered_deg, "angle_input_deg": angle_deg,
        "ref_scale": ref_scale,
    }


def _stratified_metric_from_vps(A, B, C, ab_m, ac_m, angle_deg, v_ab_hom, v_ac_hom,
                                require_same_side=False):
    """Kademeli rektifikasyonun ORTAK cekirdegi: verilen iki HOMOJEN kacis
    yonunden (v_AB, v_AC) l_inf = v_AB x v_AC -> H_p (projektif->afin) ->
    T_metric (A,B,C'den TAM afin, metrik) -> H_final; D* SADECE bundan SONRA
    turetilir (D_world = B_world + C_world, D_img = H_final^-1 * D_world).

    require_same_side=True ise A, B, C'nin kacis cizgisinin AYNI tarafinda
    olmasi sart kosulur - aksi halde (referans ufkun iki yanina dusuyorsa)
    VP tahmini fiziksel olarak imkansiz bir duzlem tanimlar."""
    angle_rad = math.radians(angle_deg)
    world_A = (0.0, 0.0)
    world_B = (ab_m, 0.0)
    world_C = (ac_m * math.cos(angle_rad), ac_m * math.sin(angle_rad))
    world_D = (world_B[0] + world_C[0], world_B[1] + world_C[1])

    l_inf = estimate_vanishing_line(v_ab_hom, v_ac_hom)
    if l_inf is None:
        return None
    if require_same_side:
        sides = [float(l_inf @ np.array([p[0], p[1], 1.0])) for p in (A, B, C)]
        if not (all(s > 0 for s in sides) or all(s < 0 for s in sides)):
            return None
    H_p = affine_rectification_from_vanishing_line(l_inf)
    try:
        A_r = apply_transform(H_p, A)
        B_r = apply_transform(H_p, B)
        C_r = apply_transform(H_p, C)
        T_metric = fit_affine([A_r, B_r, C_r], [world_A, world_B, world_C])
    except (ValueError, np.linalg.LinAlgError):
        return None
    H_final = T_metric @ H_p
    if abs(H_final[2, 2]) < 1e-12:
        return None
    H_final = H_final / H_final[2, 2]
    try:
        Hinv_final = np.linalg.inv(H_final)
        D_img = apply_transform(Hinv_final, world_D)
    except (np.linalg.LinAlgError, ValueError):
        return None
    return {"H": H_final, "Hinv": Hinv_final, "D_img": D_img, "H_p": H_p, "l_inf": l_inf,
            "world_A": world_A, "world_B": world_B, "world_C": world_C, "world_D": world_D}


# =======================================================================
# YARDIMCI CIZGI GOZLEMLERI + OLCUM-BELIRSIZLIGI AGIRLIKLI SAGLAM KACIS
# NOKTASI (VP) TAHMINI, BAGIMSIZ DOGRULAMA VE MODEL KARSILASTIRMA
#
# Her cizgi (referans AB/AC, kullanicinin yardimci cizgileri, otomatik
# LSD/Hough cizgileri, olcum-sorgusu kenarlari) bir LineObservation olur.
# Her gozlemin ACISAL belirsizligi (sigma_theta) uzunluk, uc-nokta
# hassasiyeti, destek pikseli sayisi ve kaynaktan (dogrulanmis mi) turetilir:
#
#     w_measurement = 1 / sigma_theta^2
#     w_effective   = w_measurement * w_robust      (Tukey IRLS)
#
# Kullanici-dogrulamali cizgiler (referans + elle yardimci cizgiler) VP
# hipotezleri icin SERT bir kisit olusturur (referans HER ZAMAN inlier
# kalmali; >=3 dogrulanmis cizgi varsa en fazla n//3'u aykiri olabilir -
# boylece yanlis bir yardimci cizgi TESPIT edilebilir). Dogrulanmamis
# (otomatik) cizgiler MSAC ile oy kullanir; ailesi YEREL ACIYA gore degil,
# VP tutarliligina gore belirlenir.
# =======================================================================

# Uc-nokta (veya kenar-ornegi) basina dik yondeki piksel belirsizligi (1-sigma).
LINE_ENDPOINT_SIGMA_PX = {
    "manual": 1.0,            # tek tiklama
    "manual_magnifier": 0.5,  # buyutecle hassaslastirilmis tiklama
    "auto": 0.7,              # LSD/Hough (tespit olcegine gore buyutulur)
}
# Model/yapi belirsizligi (eklenen varyans tabani): gercek kenarlar mukemmel
# duz degildir, otomatik cizgiler ise ayrica farkli bir yapi elemanina
# (pencere girintisi, hafif lens egriligi) ait olabilir. Bu bir TABAN
# belirsizliktir, fotografa ozel bir duzeltme DEGILDIR.
LINE_MODEL_SIGMA_DEG_VERIFIED = 0.05
LINE_MODEL_SIGMA_DEG_UNVERIFIED = 0.25
# Otomatik cizgilerin ORTAK (korelasyonlu) aci hatasi - cok sayida cizgiyle
# ortalanarak kuculmez; belirsizlik tahmininde (MC) ayrica modellenir.
LINE_COMMON_SIGMA_DEG_UNVERIFIED = 0.15
VP_GATE_Z = 3.0               # normalize aci kalintisi (theta/sigma) icin 3-sigma kapisi
VP_TUKEY_C = 4.685            # Tukey biweight sabiti (%95 Gauss verimliligi)
VP_MAX_HYPOTHESES = 600
AUTO_LINE_POOL_MAX = 150
AMBIGUITY_GAP_CHI2 = 9.0      # rakip VP hipotezi en iyiden < 9 (ki-kare) uzaktaysa 'belirsiz'
AMBIGUITY_MIN_AUTO = 5        # yardimcisiz bir ailede bundan az otomatik inlier + belirsizlik -> kullanma
CONF_SCALE_UNC_HIGH = 0.01    # uzak bolgede 1-sigma goreli olcek belirsizligi <= %1 -> YUKSEK adayi
CONF_SCALE_UNC_MID = 0.03     # <= %3 -> ORTA adayi


def line_angle_sigma_deg(length_px, endpoint_sigma_px, n_support=2, verified=True):
    """Bir dogru parcasinin YON (aci) belirsizligi, derece (1-sigma).

    - Sadece iki uc noktasiyla tanimli cizgi (n_support<=2): her ucun dik
      hatasi sigma_e ise sigma_theta ~ sqrt(2)*sigma_e/L (radyan).
    - Kenar boyunca n_support ornekle TLS ile fit edilmis cizgi: egim
      varyansi sigma_e^2 / sum(t_i^2) ~ 12*sigma_e^2/(n*L^2).
    Sonuca (karesel toplamla) kaynak tipine bagli model-belirsizligi tabani
    eklenir. Uzun cizgi daha kucuk sigma alir, ama ASLA sifira inmez -
    'uzun cizgi = otomatik olarak dogru cizgi' DEGILDIR (bkz. Bolum 13)."""
    L = max(float(length_px), 1.0)
    se = max(float(endpoint_sigma_px), 1e-3)
    if n_support is None or n_support <= 2:
        s_rad = math.sqrt(2.0) * se / L
    else:
        s_rad = se * math.sqrt(12.0 / float(n_support)) / L
    model = LINE_MODEL_SIGMA_DEG_VERIFIED if verified else LINE_MODEL_SIGMA_DEG_UNVERIFIED
    return math.hypot(math.degrees(s_rad), model)


@dataclass
class LineObservation:
    """Tek bir GEOMETRIK gozlem (kontrol noktasi/olcum noktasi DEGIL)."""
    p1: tuple
    p2: tuple
    source: str = "manual"
    verified: bool = True
    family: str = "auto"
    line_id: str = ""
    is_reference: bool = False
    endpoint_sigma_px: float = 1.0
    n_support: int = 2
    gradient_strength: float = None
    homogeneous_line: np.ndarray = field(init=False, repr=False)
    length_px: float = field(init=False)
    midpoint: tuple = field(init=False)
    angle_deg: float = field(init=False)
    sigma_angle_deg: float = field(init=False)

    def __post_init__(self):
        x1, y1 = float(self.p1[0]), float(self.p1[1])
        x2, y2 = float(self.p2[0]), float(self.p2[1])
        self.p1, self.p2 = (x1, y1), (x2, y2)
        l = np.cross([x1, y1, 1.0], [x2, y2, 1.0])
        n = math.hypot(l[0], l[1])
        self.homogeneous_line = l / n if n > 1e-12 else l
        self.length_px = math.hypot(x2 - x1, y2 - y1)
        self.midpoint = ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
        self.angle_deg = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180.0
        self.sigma_angle_deg = line_angle_sigma_deg(self.length_px, self.endpoint_sigma_px,
                                                    self.n_support, self.verified)


def _obs_arrays(obs):
    L = np.array([o.homogeneous_line for o in obs], dtype=np.float64).reshape(-1, 3)
    M = np.array([o.midpoint for o in obs], dtype=np.float64).reshape(-1, 2)
    S = np.array([o.sigma_angle_deg for o in obs], dtype=np.float64)
    return L, M, S


def vp_angular_residuals_deg(L, M, v):
    """Vektorize, HOMOJEN aci kalintisi: her cizgi ile, cizginin orta
    noktasindan v'ye giden yon arasindaki aci (derece). (a,b)-birim
    normalize cizgi l ve birim v icin sin(theta) = |l.v| / D,
    D = ||(vx - mx*vz, vy - my*vz)||. v sonsuzda (vz=0) ise de AYNI formul
    gecerlidir (D = ||(vx,vy)||) - near_infinity ozel durumu gerekmez."""
    v = np.asarray(v, dtype=np.float64)
    num = np.abs(L @ v)
    D = np.hypot(v[0] - M[:, 0] * v[2], v[1] - M[:, 1] * v[2])
    s = np.where(D > 1e-12, num / np.maximum(D, 1e-300), 1.0)
    return np.degrees(np.arcsin(np.clip(s, 0.0, 1.0)))


def vp_direction_angle_at(v, pt):
    """pt noktasindan (homojen) v'ye giden yonun acisi, [0, pi)."""
    dx = v[0] - pt[0] * v[2]
    dy = v[1] - pt[1] * v[2]
    return math.atan2(dy, dx) % math.pi


def _circular_std_deg_pi(angles_rad):
    """pi-periyodik (yonsuz) acilarin dairesel standart sapmasi, derece."""
    two = 2.0 * np.asarray(angles_rad, dtype=np.float64)
    R = min(max(math.hypot(float(np.mean(np.cos(two))), float(np.mean(np.sin(two)))), 1e-12), 1.0)
    return math.degrees(math.sqrt(-2.0 * math.log(R)) / 2.0)


def _conditioning_transform(M):
    c = M.mean(axis=0)
    d = float(np.hypot(M[:, 0] - c[0], M[:, 1] - c[1]).mean())
    s = math.sqrt(2.0) / d if d > 1e-9 else 1.0
    return np.array([[s, 0.0, -s * c[0]], [0.0, s, -s * c[1]], [0.0, 0.0, 1.0]])


def fit_vp_weighted(L, M, w, v_init=None, n_iter=3):
    """Agirlikli HOMOJEN en kucuk kareler VP fit'i (Hartley-tarzi
    kosullandirilmis koordinatlarda). Minimize edilen:

        sum_i w_i * sin^2(theta_i) = sum_i w_i * (l_i.v)^2 / D_i(v)^2

    D_i bir onceki iterasyondan alinir (IRLS). Boylece kalinti PIKSEL
    mesafesi degil ACI'dir (VP ne kadar uzakta olursa olsun olcek-bagimsiz)
    ve her cizgi KENDI acisal belirsizligiyle (w_i = 1/sigma_i^2)
    agirliklandirilir. Sonuc birim-norm homojen 3-vektor (sonsuz VP gecerli)."""
    L = np.asarray(L, dtype=np.float64).reshape(-1, 3)
    M = np.asarray(M, dtype=np.float64).reshape(-1, 2)
    w = np.asarray(w, dtype=np.float64).reshape(-1)
    mask = w > 0
    if mask.sum() < 2:
        return None
    L, M, w = L[mask], M[mask], w[mask]
    T = _conditioning_transform(M)
    Tinv = np.linalg.inv(T)
    Ln = L @ Tinv
    nn = np.hypot(Ln[:, 0], Ln[:, 1])
    if np.any(nn < 1e-15):
        return None
    Ln = Ln / nn[:, None]
    Mn = M @ T[:2, :2].T + T[:2, 2]
    v = None
    if v_init is not None:
        v = T @ np.asarray(v_init, dtype=np.float64)
        v = v / np.linalg.norm(v)
    for _ in range(max(1, n_iter)):
        if v is None:
            W = w.copy()
        else:
            D = np.hypot(v[0] - Mn[:, 0] * v[2], v[1] - Mn[:, 1] * v[2])
            D = np.maximum(D, 1e-6 * max(float(D.max()), 1e-12))
            W = w / D ** 2
        W = W / W.max()
        Amat = (Ln * W[:, None]).T @ Ln
        _evals, evecs = np.linalg.eigh(Amat)
        v = evecs[:, 0]
    out = Tinv @ v
    nrm = np.linalg.norm(out)
    if nrm < 1e-15:
        return None
    return out / nrm


def _tukey_weights(z, c=VP_TUKEY_C):
    r = np.asarray(z, dtype=np.float64) / c
    return np.where(r < 1.0, (1.0 - r * r) ** 2, 0.0)


def estimate_vp_weighted(obs, gate_z=VP_GATE_Z, max_hypotheses=VP_MAX_HYPOTHESES, seed=0, min_inliers=2):
    """Bir cizgi ailesi icin saglam, belirsizlik-agirlikli VP kestirimi.

    1) Hipotezler: dogrulanmis cizgi ciftleri + (dogrulanmis x otomatik)
       ciftleri (+ dogrulanmis cizgi yoksa rastgele ciftler).
    2) Her hipotez kapi-tabanli inlier secimi + agirlikli homojen fit ile
       yerel olarak inceltilir.
    3) Kisitlar: referans cizgisi inlier OLMALI; dogrulanmis aykiri sayisi
       <= (0 eger n_dogrulanmis<=2, aksi halde n//3).
    4) MSAC skoru: sum min(z^2, gate^2), z = theta/sigma.
    5) En iyi hipotezden Tukey-IRLS ile son inceltme.
    VP sonsuzda olabilir (vz~0) - gecerli bir sonuctur, None'a cevrilmez.

    Doner: sozluk (v, inliers, z, theta_deg, w_meas, w_robust, w_eff,
    verified_outliers, chi2_red, n_inliers, cost, n_hypotheses) ya da None."""
    n = len(obs)
    if n < 2:
        return None
    L, M, S = _obs_arrays(obs)
    if np.any(np.hypot(L[:, 0], L[:, 1]) < 1e-12):
        return None
    w_meas = 1.0 / S ** 2
    ver = np.array([bool(o.verified) for o in obs])
    ref = np.array([bool(o.is_reference) for o in obs])
    ver_idx = np.flatnonzero(ver)
    oth_idx = np.flatnonzero(~ver)
    n_v = len(ver_idx)
    allowed_out = 0 if n_v <= 2 else n_v // 3
    rng = np.random.default_rng(seed)

    pairs = [(int(i), int(j)) for a, i in enumerate(ver_idx) for j in ver_idx[a + 1:]]
    mixed = [(int(i), int(j)) for i in ver_idx for j in oth_idx]
    budget = max_hypotheses - len(pairs)
    if budget <= 0:
        mixed = []
    elif len(mixed) > budget:
        sel = rng.choice(len(mixed), size=budget, replace=False)
        mixed = [mixed[k] for k in sorted(sel)]
    pairs += mixed
    if n_v == 0 or len(pairs) < 20:
        n_rand = min(max(0, max_hypotheses - len(pairs)), n * (n - 1) // 2)
        for _ in range(n_rand):
            i, j = rng.choice(n, size=2, replace=False)
            pairs.append((int(i), int(j)))

    def admissible(z):
        if ref.any() and np.any(z[ref] > gate_z):
            return False
        if int(np.sum(z[ver] > gate_z)) > allowed_out:
            return False
        return int(np.sum(z <= gate_z)) >= min_inliers

    def refine(v):
        inl = None
        for _ in range(4):
            z = vp_angular_residuals_deg(L, M, v) / S
            new_inl = z <= gate_z
            if inl is not None and np.array_equal(new_inl, inl):
                break
            inl = new_inl
            if inl.sum() < 2:
                break
            v2 = fit_vp_weighted(L[inl], M[inl], w_meas[inl], v_init=v, n_iter=2)
            if v2 is None:
                break
            if admissible(z) and not admissible(vp_angular_residuals_deg(L, M, v2) / S):
                # Cok sayida (ör. sistematik yanli) dogrulanmamis cizgi fit'i
                # dogrulanmis cizgilerin kapisinin DISINA cekti. Dogrulanmis
                # cizgiler sert kisittir: kisit saglanana kadar dogrulanmamis
                # cizgilerin agirligi yarilanir.
                ww = w_meas[inl].copy()
                unv_in = ~ver[inl]
                for _k in range(10):
                    ww[unv_in] *= 0.5
                    v3 = fit_vp_weighted(L[inl], M[inl], ww, v_init=v, n_iter=2)
                    if v3 is not None and admissible(vp_angular_residuals_deg(L, M, v3) / S):
                        v2 = v3
                        break
                else:
                    break
            v = v2
        return v, vp_angular_residuals_deg(L, M, v) / S

    best_cost, best_v = None, None
    admitted = []
    for i, j in pairs:
        cand = np.cross(L[i], L[j])
        cn = np.linalg.norm(cand)
        if cn < 1e-12:
            continue
        v, z = refine(cand / cn)
        if not admissible(z):
            continue
        cost = float(np.sum(np.minimum(z * z, gate_z ** 2)))
        admitted.append((cost, v))
        if best_cost is None or cost < best_cost - 1e-9:
            best_cost, best_v = cost, v
    if best_v is None:
        return None

    # HIPOTEZ BELIRSIZLIGI: en iyi hipotezden GEOMETRIK OLARAK belirgin
    # bicimde farkli (herhangi bir cizgi orta noktasindan gorulen yon farki
    # > 1°) ama MSAC maliyeti yakin bir rakip var mi? Ornek: goz hizasindaki
    # bir referans kenari ufka yakin oldugunda, yan duvar/zemin cizgilerinin
    # ortak VP'si de referans kisitini gecebilir. Inlier-kosullu belirsizlik
    # (MC) bunu GOREMEZ; bu fark (ki-kare biriminde) gorur.
    def _max_dir_diff_deg(v1, v2):
        a1 = np.arctan2(v1[1] - M[:, 1] * v1[2], v1[0] - M[:, 0] * v1[2])
        a2 = np.arctan2(v2[1] - M[:, 1] * v2[2], v2[0] - M[:, 0] * v2[2])
        d = np.abs(a1 - a2) % np.pi
        return float(np.degrees(np.max(np.minimum(d, np.pi - d))))
    rival_gap = None
    for cost, v in admitted:
        if _max_dir_diff_deg(v, best_v) > 1.0:
            gap = cost - best_cost
            if rival_gap is None or gap < rival_gap:
                rival_gap = gap

    v = best_v
    for _ in range(5):
        z = vp_angular_residuals_deg(L, M, v) / S
        v2 = fit_vp_weighted(L, M, w_meas * _tukey_weights(z), v_init=v, n_iter=2)
        if v2 is None:
            break
        converged = abs(abs(float(v2 @ v)) - 1.0) < 1e-14
        v = v2
        if converged:
            break
    theta = vp_angular_residuals_deg(L, M, v)
    z = theta / S
    if not admissible(z):  # IRLS kisitlari bozduysa MSAC cozumune geri don
        v = best_v
        theta = vp_angular_residuals_deg(L, M, v)
        z = theta / S
    inl = z <= gate_z
    wr = _tukey_weights(z)
    n_in = int(inl.sum())
    chi2_red = float(np.sum(z[inl] ** 2) / (n_in - 2)) if n_in > 2 else None
    return {
        "v": v / np.linalg.norm(v), "inliers": inl, "z": z, "theta_deg": theta,
        "w_meas": w_meas, "w_robust": wr, "w_eff": w_meas * wr,
        "verified_outliers": [int(k) for k in np.flatnonzero(ver & ~inl)],
        "chi2_red": chi2_red, "n_inliers": n_in, "cost": best_cost, "n_hypotheses": len(pairs),
        "rival_gap": rival_gap,
    }


def _perturbed_vp_samples(obs, v, n_mc, rng):
    """Parametrik bootstrap: her cizgiyi KENDI belirsizligiyle (orta nokta
    etrafinda aci ~ N(0, sigma_theta), dik kayma ~ N(0, sigma_e/sqrt(n)))
    rastgele bozup VP'yi AYNI agirliklarla yeniden fit eder. Az cizgi (2-3)
    varken de tanimlidir (yeniden-ornekleme bootstrap'i o durumda dejenere
    olur)."""
    L0, M, S = _obs_arrays(obs)
    w = 1.0 / S ** 2
    ang = np.radians(np.array([o.angle_deg for o in obs], dtype=np.float64))
    shift_sig = np.array([o.endpoint_sigma_px / math.sqrt(max(2, o.n_support or 2)) for o in obs])
    unver = np.array([not o.verified for o in obs])
    out = []
    for _ in range(n_mc):
        # Dogrulanmamis (otomatik) cizgilerin hatasinin bir kismi ORTAKTIR
        # (artik lens distorsiyonu, sistematik kenar kaymasi): N cizgi
        # eklemek bu bileseni ortalamayla AZALTMAZ. Her ornekte tum
        # otomatik cizgilere ayni ek donme uygulanir.
        common = np.radians(rng.normal(0.0, LINE_COMMON_SIGMA_DEG_UNVERIFIED)) * unver
        a = ang + np.radians(rng.normal(0.0, S)) + common
        d = np.column_stack([np.cos(a), np.sin(a)])
        nrm = np.column_stack([-d[:, 1], d[:, 0]])
        m = M + nrm * rng.normal(0.0, shift_sig)[:, None]
        Lk = np.column_stack([nrm, -(nrm * m).sum(axis=1)])
        vk = fit_vp_weighted(Lk, m, w, v_init=v, n_iter=2)
        if vk is not None:
            out.append(vk)
    return out


def vp_direction_uncertainty_deg(obs, v, eval_points, n_mc=60, seed=0, chi2_red=None):
    """VP'nin, verilen noktalardan GORULEN yon belirsizligi (derece, 1-sigma).
    Sonlu/sonsuz VP icin aynen tanimli (Oklid VP piksel-STD'si sonsuza
    yakin VP'lerde yaniltici olur). Gozlenen kalintilar beklenenden buyukse
    (indirgenmis ki-kare > 1) belirsizlik sqrt(chi2_red) ile buyutulur -
    standart kovaryans olcekleme."""
    if len(obs) < 2:
        return [None] * len(eval_points)
    rng = np.random.default_rng(seed)
    samples = _perturbed_vp_samples(obs, v, n_mc, rng)
    infl = math.sqrt(chi2_red) if (chi2_red is not None and chi2_red > 1.0) else 1.0
    out = []
    for e in eval_points:
        angs = [vp_direction_angle_at(vk, e) for vk in samples]
        out.append(_circular_std_deg_pi(angs) * infl if len(angs) >= 5 else None)
    return out


def family_spatial_support(obs, img_size=None, weights=None):
    """Bir cizgi ailesinin UZAMSAL kapsamasi. Bir VP'nin hassasiyetini en
    cok belirleyen buyukluk, cizgilerin aile yonune DIK dogrultudaki
    yayilimidir (aralarinda d mesafesi olan iki cizginin aci hatalari, VP
    konumuna ~mesafe^2/d ile yansir). Ayni pencerede toplanmis 5 cizgi,
    cepheye yayilmis 3 uzun cizgiden daha az bilgi tasiyabilir.

    score = perp_span_frac (goruntu kosegenine oranla dik yayilim, 0-1)."""
    if not obs:
        return None
    pts = np.array([p for o in obs for p in (o.p1, o.p2)], dtype=np.float64)
    mids = np.array([o.midpoint for o in obs], dtype=np.float64)
    lengths = np.array([o.length_px for o in obs], dtype=np.float64)
    w = np.ones(len(obs)) if weights is None else np.asarray(weights, dtype=np.float64)
    if img_size:
        W, H = float(img_size[0]), float(img_size[1])
    else:
        W = max(float(np.ptp(pts[:, 0])), 1.0)
        H = max(float(np.ptp(pts[:, 1])), 1.0)
    diag = math.hypot(W, H)
    two = np.radians(2.0 * np.array([o.angle_deg for o in obs]))
    ww = w * lengths
    mean_ang = math.atan2(float(np.sum(ww * np.sin(two))), float(np.sum(ww * np.cos(two)))) / 2.0
    d = np.array([math.cos(mean_ang), math.sin(mean_ang)])
    nrm = np.array([-d[1], d[0]])
    perp = mids @ nrm
    along = pts @ d
    hull = _convex_hull_2d([tuple(m) for m in mids])
    hull_area = _polygon_area(hull) if len(hull) >= 3 else 0.0
    perp_span = float(np.ptp(perp)) / diag if len(obs) > 1 else 0.0
    return {
        "n_lines": len(obs),
        "total_weighted_length_px": float(np.sum(ww)),
        "x_span_frac": float(np.ptp(pts[:, 0])) / W,
        "y_span_frac": float(np.ptp(pts[:, 1])) / H,
        "hull_area_frac": hull_area / (W * H),
        "perp_span_frac": perp_span,
        "along_span_frac": float(np.ptp(along)) / diag,
        "score": min(1.0, perp_span),
    }


def holdout_line_validation(obs, est, seed=0, k_folds=5, n_mc=30):
    """BAGIMSIZ (fit'e katilmayan) dogrulama.

    - Dogrulanmis yardimci cizgiler icin LEAVE-ONE-OUT: cizgi cikarilir,
      VP TAM saglam kestiriciyle (RANSAC dahil) yeniden kestirilir, cikarilan
      cizginin bu VP'ye kalintisi z = theta / sqrt(sigma_line^2 + sigma_vp^2)
      ile olculur (sigma_vp: azaltilmis fit'in o noktadaki yon belirsizligi).
    - Otomatik inlier'lar icin K-katli capraz dogrulama (>=5 ise). Not:
      inlier secimi tum veriyle yapildigi icin bu kisim hafif iyimserdir.
    Referans cizgisi hicbir zaman disarida birakilmaz (A,B,C metrigi tanimlar)."""
    out = {"loo": [], "cv_z": [], "cv_theta_deg": [], "cv_rms_z": None, "cv_median_deg": None}
    for i, o in enumerate(obs):
        if not o.verified or o.is_reference:
            continue
        sub = obs[:i] + obs[i + 1:]
        e = estimate_vp_weighted(sub, seed=seed, max_hypotheses=300)
        if e is None or e["n_inliers"] < 2:
            out["loo"].append({"line_id": o.line_id, "theta_deg": None, "z": None, "vp_unc_deg": None})
            continue
        inl_obs = [sub[k] for k in np.flatnonzero(e["inliers"])]
        unc = vp_direction_uncertainty_deg(inl_obs, e["v"], [o.midpoint], n_mc=n_mc, seed=seed,
                                           chi2_red=e["chi2_red"])[0]
        theta = float(vp_angular_residuals_deg(o.homogeneous_line[None, :], np.array([o.midpoint]), e["v"])[0])
        sig = math.hypot(o.sigma_angle_deg, unc or 0.0)
        out["loo"].append({"line_id": o.line_id, "theta_deg": theta, "z": theta / sig, "vp_unc_deg": unc})

    inl_all = [int(k) for k in np.flatnonzero(est["inliers"])]
    au = [k for k in inl_all if not obs[k].verified]
    if len(au) >= 5:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(au)
        folds = np.array_split(perm, min(k_folds, len(au)))
        L, M, S = _obs_arrays(obs)
        w = 1.0 / S ** 2
        for f in folds:
            fset = set(int(x) for x in f)
            fit_idx = [k for k in inl_all if k not in fset]
            v = fit_vp_weighted(L[fit_idx], M[fit_idx], w[fit_idx], v_init=est["v"], n_iter=3)
            if v is None:
                continue
            fi = np.array(sorted(fset))
            t = vp_angular_residuals_deg(L[fi], M[fi], v)
            out["cv_theta_deg"] += [float(x) for x in t]
            out["cv_z"] += [float(x) for x in t / S[fi]]
        if out["cv_z"]:
            out["cv_rms_z"] = float(np.sqrt(np.mean(np.square(out["cv_z"]))))
            out["cv_median_deg"] = float(np.median(out["cv_theta_deg"]))
    return out


FAMILY_NAMES = {"ab": "AB", "ac": "AC"}


def estimate_family_vps(obs_ab, obs_ac, ref_point, img_size=None, seed=0, validate=True, n_mc=60):
    """Iki aile (AB, AC) icin VP'leri kestirir ve her aileyi teshis eder.

    Bir otomatik/dogrulanmamis cizgi (ayni line_id) HER IKI ailede de inlier
    cikarsa, daha kucuk normalize kalintiya sahip aileye atanir, digerinden
    cikarilip o aile yeniden kestirilir - ayni kanit iki kez kullanilmaz.

    Bir aile ancak referans disinda yeterli destek varsa gecerlidir: en az 1
    dogrulanmis yardimci cizgi YA DA en az 2 dogrulanmamis cizgi."""
    stage = {"ok": False, "families": {}, "reasons": []}
    pools = {"ab": list(obs_ab), "ac": list(obs_ac)}
    ests = {fam: estimate_vp_weighted(pools[fam], seed=seed + k) for k, fam in enumerate(("ab", "ac"))}

    if ests["ab"] is not None and ests["ac"] is not None:
        def unverified_inliers(fam):
            return {pools[fam][i].line_id: i for i in np.flatnonzero(ests[fam]["inliers"])
                    if not pools[fam][i].verified and pools[fam][i].line_id}
        ia, ic = unverified_inliers("ab"), unverified_inliers("ac")
        common = set(ia) & set(ic)
        if common:
            drop = {"ab": set(), "ac": set()}
            for lid in common:
                if ests["ab"]["z"][ia[lid]] <= ests["ac"]["z"][ic[lid]]:
                    drop["ac"].add(lid)
                else:
                    drop["ab"].add(lid)
            for k, fam in enumerate(("ab", "ac")):
                if drop[fam]:
                    pools[fam] = [o for o in pools[fam] if o.line_id not in drop[fam]]
                    ests[fam] = estimate_vp_weighted(pools[fam], seed=seed + k)

    for fam in ("ab", "ac"):
        est, pool = ests[fam], pools[fam]
        fd = {"est": est, "pool": pool, "ok": False}
        name = FAMILY_NAMES[fam]
        if est is None:
            fd["reason"] = (f"{name} yonu: referans kenariyla tutarli bir kacis yonu kurulamadi "
                            f"(yeterli paralel kenar kaniti yok).")
        else:
            inl_idx = [int(k) for k in np.flatnonzero(est["inliers"])]
            inl_obs = [pool[k] for k in inl_idx]
            n_helpers = sum(1 for o in inl_obs if o.verified and not o.is_reference)
            n_unver = sum(1 for o in inl_obs if not o.verified)
            # Yon belirsizligi SADECE referanstan degil, goruntu boyunca (3x3
            # izgara) olculur: AB ailesinde A'dan gorulen yon referans
            # kenarla zaten sabittir, VP hatasi UZAK bolgelerde ortaya cikar.
            probes = [ref_point] + ([(x * img_size[0], y * img_size[1]) for x in (0.05, 0.5, 0.95)
                                     for y in (0.05, 0.5, 0.95)] if img_size else [])
            uncs = vp_direction_uncertainty_deg(inl_obs, est["v"], probes, n_mc=n_mc, seed=seed,
                                                chi2_red=est["chi2_red"])
            finite_uncs = [u for u in uncs if u is not None]
            fd.update({
                "inlier_obs": inl_obs, "n_inliers": len(inl_obs),
                "n_verified_helpers": n_helpers, "n_unverified": n_unver,
                "unc_deg": max(finite_uncs) if finite_uncs else None,
                "unc_deg_at_ref": uncs[0],
                "spatial": family_spatial_support(inl_obs, img_size, weights=est["w_robust"][inl_idx]),
                "line_status": {pool[k].line_id: {"z": float(est["z"][k]), "inlier": bool(est["inliers"][k]),
                                                  "verified": bool(pool[k].verified)}
                                for k in range(len(pool)) if pool[k].line_id},
                "verified_outlier_ids": [pool[k].line_id for k in est["verified_outliers"]],
            })
            gap = est.get("rival_gap")
            if n_helpers == 0 and n_unver < 2:
                fd["reason"] = (f"{name} yonu: referans kenari disinda tutarli yeterli cizgi yok (en az 1 "
                                f"yardimci cizgi ya da 2 otomatik cizgi gerekli).")
            elif n_helpers == 0 and n_unver < AMBIGUITY_MIN_AUTO and gap is not None and gap < AMBIGUITY_GAP_CHI2:
                # Sentetik benchmark (tests/benchmark_helper_lines.py, 'sparse'):
                # bu durumda projektif model cogunlukla FELAKET hatali (medyan
                # %263) iken yerel afin model %14 - bu yuzden KULLANILMAZ.
                fd["ambiguous"] = True
                fd["reason"] = (f"{name} yonu: otomatik kanit BELIRSIZ - yalnizca {n_unver} otomatik cizgi var ve "
                                f"farkli bir kacis noktasi hipotezi neredeyse ayni derecede destekleniyor (baska "
                                f"bir duvar/zemin cizgileri olabilir). Bu yonde, ayni yuzeyde uzun ve net bir "
                                f"paralel kenari yardimci cizgi olarak ekleyin.")
            else:
                fd["ok"] = True
                if validate:
                    fd["validation"] = holdout_line_validation(pool, est, seed=seed)
        if fd.get("reason"):
            stage["reasons"].append(fd["reason"])
        stage["families"][fam] = fd
    stage["ok"] = all(stage["families"][f]["ok"] for f in ("ab", "ac"))
    stage["ambiguous_families"] = [f for f in ("ab", "ac") if stage["families"][f].get("ambiguous")]
    return stage


def _scale_eval_points(H, l_inf, A, img_size, ab_m, ac_m):
    """Olcek belirsizligi icin degerlendirme noktalari: goruntunun 3x3
    izgarasi (yoksa referansin 3 kati alani), sadece referansla kacis
    cizgisinin AYNI tarafinda ve ufka cok yakin olmayanlar."""
    if img_size:
        W, Hh = img_size
        cand = [(x, y) for x in (0.02 * W, 0.5 * W, 0.98 * W) for y in (0.02 * Hh, 0.5 * Hh, 0.98 * Hh)]
    else:
        cand = [(A[0] + dx, A[1] + dy) for dx in (-300, 0, 300) for dy in (-300, 0, 300)]
    wA = float(l_inf @ np.array([A[0], A[1], 1.0]))
    out = []
    for p in cand:
        wp = float(l_inf @ np.array([p[0], p[1], 1.0]))
        if wp * wA > 0 and abs(wp) >= 0.05 * abs(wA):
            out.append(p)
    return out


def _scale_uncertainty_mc(A, B, C, ab_m, ac_m, angle_deg, fam_ab, fam_ac, core, img_size, n_mc=40, seed=0):
    """VP belirsizliginin METRIK olcume yansimasi: iki ailenin inlier
    cizgileri birlikte bozulur, H yeniden kurulur, degerlendirme
    noktalarinda (dunya X ve Y yonunde) kisa bir dunya parcasinin olculen
    uzunlugunun goreli sapmasi hesaplanir. Doner: (en kotu nokta/eksen
    1-sigma goreli std, ortalama) - ya da (None, None)."""
    pts = _scale_eval_points(core["H"], core["l_inf"], A, img_size, ab_m, ac_m)
    if not pts:
        return None, None
    rng = np.random.default_rng(seed)
    s_ab = _perturbed_vp_samples(fam_ab["inlier_obs"], fam_ab["est"]["v"], n_mc, rng)
    s_ac = _perturbed_vp_samples(fam_ac["inlier_obs"], fam_ac["est"]["v"], n_mc, rng)
    delta = 0.01 * max(ab_m, ac_m)
    segs = []
    for p in pts:
        try:
            X = apply_transform(core["H"], p)
            for e in ((1.0, 0.0), (0.0, 1.0)):
                q = apply_transform(core["Hinv"], (X[0] + delta * e[0], X[1] + delta * e[1]))
                segs.append((p, q))
        except ValueError:
            continue
    if not segs:
        return None, None
    rel = [[] for _ in segs]
    for va, vc in zip(s_ab, s_ac):
        ck = _stratified_metric_from_vps(A, B, C, ab_m, ac_m, angle_deg, va, vc)
        if ck is None:
            continue
        for k, (p, q) in enumerate(segs):
            try:
                rel[k].append(dist(apply_transform(ck["H"], p), apply_transform(ck["H"], q)) / delta - 1.0)
            except ValueError:
                pass
    stds = [float(np.std(r)) for r in rel if len(r) >= 5]
    if not stds:
        return None, None
    return max(stds), float(np.mean(stds))


def _known_length_rel_error(H, known_segments):
    if not known_segments:
        return None
    errs = []
    for p, q, true_m in known_segments:
        try:
            m = dist(apply_transform(H, p), apply_transform(H, q))
        except ValueError:
            continue
        if true_m and true_m > 0:
            errs.append(abs(m / true_m - 1.0))
    return float(np.mean(errs)) if errs else None


def classify_projective_confidence(res):
    """Guveni TEK opak skor yerine ayri, gorunur bilesenlerden siniflar:
    uzak-bolge olcek belirsizligi (%), bagimsiz dogrulama (LOO / CV) ve
    dogrulama verisinin VARLIGI. Bagimsiz dogrulamasi olmayan bir model,
    kendi inlier'larina ne kadar iyi uysa da YUKSEK alamaz."""
    reasons = []
    val_ok, has_val_both, verified_both = True, True, True
    for fam in ("ab", "ac"):
        name = FAMILY_NAMES[fam]
        if res["families"][fam]["n_verified_helpers"] == 0:
            # Otomatik cizgilerin ORTAK/sistematik hatasi (ör. artik lens
            # distorsiyonu) yine otomatik cizgilerle dogrulanamaz - sentetik
            # benchmark'ta yerel+yanli otomatik kanit, dusuk tahmini
            # belirsizlige ragmen buyuk hatalar uretebildi.
            verified_both = False
            reasons.append(f"{name}: elle dogrulanmis yardimci cizgi yok - otomatik cizgilerin sistematik "
                           f"hatasi dogrulanamiyor")
        v = res["families"][fam].get("validation") or {}
        loo_z = [x["z"] for x in v.get("loo", []) if x.get("z") is not None]
        bad_loo = [x["line_id"] for x in v.get("loo", []) if x.get("z") is not None and x["z"] > VP_GATE_Z]
        if bad_loo:
            val_ok = False
            reasons.append(f"{name}: {', '.join(bad_loo)} diger kanitla tutarsiz (bagimsiz dogrulama z>3)")
        if v.get("cv_rms_z") is not None and v["cv_rms_z"] > 2.0:
            val_ok = False
            reasons.append(f"{name}: otomatik cizgilerin capraz-dogrulama kalintisi yuksek (RMS z={v['cv_rms_z']:.1f})")
        if not loo_z and v.get("cv_rms_z") is None:
            has_val_both = False
            reasons.append(f"{name}: bagimsiz dogrulama verisi yok (en az 2 yardimci cizgi ya da 5+ otomatik cizgi gerekir)")
    su = res.get("scale_unc_far")
    if su is not None and su <= CONF_SCALE_UNC_HIGH and val_ok and has_val_both and verified_both:
        return "YUKSEK", reasons
    if (su is None or su <= CONF_SCALE_UNC_MID) and val_ok:
        return "ORTA", reasons
    if su is not None and su > CONF_SCALE_UNC_MID:
        reasons.append(f"uzak bolgelerde olcek belirsizligi yuksek (~%{su * 100:.1f}, 1-sigma)")
    return "DUSUK", reasons


def compute_metric_homography_from_observations(A, B, C, ab_m, ac_m, angle_deg, obs_ab=None, obs_ac=None,
                                                img_size=None, stage=None, seed=0, known_segments=None,
                                                n_mc_scale=40):
    """ANA tek-fotograf cozucusu (kademeli rektifikasyon, gozlem tabanli):

        saglam v_AB, v_AC (agirlikli, dogrulanmis-kisitli)
        -> l_inf = v_AB x v_AC -> H_p (projektif->afin)
        -> T_metric (A/B/C GERCEK geometri, TAM) -> H_final -> D*

    Yardimci cizgiler SADECE v_AB/v_AC'yi (ve dolayisiyla l_inf'i) etkiler;
    metrik olcek her zaman A/B/C'den gelir. stage (estimate_family_vps
    sonucu) verilirse VP asamasi yeniden hesaplanmaz (uzunluklar VP'yi
    etkilemez - canli yazarken onbellek icin).

    Doner: compute_metric_homography_stratified ile AYNI anahtarlar + yeni
    teshis alanlari (families, scale_unc_far, confidence, ...), ya da None
    (stage['reasons'] nedeni aciklar)."""
    if stage is None:
        stage = estimate_family_vps(obs_ab, obs_ac, A, img_size=img_size, seed=seed)
    if not stage["ok"]:
        return None
    fa, fc = stage["families"]["ab"], stage["families"]["ac"]
    v_ab, v_ac = fa["est"]["v"], fc["est"]["v"]
    core = _stratified_metric_from_vps(A, B, C, ab_m, ac_m, angle_deg, v_ab, v_ac, require_same_side=True)
    if core is None:
        stage["reasons"].append("Kestirilen kacis cizgisi A/B/C'nin arasindan geciyor - fiziksel olarak "
                                "gecersiz; yardimci cizgileri kontrol edin.")
        return None
    H_final, Hinv_final, H_p = core["H"], core["Hinv"], core["H_p"]
    Aw, Bw, Cw = (apply_transform(H_final, p) for p in (A, B, C))
    v1 = (Bw[0] - Aw[0], Bw[1] - Aw[1])
    v2 = (Cw[0] - Aw[0], Cw[1] - Aw[1])
    ab_rec, ac_rec = dist(Aw, Bw), dist(Aw, Cw)
    scale_unc_far, scale_unc_mean = _scale_uncertainty_mc(A, B, C, ab_m, ac_m, angle_deg, fa, fc, core,
                                                          img_size, n_mc=n_mc_scale, seed=seed)
    families = {}
    for fam, f in (("ab", fa), ("ac", fc)):
        est = f["est"]
        inl = est["inliers"]
        families[fam] = {
            "n_inliers": f["n_inliers"], "n_verified_helpers": f["n_verified_helpers"],
            "n_unverified": f["n_unverified"], "unc_deg": f["unc_deg"], "spatial": f["spatial"],
            "validation": f.get("validation"),
            "residual_rms_deg": float(np.sqrt(np.average(est["theta_deg"][inl] ** 2, weights=est["w_meas"][inl]))),
            "line_status": f["line_status"], "verified_outlier_ids": f["verified_outlier_ids"],
            "is_infinite": abs(est["v"][2]) < 1e-6 * max(1.0, float(np.linalg.norm(est["v"][:2]))),
        }
    res = {
        "H": H_final, "Hinv": Hinv_final, "D_img": core["D_img"], "world_D": core["world_D"],
        "world_A": core["world_A"], "world_B": core["world_B"], "world_C": core["world_C"],
        "H_p": H_p, "l_inf": core["l_inf"], "v_ab_hom": v_ab, "v_ac_hom": v_ac,
        "n_inliers_ab": fa["n_inliers"], "n_inliers_ac": fc["n_inliers"],
        "v_ab_uncertainty": {"angular_std_deg": fa["unc_deg"]},
        "v_ac_uncertainty": {"angular_std_deg": fc["unc_deg"]},
        "affine_residual_ab_deg": _rectified_orientation_std_deg(H_p, [(o.p1, o.p2) for o in fa["inlier_obs"]]),
        "affine_residual_ac_deg": _rectified_orientation_std_deg(H_p, [(o.p1, o.p2) for o in fc["inlier_obs"]]),
        "ab_recovered": ab_rec, "ac_recovered": ac_rec, "ab_input": ab_m, "ac_input": ac_m,
        "angle_recovered_deg": _angle_between_dirs(v1, v2), "angle_input_deg": angle_deg,
        "ref_scale": (dist(A, B) + dist(A, C)) / 2.0,
        "ref_recovery_rel_err": max(abs(ab_rec - ab_m) / ab_m, abs(ac_rec - ac_m) / ac_m),
        "scale_unc_far": scale_unc_far, "scale_unc_mean": scale_unc_mean,
        "known_length_rel_err": _known_length_rel_error(H_final, known_segments),
        "families": families, "stage": stage,
    }
    res["confidence"], res["confidence_reasons"] = classify_projective_confidence(res)
    return res


def _rms(values):
    vals = [v for v in values if v is not None]
    return float(np.sqrt(np.mean(np.square(vals)))) if vals else None


def summarize_model_validation(res):
    """Model karsilastirmasi icin AYRI AYRI gorunur bilesenler (tek bir opak
    skor degil): aile basina VP yon belirsizligi, bagimsiz (hold-out)
    kalinti, uzamsal kapsama, in-sample kalinti; ayrica referans geri-kazanim
    hatasi, uzak-bolge olcek belirsizligi, bilinen-uzunluk hatasi."""
    if res is None:
        return None
    out = {"scale_unc_far": res.get("scale_unc_far"), "confidence": res.get("confidence"),
           "ref_recovery_rel_err": res.get("ref_recovery_rel_err"),
           "known_length_rel_err": res.get("known_length_rel_err")}
    for fam in ("ab", "ac"):
        f = res["families"][fam]
        val = f.get("validation") or {}
        zs = [x["z"] for x in val.get("loo", [])] + list(val.get("cv_z", []))
        ths = [x["theta_deg"] for x in val.get("loo", [])] + list(val.get("cv_theta_deg", []))
        ths = [t for t in ths if t is not None]
        out[f"vp_unc_deg_{fam}"] = f["unc_deg"]
        out[f"holdout_rms_z_{fam}"] = _rms(zs)
        out[f"holdout_median_deg_{fam}"] = float(np.median(ths)) if ths else None
        out[f"spatial_{fam}"] = (f["spatial"] or {}).get("perp_span_frac")
        out[f"residual_rms_deg_{fam}"] = f["residual_rms_deg"]
        out[f"n_lines_{fam}"] = f["n_inliers"]
    return out


def _line_z_under_family(new_obs, fam_stage, seed=0, n_mc=40):
    """Yeni bir cizginin, bir ailenin MEVCUT VP'sine normalize kalintisi
    (VP'nin o noktadaki belirsizligi dahil)."""
    est = fam_stage["est"]
    theta = float(vp_angular_residuals_deg(new_obs.homogeneous_line[None, :], np.array([new_obs.midpoint]),
                                           est["v"])[0])
    unc = vp_direction_uncertainty_deg(fam_stage["inlier_obs"], est["v"], [new_obs.midpoint], n_mc=n_mc,
                                       seed=seed, chi2_red=est["chi2_red"])[0]
    return theta, theta / math.hypot(new_obs.sigma_angle_deg, unc or 0.0), unc


def suggest_line_family(new_obs, res, seed=0):
    """'auto' aileli bir yardimci cizgi icin ONERI (kesin karar degil).
    Yerel aciya degil, VP tutarliligina bakar: l^T v_AB ~ 0 mi, l^T v_AC ~ 0
    mi? Bir aile ancak (a) z <= 3 ve (b) log-olabilirlik farki
    (z_diger^2 - z_secilen^2)/2 >= 4.5 (~90:1) ise onerilir; aksi halde None
    (belirsiz - kullaniciya sorulur)."""
    if res is None:
        return None, {}
    zs = {}
    for fam in ("ab", "ac"):
        f = res["stage"]["families"][fam]
        if not f.get("ok"):
            continue
        _theta, z, _unc = _line_z_under_family(new_obs, f, seed=seed)
        zs[fam] = z
    if len(zs) < 2:
        return None, zs
    best = min(zs, key=zs.get)
    other = "ac" if best == "ab" else "ab"
    if zs[best] <= VP_GATE_Z and zs[other] ** 2 - zs[best] ** 2 >= 9.0:
        return best, zs
    return None, zs


def helper_duplicates_reference(p1, p2, ref_p, ref_q, angle_tol_deg=2.0, offset_px=None):
    """Yardimci cizgi, referans cizgisiyle (A-B ya da A-C) neredeyse AYNI
    goruntu dogrusu uzerinde mi? Ayni dogru bagimsiz projektif bilgi
    tasimaz (VP'yi yalnizca referansin kendisi kadar belirler)."""
    a1 = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
    a2 = math.degrees(math.atan2(ref_q[1] - ref_p[1], ref_q[0] - ref_p[0]))
    da = abs(a1 - a2) % 180.0
    da = min(da, 180.0 - da)
    l = _line_through(ref_p, ref_q)
    nrm = math.hypot(l[0], l[1])
    if nrm < 1e-12:
        return False
    mid = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    off = abs(l[0] * mid[0] + l[1] * mid[1] + l[2]) / nrm
    tol = offset_px if offset_px is not None else max(5.0, 0.05 * dist(ref_p, ref_q))
    return da <= angle_tol_deg and off <= tol


def assess_helper_addition(A, B, C, ab_m, ac_m, angle_deg, obs_ab, obs_ac, new_obs, img_size=None,
                           known_segments=None, seed=0):
    """Yeni bir yardimci cizgiyi KABUL ETMEDEN ONCE aday modeli hesaplar ve
    eski modelle karsilastirir (Bolum 20-24).

    verdict:
      accept               - mevcut modelle tutarli, dogrulama kotulesmedi
      accept_validated     - catisma vardi ama BAGIMSIZ veri (diger
                             yardimci cizgilerin LOO kalintisi / bilinen
                             uzunluklar) yeni modeli destekliyor
      accept_unvalidated   - onceden model yoktu; karsilastirma yapilamaz
      inconsistent / worse - catisma var, karar icin bagimsiz veri yok -> kullaniciya sor
      rejected_by_validation - bagimsiz veri ESKI modeli destekliyor -> kullaniciya sor
      no_model             - bu cizgiyle de model kurulamiyor"""
    fam = new_obs.family
    before = compute_metric_homography_from_observations(A, B, C, ab_m, ac_m, angle_deg, obs_ab, obs_ac,
                                                         img_size=img_size, seed=seed, known_segments=known_segments)
    nab = list(obs_ab) + ([new_obs] if fam == "ab" else [])
    nac = list(obs_ac) + ([new_obs] if fam == "ac" else [])
    after = compute_metric_homography_from_observations(A, B, C, ab_m, ac_m, angle_deg, nab, nac,
                                                        img_size=img_size, seed=seed, known_segments=known_segments)
    out = {"family": fam, "before": summarize_model_validation(before), "after": summarize_model_validation(after),
           "before_result": before, "after_result": after, "z_before": None, "theta_before": None,
           "outlier_in_after": False, "worse": False, "verdict": None}
    if before is not None:
        theta, z, _unc = _line_z_under_family(new_obs, before["stage"]["families"][fam], seed=seed)
        out["theta_before"], out["z_before"] = theta, z
    if after is not None:
        out["outlier_in_after"] = new_obs.line_id in after["families"][fam]["verified_outlier_ids"]
    if after is None:
        out["verdict"] = "no_model"
        return out
    if before is None:
        out["verdict"] = "accept_unvalidated"
        return out
    sb, sa = out["before"], out["after"]
    ub, ua = sb[f"vp_unc_deg_{fam}"], sa[f"vp_unc_deg_{fam}"]
    # Bagimsiz kalinti AYNI dogrulama kumesi uzerinden karsilastirilir: yeni
    # cizginin kendi LOO kalintisi 'sonra' tarafindan cikarilir (onun
    # tutarliligi zaten z_before ile ayrica olculuyor).
    hb = sb[f"holdout_rms_z_{fam}"]
    val_a = after["families"][fam].get("validation") or {}
    ha = _rms([x["z"] for x in val_a.get("loo", []) if x["line_id"] != new_obs.line_id]
              + list(val_a.get("cv_z", [])))
    # Esik: MC belirsizlik tahmininin kendi istatistik gurultusu (~%10, maks.
    # 10 prob noktasi) sahte 'kotulesme' uretmesin diye 1.5x.
    worse = (ub is not None and ua is not None and ua > 1.5 * ub + 1e-6) or \
            (hb is not None and ha is not None and ha > 1.25 * hb + 0.25)
    out["worse"] = worse
    consistent = out["z_before"] <= VP_GATE_Z and not out["outlier_in_after"]
    if consistent and not worse:
        out["verdict"] = "accept"
        return out
    # Catisma: bagimsiz veri (ayni ailenin DIGER yardimci cizgilerinin LOO
    # kalintisi + bilinen uzunluklar) hangi modeli destekliyor?
    other_ids = {o.line_id for o in (obs_ab if fam == "ab" else obs_ac) if o.verified and not o.is_reference}
    def loo_map(r):
        val = r["families"][fam].get("validation") or {}
        return {x["line_id"]: x["z"] for x in val.get("loo", []) if x.get("z") is not None}
    lb, la = loo_map(before), loo_map(after)
    common = [i for i in other_ids if i in lb and i in la]
    evidence = []
    if common:
        evidence.append(_rms([la[i] for i in common]) < _rms([lb[i] for i in common]))
    kb, ka = sb["known_length_rel_err"], sa["known_length_rel_err"]
    if kb is not None and ka is not None:
        evidence.append(ka < kb)
    out["independent_evidence"] = evidence
    if evidence and all(evidence):
        out["verdict"] = "accept_validated"
    elif evidence:
        out["verdict"] = "rejected_by_validation"
    else:
        out["verdict"] = "inconsistent" if not consistent else "worse"
    return out


def detect_line_observations(gray, max_segments=250, min_length_px=25):
    """detect_line_segments (LSD/Hough) sonucunu LineObservation'a cevirir:
    her parcanin gradyan gucu (kenar kontrasti) ve tespit olcegine bagli
    uc-nokta belirsizligi hesaplanir. Zayif kontrastli parcalar daha buyuk
    sigma alir (sigma_e ~ 0.7px/olcek * medyan_guc/guc, [0.5, 3] ile
    sinirli). Otomatik cizgiler DOGRULANMAMIS (verified=False) isaretlenir."""
    segs = detect_line_segments(gray, max_segments=max_segments, min_length_px=min_length_px)
    if not segs:
        return []
    h, w = gray.shape[:2]
    scale = min(1.0, 1600.0 / max(h, w))
    small = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA) if scale < 1 else gray
    mag = _gradient_magnitude(small)
    sh, sw = mag.shape
    strengths = []
    for p, q in segs:
        ts = np.linspace(0.1, 0.9, 15)
        xs = np.clip(((p[0] + ts * (q[0] - p[0])) * scale).round().astype(int), 0, sw - 1)
        ys = np.clip(((p[1] + ts * (q[1] - p[1])) * scale).round().astype(int), 0, sh - 1)
        strengths.append(float(np.mean(mag[ys, xs])))
    g_med = float(np.median(strengths)) or 1.0
    obs = []
    for k, ((p, q), g) in enumerate(zip(segs, strengths)):
        length = math.hypot(q[0] - p[0], q[1] - p[1])
        sigma_e = LINE_ENDPOINT_SIGMA_PX["auto"] / scale * float(np.clip(g_med / max(g, 1e-6), 0.5, 3.0))
        obs.append(LineObservation(p, q, source="auto", verified=False, family="auto", line_id=f"AUTO{k}",
                                   endpoint_sigma_px=sigma_e, n_support=max(2, int(length * scale)),
                                   gradient_strength=g))
    return obs


def refine_line_to_edge(gray, p1, p2, search_radius=4.0, min_valid_frac=0.6, max_rms_px=1.0,
                        max_angle_change_deg=3.0, min_contrast_ratio=2.0):
    """Kaba secilmis bir yardimci cizgiyi gercek goruntu kenarina oturtur:
    cizgi boyunca orneklenen noktalarda dik yonde gradyan pikinin subpixel
    konumu bulunur, robust (MAD-tabanli) TLS ile dogru fit edilir, kaba uc
    noktalar bu dogruya izdusurulur. Dusuk kontrast, belirsiz (cift kenar)
    ya da kavisli kenarlarda (None, neden) doner - inceltme ZORLANMAZ.

    Doner: ({p1, p2, n_support, rms_px, strength}, None) ya da (None, neden)."""
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])
    L = math.hypot(x2 - x1, y2 - y1)
    if L < 15:
        return None, "cizgi cok kisa"
    pad = search_radius + 3
    h, w = gray.shape[:2]
    x0 = int(max(0, math.floor(min(x1, x2) - pad)))
    y0 = int(max(0, math.floor(min(y1, y2) - pad)))
    xe = int(min(w, math.ceil(max(x1, x2) + pad) + 1))
    ye = int(min(h, math.ceil(max(y1, y2) + pad) + 1))
    if xe - x0 < 3 or ye - y0 < 3:
        return None, "goruntu disinda"
    mag = _gradient_magnitude(gray[y0:ye, x0:xe])
    d = np.array([(x2 - x1) / L, (y2 - y1) / L])
    nrm = np.array([-d[1], d[0]])
    n = int(np.clip(L / 2.0, 10, 300))
    pts, strengths = [], []
    for t in np.linspace(0.03, 0.97, n) * L:
        c = np.array([x1 - x0, y1 - y0]) + t * d
        offsets, vals = _sample_along(mag, c, nrm, search_radius)
        finite = np.isfinite(vals)
        if finite.sum() < 5:
            continue
        idx = int(np.argmax(np.where(finite, vals, -np.inf)))
        if idx <= 0 or idx >= len(vals) - 1:
            continue  # yaricap icinde net bir tepe yok
        peak = _subpixel_peak(offsets, vals)
        if peak is None:
            continue
        pts.append(c + peak * nrm + np.array([x0, y0]))
        strengths.append(float(vals[idx]))
    if len(pts) < min_valid_frac * n:
        return None, "kenar boyunca yeterli gradyan bulunamadi"
    med_strength = float(np.median(strengths))
    if med_strength < min_contrast_ratio * max(float(np.median(mag)), 1e-6):
        return None, "dusuk kontrast"
    P = np.array(pts)
    keep = np.ones(len(P), dtype=bool)
    for _ in range(3):
        centroid, direction, normal = _fit_line_tls(P[keep])
        r = (P - centroid) @ normal
        s = 1.4826 * float(np.median(np.abs(r[keep]))) + 1e-6
        keep = np.abs(r) <= max(2.5 * s, 0.3)
        if keep.sum() < 5:
            return None, "belirsiz kenar"
    centroid, direction, normal = _fit_line_tls(P[keep])
    r = (P[keep] - centroid) @ normal
    rms = float(np.sqrt(np.mean(r ** 2)))
    if keep.sum() < 0.8 * min_valid_frac * n:
        return None, "belirsiz kenar (cok fazla aykiri ornek)"
    if rms > max_rms_px:
        return None, "kenar duz degil ya da belirsiz"
    ang = math.degrees(math.acos(min(1.0, abs(float(direction @ d)))))
    if ang > max_angle_change_deg:
        return None, "inceltilmis yon kaba secimden cok farkli"
    e1 = centroid + float((np.array([x1, y1]) - centroid) @ direction) * direction
    e2 = centroid + float((np.array([x2, y2]) - centroid) @ direction) * direction
    return {"p1": (float(e1[0]), float(e1[1])), "p2": (float(e2[0]), float(e2[1])),
            "n_support": int(keep.sum()), "rms_px": rms, "strength": med_strength}, None


# =======================================================================
# IKI FOTOGRAF MODU (TWO-PHOTO / MULTI-VIEW GEOMETRY)
#
# Tek-fotograf modu (yukarida), A/B/C + 2 uzunluk + acidan TEK bir goruntu
# icinde kacis cizgisi araciligiyla PROJEKTIF bir duzlem kurar - bu,
# matematiksel olarak temel bir sinir tasir (3 nokta + 2 uzunluk, genel
# 8-serbestlik-dereceli bir homografiyi TEK BASINA belirleyemez; kacis
# noktasi kaniti bu acigi kapatir ama HALA TEK GORUNTUYE bagli kalir).
#
# IKI fotograf modu FARKLI bir kaynaktan (gercek CAMERA HAREKETI -
# essential matrix + triangulation) BAGIMSIZ 3B geometri kurar - klasik
# iki-goruntu Structure-from-Motion (SfM) boru hatti:
#
#   ozellik eslestirme (SIFT+oran testi+simetrik kontrol)
#   -> essential matrix (E, kalibre/normalize koordinatlarda, USAC_MAGSAC)
#   -> goreli poz (R,t - t SADECE YON, olcek BILINMEZ)
#   -> triangulation (3B noktalar, ORTAK bir taban-olcegine gore)
#   -> duzlem fit (RANSAC) + A,B,C ekseni hizalama
#   -> GERCEK uzunluktan (AB/AC) olcek kurtarma (s = gercek/rekonstrukte)
#   -> METRIK 2B duzlem koordinatlari (Oklid, olceklenmis)
#
# ONEMLI: bu, tek-fotograf mimarisinden TAMAMEN BAGIMSIZ bir koddur - iki
# ayri sinama yontemi olarak (Bolum D) birbirleriyle CAPRAZ KONTROL
# edilebilir, ama biri digerini KURMAZ/KIRLETMEZ.
# =======================================================================

def match_features_sift(gray1, gray2, ratio=0.75, max_features=4000):
    """Iki gri-tonlamali goruntu arasinda SIFT ozellik noktalari tespit
    edip GUVENILIR (Lowe oran testi + simetrik/karsilikli kontrol)
    eslesmeler bulur.

    Lowe oran testi: her ozellik icin EN YAKIN VE IKINCI EN YAKIN
    eslesmenin mesafe orani 'ratio'dan kucukse kabul edilir (belirsiz/
    tekrarlayan dokulu eslesmeleri eler). Simetrik kontrol: img1->img2
    VE img2->img1 yonlerinde AYRI AYRI eslestirilip SADECE HER IKI
    yonde de BIRBIRINI secen ciftler tutulur - bu, ozellikle tekrarlayan
    mimari desenlerde (ör. ayni pencere birden fazla kez) YANLIS
    eslesmeleri onemli olcude azaltir (bkz. Bolum C4/C16).

    Doner: {"pts1": Nx2, "pts2": Nx2, "n_keypoints1", "n_keypoints2",
            "n_ratio_pass", "n_symmetric"} - N=0 ise eslesme bulunamadi."""
    sift = cv2.SIFT_create(nfeatures=max_features)
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    empty = {"pts1": np.zeros((0, 2)), "pts2": np.zeros((0, 2)),
             "n_keypoints1": len(kp1) if kp1 else 0, "n_keypoints2": len(kp2) if kp2 else 0,
             "n_ratio_pass": 0, "n_symmetric": 0}
    if des1 is None or des2 is None or len(des1) < 2 or len(des2) < 2:
        return empty

    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches_12 = bf.knnMatch(des1, des2, k=2)
    good_12 = {m.queryIdx: m.trainIdx for m, n in matches_12 if n is not None and m.distance < ratio * n.distance}
    matches_21 = bf.knnMatch(des2, des1, k=2)
    good_21 = {m.queryIdx: m.trainIdx for m, n in matches_21 if n is not None and m.distance < ratio * n.distance}

    pts1, pts2 = [], []
    for i1, i2 in good_12.items():
        if good_21.get(i2) == i1:  # simetrik/karsilikli: img2->img1 de AYNI cifti secmis olmali
            pts1.append(kp1[i1].pt)
            pts2.append(kp2[i2].pt)
    return {"pts1": np.array(pts1, dtype=np.float64), "pts2": np.array(pts2, dtype=np.float64),
            "n_keypoints1": len(kp1), "n_keypoints2": len(kp2),
            "n_ratio_pass": len(good_12), "n_symmetric": len(pts1)}


def _undistort_to_normalized(pts, K, dist=None):
    """Piksel noktalarini, KAMERA MATRISINDEN (K) BAGIMSIZ, NORMALIZE
    kamera koordinatlarina (x=(u-cx)/fx, y=(v-cy)/fy, distorsiyon
    duzeltmesiyle) cevirir - iki FARKLI kameranin (K1!=K2 olabilir)
    essential matrix ile BIRLIKTE islenebilmesi icin GEREKLI ortak
    cerceve budur (bkz. Bolum C3/C6)."""
    pts = np.asarray(pts, dtype=np.float64).reshape(-1, 1, 2)
    d = dist if dist is not None else np.zeros(5)
    und = cv2.undistortPoints(pts, K, d)  # P verilmezse SONUC zaten normalize kamera koordinatlarinda
    return und.reshape(-1, 2)


def estimate_relative_pose_two_view(pts1, pts2, K1, K2, dist1=None, dist2=None,
                                     prob=0.999, threshold_px=1.5):
    """Iki goruntu arasindaki (kalibre edilmemis olsa bile EXIF-yaklasik
    K ile) GORELI KAMERA POZUNU (R,t) essential matrix araciligiyla
    tahmin eder.

    pts1,pts2: (N,2) PIKSEL koordinatlarinda eslesen nokta ciftleri.

    Once NORMALIZE kamera koordinatlarina cevrilir (bkz. _undistort_to_
    normalized - bu, K1!=K2 olan iki FARKLI kamera/lens icin dogru ortak
    cerceve saglar), sonra normalize uzayda (focal=1, pp=(0,0)) essential
    matrix USAC_MAGSAC (mevcut degilse RANSAC) ile saglam sekilde
    kestirilir, cv2.recoverPose ile poz (R, BIRIM-NORM t) ve cheirality
    (pozitif derinlik) kontrolu ile inlier maskesi cikarilir.

    ONEMLI: t SADECE YONDUR - essential matrix'ten gelen oteleme mutlak
    olcekten (metre) BAGIMSIZDIR (klasik bir SfM sinirlamasi, bkz. Bolum
    C6/C7) - gercek metrik olcek SONRADAN, kullanicinin bildigi gercek
    AB/AC uzunluguyla (bkz. recover_scale_from_known_lengths) kurtarilir.

    threshold_px, NORMALIZE koordinat uzayinda degil piksel-esdegeri bir
    tolerans olarak yorumlanir - ortalama fx/fy ile normalize edilir.

    Doner: {"R","t","E","inlier_mask","n_inliers","n_total"} ya da
    yeterli (>=5) eslesme/gecerli poz yoksa None."""
    n = len(pts1)
    if n < 5:
        return None
    p1n = _undistort_to_normalized(pts1, K1, dist1)
    p2n = _undistort_to_normalized(pts2, K2, dist2)

    avg_focal = (K1[0, 0] + K1[1, 1] + K2[0, 0] + K2[1, 1]) / 4.0
    norm_threshold = threshold_px / avg_focal if avg_focal > 1e-9 else 1e-3

    method = getattr(cv2, "USAC_MAGSAC", cv2.RANSAC)
    try:
        E, mask = cv2.findEssentialMat(p1n, p2n, focal=1.0, pp=(0.0, 0.0),
                                        method=method, prob=prob, threshold=norm_threshold)
    except cv2.error:
        return None
    if E is None or E.shape != (3, 3):
        return None
    mask = mask.ravel().astype(bool) if mask is not None else np.ones(n, dtype=bool)
    if mask.sum() < 5:
        return None

    n_inliers, R, t, pose_mask = cv2.recoverPose(E, p1n[mask], p2n[mask], focal=1.0, pp=(0.0, 0.0))
    if n_inliers < 5:
        return None
    full_mask = np.zeros(n, dtype=bool)
    full_mask[np.where(mask)[0][pose_mask.ravel().astype(bool)]] = True
    return {"R": R, "t": t.reshape(3), "E": E, "inlier_mask": full_mask,
            "n_inliers": int(full_mask.sum()), "n_total": n}


def estimate_planar_pose_from_homography(pts1, pts2, K1, K2, dist1=None, dist2=None,
                                          prob=0.999, threshold_px=1.5):
    """ONEMLI, BU OTURUMDA DOGRUDAN SENTETIK TESTLE KESIN OLARAK
    DOGRULANAN GERCEK BIR SINIRLAMA: essential matrix tahmini, TUM
    noktalar TEK BIR DUZLEME ait oldugunda (bkz. Bolum C17/C18/final
    rapor) DEJENEREDIR - klasik bir cok-goruntulu geometri sorunu
    (Hartley&Zisserman). Test: SADECE duzlemsel (Z=0) noktalarla
    estimate_relative_pose_two_view TAMAMEN YANLIS bir poz uretti (R
    ozdeslikten 0.2 rad kadar sapiyordu, t yonu gercekle HICBIR ILGISI
    olmayan bir yon veriyordu); AYNI noktalara birkac duzlem-DISI nokta
    eklenince poz makine hassasiyetinde DOGRU cikti. Uygulamanin ANA
    hedefi (bir CEPHE - yani DUZLEMSEL bir hedef) olcmek oldugu icin, iki
    goruntudeki eslesmelerin COGU/TUMU tam da bu dejenere durumu
    tetikleyebilir - bu yuzden HOMOGRAFI AYRISTIRMASI (bu fonksiyon)
    duzlemsel sahneler icin DOGRU/GUVENILIR alternatiftir.

    cv2.findHomography (USAC_MAGSAC/RANSAC) ile H kurup,
    cv2.decomposeHomographyMat ile (normalize koordinatlarda, K=I) EN
    FAZLA 4 (R,t,n) adayina ayristirir - klasik bir cheirality
    (TUM noktalar HER IKI kamera onunde de olmali) filtresiyle GECERSIZ
    adaylar elenir. Kalan adaylar arasindan TEK BASINA SECIM YAPILMAZ
    (bkz. compute_fourth_point_camera_pose'daki P3P belirsizligi ile
    AYNI felsefe) - cagiran taraf (compute_two_view_reconstruction)
    BAGIMSIZ kanitla (bilinen AB/AC uzunluklarinin tutarliligi) hangi
    adayin dogru oldugunu belirler.

    Doner: {"candidates": [(R,t), ...], "inlier_mask", "n_inliers"} ya da
    yeterli eslesme/gecerli ayristirma yoksa None."""
    n = len(pts1)
    if n < 4:
        return None
    p1n = _undistort_to_normalized(pts1, K1, dist1)
    p2n = _undistort_to_normalized(pts2, K2, dist2)
    avg_focal = (K1[0, 0] + K1[1, 1] + K2[0, 0] + K2[1, 1]) / 4.0
    norm_threshold = threshold_px / avg_focal if avg_focal > 1e-9 else 1e-3

    method = getattr(cv2, "USAC_MAGSAC", cv2.RANSAC)
    try:
        H, mask = cv2.findHomography(p1n, p2n, method=method, ransacReprojThreshold=norm_threshold,
                                      confidence=prob)
    except cv2.error:
        return None
    if H is None:
        return None
    mask = mask.ravel().astype(bool) if mask is not None else np.ones(n, dtype=bool)
    if mask.sum() < 4:
        return None

    try:
        n_sol, Rs, Ts, Ns = cv2.decomposeHomographyMat(H, np.eye(3))
    except cv2.error:
        return None

    inlier_p1, inlier_p2 = p1n[mask], p2n[mask]
    valid_candidates = []
    for k in range(n_sol):
        R_k, t_k = Rs[k], Ts[k].reshape(3)
        ok = True
        for i in range(len(inlier_p1)):
            P1 = np.hstack([np.eye(3), np.zeros((3, 1))])
            P2 = np.hstack([R_k, t_k.reshape(3, 1)])
            X4 = cv2.triangulatePoints(P1, P2, inlier_p1[i:i + 1].T, inlier_p2[i:i + 1].T)
            X = (X4[:3] / X4[3]).ravel()
            z2 = (R_k @ X + t_k)[2]
            if X[2] <= 1e-9 or z2 <= 1e-9:
                ok = False
                break
        if ok:
            valid_candidates.append((R_k, t_k))
    if not valid_candidates:
        return None
    return {"candidates": valid_candidates, "inlier_mask": mask, "n_inliers": int(mask.sum())}


def compute_triangulation_angle_deg(X, R, t):
    """3B nokta X'in (kamera-1 CERCEVESINDE, yani P1=[I|0]) IKI kamera
    merkezinden gorulme acisini (derece) hesaplar - Bolum C9: bu aci COK
    KUCUKSE (ravlar neredeyse paralel), derinlik tahmini SAYISAL OLARAK
    KARARSIZDIR (kucuk bir piksel hatasi devasa bir derinlik hatasina
    donusur) - baseline'in GERCEKTEN yeterli oldugunun DOGRUDAN olcusu."""
    C1 = np.zeros(3)
    C2 = -R.T @ t  # kamera-2 merkezinin kamera-1 cercevesindeki konumu (P2=[R|t] -> R@C2+t=0)
    v1, v2 = X - C1, X - C2
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 < 1e-12 or n2 < 1e-12:
        return 0.0
    cos_ang = np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0)
    return math.degrees(math.acos(cos_ang))


def triangulate_two_view(pts1_norm, pts2_norm, R, t, max_reproj_err=0.01, min_angle_deg=0.5):
    """Essential-matrix pozundan (R,t) NORMALIZE koordinatlardaki eslesen
    noktalari triangulate eder (cv2.triangulatePoints, P1=[I|0], P2=[R|t]
    - HER IKISI de normalize/kalibre kamera cercevesinde). Su kriterlere
    gore GECERSIZ noktalari REDDEDER (Bolum C8):

      - cheirality: HER IKI kamera onunde de (Z>0) OLMALI, aksi halde
        gecersiz bir 3B rekonstruksiyon (kamera ARKASINDA bir nokta).
      - reprojeksiyon hatasi: normalize uzayda max_reproj_err'i asarsa
        (kotu bir eslesme/aykiri deger isareti).
      - triangulation acisi: min_angle_deg'in ALTINDAYSA (ravlar
        neredeyse paralel - bkz. compute_triangulation_angle_deg) derinlik
        GUVENILMEZ sayilir ve REDDEDILIR.

    Doner: {"points_3d": Mx3 (kamera-1 cercevesinde, BIRIM-taban olcekte -
    HENUZ GERCEK METRIK DEGIL), "valid_mask": (N,) bool, "angles_deg": (M,),
    "reproj_errors": (M,)}."""
    n = len(pts1_norm)
    P1 = np.hstack([np.eye(3), np.zeros((3, 1))])
    P2 = np.hstack([R, t.reshape(3, 1)])
    pts4d = cv2.triangulatePoints(P1, P2, pts1_norm.T, pts2_norm.T)
    pts3d = (pts4d[:3] / pts4d[3]).T  # (N,3), kamera-1 cercevesi

    valid = np.zeros(n, dtype=bool)
    angles = np.full(n, np.nan)
    reproj_errs = np.full(n, np.nan)
    for i in range(n):
        X = pts3d[i]
        z1 = X[2]
        X2 = R @ X + t
        z2 = X2[2]
        if z1 <= 1e-9 or z2 <= 1e-9:
            continue  # cheirality basarisiz - kamera(lar) ARKASINDA
        est1 = (X[0] / z1, X[1] / z1)
        est2 = (X2[0] / z2, X2[1] / z2)
        err = math.hypot(est1[0] - pts1_norm[i, 0], est1[1] - pts1_norm[i, 1]) + \
            math.hypot(est2[0] - pts2_norm[i, 0], est2[1] - pts2_norm[i, 1])
        reproj_errs[i] = err
        ang = compute_triangulation_angle_deg(X, R, t)
        angles[i] = ang
        if err <= max_reproj_err and ang >= min_angle_deg:
            valid[i] = True
    return {"points_3d": pts3d, "valid_mask": valid, "angles_deg": angles, "reproj_errors": reproj_errs}


def fit_plane_ransac(points_3d, dist_threshold=None, n_iter=500, seed=0, min_inliers=4):
    """3B nokta bulutuna (Bolum C10) RANSAC ile saglam bir DUZLEM
    (normal, duzlem-uzerinde-bir-nokta) fit eder - girinti/balkon/zemin
    gibi FARKLI bir fiziksel duzleme ait noktalari (aykiri deger olarak)
    reddeder. dist_threshold verilmezse, nokta bulutunun tipik olcegine
    (medyan komsu mesafesine YAKIN bir yaklasimla, bounding-box koseginin
    kesri olarak) gore OTOMATIK secilir.

    Doner: {"normal", "point", "inlier_mask", "n_inliers"} ya da yeterli
    nokta/gecerli duzlem yoksa None."""
    pts = np.asarray(points_3d, dtype=np.float64)
    n = len(pts)
    if n < min_inliers:
        return None
    if dist_threshold is None:
        bbox_diag = np.linalg.norm(pts.max(axis=0) - pts.min(axis=0))
        dist_threshold = max(bbox_diag * 0.01, 1e-6)

    rng = np.random.default_rng(seed)
    best_inliers, best_normal, best_point = None, None, None
    n_iter_eff = min(n_iter, max(50, n * (n - 1) // 2))
    for _ in range(n_iter_eff):
        idx = rng.choice(n, size=3, replace=False)
        p0, p1, p2 = pts[idx]
        normal = np.cross(p1 - p0, p2 - p0)
        norm = np.linalg.norm(normal)
        if norm < 1e-12:
            continue
        normal = normal / norm
        dists = np.abs((pts - p0) @ normal)
        inliers = dists <= dist_threshold
        if best_inliers is None or inliers.sum() > best_inliers.sum():
            best_inliers, best_normal, best_point = inliers, normal, p0
    if best_inliers is None or best_inliers.sum() < min_inliers:
        return None

    # SVD ile son bir kez, TUM inlier'lar uzerinde hassas duzlem fit
    # (RANSAC'in kendisi sadece BASLANGIC/aykiri-deger-eleme icindir).
    inlier_pts = pts[best_inliers]
    centroid = inlier_pts.mean(axis=0)
    _, _, Vt = np.linalg.svd(inlier_pts - centroid)
    normal = Vt[-1]
    dists = np.abs((pts - centroid) @ normal)
    final_inliers = dists <= dist_threshold
    return {"normal": normal, "point": centroid, "inlier_mask": final_inliers,
            "n_inliers": int(final_inliers.sum())}


def build_plane_basis(A3d, B3d, C3d):
    """A,B,C'nin (ayni fiziksel duzlemde, ARTIK gercek 3B triangulate
    edilmis konumlar) GERCEK geometrisinden, duzlem icin ORTONORMAL bir
    2B taban kurar: e1 = AB yonu, e2 = (AC'nin e1'e DIK bileseni,
    Gram-Schmidt) - boylece (u,v) koordinatlarinda OKLID mesafesi HER
    ZAMAN dogru fiziksel mesafeyi verir (theta 90 derece olmasa BILE -
    iki-goruntu modunda theta bir GIRDI/varsayim DEGIL, SADECE bir
    dogrulama/capraz-kontrol degeridir, bkz. Bolum C12 notu ve modul
    basi aciklamasi).

    e2'nin ISARETI, C'nin +v tarafinda kalacak sekilde secilir (kullanici
    sezgisiyle tutarli: A ortak kose, B 'yatay', C 'dikey' yonde)."""
    A3d, B3d, C3d = np.asarray(A3d, float), np.asarray(B3d, float), np.asarray(C3d, float)
    e1 = B3d - A3d
    n1 = np.linalg.norm(e1)
    if n1 < 1e-12:
        return None
    e1 = e1 / n1
    v = C3d - A3d
    e2 = v - np.dot(v, e1) * e1
    n2 = np.linalg.norm(e2)
    if n2 < 1e-12:
        return None
    e2 = e2 / n2
    if np.dot(C3d - A3d, e2) < 0:
        e2 = -e2
    return {"origin": A3d, "e1": e1, "e2": e2}


def project_points_to_plane_basis(points_3d, basis):
    """3B noktalari (Nx3), build_plane_basis'in ORTONORMAL (u,v) tabanina
    izdusurur - Oklid mesafesi KORUNUR (bkz. build_plane_basis notu)."""
    pts = np.asarray(points_3d, dtype=np.float64)
    rel = pts - basis["origin"]
    u = rel @ basis["e1"]
    v = rel @ basis["e2"]
    return np.column_stack([u, v])


def recover_scale_from_known_lengths(ab_rec, ac_rec, ab_m, ac_m, conflict_tol=0.08):
    """Essential-matrix/triangulation SADECE BIRIM-TABAN olcekte 3B
    geometri verir (bkz. estimate_relative_pose_two_view notu) - GERCEK
    metrik olcek, kullanicinin bildigi GERCEK AB/AC uzunluklariyla
    kurtarilir (Bolum C7): s = gercek_uzunluk / rekonstrukte_uzunluk.

    Iki BAGIMSIZ tahmin (s_ab, s_ac) varsa, bunlar birbirinden
    conflict_tol'dan FAZLA sapiyorsa (ör. A/B/C ayni duzlemde degil,
    yanlis gercek uzunluk girildi, yanlis eslesme) KORLEME ORTALAMA
    ALINMAZ - 'conflict' bayragiyla ACIKCA raporlanir (bkz. Bolum C7/23
    'do not blindly average inconsistent scales')."""
    if ab_rec < 1e-9 or ac_rec < 1e-9:
        return None
    s_ab = ab_m / ab_rec
    s_ac = ac_m / ac_rec
    rel_diff = abs(s_ab - s_ac) / ((s_ab + s_ac) / 2.0)
    conflict = rel_diff > conflict_tol
    s_final = s_ab if conflict else (s_ab + s_ac) / 2.0
    return {"s_ab": s_ab, "s_ac": s_ac, "scale": s_final, "conflict": conflict, "rel_diff": rel_diff}


MIN_TRIANGULATION_ANGLE_DEG = 1.0  # bu esigin ALTINDA, baseline/derinlik GUVENILMEZ sayilir (Bolum C9/C19)


def compute_two_view_reconstruction(A1, B1, C1, A2, B2, C2, ab_m, ac_m, angle_deg,
                                     K1, K2, dist1=None, dist2=None,
                                     extra_pts1=None, extra_pts2=None):
    """IKI FOTOGRAF MODU ana orkestratoru (Bolum C). A,B,C kullanici
    tarafindan HER IKI goruntude de ISARETLENMIS varsayilir (en guvenilir
    yontem - bkz. Bolum C1 notu, 'preferably both via matching' -
    otomatik eslestirme yerine dogrudan isaretleme, referans noktalari
    icin YANLIS eslesme riskini TAMAMEN ortadan kaldirir). extra_pts1/
    extra_pts2, GENELDE match_features_sift'ten gelen (ayni sirada
    eslesmis) ek noktalardir - poz tahminini GUCLENDIRIR ve olculebilir
    'keyfi' noktalar saglar.

    Akis:
      1) TUM noktalar (A,B,C + extra) normalize kamera koordinatlarina
         cevrilir (undistort + K^-1).
      2) Essential matrix (genel hareket) VE homografi-ayristirma
         (duzlemsel hareket - bkz. estimate_planar_pose_from_homography
         dokumantasyonu: essential matrix TAMAMEN duzlemsel sahnelerde
         DEJENEREDIR, bu SOMUT olarak test edilip DOGRULANDI) AYRI AYRI
         denenir.
      3) HER aday poz (E-tabanli 1 aday + H-tabanli EN FAZLA 4 aday,
         cheirality ile onceden filtrelenmis) icin A,B,C triangulate
         edilir; s_ab/s_ac SCALE TUTARLILIGI (rel_diff - kucukse aday
         daha GUVENILIR) hesaplanir - EN KUCUK celiskiyi veren aday
         KAZANIR (Bolum C6 poz belirsizligi + Bolum C18 model secimi
         AYNI kanitla, birlikte cozulur).
      4) Kazanan pozla TUM noktalar (A,B,C+extra) triangulate edilir;
         cheirality/reprojeksiyon/ucgenleme-acisi kriterlerini
         GECEMEYENLER reddedilir (bkz. triangulate_two_view).
      5) A,B,C'nin ORTONORMAL duzlem tabani kurulur (build_plane_basis);
         GERCEK olcek kurtarilir (recover_scale_from_known_lengths);
         TUM gecerli 3B nokta bu tabana izdusurulup OLCEKLENIR.

    Basarili olursa zengin bir sonuc sozlugu (asagida), degilse (yeterli
    eslesme/gecerli poz/olcek yoksa) None doner. HICBIR ASAMADA sessizce
    'muhtemelen dogru' bir sonuc UYDURULMAZ - basarisizlik ACIKCA None
    (ve ozel durumlarda bir 'reason' aciklamasi) olarak doner."""
    pts1 = np.array([A1, B1, C1] + list(extra_pts1 or []), dtype=np.float64)
    pts2 = np.array([A2, B2, C2] + list(extra_pts2 or []), dtype=np.float64)
    if len(pts1) != len(pts2) or len(pts1) < 5:
        return {"reason": "Yeterli eslesen nokta yok (en az 5 - A,B,C + en az 2 ek nokta gerekli)."}

    p1n = _undistort_to_normalized(pts1, K1, dist1)
    p2n = _undistort_to_normalized(pts2, K2, dist2)

    pose_candidates = []  # [(R,t,source_label), ...]
    e_result = estimate_relative_pose_two_view(pts1, pts2, K1, K2, dist1, dist2)
    if e_result is not None:
        pose_candidates.append((e_result["R"], e_result["t"], "essential_matrix"))
    h_result = estimate_planar_pose_from_homography(pts1, pts2, K1, K2, dist1, dist2)
    if h_result is not None:
        for R_k, t_k in h_result["candidates"]:
            pose_candidates.append((R_k, t_k, "homography_decomposition"))

    if not pose_candidates:
        return {"reason": "Ne essential matrix ne homografi ayristirmasi gecerli bir poz uretemedi - "
                           "eslesmeler yetersiz/guvenilmez olabilir."}

    # BOLUM C6/C18: HER adayi, A,B,C icin GERCEKTEN BILINEN uzunluklarla
    # (s_ab vs s_ac tutarliligi) SINA - hicbir aday 'varsayilan/ilk' diye
    # secilmez, HEPSI BAGIMSIZ kanitla degerlendirilir.
    best = None
    for R_k, t_k, label in pose_candidates:
        tri = triangulate_two_view(p1n[:3], p2n[:3], R_k, t_k, max_reproj_err=1.0, min_angle_deg=0.0)
        if not tri["valid_mask"].all():
            continue  # A,B,C'nin HEPSI cheirality/temel kontrolu GECMELI
        A3, B3, C3 = tri["points_3d"]
        ab_rec, ac_rec = np.linalg.norm(B3 - A3), np.linalg.norm(C3 - A3)
        scale_info = recover_scale_from_known_lengths(ab_rec, ac_rec, ab_m, ac_m)
        if scale_info is None:
            continue
        if best is None or scale_info["rel_diff"] < best["scale_info"]["rel_diff"]:
            best = {"R": R_k, "t": t_k, "source": label, "scale_info": scale_info,
                    "A3": A3, "B3": B3, "C3": C3}

    if best is None:
        return {"reason": "Hicbir poz adayi A,B,C icin gecerli/tutarli bir rekonstruksiyon vermedi."}

    R, t = best["R"], best["t"]
    tri_all = triangulate_two_view(p1n, p2n, R, t, max_reproj_err=0.02, min_angle_deg=0.0)
    angles = tri_all["angles_deg"][tri_all["valid_mask"]]
    median_angle = float(np.median(angles)) if len(angles) else 0.0
    weak_baseline = median_angle < MIN_TRIANGULATION_ANGLE_DEG

    basis = build_plane_basis(best["A3"], best["B3"], best["C3"])
    if basis is None:
        return {"reason": "A,B,C'den duzlem tabani kurulamadi (dejenere - neredeyse ayni dogru uzerinde)."}
    scale = best["scale_info"]["scale"]

    uv_all = project_points_to_plane_basis(tri_all["points_3d"], basis) * scale
    ab_recovered = math.hypot(*(uv_all[1] - uv_all[0]))
    ac_recovered = math.hypot(*(uv_all[2] - uv_all[0]))
    angle_recovered = _angle_between_dirs(tuple(uv_all[1] - uv_all[0]), tuple(uv_all[2] - uv_all[0]))

    plane_fit = None
    if len(tri_all["points_3d"]) >= 4:
        plane_fit = fit_plane_ransac(tri_all["points_3d"][tri_all["valid_mask"]])

    return {
        "R": R, "t": t, "pose_source": best["source"],
        "scale_info": best["scale_info"],
        "basis": basis, "uv_points": uv_all, "valid_mask": tri_all["valid_mask"],
        "triangulation_angles_deg": tri_all["angles_deg"], "median_triangulation_angle_deg": median_angle,
        "weak_baseline": weak_baseline,
        "ab_recovered": ab_recovered, "ac_recovered": ac_recovered, "ab_input": ab_m, "ac_input": ac_m,
        "angle_recovered_deg": angle_recovered, "angle_input_deg": angle_deg,
        "plane_fit": plane_fit,
        "n_points": len(pts1), "n_valid": int(tri_all["valid_mask"].sum()),
    }


def measure_two_view_distance(uv_all, valid_mask, i, j):
    """uv_all[i], uv_all[j] arasindaki (ZATEN metrik-olcekli, bkz.
    compute_two_view_reconstruction) Oklid mesafesini doner - i ya da j
    gecersiz (cheirality/reprojeksiyon basarisiz) ise None doner."""
    if not (valid_mask[i] and valid_mask[j]):
        return None
    return float(math.hypot(uv_all[j][0] - uv_all[i][0], uv_all[j][1] - uv_all[i][1]))


def compute_fourth_point_projective(A, B, C, helper_ab=None, helper_ac=None,
                                     extra_lines_ab=None, extra_lines_ac=None,
                                     auto_lines_ab=None, auto_lines_ac=None):
    """A ortak kose olmak uzere, ABDC paralelkenarinin (bilinmeyen D)
    goruntudeki GERCEK projektif konumunu, AB ve AC yonlerine ait GERCEK
    kanitlardan (yardimci cizgiler) hesaplar.

    extra_lines_ab / extra_lines_ac: (opsiyonel) AYNI yon ailesinden,
    fotografta ZATEN tanimlanmis baska (p,q) nokta ciftleri listesi -
    ör. kullanicinin baska pencereler icin eklemis oldugu olcum sorgulari.
    Bunlar, TEK bir yardimci cizgiye bagli kalmak yerine, o yondeki
    TUM mevcut kanitlarin en-kucuk-kareler ile birlikte degerlendirildigi
    daha kararli bir kacis noktasi tahmini saglar.

    NEDEN YARDIMCI CIZGI SART: bir kacis noktasi, bir yondeki EN AZ IKI
    GERCEK goruntu cizgisinin kesisimidir - TEK bir cizgiden kacis noktasi
    HESAPLANAMAZ. Bu yuzden sadece A,B,C + iki uzunluk (+ aci) ile D'nin
    goruntudeki konumu ASLA tek ve dogru sekilde belirlenemez (bkz.
    test_d_ambiguity.py - kamera ic parametreleri BILINSE BILE birden
    fazla gecerli kamera pozu farkli D verir).

    DORT DURUM (her yon icin ayri ayri degerlendirilir - bkz.
    _resolve_vanishing_point, artik "finite_strong/finite_weak/
    near_infinity/invalid" dereceli siniflandirmasi kullanir):
      1) Her iki yon de SONLU (strong ya da weak) ise: TAM PROJEKTIF
         cozum (D, iki kacis noktasinin kesisiminden).
      2) Bir yon SONLU, diger yon "near_infinity" ise: KARMA cozum -
         guvenilir yondeki GERCEK perspektifi kullanir, diger yonde
         (sayisal olarak kanitlanmis) paralelligi kullanir.
      3) Diger tum durumlarda (ikisi de near_infinity/invalid, ya da
         yardimci cizgi yok): None - sahte kesinlik uretilmez, cagiran
         taraf afin yaklasima acikca belirterek doner.

    Basarili olursa (D_image, (kind_ab, vp_ab), (kind_ac, vp_ac)) doner."""
    ref_scale = (math.hypot(B[0] - A[0], B[1] - A[1]) + math.hypot(C[0] - A[0], C[1] - A[1])) / 2.0
    kind_ab, vp_ab = _resolve_vanishing_point(A, B, helper_ab, extra_lines_ab, ref_scale, auto_lines_ab)
    kind_ac, vp_ac = _resolve_vanishing_point(A, C, helper_ac, extra_lines_ac, ref_scale, auto_lines_ac)

    ab_finite = kind_ab in _FINITE_KINDS
    ac_finite = kind_ac in _FINITE_KINDS

    if ab_finite and ac_finite:
        # D: C'den gecen (dunyada AB'ye paralel -> goruntude VP_AB'ye giden)
        # dogru ile B'den gecen (dunyada AC'ye paralel -> goruntude VP_AC'ye
        # giden) dogrunun kesisimi.
        line_c_side = _line_through(C, vp_ab)
        line_b_side = _line_through(B, vp_ac)
    elif ab_finite and kind_ac == "near_infinity":
        # AC yonunde kacis noktasi sonsuzda (sayisal olarak kanitlandi) -
        # C'den AB'ye giden gercek kacis noktasina dogru cizgi kullanilir,
        # B'den ise AC yonunde OKLID PARALELI kullanilir.
        line_c_side = _line_through(C, vp_ab)
        dir_ac = (C[0] - A[0], C[1] - A[1])
        B2 = (B[0] + dir_ac[0], B[1] + dir_ac[1])
        line_b_side = _line_through(B, B2)
    elif kind_ab == "near_infinity" and ac_finite:
        # Simetrik durum: AB yonunde kacis noktasi sonsuzda.
        dir_ab = (B[0] - A[0], B[1] - A[1])
        C2 = (C[0] + dir_ab[0], C[1] + dir_ab[1])
        line_c_side = _line_through(C, C2)
        line_b_side = _line_through(B, vp_ac)
    else:
        return None

    D = _intersect_lines(line_c_side, line_b_side)
    if D is None:
        return None
    return D, (kind_ab, vp_ab), (kind_ac, vp_ac)


# ---------------------------------------------------------------------
# ROUTE A: kalibre kamera pozu (P3P/SQPNP) ile dorduncu nokta turetimi.
#
# Route B (yukarida) kacis noktasi/yardimci cizgi kanitina dayanir. Bu
# rota bunun yerine, EXIF'ten (varsa) yaklasik kamera ic parametrelerini
# (K) cikarip, SADECE A/B/C'nin 3 nokta karsiligindan kamera pozunu (R,t)
# cozup D'yi DOGRUDAN projekte etmeye calisir - hicbir kacis noktasi ya
# da yardimci cizgiye ihtiyac duymaz.
#
# ONEMLI SINIRLAMA (bu oturumda sentetik testlerle DOGRULANDI - bkz.
# tests/test_camera_pose.py): 3 nokta + K'dan kamera pozu kestirimi
# (P3P ailesi) matematiksel olarak COGU ZAMAN BELIRSIZDIR - 2-4 farkli
# fiziksel gecerli (kamera onunde/pozitif derinlik) poz cikabilir, ve
# TAM DE guclu perspektif altinda (Route A'nin en cok ise yarayacagi
# durum) bu adaylarin projekte ettigi D noktalari birbirinden onemli
# olcude FARKLI olabilir (bu oturumda test edilen senaryolarda adaylar
# arasi fark referans olcegin %3-15'i kadar cikti). Bu yuzden:
#   - Adaylar (ref_scale'e oranla) YETERINCE ORTUSUYORSA (tipik olarak
#     zayif perspektif / kamera odak eksenine yakin cekimlerde): TEKIL
#     bir D olarak kabul edilir.
#   - ORTUSMUYORSA: sahte kesinlik uretmek yerine None doner - cagiran
#     taraf Route B'ye (kacis noktasi) duser. Bu, "asla yanlis ama
#     kendinden emin gorunen bir cevap verme" ilkesinin dogrudan
#     uygulanmasidir.
# ---------------------------------------------------------------------

CAMERA_POSE_AGREE_TOL_RATIO = 0.03  # poz adaylarinin D projeksiyonlari
                                     # arasindaki izin verilen maksimum
                                     # fark (ref_scale'e oran olarak)

_EXIF_TAG_FOCAL_35MM = 41989  # FocalLengthIn35mmFilm


def estimate_camera_intrinsics_from_exif(exif, img_w, img_h):
    """Fotografin EXIF meta verisinden (varsa) YAKLASIK kamera ic
    parametrelerini (K) tahmin eder - GERCEK bir checkerboard
    kalibrasyonunun YERINE GECMEZ, sadece Route A (kamera pozu) icin
    kaba bir baslangic K'si saglar (35mm-esdeger odak uzunlugu
    uzerinden: fx=fy=(focal_35mm/36mm)*goruntu_genisligi_px, temel nokta
    goruntu merkezinde varsayilir). EXIF'te bu bilgi yoksa (ya da
    okunamazsa) None doner - bu durumda Route A sessizce devre disi
    kalir ve sistem doğrudan Route B'ye (kacis noktasi) duser; SAHTE bir
    K UYDURULMAZ."""
    if not exif:
        return None
    try:
        focal_35mm = exif.get(_EXIF_TAG_FOCAL_35MM)
        if not focal_35mm:
            return None
        focal_35mm = float(focal_35mm)
        if focal_35mm <= 0 or not img_w or not img_h:
            return None
    except Exception:
        return None
    fx = fy = (focal_35mm / 36.0) * img_w
    cx, cy = img_w / 2.0, img_h / 2.0
    return np.array([[fx, 0.0, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]], dtype=np.float64)


def solve_camera_pose_3pt(K, world_pts_3d, img_pts):
    """3 nokta karsiligindan (A,B,C) olasi kamera pozu (R,t) adaylarini
    cozer. NOT: kurulu OpenCV surumunde (5.0.0) klasik P3P/AP3P
    bayraklari 3 nokta ile calismiyor (npoints>=4 sarti getiriyor,
    dogrudan test edilip DOGRULANDI) - bunun yerine, 3 noktadan da
    (matematiksel olarak esdeger sekilde) cozebilen genel amacli SQPNP
    cozucusu kullanilir. Sadece pozitif derinlikli (kamera onunde)
    adaylar dondurulur; bu TEK BASINA belirsizligi cozmez (bkz.
    compute_fourth_point_camera_pose)."""
    obj = np.array(world_pts_3d, dtype=np.float64).reshape(-1, 1, 3)
    img = np.array(img_pts, dtype=np.float64).reshape(-1, 1, 2)
    dist = np.zeros((4, 1))
    try:
        ok, rvecs, tvecs, _ = cv2.solvePnPGeneric(obj, img, K, dist, flags=cv2.SOLVEPNP_SQPNP)
    except Exception:
        return []
    if not ok or not rvecs:
        return []
    valid = []
    for rvec, tvec in zip(rvecs, tvecs):
        R, _ = cv2.Rodrigues(rvec)
        t = tvec.reshape(3)
        depths = [float((R @ np.array(p) + t)[2]) for p in world_pts_3d]
        if all(z > 1e-6 for z in depths):
            valid.append((R, t))
    return valid


def compute_fourth_point_camera_pose(A, B, C, K, ab_m, ac_m, angle_deg=90.0):
    """Route A: EXIF-tabanli K ve 3 noktadan (SQPNP) kamera pozu
    kestirimiyle D'nin goruntudeki GERCEK izdusumunu hesaplar.
    Basarili olursa (D_img, n_gecerli_poz_adayi) doner; K yoksa, poz
    cozulemezse ya da adaylar birbirinden ONEMLI OLCUDE sapiyorsa
    (belirsiz poz - yukaridaki modul dokumantasyonuna bkz.) None doner."""
    if K is None:
        return None
    angle_rad = math.radians(angle_deg)
    world_A = (0.0, 0.0, 0.0)
    world_B = (ab_m, 0.0, 0.0)
    world_C = (ac_m * math.cos(angle_rad), ac_m * math.sin(angle_rad), 0.0)
    world_D = np.array([world_B[0] + world_C[0], world_B[1] + world_C[1], 0.0])

    candidates = solve_camera_pose_3pt(K, [world_A, world_B, world_C], [A, B, C])
    if not candidates:
        return None

    ref_scale = (math.hypot(B[0] - A[0], B[1] - A[1]) + math.hypot(C[0] - A[0], C[1] - A[1])) / 2.0
    if ref_scale < 1e-6:
        return None

    D_candidates = []
    for R, t in candidates:
        v = K @ (R @ world_D + t)
        if abs(v[2]) < 1e-9:
            continue
        D_candidates.append((float(v[0] / v[2]), float(v[1] / v[2])))
    if not D_candidates:
        return None

    max_spread = 0.0
    for i in range(len(D_candidates)):
        for j in range(i + 1, len(D_candidates)):
            d = math.hypot(D_candidates[i][0] - D_candidates[j][0], D_candidates[i][1] - D_candidates[j][1])
            max_spread = max(max_spread, d)

    if max_spread > CAMERA_POSE_AGREE_TOL_RATIO * ref_scale:
        return None  # poz belirsiz - sahte kesinlik uretme, Route B'ye birak

    return D_candidates[0], len(candidates)


# ---------------------------------------------------------------------
# BAGIMSIZ DOGRULAMA YARDIMCILARI (Bolum 17/18): H_final'i, ONU KURAN
# noktalarin/yonlerin OTESINDE (mumkun oldugunca BAGIMSIZ kanitla) test
# etmek icin. Tek basina "fit hatasi ~0" raporlamak yaniltici olurdu -
# minimum kisit kumesiyle kurulan bir sistem, KENDI kisitlarinda hep
# kucuk/sifir hata verir (bu bir dogrulama degil, tanim geregi boyle).
# ---------------------------------------------------------------------

def _point_reprojection_stats(H, point_pairs):
    """H (goruntu->dunya) ile, verilen (img,world) ciftlerinin HER BIRI
    icin metre cinsinden reprojeksiyon hatasini hesaplar; RMSE/medyan/max
    doner (n=0 ise None)."""
    errs = []
    for img_pt, world_pt in point_pairs:
        try:
            est = apply_transform(H, img_pt)
        except ValueError:
            continue
        errs.append(math.hypot(est[0] - world_pt[0], est[1] - world_pt[1]))
    if not errs:
        return None
    arr = np.array(errs)
    return {"n": len(errs), "rmse": float(np.sqrt(np.mean(arr ** 2))),
            "median": float(np.median(arr)), "max": float(np.max(arr))}


def _line_family_angular_stats(Hinv, world_dir_xy, segments):
    """Bir yon-ailesindeki (AB ya da AC) GOZLENEN cizgilerin (kullanicinin
    ek olcumleri + otomatik tespit edilenler - bkz. Bolum 18), H_final'in
    O YON ICIN ONGORDUGU goruntu kacis noktasindan ACISAL sapmasini
    (derece) hesaplar. Bu, H_final'i KURAN kanitla AYNI olmayan (genelde
    daha genis) bir cizgi kumesi uzerinde calisir - GERCEK bir bagimsiz
    tutarlilik testidir: cizgiler sistematik olarak anlasmazsa (buyuk
    max/medyan), global model GUVENILMEZ demektir."""
    if not segments:
        return None
    dx, dy = world_dir_xy
    vp_h = Hinv @ np.array([dx, dy, 0.0])
    residuals = []
    if abs(vp_h[2]) > 1e-9:
        vpx, vpy = vp_h[0] / vp_h[2], vp_h[1] / vp_h[2]
        for p, q in segments:
            residuals.append(_angular_residual_deg(p, q, (vpx, vpy)))
    else:
        inf_ang = math.degrees(math.atan2(vp_h[1], vp_h[0]))
        for p, q in segments:
            seg_ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
            diff = abs(seg_ang - inf_ang) % 180.0
            residuals.append(180.0 - diff if diff > 90.0 else diff)
    arr = np.array(residuals)
    return {"n": len(residuals), "mean_deg": float(np.mean(arr)),
            "median_deg": float(np.median(arr)), "max_deg": float(np.max(arr))}


HOMOGRAPHY_REFINE_F_SCALE = 0.03  # Huber robust-loss esigi (bkz. refine_homography_nonlinear)


def refine_homography_nonlinear(H_init, point_pairs, direction_pairs, line_families=None,
                                 known_length_constraints=None,
                                 point_weights=None, direction_weights=None,
                                 loss="huber", f_scale=HOMOGRAPHY_REFINE_F_SCALE):
    """H_init (dogrusal DLT baslangici) etrafinda, H'nin 8 bagimsiz
    parametresini (H[2,2]=1 sabit), TUM kanitlari (nokta + yon + varsa
    GOZLENEN cizgi-ailesi tutarliligi + varsa BAGIMSIZ bilinen kontrol
    uzunluklari) BIRLIKTE kullanan robust (Huber/Cauchy) dogrusal-olmayan
    en-kucuk-kareler ile inceltir.

    Kalinti (residual) turleri:
      - nokta: dunya-uzayi (metre) konum farki, 2 bilesen/nokta, ISTEGE
        BAGLI point_weights ile agirliklandirilir (bkz. POINT_SOURCE_
        SIGMA_PX - manuel tiklama vs buyutecli/subpixel farkli guven
        tasir; agirlik = 1/sigma, DAHA GUVENILIR nokta optimizasyonda
        DAHA fazla soz sahibi olur).
      - yon: H*V'nin (normalize) yonu ile beklenen dunya yonu arasindaki
        capraz-carpim (sin-benzeri, kucuk-aci) hizasizligi + H*V'nin
        ucuncu (homojen) bileseninin sifira yakinligi - ISTEGE BAGLI
        direction_weights ile agirliklandirilir (bkz. bootstrap_vp_
        uncertainty: numerik olarak KARARSIZ - ör. neredeyse paralel,
        cok uzak - bir kacis noktasi kisitinin agirligi otomatik
        dusurulur, boylece GURULTULU bir yon, GUCLU/SAGLAM bir yonle
        AYNI agirlikta H'yi zorlamaz).
      - cizgi-ailesi (opsiyonel): GOZLENEN her (p,q) cizgisinin, H'nin O
        ANKI tahminine gore ongordugu kacis noktasindan acisal sapmasi
        (radyan) - bkz. _line_family_angular_stats ile AYNI mantik.
      - bilinen uzunluk (opsiyonel, Bolum 11): kullanicinin BAGIMSIZ
        olarak dogrulugundan emin oldugu ek gercek uzunluklar - residual
        = agirlik * (||H(p)-H(q)|| - gercek_uzunluk). Bu, kalan bir
        metrik olcek sapmasini (global ya da eksene ozel) GERCEK kanitla
        DUZELTMENIN prensipli yolu - "Y *= 1.08" gibi kor bir duzeltme
        DEGIL (bkz. final rapor, "yanlis post-hoc hile yapma" notu).

    Dogrusal-olmayan cozucu YAKINSAMAZSA/hata verirse, H_init AYNEN
    (basari=False ile) geri dondurulur - sessizce kotu bir sonuc
    UYDURULMAZ."""
    known_length_constraints = known_length_constraints or []
    point_weights = list(point_weights) if point_weights is not None else [1.0] * len(point_pairs)
    direction_weights = list(direction_weights) if direction_weights is not None else [1.0] * len(direction_pairs)
    h0 = (H_init / H_init[2, 2]).flatten()[:8]
    n_expected = (2 * len(point_pairs) + 2 * len(direction_pairs) +
                  sum(len(segs) for _, segs in (line_families or [])) +
                  len(known_length_constraints))

    def residuals(h_free):
        H = np.concatenate([h_free, [1.0]]).reshape(3, 3)
        try:
            Hinv = np.linalg.inv(H)
        except np.linalg.LinAlgError:
            return np.full(n_expected, 10.0)
        res = []
        for (img_pt, world_pt), pw in zip(point_pairs, point_weights):
            v = H @ np.array([img_pt[0], img_pt[1], 1.0])
            if abs(v[2]) < 1e-9:
                res.extend([10.0, 10.0])
                continue
            res.append(pw * (v[0] / v[2] - world_pt[0]))
            res.append(pw * (v[1] / v[2] - world_pt[1]))
        for (p_hom, (dx, dy)), dw in zip(direction_pairs, direction_weights):
            v = H @ np.array(p_hom)
            norm_d = math.hypot(dx, dy)
            udx, udy = dx / norm_d, dy / norm_d
            norm_v = math.hypot(v[0], v[1])
            if norm_v < 1e-12:
                res.extend([0.0, dw * float(v[2])])
                continue
            uvx, uvy = v[0] / norm_v, v[1] / norm_v
            cross = uvx * udy - uvy * udx
            if (uvx * udx + uvy * udy) < 0:
                cross = -cross  # yon yonsuz (180 derece ters de gecerli) - isaretini normalize et
            res.append(dw * cross)
            res.append(dw * v[2] / (norm_v + 1e-9))
        for world_dir_xy, segs in (line_families or []):
            dxw, dyw = world_dir_xy
            vp_h = Hinv @ np.array([dxw, dyw, 0.0])
            if abs(vp_h[2]) > 1e-9:
                vpx, vpy = vp_h[0] / vp_h[2], vp_h[1] / vp_h[2]
                for p, q in segs:
                    res.append(math.radians(_angular_residual_deg(p, q, (vpx, vpy))))
            else:
                inf_ang = math.degrees(math.atan2(vp_h[1], vp_h[0]))
                for p, q in segs:
                    seg_ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
                    diff = abs(seg_ang - inf_ang) % 180.0
                    res.append(math.radians(180.0 - diff if diff > 90.0 else diff))
        for p, q, true_len, weight in known_length_constraints:
            v1 = H @ np.array([p[0], p[1], 1.0])
            v2 = H @ np.array([q[0], q[1], 1.0])
            if abs(v1[2]) < 1e-9 or abs(v2[2]) < 1e-9:
                res.append(weight * 10.0)
                continue
            est_len = math.hypot(v1[0] / v1[2] - v2[0] / v2[2], v1[1] / v1[2] - v2[1] / v2[2])
            res.append(weight * (est_len - true_len))
        return np.array(res)

    cost_before = float(0.5 * np.sum(residuals(h0) ** 2))
    try:
        result = least_squares(residuals, h0, loss=loss, f_scale=f_scale, method="trf", max_nfev=2000)
    except Exception:
        return H_init, {"success": False, "cost_before": cost_before, "cost_after": cost_before}
    H_final = np.concatenate([result.x, [1.0]]).reshape(3, 3)
    if abs(H_final[2, 2]) < 1e-9 or not np.all(np.isfinite(H_final)):
        return H_init, {"success": False, "cost_before": cost_before, "cost_after": cost_before}
    cost_after = float(result.cost * 2)
    return H_final, {"success": bool(result.success), "cost_before": cost_before, "cost_after": cost_after}


def compute_global_homography(A, B, C, ab_m, ac_m, angle_deg,
                               helper_ab=None, helper_ac=None,
                               extra_ab=None, extra_ac=None,
                               auto_ab=None, auto_ac=None,
                               camera_pose_seed=None,
                               known_length_constraints=None,
                               point_sources=None,
                               img_size=None):
    """YENI ANA YONTEM (Route B): A,B,C + V_AB/V_AC kisitlarindan H'yi
    DOGRUDAN kurar (bkz. compute_constrained_homography). D, H_final
    KURULDUKTAN SONRA ondan geriye turetilir - bir GIRDI degil bir
    CIKTIDIR (eski compute_fourth_point_projective'in aksine, ki o D'yi
    ONCE turetip SONRA 4-noktali bagimsiz bir homografi kuruyordu - bu,
    D'nin KENDI hatasini H'ye ikinci kez enjekte eden 'self-confirming'
    bir model olusturuyordu, bkz. modul basi notu).

    camera_pose_seed: (D_img_kamera, n_poz_adayi) ya da None - Route A
    (EXIF K + P3P/SQPNP, bkz. compute_fourth_point_camera_pose) BASARILI
    olduysa, kamera pozunun onerdigi D, buraya BAGIMSIZ bir DORDUNCU
    NOKTA GOZLEMI olarak eklenir (point_pairs'e) - H'yi TEK BASINA
    belirlemez, sadece SISTEME EK BIR KANIT olarak katilir; nihai H yine
    de (varsa) VP/cizgi kisitlariyla BIRLIKTE, ayni en-kucuk-kareler
    sisteminde cozulur. Boylece yaklasik EXIF K'dan gelen tek basina asla
    YUKSEK guvenli bir global model URETEMEZ (bkz. Bolum 8 talebi).

    known_length_constraints: opsiyonel [(img_p, img_q, true_length_m,
    weight), ...] - kullanicinin BAGIMSIZ olarak dogrulugundan emin
    oldugu ek gercek uzunluklar (Bolum 11) - nonlineer inceltmeye
    dogrudan kisit olarak eklenir. Kalan bir metrik olcek sapmasini
    (compute_axis_scale_diagnostics ile TESHIS edildikten sonra) GERCEK
    kanitla duzeltmenin prensipli yolu.

    img_size: opsiyonel (img_w, img_h) - verilirse ve angle_deg==90 ise,
    VP_AB/VP_AC'nin GERCEKTEN dik yonlere karsilik gelip gelmedigi
    kalibrasyon-bagimsiz olarak kontrol edilir (bkz. validate_orthogonality,
    Bolum 15) - sonuc "orthogonality" alaninda doner.

    point_sources: opsiyonel [source_A, source_B, source_C] - bkz.
    POINT_SOURCE_SIGMA_PX (manuel/buyutecli/subpixel farkli guven tasir).
    Nonlineer inceltmede nokta agirligi = 1/sigma(source) olarak kullanilir
    (Bolum 3) - ör. buyutecle hassas isaretlenmis bir nokta, kaba
    tiklanmis bir noktadan DAHA FAZLA soz sahibi olur. Verilmezse hepsi
    'manual' (esit agirlik, ONCEKI davranisla AYNI) kabul edilir.

    Basarili olursa zengin bir sonuc sozlugu, degilse (ne VP ne kamera
    pozu kaniti varsa) None doner."""
    angle_rad = math.radians(angle_deg)
    world_A = (0.0, 0.0)
    world_B = (ab_m, 0.0)
    world_C = (ac_m * math.cos(angle_rad), ac_m * math.sin(angle_rad))
    world_D = (world_B[0] + world_C[0], world_B[1] + world_C[1])
    world_dir_ab = (1.0, 0.0)
    world_dir_ac = (math.cos(angle_rad), math.sin(angle_rad))

    ref_scale = (math.hypot(B[0] - A[0], B[1] - A[1]) + math.hypot(C[0] - A[0], C[1] - A[1])) / 2.0
    kind_ab, vp_ab = _resolve_vanishing_point(A, B, helper_ab, extra_ab, ref_scale, auto_ab)
    kind_ac, vp_ac = _resolve_vanishing_point(A, C, helper_ac, extra_ac, ref_scale, auto_ac)

    # ONEMLI: burada RANSAC/IRLS ile ZATEN dogrulanmis kacis noktasina
    # (vp_ab/vp_ac) gore HAM (extra_ab/auto_ab) havuzunu YENIDEN
    # ACISAL olarak suzuyoruz - ham havuzun KENDISINI degil. Aksi halde
    # (bu oturumda sentetik bir 'yabanci duzlem' testiyle - bkz.
    # tests/test_bad_vp.py - SOMUT olarak tespit edilen gercek bir bug)
    # _resolve_vanishing_point DOGRU vp_ab'yi bulsa bile, nonlineer
    # inceltme ve bagimsiz dogrulama (line_residuals) HAM havuzdaki
    # (RANSAC'in ZATEN elemis oldugu) yabanci cizgileri de kullanarak
    # H'yi tekrar bozabilir - RANSAC'in tum degerini gecersiz kilar.
    ab_lines_validated = ([seg for seg in (list(extra_ab or []) + list(auto_ab or []))
                            if _angular_residual_deg(seg[0], seg[1], vp_ab) <= VP_RANSAC_ANGLE_TOL_DEG]
                           if kind_ab in _FINITE_KINDS else [])
    ac_lines_validated = ([seg for seg in (list(extra_ac or []) + list(auto_ac or []))
                            if _angular_residual_deg(seg[0], seg[1], vp_ac) <= VP_RANSAC_ANGLE_TOL_DEG]
                           if kind_ac in _FINITE_KINDS else [])

    # BOLUM 16: bir kacis noktasi SONLU olarak siniflandirilmis olsa BILE
    # (ör. cizgiler neredeyse ama tam paralel degil), NUMERIK OLARAK ne
    # kadar KARARLI oldugunu bootstrap ile olc ve nonlineer inceltmedeki
    # agirligini buna gore ayarla - bkz. bootstrap_vp_uncertainty/
    # direction_weight_from_uncertainty dokumantasyonu.
    ab_boot = (bootstrap_vp_uncertainty([(A, B)] + ([helper_ab] if helper_ab else []) + ab_lines_validated,
                                         ref_scale) if kind_ab in _FINITE_KINDS else None)
    ac_boot = (bootstrap_vp_uncertainty([(A, C)] + ([helper_ac] if helper_ac else []) + ac_lines_validated,
                                         ref_scale) if kind_ac in _FINITE_KINDS else None)
    w_ab_dir = direction_weight_from_uncertainty(ab_boot)
    w_ac_dir = direction_weight_from_uncertainty(ac_boot)

    point_sources = list(point_sources) if point_sources else ["manual", "manual", "manual"]
    point_weights = [1.0 / point_sigma_px(s) for s in point_sources]

    point_pairs = [(A, world_A), (B, world_B), (C, world_C)]
    direction_pairs = []
    direction_weights = []
    dir_ab_hom = _direction_constraint_for_kind(kind_ab, vp_ab, A, B)
    if dir_ab_hom is not None:
        direction_pairs.append((dir_ab_hom, world_dir_ab))
        direction_weights.append(w_ab_dir)
    dir_ac_hom = _direction_constraint_for_kind(kind_ac, vp_ac, A, C)
    if dir_ac_hom is not None:
        direction_pairs.append((dir_ac_hom, world_dir_ac))
        direction_weights.append(w_ac_dir)

    used_camera_pose = False
    if camera_pose_seed is not None:
        D_img_cam, _n_pose = camera_pose_seed
        point_pairs.append((D_img_cam, world_D))
        point_weights.append(1.0 / point_sigma_px("derived_projective"))
        used_camera_pose = True

    if not direction_pairs and not used_camera_pose:
        return None  # ne kacis noktasi kaniti ne kamera pozu - projektif cozum icin kanit yok

    try:
        H_lin = compute_constrained_homography(point_pairs, direction_pairs)
    except (ValueError, np.linalg.LinAlgError):
        return None

    line_families = [(d, segs) for d, segs in
                      ((world_dir_ab, ab_lines_validated), (world_dir_ac, ac_lines_validated)) if segs]

    H_final, refine_info = refine_homography_nonlinear(H_lin, point_pairs, direction_pairs, line_families,
                                                        known_length_constraints,
                                                        point_weights=point_weights,
                                                        direction_weights=direction_weights)

    try:
        Hinv_final = np.linalg.inv(H_final)
    except np.linalg.LinAlgError:
        return None

    try:
        D_img = apply_transform(Hinv_final, world_D)
    except ValueError:
        return None

    # BOLUM 2 (teshis): H_final ile AB/AC'yi GERI olc - A,B,C artik (VP/yon
    # kisitlariyla BIRLIKTE, asiri-belirlenmis bir en-kucuk-kareler
    # sisteminde) sadece YAKLASIK olarak saglanir, ESKI mimarideki gibi
    # TAM (4 nokta = tam belirlenmis) degil. Girdiyle (ab_m,ac_m) onemli
    # olcude farkli cikarsa, bu ZATEN kendi basina bir teshis sinyalidir
    # (bkz. compute_axis_scale_diagnostics ve final rapor).
    try:
        ab_recovered = dist(apply_transform(H_final, A), apply_transform(H_final, B))
        ac_recovered = dist(apply_transform(H_final, A), apply_transform(H_final, C))
    except ValueError:
        ab_recovered = ac_recovered = None

    orthogonality = (validate_orthogonality(
        vp_ab if kind_ab in _FINITE_KINDS else None,
        vp_ac if kind_ac in _FINITE_KINDS else None,
        img_size[0], img_size[1], angle_deg) if img_size else None)

    return {
        "H": H_final, "Hinv": Hinv_final,
        "D_img": D_img, "world_D": world_D,
        "world_A": world_A, "world_B": world_B, "world_C": world_C,
        "kind_ab": kind_ab, "vp_ab": vp_ab,
        "kind_ac": kind_ac, "vp_ac": vp_ac,
        "used_camera_pose": used_camera_pose,
        "point_reproj": _point_reprojection_stats(H_final, point_pairs),
        "line_residuals_ab": _line_family_angular_stats(Hinv_final, world_dir_ab, ab_lines_validated)
            if kind_ab in _FINITE_KINDS else None,
        "line_residuals_ac": _line_family_angular_stats(Hinv_final, world_dir_ac, ac_lines_validated)
            if kind_ac in _FINITE_KINDS else None,
        "refine_info": refine_info,
        "ab_recovered": ab_recovered, "ac_recovered": ac_recovered,
        "ab_input": ab_m, "ac_input": ac_m,
        "vp_ab_uncertainty": ab_boot, "vp_ac_uncertainty": ac_boot,
        "vp_ab_weight": w_ab_dir, "vp_ac_weight": w_ac_dir,
        "orthogonality": orthogonality,
    }


# ---------------------------------------------------------------------
# BOLUM 1/3 TESHIS ALTYAPISI: "yaklasik %5-8 dusuk olcum, ozellikle dikey
# yonde" gibi bir semptomun GERCEK nedenini (global scale bias mi, eksene
# ozel/anizotropik bias mi, yoksa konuma bagli bir homografi sorunu mu)
# AYIRT etmek icin - herhangi bir "duzeltme" UYGULAMADAN ONCE. Bkz. final
# rapor: "once olc, korleme kod degistirme".
# ---------------------------------------------------------------------

AXIS_BIAS_TOLERANCE = 0.03  # %3 - "gercek degere yakin" sayilacak esik (asagidaki siniflandirmada kullanilir)


def compute_axis_scale_diagnostics(H, known_segments):
    """known_segments: [{"name", "p":(x,y), "q":(x,y), "true_length_m", "axis": "horizontal"/"vertical"/"arbitrary"}, ...]
    (p,q) GORUNTU piksel koordinatlaridir - H (goruntu->dunya) ile
    olculur. Her segment icin olculen uzunluk/oran/mutlak-goreli hata
    hesaplanir; eksen bazinda (uzunluga gore AGIRLIKLI - uzun segmentler
    tiklama gurultusune orantili olarak daha az duyarlidir) ortalama oran
    (r_x, r_y), TUM segmentlerin agirlikli ortalamasi (global_scale_ratio)
    ve r_y/r_x (axis_anisotropy) doner.

    Ayrica HER eksen icinde, KONUMA BAGLI tutarliligi (o eksendeki
    oranlarin degisim katsayisi - CV) raporlar: bu YUKSEKSE (r_x ya da
    r_y'nin KENDISI degil, o eksendeki segmentler ARASI TUTARSIZLIK),
    'ayni yon icinde konuma gore fark var -> VP/homografi hala sorunlu'
    demektir (bkz. kullanicinin teshis rehberi) - bu, TEK bir global/eksen
    olcek duzeltmesiyle COZULEMEZ, cunku sabit bir carpan degil.

    Bir 'siniflandirma' metni de doner (global scale bias / dikey-ozel /
    yatay-ozel / eksen-bagimli anizotropi / konuma-bagli tutarsizlik /
    sapma yok) - bu SADECE bir ON-YORUM, kesin bir karar degil; kesin
    karar icin AB_recovered/AC_recovered (bkz. compute_global_homography)
    ve bagimsiz cizgi/nokta residuallariyla BIRLIKTE degerlendirilmelidir."""
    segs = []
    for seg in known_segments:
        true_len = seg.get("true_length_m")
        if true_len is None or true_len <= 1e-9:
            continue
        try:
            measured = dist(apply_transform(H, seg["p"]), apply_transform(H, seg["q"]))
        except ValueError:
            continue
        ratio = measured / true_len
        segs.append({**seg, "measured_length": measured, "ratio": ratio,
                     "abs_error": measured - true_len, "rel_error": (measured - true_len) / true_len})

    def weighted_ratio(items):
        items = [s for s in items if s["ratio"] is not None]
        if not items:
            return None
        wsum = sum(s["true_length_m"] for s in items)
        return sum(s["ratio"] * s["true_length_m"] for s in items) / wsum if wsum > 1e-9 else None

    def ratio_cv(items):
        vals = [s["ratio"] for s in items]
        if len(vals) < 2:
            return None
        arr = np.array(vals, dtype=np.float64)
        return float(arr.std() / arr.mean()) if arr.mean() > 1e-9 else None

    horiz = [s for s in segs if s["axis"] == "horizontal"]
    vert = [s for s in segs if s["axis"] == "vertical"]
    r_x = weighted_ratio(horiz)
    r_y = weighted_ratio(vert)
    r_x_cv = ratio_cv(horiz)
    r_y_cv = ratio_cv(vert)
    global_scale_ratio = weighted_ratio(segs)
    axis_anisotropy = (r_y / r_x) if (r_x is not None and r_y is not None and r_x > 1e-9) else None

    POSITION_CV_TOL = 0.03  # %3 - eksen ICI konuma bagli tutarsizlik esigi
    classification = "belirsiz (yetersiz veri - en az bir yatay VE bir dikey bilinen uzunluk girin)"
    if r_x is not None and r_y is not None:
        if (r_x_cv is not None and r_x_cv > POSITION_CV_TOL) or (r_y_cv is not None and r_y_cv > POSITION_CV_TOL):
            classification = ("KONUMA BAGLI TUTARSIZLIK - ayni eksendeki segmentler birbirinden "
                               "farkli oranlar veriyor (VP/homografi hala sorunlu olabilir, TEK bir "
                               "olcek duzeltmesiyle cozulemez)")
        elif abs(r_x - 1.0) < AXIS_BIAS_TOLERANCE and abs(r_y - 1.0) < AXIS_BIAS_TOLERANCE:
            classification = "SAPMA YOK (r_x ve r_y ikisi de gercek degere yakin)"
        elif abs(r_x - r_y) < AXIS_BIAS_TOLERANCE and abs(global_scale_ratio - 1.0) > AXIS_BIAS_TOLERANCE:
            classification = "GLOBAL SCALE BIAS (r_x ~ r_y, ikisi de ayni yonde sapiyor)"
        elif abs(r_x - 1.0) < AXIS_BIAS_TOLERANCE and abs(r_y - 1.0) > AXIS_BIAS_TOLERANCE:
            classification = "DIKEY-OZEL METRIC BIAS (r_x gercek degere yakin, r_y sapiyor)"
        elif abs(r_y - 1.0) < AXIS_BIAS_TOLERANCE and abs(r_x - 1.0) > AXIS_BIAS_TOLERANCE:
            classification = "YATAY-OZEL METRIC BIAS (r_y gercek degere yakin, r_x sapiyor)"
        else:
            classification = "EKSEN-BAGIMLI ANIZOTROPI (r_x != r_y, ikisi de sapiyor)"

    return {
        "segments": segs, "r_x": r_x, "r_y": r_y, "r_x_cv": r_x_cv, "r_y_cv": r_y_cv,
        "global_scale_ratio": global_scale_ratio, "axis_anisotropy": axis_anisotropy,
        "classification": classification,
    }


def classify_query_axis(snap, p, q, angle_tol_deg=30.0):
    """Bir sorgu (p,q) cizgisinin, VERILEN referans anlik-goruntusunun
    (snap) A->B (yatay/AB) ya da A->C (dikey/AC) yonlerinden HANGISINE
    daha yakin oldugunu (± angle_tol_deg icinde) belirler - 3-nokta+2-
    uzunluk ('abc2len') akisinda img_pts sirasi hep [A,B,C,(D)] oldugu
    icin bu GECERLI bir yaklasimdir. Ne yatay ne dikeye yeterince yakinsa
    (ör. capraz/rastgele bir cizgi) 'arbitrary' doner - compute_axis_
    scale_diagnostics bu segmentleri r_x/r_y hesabina KATMAZ (sadece
    global_scale_ratio'ya katkida bulunurlar)."""
    img_pts = snap.get("img_pts")
    if not img_pts or len(img_pts) < 3:
        return "arbitrary"
    A_, B_, C_ = img_pts[0], img_pts[1], img_pts[2]
    ang_ab = math.degrees(math.atan2(B_[1] - A_[1], B_[0] - A_[0]))
    ang_ac = math.degrees(math.atan2(C_[1] - A_[1], C_[0] - A_[0]))
    ang_q = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))

    def _angdiff(a, b):
        d = abs(a - b) % 180.0
        return 180.0 - d if d > 90.0 else d

    d_ab, d_ac = _angdiff(ang_q, ang_ab), _angdiff(ang_q, ang_ac)
    if d_ab <= angle_tol_deg and d_ab <= d_ac:
        return "horizontal"
    if d_ac <= angle_tol_deg and d_ac < d_ab:
        return "vertical"
    return "arbitrary"


def validate_orthogonality(vp_ab, vp_ac, img_w, img_h, angle_deg):
    """Kullanici A-B ⟂ A-C (90 derece) VARSAYIYORSA, bunun goruntu
    KANITIYLA TUTARLI olup olmadigini, GERCEK bir kamera kalibrasyonu
    OLMADAN bile, MATEMATIKSEL OLARAK KESIN bir gerek-sart ile kontrol
    eder (bkz. metric_rectify_quad'daki AYNI f^2 turetimi):

    Iki goruntu-kacis-noktasi (vp1,vp2), ANCAK VE ANCAK dunyada birbirine
    DIK iki yonu temsil ediyorsa, ve temel nokta goruntu merkezinde
    varsayilirsa:
        f^2 = -((vp1-pp) . (vp2-pp))
    POZITIF bir gercek odak uzakligi karesi vermelidir. f^2 <= 0 cikarsa,
    HICBIR pozitif f degeri bu iki kacis noktasini "dik" yapamaz - yani
    referansin GERCEKTE 90 derece OLMADIGININ kesin (kalibrasyon-bagimsiz)
    bir kanitidir (yalnizca 90 derece varsayimi ACIKCA yapildiginda -
    custom bir aci girildiyse bu kontrol ANLAMSIZDIR ve atlanir).

    Her iki yon de sonlu (finite_strong/weak) DEGILSE (ör. biri
    near_infinity) kontrol edilemez - None doner (ne dogrulanabilir ne
    reddedilebilir, SESSIZCE 'tutarli' SAYILMAZ)."""
    if abs(angle_deg - 90.0) > 1e-6:
        return None  # kullanici zaten custom bir aci girdi - 90 derece varsayimi YOK
    if vp_ab is None or vp_ac is None:
        return None
    u0, v0 = img_w / 2.0, img_h / 2.0
    f2 = -((vp_ab[0] - u0) * (vp_ac[0] - u0) + (vp_ab[1] - v0) * (vp_ac[1] - v0))
    if f2 <= 1.0:
        return {"consistent": False, "implied_focal_px": None,
                "message": ("Referans GERCEKTE fiziksel olarak 90 derece OLMAYABILIR - "
                            "goruntudeki iki kacis noktasi, HICBIR pozitif odak uzakligi icin "
                            "dik yonlere karsilik gelmiyor (kalibrasyon-bagimsiz kesin bir kontrol).")}
    return {"consistent": True, "implied_focal_px": math.sqrt(f2), "message": None}


def metric_rectify_quad(img_pts, img_w, img_h):
    """Tek referans uzunlukla dogru olcum yapabilmek icin: 4 kosenin
    (gercekte bir DIKDORTGEN oldugu varsayimiyla) karsilikli kenar
    ciftlerinden (1-2 & 4-3, 1-4 & 2-3) iki KACIS NOKTASI (vanishing
    point) bulunur. Bu iki kacis noktasinin GERCEKTE BIRBIRINE DIK
    (dikdortgen kosesi = 90 derece) yonleri temsil ettigi varsayimindan
    kameranin odak uzakligi (f) geriye cikarilir (goruntu merkezi optik
    merkez kabul edilir). Sonra her kose, duzlemin kendi ortonormal
    (u,v) tabaninda projekte edilir.

    Sonuc: 4 noktanin GERCEK SEKLE (aci ve ORANLARA) sadik ama mutlak
    olcegi bilinmeyen (u,v) konumlari - tek bir bilinen uzunlukla bu
    olcek sabitlenebilir, boylece "genislik VE yukseklik" ikisinin de
    ayrica olculmesine gerek kalmaz.

    Bu goruntude yeterli perspektif yoksa (ör. neredeyse tam karsidan
    cekim - kenarlar goruntude paralel kaliyor) veya kacis noktalari
    matematiksel olarak tutarsizsa None doner; bu durumda cagiran kod
    eski (iki uzunluk gerektiren) yonteme donmelidir.

    ONEMLI GUVENLIK KONTROLU: bir kenar cifti goruntude neredeyse
    paralel ise (aci < ~4 derece), o yondeki kacis noktasi matematiksel
    olarak GECERLI olsa da SAYISAL OLARAK COK KARARSIZDIR - birkac
    pikselli tiklama hatasi bile sonucu %100'un uzerinde saptirabilir
    (bu, sentetik testlerle olculmus bir esiktir). Boyle durumlarda da
    None donup guvenli (iki uzunluk gerektiren) yonteme birakiyoruz.
    """
    p1, p2, p3, p4 = img_pts
    ang1 = _angle_between_dirs((p2[0] - p1[0], p2[1] - p1[1]), (p3[0] - p4[0], p3[1] - p4[1]))
    ang2 = _angle_between_dirs((p4[0] - p1[0], p4[1] - p1[1]), (p3[0] - p2[0], p3[1] - p2[1]))
    if min(ang1, ang2) < MIN_VANISHING_ANGLE_DEG:
        return None

    vp1 = _intersect_lines(_line_through(p1, p2), _line_through(p4, p3))
    vp2 = _intersect_lines(_line_through(p1, p4), _line_through(p2, p3))
    if vp1 is None or vp2 is None:
        return None

    u0, v0 = img_w / 2.0, img_h / 2.0
    f2 = -((vp1[0] - u0) * (vp2[0] - u0) + (vp1[1] - v0) * (vp2[1] - v0))
    if f2 <= 1.0:
        return None
    f = math.sqrt(f2)

    # f, bir piksel odak uzakligi - gercek kameralar icin bu, goruntu
    # boyutuyla KIYASLANABILIR olmali (tipik olarak ~0.2x - 20x arasi;
    # asiri genis acidan asiri teleye kadar). f2>1 testi SADECE tam
    # dejenere durumu eler - noktalar biraz gurultulu/sinira yakin
    # secildiginde f fizik-disi kucuk (ör. birkac piksel) cikabilir ve
    # bu durumda sonuc SESSIZCE anlamsiz olur. Boyle bir f'i reddedip
    # guvenli (iki uzunluk gerektiren) yonteme donmek daha dogru.
    scale_ref = max(img_w, img_h)
    if f < 0.2 * scale_ref or f > 20.0 * scale_ref:
        return None

    def to_ray(pt):
        return np.array([(pt[0] - u0) / f, (pt[1] - v0) / f, 1.0])

    d1, d2 = to_ray(vp1), to_ray(vp2)
    n1, n2 = np.linalg.norm(d1), np.linalg.norm(d2)
    if n1 < 1e-9 or n2 < 1e-9:
        return None
    e1, e2 = d1 / n1, d2 / n2
    normal = np.cross(e1, e2)
    nn = np.linalg.norm(normal)
    if nn < 1e-9:
        return None
    normal = normal / nn

    def to_plane_uv(pt):
        r = to_ray(pt)
        denom = float(np.dot(normal, r))
        if abs(denom) < 1e-9:
            return None
        P = r / denom
        return (float(np.dot(P, e1)), float(np.dot(P, e2)))

    raw = [to_plane_uv(p) for p in img_pts]
    if any(x is None for x in raw):
        return None
    ox, oy = raw[0]
    return [(x - ox, y - oy) for x, y in raw]


# --------------------------------------------------------------------------
# Kenar boyunca subpixel hizalama: kaba tiklanan noktalari, o kenarin
# GERCEK piksel konumuna (gradyan pikine) oturtur. Elle tiklamak yerine
# bunu kullanmak, kose/nokta konumlama hassasiyetini (ve dolayisiyla
# olcum dogrulugunu) onemli olcude artirir.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Lens distorsiyon (kavis) duzeltmesi. Genis acili ("0.5x" gibi) telefon
# lensleri belirgin fici/varil distorsiyonu icerir - duz kenarlar
# fotografta hafif kavisli gorunur. Bu, kacis noktasi (vanishing point)
# yontemi icin ciddi bir hata kaynagidir (duz cizgi varsayimini bozar).
# Kesin lens kalibrasyon verisi olmadan, kullaniciya bir kaydiricI ile
# "gozle" duzeltme yaptiriyoruz (fotograf editoru yazilimlarinda yaygin
# bir teknik) - tek parametreli standart radyal distorsiyon modeli (k1).
# --------------------------------------------------------------------------

def _distortion_K(img_w, img_h, offset_x=0.0, offset_y=0.0):
    f = float(max(img_w, img_h))
    cx = img_w / 2.0 - offset_x
    cy = img_h / 2.0 - offset_y
    return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]], dtype=np.float64)


def undistort_image(pil_img, k):
    """Tam goruntuye kalici lens duzeltmesi uygular (k=0 ise degisiklik yok)."""
    if abs(k) < 1e-6:
        return pil_img
    arr = np.array(pil_img)
    img_h, img_w = arr.shape[:2]
    K = _distortion_K(img_w, img_h)
    dist = np.array([k, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
    return Image.fromarray(cv2.undistort(arr, K, dist))


def undistort_crop(crop_pil, k, full_w, full_h, crop_left, crop_top):
    """Canli onizleme icin: sadece ekranda gorunen KIRPILMIS bolgeye
    duzeltme uygular (tam goruntuyle ayni optik merkez/odak varsayimini
    korumak icin kirpma ofsetini hesaba katar)."""
    if abs(k) < 1e-6:
        return crop_pil
    arr = np.array(crop_pil)
    K = _distortion_K(full_w, full_h, offset_x=crop_left, offset_y=crop_top)
    dist = np.array([k, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
    return Image.fromarray(cv2.undistort(arr, K, dist))


def _gradient_magnitude(gray):
    gray_f = gray.astype(np.float32)
    gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3)
    return cv2.magnitude(gx, gy)


def _sample_along(mag, center, direction, radius, step=0.25):
    h, w = mag.shape
    offsets = np.arange(-radius, radius + step, step)
    pts = center[None, :] + offsets[:, None] * direction[None, :]
    xs, ys = pts[:, 0], pts[:, 1]
    valid = (xs >= 0) & (xs <= w - 1) & (ys >= 0) & (ys <= h - 1)
    values = np.full(len(offsets), -np.inf, dtype=np.float32)
    if valid.any():
        map_x = xs[valid].astype(np.float32).reshape(-1, 1)
        map_y = ys[valid].astype(np.float32).reshape(-1, 1)
        sampled = cv2.remap(mag, map_x, map_y, interpolation=cv2.INTER_LINEAR)
        values[valid] = sampled.reshape(-1)
    return offsets, values


def _subpixel_peak(offsets, values):
    finite = np.isfinite(values)
    if finite.sum() < 3:
        return None
    idx = int(np.argmax(np.where(finite, values, -np.inf)))
    if idx == 0 or idx == len(values) - 1:
        return float(offsets[idx])
    y0, y1, y2 = values[idx - 1], values[idx], values[idx + 1]
    denom = y0 - 2 * y1 + y2
    if abs(denom) < 1e-6:
        return float(offsets[idx])
    delta = float(np.clip(0.5 * (y0 - y2) / denom, -1, 1))
    step = offsets[1] - offsets[0]
    return float(offsets[idx] + delta * step)


def _fit_line_tls(points):
    """Total least squares (dik mesafeyi minimize eden) dogru fit."""
    centroid = points.mean(axis=0)
    centered = points - centroid
    cov = centered.T @ centered
    eigvals, eigvecs = np.linalg.eigh(cov)
    direction = eigvecs[:, np.argmax(eigvals)]
    direction = direction / np.linalg.norm(direction)
    normal = np.array([-direction[1], direction[0]])
    return centroid, direction, normal


# --------------------------------------------------------------------------
# Otomatik lens distorsiyon tahmini ("plumb-line" yontemi). Kaydiriciyi
# gozle ayarlamak yerine: kullanici, GERCEKTE DUZ olan (ama distorsiyon
# yuzunden fotografta hafifce kavisli gorunen) bir kenar boyunca 3+ nokta
# tiklar; k, o noktalarin duzeltme sonrasi MUMKUN OLDUGUNCA DUZ bir
# dogruya oturmasini saglayacak sekilde secilir. Checkerboard/ozel
# kalibrasyon hedefi gerektirmeyen, tek fotografla calisan klasik bir
# teknik (Brown, 1971). Birden fazla kenar (ideal olarak biri yataya,
# biri dikeye yakin) verilirse tahmin daha saglam olur.
# --------------------------------------------------------------------------

def _undistort_points_k(pts, img_w, img_h, k):
    pts = np.asarray(pts, dtype=np.float64)
    if abs(k) < 1e-9:
        return pts.copy()
    K = _distortion_K(img_w, img_h)
    dist = np.array([k, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
    src = pts.reshape(-1, 1, 2)
    und = cv2.undistortPoints(src, K, dist, P=K)
    return und.reshape(-1, 2)


def _line_straightness_cost(k, lines, img_w, img_h):
    total = 0.0
    for pts in lines:
        und = _undistort_points_k(pts, img_w, img_h, k)
        centroid, _, normal = _fit_line_tls(und)
        resid = (und - centroid) @ normal
        total += float(np.sum(resid ** 2))
    return total


def estimate_distortion_k(lines, img_w, img_h, k_range=(-1.0, 1.0)):
    """1 ya da daha fazla dogru (her biri, gercekte duz olan bir kenar
    uzerinde tiklanmis en az 3 nokta) icin, duzeltme sonrasi TUM
    noktalarin kendi dogrularina olan dik-mesafe-karesi toplamini en aza
    indiren tek bir radyal distorsiyon katsayisini (k) bulur.

    Once kaba bir grid taramasiyla yaklasik minimum bolgesi bulunur
    (maliyet fonksiyonu k'ya gore her zaman tek-tepeli/unimodal olmayabilir
    - ör. noktalar goruntu merkezine cok yakinsa distorsiyonun etkisi kucuk
    kalir ve fonksiyon oldukca duzlesir), sonra o bolgede altin oran
    aramasiyla ince ayar yapilir."""
    lines = [np.asarray(p, dtype=np.float64) for p in lines if len(p) >= 3]
    if not lines:
        raise ValueError("En az 3 noktali (ayni kenar uzerinde) 1 cizgi gerekli.")

    lo, hi = k_range
    grid = np.linspace(lo, hi, 81)
    costs = [_line_straightness_cost(float(k), lines, img_w, img_h) for k in grid]
    best_idx = int(np.argmin(costs))

    a = float(grid[max(0, best_idx - 2)])
    b = float(grid[min(len(grid) - 1, best_idx + 2)])
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc = _line_straightness_cost(c, lines, img_w, img_h)
    fd = _line_straightness_cost(d, lines, img_w, img_h)
    for _ in range(60):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = _line_straightness_cost(c, lines, img_w, img_h)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = _line_straightness_cost(d, lines, img_w, img_h)
        if b - a < 1e-6:
            break
    return float((a + b) / 2.0)


# --------------------------------------------------------------------------
# Referans bolgesinden "ekstrapolasyon" uzakligi. Projektif/afin
# donusumler, kalibre edilen (referans noktalarinin kapladigi) bolgenin
# DISINA cikildikca kucuk tiklama/model hatalarini orantisiz buyutebilir
# (bkz. compute_homography ustundeki not) - bu, sadece referans
# noktalarina yakin degil, fotografin HER YERINDE tutarli sonuc bekleyen
# kullanicilar icin en sik yanilgi kaynagidir. Bu fonksiyon, bir sorgunun
# ne kadar "ekstrapolasyon" gerektirdigini kaba ama kullanisli tek bir
# sayiyla (referans bolgesinin capina oranla kac kati uzakta oldugu)
# ozetler; sonuclar panelinde kullaniciyi uyarmak icin kullanilir.
# --------------------------------------------------------------------------

def extrapolation_ratio(ref_img_pts, query_img_pts):
    ref = np.asarray(ref_img_pts, dtype=np.float64)
    if len(ref) < 2:
        return None
    x0, y0 = ref[:, 0].min(), ref[:, 1].min()
    x1, y1 = ref[:, 0].max(), ref[:, 1].max()
    span = max(x1 - x0, y1 - y0, 1e-6)

    def dist_outside(pt):
        dx = max(x0 - pt[0], 0.0, pt[0] - x1)
        dy = max(y0 - pt[1], 0.0, pt[1] - y1)
        return math.hypot(dx, dy)

    d = max(dist_outside(p) for p in query_img_pts)
    return d / span


def refine_edge_points(gray, rough_points, search_radius=6.0, iterations=2):
    """Kenar uzerinde kaba tiklanan noktalari subpixel hassasiyette gercek
    kenara oturtur (TLS dogru fit + dogruya dik yonde gradyan piki arama,
    birkac iterasyonla stabilize). Sonuc: (refined_points, centroid,
    direction, endpoint1, endpoint2) - endpoint'ler, refine edilmis
    noktalarin dogru uzerine izdusumunun en uc ikisidir."""
    points = np.asarray(rough_points, dtype=np.float64)
    mag = _gradient_magnitude(gray)

    for _ in range(iterations):
        centroid, direction, normal = _fit_line_tls(points)
        refined = []
        for p in points:
            offsets, values = _sample_along(mag, p, normal, search_radius)
            peak_offset = _subpixel_peak(offsets, values)
            refined.append(p if peak_offset is None else p + peak_offset * normal)
        points = np.array(refined)

    centroid, direction, _ = _fit_line_tls(points)
    projections = (points - centroid) @ direction
    end1 = centroid + projections.min() * direction
    end2 = centroid + projections.max() * direction
    return points, centroid, direction, (float(end1[0]), float(end1[1])), (float(end2[0]), float(end2[1]))


class MeasureApp(tk.Tk):
    def _prompt_measurement_mode(self):
        """BOLUM A: uygulama baslarken kullaniciya "Kac fotograf?" sorusunu
        sorar. "1 Fotograf" (tek-goruntu, tek-view single-view metrology -
        stratified rektifikasyon) TAM CALISIR ve varsayilan/onerilen
        secenektir. "2 Fotograf" (iki-goruntu coklu-gorunum SfM - essential
        matrix/homografi ayristirma/triangulation/olcek kurtarma) icin
        matematiksel CEKIRDEK bu surumde TAMAMLANDI ve GERCEK sentetik
        testlerle dogrulandi (bkz. compute_two_view_reconstruction ve
        tests/test_two_view_geometry.py - 7/7 test geciyor), ANCAK bu
        surumde ETKILESIMLI ARAYUZU (iki fotograf yukleme, goruntude
        eslesme gosterimi, sonuc paneli) HENUZ BAGLANMADI - bu ACIKCA
        soylenir, YARIM bir ozellik TAM calisirmis gibi SUNULMAZ."""
        use_one = messagebox.askyesno(
            "Olcum Modu",
            "Kac fotograf kullanmak istiyorsunuz?\n\n"
            "EVET = 1 Fotograf (tek-goruntu projektif rektifikasyon - TAM CALISIR, onerilen)\n"
            "HAYIR = 2 Fotograf (iki-goruntu coklu-gorunum/SfM geometrisi)\n\n"
            "NOT: 2 fotograf modunun matematiksel cekirdegi (essential matrix, homografi "
            "ayristirma, triangulation, olcek kurtarma) bu surumde tamamlandi ve gercek "
            "testlerle dogrulandi, ANCAK etkilesimli arayuzu (iki fotograf yukleme, eslesme "
            "gosterimi) HENUZ bu surume baglanmadi. Su an icin sadece 1 Fotograf modu tam "
            "calisir durumda.",
        )
        if not use_one:
            messagebox.showinfo(
                "2 Fotograf Modu - Arayuz Henuz Hazir Degil",
                "2 fotograf modunun matematiksel cekirdegi (compute_two_view_reconstruction ve "
                "ilgili fonksiyonlar: ozellik eslestirme, essential matrix/homografi ayristirma, "
                "triangulation, duzlem fit, olcek kurtarma) uygulamaya eklendi ve sentetik "
                "testlerle dogrulandi.\n\n"
                "Ancak bu surumde ETKILESIMLI kullanici arayuzu (iki fotograf yukleme, her "
                "ikisinde de A/B/C isaretleme, sonuc paneli) HENUZ YOK.\n\n"
                "Su an icin 1 Fotograf moduna devam ediliyor."
            )
            return "two_photo_core_only"
        return "single"

    def __init__(self):
        super().__init__()
        self.title("Fotograftan Uzunluk Olcumu")
        self.geometry("1500x900")
        # Acilista soru sorulmaz: 2-fotograf modunun arayuzu henuz yok, bu yuzden
        # dogrudan 1-fotograf modu (bkz. _prompt_measurement_mode - korunuyor).
        self.measurement_mode = "single"

        self.pil_img = None
        self.pil_img_original = None
        self.sharpened = False
        self.photo_path = None
        self.pdf_page = None
        self.photo_exif = None  # Route A (kamera pozu) icin - bkz. estimate_camera_intrinsics_from_exif
        self.fit_scale = 1.0
        self.view_scale = 1.0    # canvas piksel / orijinal resim pikseli
        self.view_x = 0.0        # canvas'in sol-ustune denk gelen orijinal resim X
        self.view_y = 0.0
        self.tk_img = None
        self._pan_start = None

        self.points = []          # [{label, x, y}]
        self.queries = []         # [{name, a, b, ground_truth_m}]

        self.edge_mode = False
        self.edge_rough_points = []   # [(x,y), ...] orijinal resim pikseli

        self.line_calib_mode = False
        self.line_calib_current = []   # aktif ("bitirilmemis") duz kenarin kaba noktalari
        self.line_calib_lines = []     # bitirilmis duz kenarlar: [[(x,y), ...], ...]

        # YARDIMCI CIZGILER: noktalardan AYRI geometrik gozlemler (kontrol/
        # olcum noktasi DEGIL). Hem nokta-sonrasi akis hem de "Daha Yuksek
        # Dogruluk" paneli (eski nokta-cifti comboboxlari dahil) AYNI listeyi
        # kullanir. Ornek kayit:
        #   {"id": "HL1", "p1": [x, y], "p2": [x, y], "family": "ab"|"ac"|"auto",
        #    "source": "manual"|"manual_magnifier"|"manual_refined"|"point_pair",
        #    "anchor_label": "B"|None, "point_labels": [l1, l2]|None,
        #    "verified": True, "endpoint_sigma_px": 1.0, "n_support": 2,
        #    "sigma_angle_deg": ..., "note": ""}
        self.helper_lines = []
        self._helper_counter = 0
        # Yardimci cizgi yakalama durumu (normal nokta/kenar/lens modlarindan
        # AYRI): {"family", "anchor_label", "points": [(x,y)], "sigmas": [px]}
        self.helper_capture = None
        self.helper_status = {}        # son cozumdeki cizgi tutarliligi: {id: {...}}
        self._selected_helper_id = None
        self._vp_stage_cache = (None, None)
        self._pan_press_xy = None

        # Kolay mod (adim adim sihirbaz): "open" -> "A" -> "B" -> "C" ->
        # "lengths" -> "measure". Gelismis paneller gizli; sorular yok.
        self.easy_mode = True
        self.advanced_visible = False
        self.wizard_step = "open"
        self.wizard_pending = None      # olcumde ilk tiklanan nokta
        self._wizard_counter = 0

        self.unit_var = tk.StringVar(value="m")
        self.ref_mode_var = tk.StringVar(value="abc2len")
        self.coords_rows = []          # [{"label":..., "x_m":..., "y_m":...}, ...] ("coords" modu)
        self._last_confirmed_ref_signature = None
        self._last_unit = "m"

        self.plane_corners = None     # [label1,label2,label3,label4]
        self.plane_width_m = None
        self.plane_height_m = None
        self.plane_H = None           # image -> world(metre) homografisi
        self.plane_Hinv = None
        self.plane_calibrated = False  # True: gercek uzunluklarla olcekli; False: sadece egim onizlemesi
        self.plane_origin = None      # izgara tabani: dunya orijini (=world_pts[0])
        self.plane_axis1 = None       # izgara tabani: 1->2 kenar vektoru (dunya)
        self.plane_axis2 = None       # izgara tabani: 2->3 kenar vektoru (dunya, 1'e dik OLMAK ZORUNDA DEGIL)
        # model_type: "projective" (D gercek/kismi kacis noktasindan) ya da
        # "affine_local" (yeterli kanit yok, D=B+C-A afin yaklasimi) - grid
        # cizimi VE olcum guvenilirlik etiketleri bunu kullanir (bkz.
        # _draw_grid, compute()).
        self.plane_model_type = None
        self.plane_vp_confidence = "N/A"   # "YUKSEK" / "ORTA" / "N/A"
        self.plane_vanishing_points = {"ab": None, "ac": None}
        # d_route: D hangi rotadan geldi - "camera_pose" (Route A, P3P/SQPNP),
        # "vanishing_point" (Route B) ya da "affine_fallback" (kanit yok).
        self.plane_d_route = None
        # camera_status: "EXIF YAKLASIK" / "BILINMIYOR" - gercek bir kalibrasyon
        # profili henuz YOK (bkz. Bolum 4/5) - EXIF K SADECE baslangic tahmini.
        self.plane_camera_status = "BILINMIYOR"
        # kademeli (stratified) rektifikasyon sonucu (Bolum 3-13) - varsa,
        # tercih edilen ana yontem budur (bkz. _recompute_plane_abc2len).
        self.plane_strat_result = None
        # BAGIMSIZ dogrulama (Bolum 17/18): H_final'i KURAN kanitin OTESINDEKI
        # gozlemlerle (ek/otomatik cizgiler) acisal tutarlilik - bkz.
        # _line_family_angular_stats / compute_global_homography.
        self.plane_line_residuals = {"ab": None, "ac": None}
        self.plane_point_reproj = None
        self.plane_condition_number = None
        self.plane_quality = "N/A"
        self.plane_img_pts = None
        self.plane_world_pts = None
        self.plane_point_sources = None

        self.last_results = {}        # {query_name: metre}

        self.saved_planes = []        # [{name, mode, corners, H, width_m, height_m, lengths_m}]
        self._ref_counter = 0
        self._last_ref_corners = None
        self._last_ref_label = None

        self.font_small = load_font(14)
        self.font_label = load_font(16)

        self._build_menu()
        self._build_layout()
        self._apply_ref_mode()

    # ---------- Menu ----------

    def _build_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Fotograf / PDF Ac...", command=self.open_photo)
        filemenu.add_separator()
        filemenu.add_command(label="Config Yukle (JSON)...", command=self.load_config)
        filemenu.add_command(label="Config Kaydet (JSON)...", command=self.save_config)
        filemenu.add_separator()
        filemenu.add_command(label="Isaretli Gorseli Kaydet...", command=self.save_annotated)
        filemenu.add_separator()
        filemenu.add_command(label="Cikis", command=self.destroy)
        menubar.add_cascade(label="Dosya", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Nasil kullanilir?", command=self.show_help)
        menubar.add_cascade(label="Yardim", menu=helpmenu)
        self.config(menu=menubar)

    # ---------- Layout ----------

    def _build_layout(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=8, pady=8)

        # --- Sol: canvas ---
        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        toolbar = ttk.Frame(left)
        toolbar.pack(fill="x", pady=(0, 6))
        self._toolbar_main = toolbar
        ttk.Button(toolbar, text="Fotograf / PDF Ac", command=self.open_photo).pack(side="left")
        ttk.Label(toolbar, text="Birim:").pack(side="left", padx=(16, 2))
        unit_combo = ttk.Combobox(toolbar, textvariable=self.unit_var, values=list(UNITS.keys()),
                                   state="readonly", width=5)
        unit_combo.pack(side="left")
        unit_combo.bind("<<ComboboxSelected>>", self._on_unit_change)
        ttk.Button(toolbar, text="Sigdir", command=self.reset_view).pack(side="left", padx=(12, 0))
        ttk.Button(toolbar, text="Netlestir", command=self.toggle_sharpen).pack(side="left", padx=(6, 0))
        self.show_grid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar, text="Izgara", variable=self.show_grid_var,
                        command=self._redraw).pack(side="left", padx=(10, 0))
        self.advanced_btn = ttk.Button(toolbar, text="Gelismis ▸", command=self.toggle_advanced)
        self.advanced_btn.pack(side="right")
        self.status_var = tk.StringVar(value="Once bir fotograf acin.")
        ttk.Label(toolbar, textvariable=self.status_var, foreground="#555").pack(side="left", padx=12)

        # Kolay mod talimat seridi (adim adim sihirbaz)
        self._build_wizard_banner(left)

        toolbar_adv = ttk.Frame(left)
        self.easy_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar_adv, text="Adim adim sihirbaz", variable=self.easy_mode_var,
                        command=self._on_easy_mode_toggle).pack(side="left")
        ttk.Button(toolbar_adv, text="Son Noktayi Sil", command=self.undo_last_point).pack(side="left", padx=(12, 0))
        self.magnifier_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar_adv, text="Buyutecli Nokta Ekleme", variable=self.magnifier_var).pack(
            side="left", padx=(12, 0))
        self.helper_prompt_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar_adv, text="Noktadan sonra yardimci cizgi oner",
                        variable=self.helper_prompt_var).pack(side="left", padx=(12, 0))

        toolbar2 = ttk.Frame(left)
        ttk.Label(toolbar2, text="Kontrast (sadece ekran gorunumu):").pack(side="left")
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = ttk.Scale(toolbar2, from_=0.5, to=2.5, orient="horizontal",
                                    variable=self.contrast_var, length=160,
                                    command=self._on_contrast_change)
        contrast_scale.pack(side="left", padx=6)
        self.contrast_label = ttk.Label(toolbar2, text="1.00x", width=6)
        self.contrast_label.pack(side="left")
        ttk.Button(toolbar2, text="Kontrasti Sifirla", command=self._reset_contrast).pack(side="left", padx=(6, 0))

        toolbar_lens = ttk.Frame(left)
        ttk.Label(toolbar_lens, text="Lens Duzeltmesi (kavisli kenarlari duzler, ör. 0.5x genis acili fotolar):").pack(
            side="left")
        self.distortion_k_var = tk.DoubleVar(value=0.0)
        distortion_scale = ttk.Scale(toolbar_lens, from_=-1.0, to=1.0, orient="horizontal",
                                      variable=self.distortion_k_var, length=160,
                                      command=self._on_distortion_change)
        distortion_scale.pack(side="left", padx=6)
        self.distortion_label = ttk.Label(toolbar_lens, text="0.00", width=6)
        self.distortion_label.pack(side="left")
        ttk.Button(toolbar_lens, text="Uygula (Kaydet)", command=self.apply_distortion_correction).pack(
            side="left", padx=(6, 0))
        ttk.Button(toolbar_lens, text="Sifirla", command=self._reset_distortion_preview).pack(
            side="left", padx=(6, 0))

        toolbar_lens2 = ttk.Frame(left)
        self.line_calib_btn = ttk.Button(toolbar_lens2, text="Duz Kenar Modu: KAPALI",
                                          command=self.toggle_line_calib_mode)
        self.line_calib_btn.pack(side="left")
        ttk.Button(toolbar_lens2, text="Bu Kenari Bitir", command=self.finish_line_calib_line).pack(
            side="left", padx=6)
        ttk.Button(toolbar_lens2, text="Son Noktayi Sil", command=self.undo_line_calib_point).pack(
            side="left", padx=6)
        ttk.Button(toolbar_lens2, text="Tumunu Temizle", command=self.clear_line_calib).pack(
            side="left", padx=6)
        ttk.Button(toolbar_lens2, text="Otomatik k Tahmin Et", command=self.auto_estimate_distortion).pack(
            side="left", padx=(12, 0))
        ttk.Label(toolbar_lens2,
                  text="(Yukaridaki kaydiriciyi gozle ayarlamak yerine: gercekte DUZ olan bir kenar\n"
                       "-ör. bir pencere sirasi, cati hatti- boyunca 3+ nokta tiklayip 'Bitir'e basin;\n"
                       "1-2 kenar yeterli. k, bu noktalari en duz hale getirecek sekilde hesaplanir.)",
                  foreground="#777").pack(side="left", padx=8)

        toolbar3 = ttk.Frame(left)
        self.edge_mode_btn = ttk.Button(toolbar3, text="Kenar Hizalama Modu: KAPALI",
                                         command=self.toggle_edge_mode)
        self.edge_mode_btn.pack(side="left")
        ttk.Button(toolbar3, text="Hizala ve 2 Nokta Ekle", command=self.finalize_edge_alignment).pack(
            side="left", padx=6)
        ttk.Button(toolbar3, text="Son Kaba Noktayi Sil", command=self.undo_edge_rough_point).pack(
            side="left", padx=6)
        ttk.Label(toolbar3, text="(Kenar boyunca 2+ kaba nokta tiklayin - kirmizi; "
                                  "gercek kenara subpixel hassasiyette oturtulur)",
                  foreground="#777").pack(side="left", padx=8)

        self._adv_toolbars = [toolbar_adv, toolbar2, toolbar_lens, toolbar_lens2, toolbar3]
        hint = ttk.Label(left, text="Fare tekerlegi: yakinlastir/uzaklastir   |   Sag tik + surukle VEYA "
                                     "kenardaki kaydirma cubuklari: yukari/asagi/sag/sol kaydir",
                          foreground="#777")
        hint.pack(fill="x")
        self._hint_label = hint

        canvas_frame = ttk.Frame(left)
        canvas_frame.pack(fill="both", expand=True)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="#222", width=MAX_CANVAS_W, height=MAX_CANVAS_H,
                                 highlightthickness=1, highlightbackground="#888")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<ButtonPress-3>", self.on_pan_start)
        self.canvas.bind("<B3-Motion>", self.on_pan_move)
        self.canvas.bind("<ButtonRelease-3>", self.on_pan_release)
        self.canvas.bind("<Motion>", self._on_canvas_motion)
        self.bind("<Escape>", lambda e: self.cancel_helper_capture())
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self.vscroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self._on_vscroll)
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self._on_hscroll)
        self.hscroll.grid(row=1, column=0, sticky="ew")

        # --- Sag: scrollable panel ---
        right_container = ttk.Frame(main, width=460)
        self.right_container = right_container
        right_container.pack_propagate(False)

        right_canvas = tk.Canvas(right_container, highlightthickness=0)
        right_scroll = ttk.Scrollbar(right_container, orient="vertical", command=right_canvas.yview)
        right_canvas.configure(yscrollcommand=right_scroll.set)
        right_scroll.pack(side="right", fill="y")
        right_canvas.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(right_canvas)
        right_canvas.create_window((0, 0), window=right, anchor="nw", width=440)
        right.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))

        # Noktalar
        pts_frame = ttk.LabelFrame(right, text="Noktalar")
        pts_frame.pack(fill="x", pady=(0, 8))
        self.pts_frame = pts_frame
        self.tree = ttk.Treeview(pts_frame, columns=("label", "xy"), show="headings", height=5)
        self.tree.heading("label", text="Etiket")
        self.tree.heading("xy", text="Resim X,Y")
        self.tree.column("label", width=100)
        self.tree.column("xy", width=140)
        self.tree.pack(fill="x", padx=4, pady=4)
        ttk.Button(pts_frame, text="Secili Noktayi Sil", command=self.delete_point).pack(
            anchor="w", padx=4, pady=(0, 4))

        # Referans olusturma - TEK akis (3 nokta + 2 uzunluk, D otomatik).
        # ONEMLI: kullaniciya birden fazla referans YONTEMI arasinda secim
        # YAPTIRMIYORUZ - ref_mode_var sabit "abc2len" olarak kalir. Eski
        # afin(3-nokta)/4-kose/N-nokta hesaplama kodlari (asagida) ve
        # bunlarin widget'lari, REGRESYON TESTLERI ve olasi arka-plan
        # kullanimlari icin BILEREK korunuyor - sadece GORUNMUYORLAR
        # (hicbir yerde pack() edilmiyorlar). Bkz. _apply_ref_mode.
        ref_mode_frame = ttk.Frame(right)  # gorunmez capa (eski kod pack(after=...) icin kullanir)
        self.ref_mode_frame = ref_mode_frame

        # --- 3 referans noktasi (afin, SSS ucgen) - GIZLI, sadece regresyon/arka plan icin ---
        self.affine3_frame = ttk.LabelFrame(right, text="Referans Noktalari (3 Nokta)")

        info3 = ("3 referans noktasi secin (sirayla 1,2,3).\n\n"
                 "1-2 VE 2-3 uzunluklarini girmeniz yeterlidir (Nokta 2'de\n"
                 "90 derece varsayilir, 1-3'u olcmenize gerek yok).\n\n"
                 "Daha kesin sonuc icin (Nokta 2'nin gercekte 90 derece\n"
                 "olmasi gerekmeden) 1-3 uzunlugunu da girebilirsiniz -\n"
                 "o zaman hicbir aci varsayimi yapilmaz (SSS).\n\n"
                 "Fotografta guclu egim/perspektif varsa '4 Kose' yontemi\n"
                 "daha dogru sonuc verir.")
        ttk.Label(self.affine3_frame, text=info3, foreground="#555", justify="left").pack(
            anchor="w", padx=4, pady=(4, 6))

        self.tri_combos = []
        for i in range(3):
            row = ttk.Frame(self.affine3_frame)
            row.pack(fill="x", padx=4, pady=2)
            ttk.Label(row, text=f"Nokta {i + 1}:", width=8).pack(side="left")
            cb = ttk.Combobox(row, width=10, state="readonly")
            cb.pack(side="left", padx=4)
            cb.bind("<<ComboboxSelected>>", self._on_corner_combo_change)
            self.tri_combos.append(cb)

        self.tri_len_entries = []
        for label_text in ("1-2 Uzunluk:", "2-3 Uzunluk:", "1-3 (opsiyonel):"):
            row = ttk.Frame(self.affine3_frame)
            row.pack(fill="x", padx=4, pady=2)
            ttk.Label(row, text=label_text, width=12).pack(side="left")
            e = ttk.Entry(row, width=8)
            e.pack(side="left", padx=4)
            e.bind("<KeyRelease>", self._try_auto_compute_plane)
            self.tri_len_entries.append(e)

        # --- 4 kose (projektif) ---
        self.quad4_frame = ttk.LabelFrame(right, text="Duzlem Kosesi (4 Nokta)")

        info4 = ("Gercekte DIKDORTGEN olan bir yuzeyin (duvar, kapi, cati\n"
                 "yuzu vb.) 4 kosesini sirayla secin (1->2->3->4). Uzunluklari\n"
                 "girmeden once bile egim onizlemesini hemen gorursunuz.\n\n"
                 "ONERILEN: Genislik VE Yukseklik/Egim - ikisini de biliyorsaniz\n"
                 "girin (tahmin yok, en dogru sonuc). Sadece birini biliyorsaniz\n"
                 "digeri kacis noktalarindan (vanishing point) TAHMIN edilir\n"
                 "(genelde <%1 hata ama garantili degil).")
        ttk.Label(self.quad4_frame, text=info4, foreground="#555", justify="left").pack(
            anchor="w", padx=4, pady=(4, 6))

        self.corner_combos = []
        for i in range(4):
            row = ttk.Frame(self.quad4_frame)
            row.pack(fill="x", padx=4, pady=2)
            ttk.Label(row, text=f"Kose {i + 1}:", width=8).pack(side="left")
            cb = ttk.Combobox(row, width=10, state="readonly")
            cb.pack(side="left", padx=4)
            cb.bind("<<ComboboxSelected>>", self._on_corner_combo_change)
            self.corner_combos.append(cb)

        prow1 = ttk.Frame(self.quad4_frame)
        prow1.pack(fill="x", padx=4, pady=(6, 2))
        ttk.Label(prow1, text="Genislik (Kose1-Kose2):").pack(side="left")
        self.plane_width_entry = ttk.Entry(prow1, width=8)
        self.plane_width_entry.pack(side="left", padx=4)
        self.plane_width_entry.bind("<KeyRelease>", self._try_auto_compute_plane)

        prow2 = ttk.Frame(self.quad4_frame)
        prow2.pack(fill="x", padx=4, pady=(2, 6))
        ttk.Label(prow2, text="Yukseklik/Egim (Kose2-Kose3):").pack(side="left")
        self.plane_height_entry = ttk.Entry(prow2, width=8)
        self.plane_height_entry.pack(side="left", padx=4)
        self.plane_height_entry.bind("<KeyRelease>", self._try_auto_compute_plane)

        # --- N-nokta (gercek duzlem koordinati) ---
        self.coords_frame = ttk.LabelFrame(right, text="Referans Noktalari (Gercek Duzlem Koordinati)")

        info_coords = ("Her referans noktasi icin, AYNI duzlemde ortak bir X,Y\n"
                       "ekseni secip GERCEK koordinatini (metre) girin - dikdortgen\n"
                       "VEYA baska hicbir sekil VARSAYILMAZ. En az 4 nokta gerekir.\n\n"
                       "5+ nokta girerseniz fazlalar EN KUCUK KARELER ile kullanilir:\n"
                       "hem tiklama hatalarina karsi daha saglam olur, HEM DE referansi\n"
                       "genis bir alana yayarak o alanin TAMAMINDA (kucuk tek bir\n"
                       "referanstan uzak bolgelerde buyuyen hatayi azaltarak) daha\n"
                       "dogru sonuc verir.\n\n"
                       "Ipucu: bir noktayi (0,0) yapip digerlerini ona gore olcmek\n"
                       "en kolayidir.")
        ttk.Label(self.coords_frame, text=info_coords, foreground="#555", justify="left").pack(
            anchor="w", padx=4, pady=(4, 6))

        self.coords_tree = ttk.Treeview(self.coords_frame, columns=("label", "x", "y"),
                                         show="headings", height=5)
        self.coords_tree.heading("label", text="Nokta")
        self.coords_tree.heading("x", text="Gercek X")
        self.coords_tree.heading("y", text="Gercek Y")
        self.coords_tree.column("label", width=70)
        self.coords_tree.column("x", width=90)
        self.coords_tree.column("y", width=90)
        self.coords_tree.pack(fill="x", padx=4, pady=4)

        coords_add_row = ttk.Frame(self.coords_frame)
        coords_add_row.pack(fill="x", padx=4, pady=2)
        self.coords_point_combo = ttk.Combobox(coords_add_row, width=8, state="readonly")
        self.coords_point_combo.pack(side="left", padx=(0, 4))
        self.coords_x_entry = ttk.Entry(coords_add_row, width=7)
        self.coords_x_entry.pack(side="left", padx=2)
        self.coords_y_entry = ttk.Entry(coords_add_row, width=7)
        self.coords_y_entry.pack(side="left", padx=2)
        ttk.Button(coords_add_row, text="Ekle", command=self._add_coords_row).pack(side="left", padx=4)

        ttk.Button(self.coords_frame, text="Secili Satiri Sil", command=self._delete_coords_row).pack(
            anchor="w", padx=4, pady=(0, 6))

        # --- 3 Nokta + 2 Uzunluk (4. kose otomatik) ---
        self.abc2len_frame = ttk.LabelFrame(right, text="Referans Olustur")

        info_abc = ("1) A, B, C olmak uzere UC nokta secin (A ortak kose;\n"
                    "   AB ve AC iki referans kenari olur).\n"
                    "2) AB ve AC'nin GERCEK uzunluklarini girin.\n"
                    "3) 4. kose (D) OTOMATIK olusturulur - elle isaretlemenize\n"
                    "   gerek yoktur.\n\n"
                    "A'daki aci bilinmiyorsa 'Dikdortgen' varsayilir (90°);\n"
                    "degilse gercek aciyi girin.")
        ttk.Label(self.abc2len_frame, text=info_abc, foreground="#555", justify="left",
                  wraplength=410).pack(anchor="w", padx=4, pady=(4, 6))

        self.abc_combos = []
        for label_text in ("A (ortak kose):", "B:", "C:"):
            row = ttk.Frame(self.abc2len_frame)
            row.pack(fill="x", padx=4, pady=2)
            ttk.Label(row, text=label_text, width=12).pack(side="left")
            cb = ttk.Combobox(row, width=10, state="readonly")
            cb.pack(side="left", padx=4)
            cb.bind("<<ComboboxSelected>>", self._on_corner_combo_change)
            self.abc_combos.append(cb)

        self.abc_len_entries = []
        for label_text in ("AB Uzunluk:", "AC Uzunluk:"):
            row = ttk.Frame(self.abc2len_frame)
            row.pack(fill="x", padx=4, pady=2)
            ttk.Label(row, text=label_text, width=12).pack(side="left")
            e = ttk.Entry(row, width=8)
            e.pack(side="left", padx=4)
            e.bind("<KeyRelease>", self._try_auto_compute_plane)
            self.abc_len_entries.append(e)

        self.abc_right_angle_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.abc2len_frame, text="A'daki aci 90 derece (dikdortgen)",
                        variable=self.abc_right_angle_var,
                        command=self._try_auto_compute_plane).pack(anchor="w", padx=4, pady=2)
        angle_row = ttk.Frame(self.abc2len_frame)
        angle_row.pack(fill="x", padx=4, pady=2)
        ttk.Label(angle_row, text="Degilse gercek aci (derece):", width=20).pack(side="left")
        self.abc_angle_entry = ttk.Entry(angle_row, width=8)
        self.abc_angle_entry.pack(side="left", padx=4)
        self.abc_angle_entry.bind("<KeyRelease>", self._try_auto_compute_plane)

        # Yardimci cizgiler: A-B ya da A-C ile GERCEKTE paralel olan baska
        # kenarlar. Nokta-sonrasi akisla eklenenler ve asagidaki eski
        # nokta-cifti secimleri AYNI self.helper_lines listesine yazilir.
        self.helper_lines_frame = ttk.LabelFrame(self.abc2len_frame, text="Daha Yuksek Dogruluk (opsiyonel)")
        self.helper_lines_frame.pack(fill="x", padx=4, pady=(8, 4))
        ttk.Label(self.helper_lines_frame,
                  text="Yardimci cizgi, A-B veya A-C ile gercekte paralel olan baska bir kenardir. "
                       "Fotografin farkli bir bolgesindeki uzun ve net bir kenar secmek perspektif "
                       "hesabini iyilestirir. (Kenar, A/B/C ile AYNI yuzeyde olmali - zemin, yan "
                       "duvar, balkon onu ya da pencere icindeki girinti kullanilmamali.)",
                  foreground="#555", justify="left", wraplength=410).pack(anchor="w", padx=4, pady=(4, 4))

        hl_opts = ttk.Frame(self.helper_lines_frame)
        hl_opts.pack(fill="x", padx=4, pady=2)
        self.show_helpers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(hl_opts, text="Yardimci cizgileri goster", variable=self.show_helpers_var,
                        command=self._redraw).pack(side="left")
        self.helper_refine_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(hl_opts, text="Kenara oturt (subpixel)", variable=self.helper_refine_var).pack(
            side="left", padx=(10, 0))

        hl_new = ttk.Frame(self.helper_lines_frame)
        hl_new.pack(fill="x", padx=4, pady=2)
        ttk.Label(hl_new, text="Yeni kenar sec:").pack(side="left")
        ttk.Button(hl_new, text="AB yonu", command=lambda: self.start_helper_capture("ab")).pack(side="left", padx=2)
        ttk.Button(hl_new, text="AC yonu", command=lambda: self.start_helper_capture("ac")).pack(side="left", padx=2)
        ttk.Button(hl_new, text="Otomatik", command=lambda: self.start_helper_capture("auto")).pack(side="left", padx=2)

        self.helper_tree = ttk.Treeview(self.helper_lines_frame,
                                        columns=("id", "family", "source", "anchor", "status"),
                                        show="headings", height=4, selectmode="browse")
        for col, txt, wdt in (("id", "ID", 50), ("family", "Yon", 50), ("source", "Kaynak", 95),
                              ("anchor", "Capa", 45), ("status", "Tutarlilik", 150)):
            self.helper_tree.heading(col, text=txt)
            self.helper_tree.column(col, width=wdt, stretch=(col == "status"))
        self.helper_tree.pack(fill="x", padx=4, pady=2)
        self.helper_tree.bind("<<TreeviewSelect>>", self._on_helper_tree_select)
        hl_btns = ttk.Frame(self.helper_lines_frame)
        hl_btns.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Button(hl_btns, text="Sil", command=self.delete_selected_helper).pack(side="left")
        ttk.Button(hl_btns, text="AB yap", command=lambda: self.set_selected_helper_family("ab")).pack(
            side="left", padx=2)
        ttk.Button(hl_btns, text="AC yap", command=lambda: self.set_selected_helper_family("ac")).pack(
            side="left", padx=2)
        ttk.Button(hl_btns, text="Otomatik (oner)", command=self.suggest_selected_helper_family).pack(
            side="left", padx=2)

        ttk.Label(self.helper_lines_frame, text="Eski yontem - mevcut iki noktayla (AB yonunde baska bir kenar):",
                  foreground="#555", justify="left", wraplength=410).pack(anchor="w", padx=4, pady=(6, 0))
        hab_row = ttk.Frame(self.helper_lines_frame)
        hab_row.pack(fill="x", padx=4, pady=2)
        self.abc_helper_ab_combos = []
        for _ in range(2):
            cb = ttk.Combobox(hab_row, width=10, state="readonly")
            cb.pack(side="left", padx=4)
            cb.bind("<<ComboboxSelected>>", lambda e: self._on_legacy_helper_combo("ab"))
            self.abc_helper_ab_combos.append(cb)

        ttk.Label(self.helper_lines_frame, text="Eski yontem - mevcut iki noktayla (AC yonunde baska bir kenar):",
                  foreground="#555", justify="left", wraplength=410).pack(anchor="w", padx=4, pady=(6, 0))
        hac_row = ttk.Frame(self.helper_lines_frame)
        hac_row.pack(fill="x", padx=4, pady=2)
        self.abc_helper_ac_combos = []
        for _ in range(2):
            cb = ttk.Combobox(hac_row, width=10, state="readonly")
            cb.pack(side="left", padx=4)
            cb.bind("<<ComboboxSelected>>", lambda e: self._on_legacy_helper_combo("ac"))
            self.abc_helper_ac_combos.append(cb)

        # --- ortak: durum/kontrol ---
        ttk.Button(right, text="Referansi Olustur", command=self.compute_plane).pack(
            fill="x", padx=0, pady=(0, 4))

        self.plane_status_var = tk.StringVar(value="Duzlem henuz ayarlanmadi.")
        ttk.Label(right, textvariable=self.plane_status_var, foreground="#555",
                  wraplength=420, justify="left").pack(anchor="w", padx=4, pady=(0, 6))

        # Kayitli duzlemler - fotografta birden fazla farkli yuzey/alan
        # (ör. bina, pencere, calinin yanindaki bir duvar) olcerken, her
        # birini isimleyip kaydedip sonra tekrar yukleyebilmek icin.
        saved_frame = ttk.LabelFrame(right, text="Kayitli Duzlemler (Farkli Alanlar Icin)")
        saved_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(saved_frame,
                  text="Farkli bir alan (ör. calinin yanindaki duvar, pencere) icin ayri bir\n"
                       "referans kurdugunuzda, asagidan isimleyip kaydedin - sonra tekrar\n"
                       "yuklemek icin listeden secip 'Yukle'ye basin.",
                  foreground="#555", justify="left").pack(anchor="w", padx=4, pady=(4, 4))
        self.saved_planes_list = tk.Listbox(saved_frame, height=4)
        self.saved_planes_list.pack(fill="x", padx=4, pady=(0, 4))
        saved_btns = ttk.Frame(saved_frame)
        saved_btns.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Button(saved_btns, text="Bu Duzlemi Kaydet", command=self.save_named_plane).pack(side="left")
        ttk.Button(saved_btns, text="Yukle", command=self.load_named_plane).pack(side="left", padx=6)
        ttk.Button(saved_btns, text="Sil", command=self.delete_named_plane).pack(side="left")

        # Sorgular
        q_frame = ttk.LabelFrame(right, text="Olcum Sorgulari (Uzunlugunu Merak Ettikleriniz)")
        q_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(q_frame, text="Duz uzunluk icin A ve B yeterli. Kirikli/koseli bir\n"
                                 "uzunluk (ör. bir koseden donen duvar: A->B->C, iki\n"
                                 "parcanin TOPLAMI) icin C'yi de secin (opsiyonel).",
                  foreground="#555", justify="left").pack(anchor="w", padx=4, pady=(4, 2))

        row1 = ttk.Frame(q_frame)
        row1.pack(fill="x", padx=4, pady=4)
        ttk.Label(row1, text="A:").pack(side="left")
        self.combo_a = ttk.Combobox(row1, width=7, state="readonly")
        self.combo_a.pack(side="left", padx=4)
        ttk.Label(row1, text="B:").pack(side="left")
        self.combo_b = ttk.Combobox(row1, width=7, state="readonly")
        self.combo_b.pack(side="left", padx=4)
        ttk.Label(row1, text="C (opsiyonel):").pack(side="left")
        self.combo_c = ttk.Combobox(row1, width=7, state="readonly")
        self.combo_c.pack(side="left", padx=4)
        ttk.Button(row1, text="C'yi Temizle", command=lambda: self.combo_c.set("")).pack(side="left", padx=4)

        row2 = ttk.Frame(q_frame)
        row2.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Label(row2, text="Isim:").pack(side="left")
        self.query_name_entry = ttk.Entry(row2, width=14)
        self.query_name_entry.pack(side="left", padx=4)
        ttk.Label(row2, text="Gercek (opsiyonel):").pack(side="left")
        self.query_gt_entry = ttk.Entry(row2, width=8)
        self.query_gt_entry.pack(side="left", padx=4)

        row3 = ttk.Frame(q_frame)
        row3.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Button(row3, text="Ekle", command=self.add_query).pack(side="left")
        ttk.Button(row3, text="Secili Sorguyu Sil", command=self.delete_query).pack(side="left", padx=6)
        ttk.Button(row3, text="Secilinin Referansini Guncelle (Aktif Referansa)",
                   command=self.refresh_query_reference).pack(side="left", padx=6)

        self.query_list = tk.Listbox(q_frame, height=5)
        self.query_list.pack(fill="x", padx=4, pady=(0, 4))

        # Hesapla
        ttk.Button(right, text="HESAPLA", command=self.compute).pack(fill="x", pady=(0, 8), ipady=6)

        # Sonuclar
        res_frame = ttk.LabelFrame(right, text="Sonuclar")
        res_frame.pack(fill="both", expand=True)
        self.results_text = scrolledtext.ScrolledText(res_frame, wrap="word", height=10, state="disabled")
        self.results_text.pack(fill="both", expand=True, padx=4, pady=4)
        ttk.Button(res_frame, text="Sonucu Gorsel Olarak Kaydet (.jpg/.png)",
                   command=self.save_annotated).pack(fill="x", padx=4, pady=(0, 4))

    # ---------- Foto / canvas ----------

    def _apply_sharpen(self, img):
        out = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        out = ImageEnhance.Contrast(out).enhance(1.1)
        out = ImageEnhance.Sharpness(out).enhance(1.5)
        return out

    def _on_contrast_change(self, _value):
        self.contrast_label.config(text=f"{self.contrast_var.get():.2f}x")
        self._redraw()

    def _reset_contrast(self):
        self.contrast_var.set(1.0)
        self.contrast_label.config(text="1.00x")
        self._redraw()

    def _on_distortion_change(self, _value=None):
        self.distortion_label.config(text=f"{self.distortion_k_var.get():.2f}")
        self._redraw()

    def _reset_distortion_preview(self):
        self.distortion_k_var.set(0.0)
        self.distortion_label.config(text="0.00")
        self._redraw()

    def apply_distortion_correction(self):
        """Su an kaydiricida gorunen lens duzeltmesini KALICI hale getirir
        (yeni bir dosyaya kaydedip fotografi onunla degistirir). ONEMLI:
        bu, TUM piksel konumlarini degistirir - bu yuzden mevcut noktalar/
        sorgular/duzlemler artik gecersiz olur ve temizlenir. Sadece
        onizleme (canli kaydirici) piksel konumlarini degistirmez, o
        yuzden noktalari isaretlemeden ONCE bu duzeltmeyi yapip
        uygulamaniz onerilir."""
        k = self.distortion_k_var.get()
        if abs(k) < 1e-3:
            messagebox.showinfo("Bilgi", "Kaydirici 0'da - uygulanacak bir duzeltme yok.")
            return
        if self.pil_img_original is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        if self.points:
            if not messagebox.askyesno(
                    "Onay",
                    "Lens duzeltmesini kalici olarak uygulamak, TUM piksel konumlarini "
                    "degistirecegi icin mevcut noktalari/sorgulari/duzlemleri gecersiz "
                    "kilar ve temizler. Devam edilsin mi?"):
                return

        corrected = undistort_image(self.pil_img_original, k)

        if self.photo_path:
            base, ext = os.path.splitext(self.photo_path)
            if not ext or ext.lower() == ".pdf":
                ext = ".png"
            default_name = os.path.basename(base) + "_lens_duzeltilmis" + ext
            default_dir = os.path.dirname(self.photo_path)
        else:
            default_name, default_dir, ext = "lens_duzeltilmis.jpg", "", ".jpg"
        out_path = filedialog.asksaveasfilename(
            title="Duzeltilmis fotografi kaydet", initialfile=default_name,
            initialdir=default_dir or None, defaultextension=ext,
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if not out_path:
            return
        corrected.save(out_path)

        self.photo_path = out_path
        self.pil_img_original = corrected
        self.pil_img = self._apply_sharpen(corrected) if self.sharpened else corrected
        self._reset_state_for_new_photo()
        self.distortion_k_var.set(0.0)
        self.distortion_label.config(text="0.00")
        self._compute_display_scale()
        self._redraw()
        self._refresh_all_display()
        self.status_var.set(f"Lens duzeltmesi uygulandi ve kaydedildi: {os.path.basename(out_path)}. "
                             f"Noktalari yeniden isaretleyin.")

    # ---------- Duz kenardan otomatik lens distorsiyon tahmini ----------

    def toggle_line_calib_mode(self):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        self.line_calib_mode = not self.line_calib_mode
        if self.line_calib_mode and self.edge_mode:
            self.edge_mode = False
            self.edge_rough_points = []
            self.edge_mode_btn.config(text="Kenar Hizalama Modu: KAPALI")
        self.line_calib_btn.config(text=f"Duz Kenar Modu: {'ACIK' if self.line_calib_mode else 'KAPALI'}")
        self._redraw()
        if self.line_calib_mode:
            self.status_var.set("Duz Kenar Modu acik: gercekte duz olan bir kenar boyunca 3+ nokta tiklayin.")

    def undo_line_calib_point(self):
        if self.line_calib_current:
            self.line_calib_current.pop()
            self._redraw()

    def finish_line_calib_line(self):
        if len(self.line_calib_current) < 3:
            messagebox.showerror("Hata", "Bir kenar icin (Duz Kenar Modunda) en az 3 nokta tiklamalisiniz.")
            return
        self.line_calib_lines.append(self.line_calib_current)
        self.line_calib_current = []
        self._redraw()
        self.status_var.set(f"{len(self.line_calib_lines)} duz kenar kaydedildi. Istersen baska bir "
                             f"kenar daha ekleyip 'Otomatik k Tahmin Et'e basabilirsin.")

    def clear_line_calib(self):
        self.line_calib_current = []
        self.line_calib_lines = []
        self._redraw()

    def auto_estimate_distortion(self):
        """3+ noktali, gercekte duz kenar(lar)dan (bkz. estimate_distortion_k)
        otomatik bir lens distorsiyon katsayisi (k) tahmin eder ve kaydiriciyi
        buna ayarlar. Bu, kaydiriciyi 'gozle' ayarlamaktan cok daha kesin bir
        sonuc verir cunku dogrudan 'bu kenar gercekte duzdur' bilgisini
        sayisallastirir - ozellikle genis acili (ör. 0.5x) telefon
        lensleriyle cekilmis, kenarlari hafifce kavisli gorunen fotograflarda
        (bu kavis, referans bolgesinden uzak noktalarda beklenmedik olcum
        farklarinin en sik goz ardi edilen sebebidir)."""
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        lines = list(self.line_calib_lines)
        if len(self.line_calib_current) >= 3:
            lines.append(self.line_calib_current)
        if not lines:
            messagebox.showerror("Hata", "Once Duz Kenar Modunu acip, gercekte duz olan bir kenar "
                                          "boyunca en az 3 nokta tiklayin (ve istersen 'Bu Kenari Bitir'e basin).")
            return
        img_w, img_h = self.pil_img.size
        try:
            k = estimate_distortion_k(lines, img_w, img_h)
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return

        self.distortion_k_var.set(k)
        self.distortion_label.config(text=f"{k:.2f}")
        self.line_calib_mode = False
        self.line_calib_btn.config(text="Duz Kenar Modu: KAPALI")
        self._redraw()
        messagebox.showinfo(
            "Tahmin tamamlandi",
            f"Otomatik tahmin edilen lens duzeltme katsayisi: k = {k:.3f}\n\n"
            "Kaydirici bu degere ayarlandi ve onizleme guncellendi - isaretlediginiz "
            "kenarin (ve genel olarak diger duz kenarlarin) artik daha duz gorundugunu "
            "kontrol edin. Memnun kaldiysaniz 'Uygula (Kaydet)' ile KALICI hale getirin "
            "(bu, mevcut noktalari sifirlayacagi icin duzeltmeyi noktalari isaretlemeden "
            "ONCE yapmaniz onerilir).")

    def toggle_sharpen(self):
        if self.pil_img_original is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        self.sharpened = not self.sharpened
        self.pil_img = self._apply_sharpen(self.pil_img_original) if self.sharpened else self.pil_img_original
        self._redraw()
        self.status_var.set("Netlestirme: Acik" if self.sharpened else "Netlestirme: Kapali")

    def _load_photo(self, path, pdf_page=None):
        """Fotografi (veya PDF sayfasini) yukler; bulanik/net olmayan
        bolgeler icin kullaniciya netlestirme (keskinlik+kontrast artirma)
        uygulanip uygulanmayacagini sorar. Basarili olursa True doner.

        PDF icin: pdf_page (0 tabanli) verilmezse ve birden fazla sayfa
        varsa kullaniciya hangi sayfanin acilacagi sorulur."""
        if path.lower().endswith(".pdf"):
            return self._load_pdf(path, pdf_page)
        try:
            raw = Image.open(path)
            try:
                # EXIF, .convert("RGB") SONRASI kaybolabilir (yeni bir Image
                # nesnesi olusur) - bu yuzden ham acilista, donusumden ONCE
                # okunuyor. Route A (kamera pozu) icin kullanilir - bkz.
                # estimate_camera_intrinsics_from_exif. Yoksa/okunamazsa
                # None - Route A sessizce devre disi kalir.
                exif = raw.getexif()
            except Exception:
                exif = None
            img = raw.convert("RGB")
        except Exception as e:
            messagebox.showerror("Hata", f"Fotograf acilamadi:\n{e}")
            return False

        self.photo_path = path
        self.pdf_page = None
        self.photo_exif = exif
        self.pil_img_original = img
        # Soru sorulmaz; gerekirse "Netlestir" dugmesiyle acilir.
        self.pil_img = img
        self.sharpened = False
        self._compute_display_scale()
        return True

    def _load_pdf(self, path, pdf_page=None):
        """PDF'in bir sayfasini goruntu olarak yukler. Cizim/plan PDF'leri
        zaten net oldugu icin netlestirme sorulmaz (menuden acilabilir).
        PDF'te EXIF yoktur; Route A (kamera pozu) devre disi kalir - duz bir
        cizimde zaten perspektif yoktur, referans uzunluklarla olcek
        dogrudan kurulur."""
        try:
            n_pages = pdf_page_count(path)
            if n_pages < 1:
                raise RuntimeError("PDF'te sayfa yok.")
            if pdf_page is None:
                if n_pages == 1:
                    pdf_page = 0
                else:
                    num = simpledialog.askinteger(
                        "PDF sayfasi",
                        f"Bu PDF {n_pages} sayfa iceriyor.\nHangi sayfa acilsin? (1-{n_pages})",
                        parent=self,
                        minvalue=1, maxvalue=n_pages, initialvalue=1)
                    if num is None:
                        return False
                    pdf_page = num - 1
            if not (0 <= pdf_page < n_pages):
                raise RuntimeError(f"Sayfa {pdf_page + 1} yok (PDF {n_pages} sayfa).")
            img = render_pdf_page(path, pdf_page)
        except Exception as e:
            messagebox.showerror("Hata", f"PDF acilamadi:\n{e}")
            return False

        self.photo_path = path
        self.pdf_page = pdf_page
        self.photo_exif = None
        self.pil_img_original = img
        self.pil_img = img
        self.sharpened = False
        self._compute_display_scale()
        return True

    def _reset_state_for_new_photo(self):
        """Yeni bir fotograf yuklenirken TUM eski veriyi ve widget
        icerigini temizler. Onemli: Combobox'lar values listesi degisse
        bile ESKI SECILI METNI ekranda tutar - temizlenmezse, yeni
        fotografta noktalar yine A/B/C/D... diye adlandirildigi icin eski
        Kose secimleri yeni (ama farkli konumdaki) ayni-isimli noktalarla
        sessizce eslesip YANLIS bir duzlem kurabilir."""
        self.points = []
        self.queries = []
        self.plane_corners = None
        self.plane_H = None
        self.plane_Hinv = None
        self.plane_width_m = None
        self.plane_height_m = None
        self.plane_calibrated = False
        self.plane_origin = None
        self.plane_axis1 = None
        self.plane_axis2 = None
        self.plane_model_type = None
        self.plane_vp_confidence = "N/A"
        self.plane_vanishing_points = {"ab": None, "ac": None}
        self.plane_d_route = None
        self.plane_camera_status = "BILINMIYOR"
        self.plane_strat_result = None
        self.plane_line_residuals = {"ab": None, "ac": None}
        self.plane_point_reproj = None
        self.plane_condition_number = None
        self.plane_quality = "N/A"
        self.plane_img_pts = None
        self.plane_world_pts = None
        self.plane_point_sources = None
        self.last_results = {}
        self.edge_mode = False
        self.edge_rough_points = []
        self.line_calib_mode = False
        self.line_calib_current = []
        self.line_calib_lines = []
        self.saved_planes = []
        self._ref_counter = 0
        self._last_ref_corners = None
        self._last_ref_label = None
        self._last_confirmed_ref_signature = None
        self.helper_lines = []
        self._helper_counter = 0
        self.helper_capture = None
        self.helper_status = {}
        self._selected_helper_id = None
        self._vp_stage_cache = (None, None)
        if hasattr(self, "helper_tree"):
            self._refresh_helper_tree()
        if hasattr(self, "saved_planes_list"):
            self._refresh_saved_planes_list()
        if hasattr(self, "edge_mode_btn"):
            self.edge_mode_btn.config(text="Kenar Hizalama Modu: KAPALI")
        if hasattr(self, "line_calib_btn"):
            self.line_calib_btn.config(text="Duz Kenar Modu: KAPALI")
        if hasattr(self, "distortion_k_var"):
            self.distortion_k_var.set(0.0)
            self.distortion_label.config(text="0.00")

        for cb in self.corner_combos:
            cb.set("")
            cb["values"] = []
        for cb in self.tri_combos:
            cb.set("")
            cb["values"] = []
        for e in self.tri_len_entries:
            e.delete(0, "end")
        self.coords_rows = []
        self.coords_point_combo.set("")
        self.coords_point_combo["values"] = []
        self.coords_x_entry.delete(0, "end")
        self.coords_y_entry.delete(0, "end")
        self._refresh_coords_tree()
        for cb in self.abc_combos:
            cb.set("")
            cb["values"] = []
        for e in self.abc_len_entries:
            e.delete(0, "end")
        self.abc_right_angle_var.set(True)
        self.abc_angle_entry.delete(0, "end")
        for cb in self.abc_helper_ab_combos:
            cb.set("")
            cb["values"] = []
        for cb in self.abc_helper_ac_combos:
            cb.set("")
            cb["values"] = []
        self.combo_a.set("")
        self.combo_b.set("")
        self.combo_c.set("")
        self.combo_a["values"] = []
        self.combo_b["values"] = []
        self.combo_c["values"] = []
        self.plane_width_entry.delete(0, "end")
        self.plane_height_entry.delete(0, "end")
        self.query_name_entry.delete(0, "end")
        self.query_gt_entry.delete(0, "end")
        self._reset_contrast()

        self.plane_status_var.set("Duzlem henuz ayarlanmadi.")

    def open_photo(self):
        path = filedialog.askopenfilename(
            title="Fotograf veya PDF sec",
            filetypes=IMAGE_FILETYPES,
        )
        if not path:
            return
        if not self._load_photo(path):
            return
        self._reset_state_for_new_photo()
        self._redraw()
        self._refresh_all_display()
        name = os.path.basename(path)
        if self.pdf_page is not None:
            name += f" (sayfa {self.pdf_page + 1})"
        self.status_var.set(f"{name} yuklendi.")
        self.wizard_start()

    def _canvas_size(self):
        """Canvas'in GERCEK (o anki pencere boyutuna gore) genislik/
        yuksekligini doner. ONEMLI: eskiden burada her yerde sabit
        MAX_CANVAS_W/H kullaniliyordu, ama canvas'i saran cerceve
        pencereyle birlikte buyuyecek sekilde ayarlandigi icin (kaydirma
        cubuklari eklenirken), gercekte gosterilen alan ile hesaplamalarda
        kullanilan sabit boyut UYUSMUYORDU - bu da bazi bolgelere
        (ozellikle alt kisimlara) hicbir sekilde kaydirarak ulasilamamasina
        yol aciyordu. Artik her yerde bu fonksiyon kullaniliyor."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return MAX_CANVAS_W, MAX_CANVAS_H
        return w, h

    def _compute_display_scale(self):
        w, h = self.pil_img.size
        cw, ch = self._canvas_size()
        scale = min(cw / w, ch / h)
        if scale > 2.0:
            scale = 2.0
        self.fit_scale = scale
        self.reset_view()

    def reset_view(self):
        if self.pil_img is None:
            return
        self.view_scale = self.fit_scale
        self.view_x = 0.0
        self.view_y = 0.0
        self._redraw()

    def _on_canvas_resize(self, event=None):
        """Pencere/canvas boyutu degistiginde (ör. pencereyi buyutunce)
        gorunumu YENIDEN CIZER - eskiden canvas buyuse bile render sabit
        1000x700 kaliyordu, bu da 'alta ulasamiyorum' sorununun ana
        sebebiydi. Kullanicinin mevcut yakinlastirma/kaydirma durumunu
        BOZMADAN (sadece yeni boyuta gore kenetleyerek) gunceller."""
        if self.pil_img is None:
            return
        img_w, img_h = self.pil_img.size
        cw, ch = self._canvas_size()
        new_fit = min(cw / img_w, ch / img_h)
        if new_fit > 2.0:
            new_fit = 2.0
        self.fit_scale = new_fit
        if self.view_scale < new_fit:
            self.view_scale = new_fit
        self._clamp_view()
        self._redraw()

    def _clamp_view(self):
        img_w, img_h = self.pil_img.size
        cw, ch = self._canvas_size()
        view_w = cw / self.view_scale
        view_h = ch / self.view_scale
        if view_w >= img_w:
            self.view_x = (img_w - view_w) / 2
        else:
            margin = view_w * 0.3
            self.view_x = max(-margin, min(self.view_x, img_w - view_w + margin))
        if view_h >= img_h:
            self.view_y = (img_h - view_h) / 2
        else:
            margin = view_h * 0.3
            self.view_y = max(-margin, min(self.view_y, img_h - view_h + margin))

    def _on_hscroll(self, *args):
        if self.pil_img is None:
            return
        img_w, _ = self.pil_img.size
        cw, _ = self._canvas_size()
        view_w = cw / self.view_scale
        if args[0] == "moveto":
            self.view_x = float(args[1]) * img_w
        elif args[0] == "scroll":
            amount = int(args[1])
            step = view_w * (0.9 if args[2] == "pages" else 0.1)
            self.view_x += amount * step
        self._clamp_view()
        self._redraw()

    def _on_vscroll(self, *args):
        if self.pil_img is None:
            return
        _, img_h = self.pil_img.size
        _, ch = self._canvas_size()
        view_h = ch / self.view_scale
        if args[0] == "moveto":
            self.view_y = float(args[1]) * img_h
        elif args[0] == "scroll":
            amount = int(args[1])
            step = view_h * (0.9 if args[2] == "pages" else 0.1)
            self.view_y += amount * step
        self._clamp_view()
        self._redraw()

    def _sync_scrollbars(self):
        img_w, img_h = self.pil_img.size
        cw, ch = self._canvas_size()
        view_w = cw / self.view_scale
        view_h = ch / self.view_scale
        self.hscroll.set(max(0.0, self.view_x / img_w), min(1.0, (self.view_x + view_w) / img_w))
        self.vscroll.set(max(0.0, self.view_y / img_h), min(1.0, (self.view_y + view_h) / img_h))

    def on_mousewheel(self, event):
        if self.pil_img is None:
            return
        old_scale = self.view_scale
        factor = 1.15 if event.delta > 0 else 1 / 1.15
        new_scale = max(self.fit_scale, min(self.fit_scale * 20, old_scale * factor))
        orig_x = self.view_x + event.x / old_scale
        orig_y = self.view_y + event.y / old_scale
        self.view_scale = new_scale
        self.view_x = orig_x - event.x / new_scale
        self.view_y = orig_y - event.y / new_scale
        self._clamp_view()
        self._redraw()

    def on_pan_start(self, event):
        if self.pil_img is None:
            return
        self._pan_start = (event.x, event.y, self.view_x, self.view_y)
        self._pan_press_xy = (event.x, event.y)

    def on_pan_move(self, event):
        if self.pil_img is None or self._pan_start is None:
            return
        sx, sy, ox, oy = self._pan_start
        self.view_x = ox - (event.x - sx) / self.view_scale
        self.view_y = oy - (event.y - sy) / self.view_scale
        self._clamp_view()
        self._redraw()

    def on_pan_release(self, event):
        """Sag tik SURUKLENMEDEN birakilirsa ve yardimci cizgi yakalaniyorsa
        yakalamayi iptal eder (sag tik + surukle hala kaydirma yapar)."""
        press = self._pan_press_xy
        self._pan_press_xy = None
        if self.helper_capture is not None and press is not None and                 math.hypot(event.x - press[0], event.y - press[1]) < 4:
            self.cancel_helper_capture()

    def _on_canvas_motion(self, event):
        """Yardimci cizginin ilk ucu secildiyse, fareye kadar uzanan gecici
        bir onizleme cizgisi (tuval ogesi - tam yeniden cizim yapmadan)."""
        self.canvas.delete("helper_rubber")
        cap = self.helper_capture
        if cap is None or len(cap["points"]) != 1:
            return
        x0 = (cap["points"][0][0] - self.view_x) * self.view_scale
        y0 = (cap["points"][0][1] - self.view_y) * self.view_scale
        color = "#%02x%02x%02x" % HELPER_COLORS.get(cap["family"], HELPER_COLORS["auto"])
        self.canvas.create_line(x0, y0, event.x, event.y, fill=color, width=2, dash=(6, 4),
                                tags="helper_rubber")

    def _canvas_to_image(self, cx, cy):
        return self.view_x + cx / self.view_scale, self.view_y + cy / self.view_scale

    def _redraw(self):
        if self.pil_img is None:
            return
        img_w, img_h = self.pil_img.size
        vs = self.view_scale
        vx, vy = self.view_x, self.view_y
        cw, ch = self._canvas_size()
        view_w = cw / vs
        view_h = ch / vs

        canvas_img = Image.new("RGB", (cw, ch), (34, 34, 34))
        left, top = max(vx, 0), max(vy, 0)
        right, bottom = min(vx + view_w, img_w), min(vy + view_h, img_h)
        if right > left and bottom > top:
            crop = self.pil_img.crop((int(left), int(top), int(math.ceil(right)), int(math.ceil(bottom))))
            k = self.distortion_k_var.get()
            if abs(k) > 1e-3:
                crop = undistort_crop(crop, k, img_w, img_h, int(left), int(top))
            contrast = self.contrast_var.get()
            if abs(contrast - 1.0) > 1e-3:
                crop = ImageEnhance.Contrast(crop).enhance(contrast)
            disp_w = max(1, int(round((right - left) * vs)))
            disp_h = max(1, int(round((bottom - top) * vs)))
            crop = crop.resize((disp_w, disp_h), Image.LANCZOS)
            paste_x = int(round((left - vx) * vs))
            paste_y = int(round((top - vy) * vs))
            canvas_img.paste(crop, (paste_x, paste_y))

        draw = ImageDraw.Draw(canvas_img)
        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}

        def sc(pt):
            return (pt[0] - vx) * vs, (pt[1] - vy) * vs

        # Referans noktasi secimi ONIZLEMESI (izgaradan once, secim
        # yapilirken canli gorunmesi icin) + tam izgara (secim tamamlanir
        # tamamlanmaz otomatik).
        active_combos = self.tri_combos if self.ref_mode_var.get() == "affine3" else self.corner_combos
        expected_n = 3 if self.ref_mode_var.get() == "affine3" else 4
        current_labels = [cb.get() for cb in active_combos]
        preview_pts = [lookup[lb] for lb in current_labels if lb and lb in lookup]
        if len(preview_pts) >= 2:
            poly = [sc(p) for p in preview_pts]
            if len(preview_pts) == expected_n:
                poly.append(sc(preview_pts[0]))
            draw.line(poly, fill=(0, 230, 230), width=2)

        if self.plane_H is not None and self.plane_Hinv is not None:
            # Renk: tam guven (sari, GRID_COLOR) SADECE olcek kalibre VE
            # model TAM PROJEKTIF ise. Model afin_local (perspektif
            # cozulemedi) ise, kalibre olsa bile mevcut "on izleme" turuncu
            # rengini (PREVIEW_GRID_COLOR) kullaniyoruz - boylece kullanici,
            # izgaranin SADECE referans yakininda guvenilir oldugunu renkten
            # de anlar (yeni renk eklemedik, mevcut anlamli renk yeniden
            # kullanildi).
            is_full_confidence = self.plane_calibrated and getattr(self, "plane_model_type", None) == "projective"
            grid_color = GRID_COLOR if is_full_confidence else PREVIEW_GRID_COLOR
            if self.show_grid_var.get():
                self._draw_grid(draw, sc, color=grid_color)
            if self.plane_corners:
                pts = [lookup[c] for c in self.plane_corners if c in lookup]
                if len(pts) == len(self.plane_corners):
                    poly = [sc(p) for p in pts] + [sc(pts[0])]
                    draw.line(poly, fill=PLANE_COLOR, width=3)

        if self.last_results:
            for q in self.queries:
                if q["name"] not in self.last_results:
                    continue
                if q["a"] not in lookup or q["b"] not in lookup:
                    continue
                path_pts = [lookup[q["a"]], lookup[q["b"]]]
                if q.get("c") and q["c"] in lookup:
                    path_pts.append(lookup[q["c"]])
                path_sc = [sc(p) for p in path_pts]
                draw.line(path_sc, fill=QUERY_COLOR, width=3)
                mid_idx = len(path_sc) // 2
                mp1, mp2 = path_sc[mid_idx - 1], path_sc[mid_idx]
                mid = ((mp1[0] + mp2[0]) / 2, (mp1[1] + mp2[1]) / 2)
                draw.text(mid, f"{q['name']}: {self._fmt(self.last_results[q['name']])}", fill=QUERY_COLOR,
                          font=self.font_small, stroke_width=2, stroke_fill=(0, 0, 0))

        for p in self.points:
            x, y = sc((p["x"], p["y"]))
            is_corner = self.plane_corners is not None and p["label"] in self.plane_corners
            color = PLANE_COLOR if is_corner else POINT_COLOR
            r = 5
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=2)
            draw.text((x + 8, y - 10), p["label"], fill=color, font=self.font_label,
                      stroke_width=2, stroke_fill=(0, 0, 0))

        self._draw_helper_lines(draw, sc)

        if self.edge_rough_points:
            pts_sc = [sc(p) for p in self.edge_rough_points]
            if len(pts_sc) >= 2:
                draw.line(pts_sc, fill=EDGE_ROUGH_COLOR, width=1)
            for x, y in pts_sc:
                r = 4
                draw.ellipse([x - r, y - r, x + r, y + r], outline=EDGE_ROUGH_COLOR, width=2)

        for line_pts in self.line_calib_lines:
            pts_sc = [sc(p) for p in line_pts]
            if len(pts_sc) >= 2:
                draw.line(pts_sc, fill=LINE_CALIB_COLOR, width=1)
            for x, y in pts_sc:
                r = 4
                draw.ellipse([x - r, y - r, x + r, y + r], outline=LINE_CALIB_COLOR, width=2)
        if self.line_calib_current:
            pts_sc = [sc(p) for p in self.line_calib_current]
            if len(pts_sc) >= 2:
                draw.line(pts_sc, fill=LINE_CALIB_ACTIVE_COLOR, width=1)
            for x, y in pts_sc:
                r = 4
                draw.ellipse([x - r, y - r, x + r, y + r], outline=LINE_CALIB_ACTIVE_COLOR, width=2)

        self.tk_img = ImageTk.PhotoImage(canvas_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self._sync_scrollbars()

    def _draw_grid(self, draw, sc, color=GRID_COLOR):
        """Egim duzeltmesini gorsellestiren izgara - TUM FOTOGRAFI
        kaplayacak sekilde duzlemin perspektifine gore uzatilir.

        ONEMLI: izgaranin iki dogrultusu, referans kenarlarin KENDISINI
        (1->2 ve 2->3) takip eder - bunlar 4-kose modunda zaten birbirine
        dik (dikdortgen varsayimi) ama 3-nokta (afin/SSS) modunda GENELDE
        DIK DEGILDIR. Izgarayi rastgele bir dik (ortonormal) eksen
        takimiyla degil, bu GERCEK iki kenar dogrultusuyla (gerekirse
        egik/paralelkenar seklinde) cizmek, izgaranin isaretlenen
        referans kenarlarla gorsel olarak tutarli olmasini saglar."""
        wm, hm = self.plane_width_m, self.plane_height_m
        img_w, img_h = self.pil_img.size

        len1 = float(np.linalg.norm(self.plane_axis1))
        len2 = float(np.linalg.norm(self.plane_axis2))
        if len1 < 1e-9 or len2 < 1e-9:
            return
        e1 = self.plane_axis1 / len1   # 1->2 kenari yonunde birim vektor
        e2 = self.plane_axis2 / len2   # 2->3 kenari yonunde birim vektor
        basis = np.column_stack([e1, e2])
        try:
            basis_inv = np.linalg.inv(basis)
        except np.linalg.LinAlgError:
            return  # e1//e2 (referans noktalari dogrusal) - izgara kurulamaz

        def to_world(image_pt):
            try:
                return apply_transform(self.plane_H, image_pt)
            except ValueError:
                return None

        def to_ab(world_pt):
            vec = np.array(world_pt, dtype=np.float64) - self.plane_origin
            ab = basis_inv @ vec
            return float(ab[0]), float(ab[1])

        def ab_to_img(a, b):
            world_pt = self.plane_origin + a * e1 + b * e2
            try:
                return apply_transform(self.plane_Hinv, tuple(world_pt))
            except ValueError:
                return None

        # Fotografin 4 kosesini (a,b) tabanina yansitip, izgarayi TAM
        # OLARAK bu sinirlara kadar genislet - boylece izgara HER ZAMAN
        # fotografin tamamini kapliyor; cizgi sayisi asagidaki max_lines
        # mekanizmasiyla (adim buyuklugunu gerektikce ikiye katlayarak)
        # makul tutuluyor.
        corners_world = [to_world(c) for c in [(0, 0), (img_w, 0), (img_w, img_h), (0, img_h)]]
        corners_ab = [to_ab(c) for c in corners_world if c is not None]
        if corners_ab:
            avals = [c[0] for c in corners_ab]
            bvals = [c[1] for c in corners_ab]
            pad_a = (max(avals) - min(avals)) * 0.05 or wm * 0.05
            pad_b = (max(bvals) - min(bvals)) * 0.05 or hm * 0.05
            amin, amax = min(avals) - pad_a, max(avals) + pad_a
            bmin, bmax = min(bvals) - pad_b, max(bvals) + pad_b
        else:
            amin, amax, bmin, bmax = 0.0, wm, 0.0, hm

        # ONEMLI DUZELTME: model "affine_local" ise (yeterli kacis noktasi
        # kaniti YOK, D=B+C-A yaklasimi kullanildi), izgarayi TUM FOTOGRAFA
        # yaymak GEOMETRIK OLARAK YANILTICI - afin donusum perspektif
        # yakinsamasini modellemedigi icin, referanstan uzaklastikca
        # GERCEK mimari cizgilerin yonu artik afin izgarayla ORTUSMEZ.
        # Bu yuzden afin modda izgarayi, referansin KENDI (a,b) alaninin
        # (0..len1, 0..len2 - cunku e1/e2 zaten referans kenarlarinin
        # birim vektorleri) etrafinda, "guclu ekstrapolasyon" esigiyle
        # (extrapolation_ratio()'da kullanilan ayni 1.5x sabiti - bkz. o
        # fonksiyon, INTERNAL TUTARLILIK icin ayni deger kullanildi)
        # SINIRLI bir yerel bolgeye kesiyoruz.
        if getattr(self, "plane_model_type", None) == "affine_local":
            local_span = max(len1, len2)
            pad_local = local_span * 1.5
            safe_amin, safe_amax = -pad_local, len1 + pad_local
            safe_bmin, safe_bmax = -pad_local, len2 + pad_local
            amin, amax = max(amin, safe_amin), min(amax, safe_amax)
            bmin, bmax = max(bmin, safe_bmin), min(bmax, safe_bmax)
            if amin >= amax or bmin >= bmax:
                return  # referans dejenere/cok kucuk - izgara cizilemez

        for candidate in (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 50):
            if wm / candidate <= 20:
                step = candidate
                break
        else:
            step = max(wm, hm) / 10

        # Cok fazla cizgi olusursa (asiri perspektif ucusu ya da izgaranin
        # simdi fotografin tamamini kaplamasi yuzunden) adimlari buyuterek
        # makul bir sayida tut.
        max_lines = 150
        while step <= 0 or (amax - amin) / step > max_lines or (bmax - bmin) / step > max_lines:
            step = step * 2 if step > 0 else max(amax - amin, bmax - bmin) / max_lines

        # Sabit-a cizgileri (2->3 kenarina PARALEL), b boyunca tam genislikte
        ga = math.floor(amin / step) * step
        while ga <= amax:
            p1, p2 = ab_to_img(ga, bmin), ab_to_img(ga, bmax)
            if p1 and p2:
                draw.line([sc(p1), sc(p2)], fill=color, width=1)
            ga += step

        # Sabit-b cizgileri (1->2 kenarina PARALEL), a boyunca tam genislikte
        gb = math.floor(bmin / step) * step
        while gb <= bmax:
            p1, p2 = ab_to_img(amin, gb), ab_to_img(amax, gb)
            if p1 and p2:
                draw.line([sc(p1), sc(p2)], fill=color, width=1)
            gb += step

    def on_canvas_click(self, event):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        if abs(self.distortion_k_var.get()) > 1e-3:
            # ONEMLI GUVENLIK KONTROLU: ekranda gordugunuz Lens Duzeltmesi
            # ONIZLEMESI, goruntuyu piksel piksel EGRISTIRIYOR (cv2.undistort),
            # ama tiklamayi gercek goruntu pikseline ceviren _canvas_to_image
            # bu egriltmeyi hesaba KATMIYOR - yani tikladiginiz yer ile
            # kaydedilen nokta farkli olabilirdi (konuma bagli, ongorulemez
            # bir hata). Bunu onlemek icin, duzeltme henuz KALICI hale
            # getirilmeden (Uygula/Sifirla ile) nokta eklemeyi engelliyoruz.
            messagebox.showerror(
                "Hata",
                "Lens Duzeltmesi kaydiricisi hala 0'dan farkli (sadece onizlemedesiniz).\n\n"
                "Onizleme aktifken nokta eklerseniz, gordugunuz yer ile kaydedilen "
                "nokta konumu FARKLI olabilir ve olcumler yanlis cikar.\n\n"
                "Lutfen once 'Uygula (Kaydet)' ile duzeltmeyi kalici hale getirin, "
                "ya da duzeltme istemiyorsaniz kaydiriciyi 'Sifirla' ile 0'a getirin.")
            return
        orig_x, orig_y = self._canvas_to_image(event.x, event.y)

        if self.helper_capture is not None:
            if self.magnifier_var.get():
                self._open_point_magnifier(orig_x, orig_y, on_confirm=self._helper_capture_add_endpoint)
            else:
                self._helper_capture_add_endpoint(orig_x, orig_y, "manual")
            return

        if self.easy_mode and not self.edge_mode and not self.line_calib_mode:
            self._wizard_click(orig_x, orig_y)
            return

        if self.edge_mode:
            self.edge_rough_points.append((orig_x, orig_y))
            self._redraw()
            self.status_var.set(f"Kenar icin {len(self.edge_rough_points)} kaba nokta secildi "
                                 f"('Hizala ve 2 Nokta Ekle' ile bitirin).")
            return

        if self.line_calib_mode:
            self.line_calib_current.append((orig_x, orig_y))
            self._redraw()
            self.status_var.set(f"Bu duz kenar icin {len(self.line_calib_current)} nokta secildi "
                                 f"('Bu Kenari Bitir' ile kaydedin, sonra 'Otomatik k Tahmin Et'e basin).")
            return

        if self.magnifier_var.get():
            self._open_point_magnifier(orig_x, orig_y)
        else:
            self._finish_adding_point(orig_x, orig_y)

    def _finish_adding_point(self, x, y, source="manual"):
        existing = {p["label"] for p in self.points}
        suggestion = chr(ord('A') + len(self.points)) if len(self.points) < 26 else f"P{len(self.points) + 1}"
        while suggestion in existing:
            suggestion = suggestion + "'"

        label = simpledialog.askstring("Nokta Etiketi", "Bu nokta icin bir etiket girin:",
                                        initialvalue=suggestion, parent=self)
        if not label:
            return
        if label in existing:
            messagebox.showerror("Hata", f"'{label}' etiketi zaten kullaniliyor.")
            return

        # source: bu noktanin NASIL yerlestirildigini kaydeder (manuel tiklama/
        # buyutecli/subpixel kenar) - Monte Carlo olcum belirsizligi (bkz.
        # point_sigma_px) bunu kullanarak her noktaya farkli guven agirligi verir.
        self.points.append({"label": label, "x": x, "y": y, "source": source})
        self._redraw()
        self._refresh_all_display()
        self.status_var.set(f"'{label}' eklendi. Toplam {len(self.points)} nokta.")
        if self.helper_prompt_var.get():
            self.after_idle(lambda: self._offer_helper_after_point(label))

    # ---------- Buyutecli hassas nokta yerlestirme ----------
    # SimpleMeasure gibi profesyonel olcum yazilimlarinda goruldugu uzere:
    # tiklanan yer buyutulup gosterilir, yon oklariyla piksel piksel (veya
    # daha ince) ayarlanip Onayla ile kesinlestirilir. Bu, otomatik kenar
    # yakalamanin (Kenar Hizalama) uygun olmadigi durumlarda (ör. iki
    # kenarin kesistigi bir kose noktasi) elle maksimum hassasiyet saglar.

    MAGNIFIER_SIZE = 320
    MAGNIFIER_ZOOM = 8
    MAGNIFIER_NUDGE = 1.0

    def _open_point_magnifier(self, init_x, init_y, on_confirm=None):
        self._mag_point = [init_x, init_y]
        self._mag_on_confirm = on_confirm
        win = tk.Toplevel(self)
        win.title("Nokta Konumunu Ayarla")
        win.transient(self)
        win.resizable(False, False)
        self._mag_win = win

        canvas = tk.Canvas(win, width=self.MAGNIFIER_SIZE, height=self.MAGNIFIER_SIZE, bg="black",
                            highlightthickness=1, highlightbackground="#888")
        canvas.pack(padx=8, pady=(8, 4))
        self._mag_canvas = canvas

        self._mag_coord_var = tk.StringVar()
        ttk.Label(win, textvariable=self._mag_coord_var, foreground="#555").pack(pady=(0, 4))

        pad = ttk.Frame(win)
        pad.pack(pady=(0, 8))
        ttk.Button(pad, text="↑", width=3, command=lambda: self._nudge_mag(0, -1)).grid(row=0, column=1)
        ttk.Button(pad, text="←", width=3, command=lambda: self._nudge_mag(-1, 0)).grid(row=1, column=0)
        ttk.Button(pad, text="→", width=3, command=lambda: self._nudge_mag(1, 0)).grid(row=1, column=2)
        ttk.Button(pad, text="↓", width=3, command=lambda: self._nudge_mag(0, 1)).grid(row=2, column=1)

        btns = ttk.Frame(win)
        btns.pack(pady=(0, 8))
        ttk.Button(btns, text="Onayla (Enter)", command=self._confirm_mag).pack(side="left", padx=4)
        ttk.Button(btns, text="Iptal (Esc)", command=self._cancel_mag).pack(side="left", padx=4)

        win.bind("<Up>", lambda e: self._nudge_mag(0, -1))
        win.bind("<Down>", lambda e: self._nudge_mag(0, 1))
        win.bind("<Left>", lambda e: self._nudge_mag(-1, 0))
        win.bind("<Right>", lambda e: self._nudge_mag(1, 0))
        win.bind("<Return>", lambda e: self._confirm_mag())
        win.bind("<Escape>", lambda e: self._cancel_mag())
        win.protocol("WM_DELETE_WINDOW", self._cancel_mag)

        self._redraw_magnifier()
        win.grab_set()
        win.focus_set()

    def _nudge_mag(self, dx, dy):
        self._mag_point[0] += dx * self.MAGNIFIER_NUDGE
        self._mag_point[1] += dy * self.MAGNIFIER_NUDGE
        self._redraw_magnifier()

    def _redraw_magnifier(self):
        x, y = self._mag_point
        img_w, img_h = self.pil_img.size
        size, zoom = self.MAGNIFIER_SIZE, self.MAGNIFIER_ZOOM
        half = (size / zoom) / 2.0
        left, top, right, bottom = x - half, y - half, x + half, y + half

        canvas_img = Image.new("RGB", (size, size), (20, 20, 20))
        clip_left, clip_top = max(left, 0), max(top, 0)
        clip_right, clip_bottom = min(right, img_w), min(bottom, img_h)
        if clip_right > clip_left and clip_bottom > clip_top:
            crop = self.pil_img.crop((int(clip_left), int(clip_top),
                                       int(math.ceil(clip_right)), int(math.ceil(clip_bottom))))
            disp_w = max(1, int(round((clip_right - clip_left) * zoom)))
            disp_h = max(1, int(round((clip_bottom - clip_top) * zoom)))
            crop = crop.resize((disp_w, disp_h), Image.LANCZOS)
            paste_x = int(round((clip_left - left) * zoom))
            paste_y = int(round((clip_top - top) * zoom))
            canvas_img.paste(crop, (paste_x, paste_y))

        draw = ImageDraw.Draw(canvas_img)
        cx, cy = size // 2, size // 2
        draw.line([(cx - 24, cy), (cx + 24, cy)], fill=(255, 60, 60), width=1)
        draw.line([(cx, cy - 24), (cx, cy + 24)], fill=(255, 60, 60), width=1)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=(255, 230, 0), width=2)

        self._mag_tk_img = ImageTk.PhotoImage(canvas_img)
        self._mag_canvas.delete("all")
        self._mag_canvas.create_image(0, 0, anchor="nw", image=self._mag_tk_img)
        self._mag_coord_var.set(f"X: {x:.1f}   Y: {y:.1f}   (yon tuslariyla ince ayar yapin)")

    def _confirm_mag(self):
        x, y = self._mag_point
        self._mag_win.destroy()
        callback = getattr(self, "_mag_on_confirm", None) or self._finish_adding_point
        self._mag_on_confirm = None
        callback(x, y, "manual_magnifier")

    def _cancel_mag(self):
        self._mag_win.destroy()

    def undo_last_point(self):
        if not self.points:
            return
        removed = self.points.pop()
        self._remove_references_to(removed["label"])
        self._redraw()
        self._refresh_all_display()

    def _remove_references_to(self, label):
        self.queries = [q for q in self.queries if label not in (q["a"], q["b"], q.get("c"))]
        # Yardimci cizgiler: silinen noktaya bagli bir iliski SESSIZCE
        # korunmaz. Fiziksel uc noktalar (kenarin goruntudeki konumu) aynen
        # kalir, ama etiket bagi koparilir - ayni etiket sonradan baska bir
        # noktaya verilirse cizgi o noktayi TAKIP ETMEZ.
        detached = []
        for hl in self.helper_lines:
            if hl.get("anchor_label") == label:
                hl["anchor_label"] = None
                hl["note"] = f"capa noktasi '{label}' silindi; kenar konumu korundu"
                detached.append(hl["id"])
            if hl.get("point_labels") and label in hl["point_labels"]:
                hl["point_labels"] = None
                hl["source"] = "manual"
                hl["note"] = f"'{label}' noktasi silindi; kenar konumu korundu, nokta bagi koparildi"
                detached.append(hl["id"])
        for combos in (self.abc_helper_ab_combos, self.abc_helper_ac_combos):
            if any(cb.get() == label for cb in combos):
                for cb in combos:
                    cb.set("")
        if detached:
            self._vp_stage_cache = (None, None)
            self._refresh_helper_tree()
            self.status_var.set(f"'{label}' silindi - bagli yardimci cizgi(ler) ({', '.join(sorted(set(detached)))}) "
                                 f"noktadan ayrildi, kenar konumu korundu.")
        if self.plane_corners and label in self.plane_corners:
            self.plane_corners = None
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_calibrated = False
            self.plane_status_var.set("Duzlem henuz ayarlanmadi (bir kose silindi).")

    # ---------- Kolay mod: adim adim sihirbaz ----------
    # Tek bir talimat seridi kullaniciyi yonlendirir; soru penceresi acilmaz.
    # Arka planda AYNI hesaplama kodu (referans, yardimci cizgi, sorgu)
    # kullanilir - sihirbaz sadece bir arayuz katmanidir.

    WZ_BG = "#fff6d6"

    def _build_wizard_banner(self, parent):
        bg = self.WZ_BG
        f = tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground="#e0c060")
        f.pack(fill="x", pady=(0, 6))
        self.wizard_frame = f
        self.wizard_title = tk.Label(f, text="", bg=bg, font=("Segoe UI", 14, "bold"), anchor="w",
                                     justify="left")
        self.wizard_title.pack(fill="x", padx=10, pady=(6, 0))
        self.wizard_sub = tk.Label(f, text="", bg=bg, fg="#444", font=("Segoe UI", 10), anchor="w",
                                   justify="left", wraplength=950)
        self.wizard_sub.pack(fill="x", padx=10, pady=(0, 4))

        row = tk.Frame(f, bg=bg)
        self.wizard_len_row = row
        font = ("Segoe UI", 11)
        tk.Label(row, text="A–B uzunlugu:", bg=bg, font=font).pack(side="left")
        self.wz_ab = ttk.Entry(row, width=9, font=font)
        self.wz_ab.pack(side="left", padx=(4, 12))
        tk.Label(row, text="A–C uzunlugu:", bg=bg, font=font).pack(side="left")
        self.wz_ac = ttk.Entry(row, width=9, font=font)
        self.wz_ac.pack(side="left", padx=(4, 4))
        self.wz_unit_lbl = tk.Label(row, textvariable=self.unit_var, bg=bg, font=font)
        self.wz_unit_lbl.pack(side="left", padx=(0, 12))
        self.wz_right_var = tk.BooleanVar(value=True)
        tk.Checkbutton(row, text="A kosesi dik aci (90°)", variable=self.wz_right_var, bg=bg, font=font,
                       activebackground=bg, command=self._wizard_angle_toggle).pack(side="left")
        self.wz_angle = ttk.Entry(row, width=6, font=font, state="disabled")
        self.wz_angle.pack(side="left", padx=(4, 12))
        ttk.Button(row, text="Tamam", command=self._wizard_apply_lengths).pack(side="left")
        for e in (self.wz_ab, self.wz_ac, self.wz_angle):
            e.bind("<Return>", lambda ev: self._wizard_apply_lengths())

        btns = tk.Frame(f, bg=bg)
        self.wizard_btn_row = btns
        self.wz_buttons = {
            "undo": ttk.Button(btns, text="↶ Geri al", command=self._wizard_undo),
            "edge_ab": ttk.Button(btns, text="Dogrulugu artir: A–B'ye paralel kenar ekle",
                                  command=lambda: self._wizard_add_edge("ab")),
            "edge_ac": ttk.Button(btns, text="Dogrulugu artir: A–C'ye paralel kenar ekle",
                                  command=lambda: self._wizard_add_edge("ac")),
            "lengths": ttk.Button(btns, text="Uzunluklari degistir", command=lambda: self._wizard_go("lengths")),
            "cancel": ttk.Button(btns, text="Vazgec", command=self.cancel_helper_capture),
            "restart": ttk.Button(btns, text="Bastan basla", command=self._wizard_restart),
        }
        self.wizard_go_pending = None
        self._wizard_render("open")

    def _wizard_render(self, step, title=None, sub=None, sub_color="#444"):
        texts = {
            "open": ("Baslamak icin bir fotograf veya PDF acin",
                     "Ustteki 'Fotograf / PDF Ac' dugmesine basin."),
            "A": ("Adim 1/4 — A kosesine tiklayin",
                  "Uzunlugunu bildiginiz IKI kenarin birlestigi kose (ör. bir pencerenin sol alt kosesi). "
                  "Hassas tiklamak icin fare tekerlegiyle yakinlastirin; sag tik + surukle ile kaydirin."),
            "B": ("Adim 2/4 — B noktasina tiklayin",
                  "A'dan cikan BIRINCI kenarin diger ucu (ör. pencerenin sag alt kosesi)."),
            "C": ("Adim 3/4 — C noktasina tiklayin",
                  "A'dan cikan IKINCI kenarin diger ucu (ör. pencerenin sol ust kosesi)."),
            "lengths": ("Adim 4/4 — Gercek uzunluklari yazin",
                        "Bu iki kenarin gercek uzunluklarini yazip Tamam'a (ya da Enter'a) basin."),
            "measure": ("Olcmek istediginiz iki noktaya tiklayin", ""),
            "edge": ("Kenarin iki ucuna tiklayin", ""),
        }
        t, s_ = texts.get(step, ("", ""))
        self.wizard_title.config(text=title if title is not None else t)
        self.wizard_sub.config(text=sub if sub is not None else s_, fg=sub_color)
        self.wizard_len_row.pack_forget()
        self.wizard_btn_row.pack_forget()
        if step == "lengths":
            self.wizard_len_row.pack(fill="x", padx=10, pady=(0, 6))
        visible = {"open": [], "A": [], "B": ["undo", "restart"], "C": ["undo", "restart"],
                   "lengths": ["undo", "restart"], "measure": ["undo", "edge_ab", "edge_ac", "lengths", "restart"],
                   "edge": ["cancel"]}.get(step, [])
        for key, b in self.wz_buttons.items():
            b.pack_forget()
        for key in visible:
            self.wz_buttons[key].pack(side="left", padx=(0, 6))
        if visible:
            self.wizard_btn_row.pack(fill="x", padx=10, pady=(0, 8))

    def _wizard_go(self, step):
        self.wizard_step = step
        self.wizard_pending = None
        if step == "lengths":
            for e, src in ((self.wz_ab, self.abc_len_entries[0]), (self.wz_ac, self.abc_len_entries[1])):
                if not e.get().strip() and src.get().strip():
                    e.insert(0, src.get().strip())
            self._wizard_render("lengths")
            self.wz_ab.focus_set()
        elif step == "measure":
            self._wizard_render("measure", sub=self._wizard_measure_text())
        else:
            self._wizard_render(step)
        self._redraw()

    def wizard_start(self):
        self.wizard_pending = None
        self._wizard_counter = 0
        for e in (self.wz_ab, self.wz_ac):
            e.delete(0, "end")
        self._wizard_go("A" if self.pil_img is not None else "open")

    def _wizard_sync(self):
        """Config yukleme gibi disaridan gelen degisikliklerden sonra adimi belirler."""
        if not self.easy_mode:
            return
        labels = {p["label"] for p in self.points}
        if self.pil_img is None:
            self._wizard_go("open")
        elif self.plane_calibrated and self.plane_H is not None:
            self._wizard_go("measure")
        elif "A" not in labels:
            self._wizard_go("A")
        elif "B" not in labels:
            self._wizard_go("B")
        elif "C" not in labels:
            self._wizard_go("C")
        else:
            self._wizard_go("lengths")

    def _wizard_put_point(self, label, x, y):
        self.points = [p for p in self.points if p["label"] != label]
        self.points.append({"label": label, "x": x, "y": y, "source": "manual"})
        self._refresh_all_display()

    def _wizard_remove_point(self, label):
        if any(p["label"] == label for p in self.points):
            self.points = [p for p in self.points if p["label"] != label]
            self._remove_references_to(label)
            self._refresh_all_display()

    def _wizard_click(self, x, y):
        st = self.wizard_step
        if st in ("A", "B", "C"):
            self._wizard_put_point(st, x, y)
            if st == "C":
                for cb, lb in zip(self.abc_combos, "ABC"):
                    cb.set(lb)
            self._wizard_go({"A": "B", "B": "C", "C": "lengths"}[st])
        elif st == "lengths":
            self._wizard_render("lengths", sub="Once uzunluklari yazip Tamam'a basin.", sub_color="#b00")
        elif st == "measure":
            if self.wizard_pending is None:
                label = self._wizard_free_label()
                self._wizard_put_point(label, x, y)
                self.wizard_pending = label
                self._wizard_render("measure", title="Simdi ikinci noktaya tiklayin",
                                    sub="Iki nokta arasindaki gercek uzunluk hesaplanacak.")
                self._redraw()
            else:
                first = self.wizard_pending
                label = self._wizard_free_label()
                self._wizard_put_point(label, x, y)
                self.wizard_pending = None
                self._wizard_add_measurement(first, label)

    def _wizard_free_label(self):
        used = {p["label"] for p in self.points}
        k = 1
        while f"M{k}" in used:
            k += 1
        return f"M{k}"

    def _wizard_angle_toggle(self):
        self.wz_angle.config(state="disabled" if self.wz_right_var.get() else "normal")
        if not self.wz_right_var.get():
            self.wz_angle.focus_set()

    def _wizard_apply_lengths(self):
        def parse(e):
            try:
                v = float(e.get().strip().replace(",", "."))
            except ValueError:
                return None
            return v if v > 0 else None
        ab, ac = parse(self.wz_ab), parse(self.wz_ac)
        if ab is None or ac is None:
            self._wizard_render("lengths", sub="Iki kutuya da pozitif bir sayi yazin (ör. 1.20).", sub_color="#b00")
            return
        right = self.wz_right_var.get()
        angle = None
        if not right:
            angle = parse(self.wz_angle)
            if angle is None or angle >= 180:
                self._wizard_render("lengths", sub="A kosesindeki aciyi 0-180 derece arasinda yazin.",
                                    sub_color="#b00")
                return
        if self.ref_mode_var.get() != "abc2len":
            # (ör. ref_mode alani olmayan eski bir config 'affine3' birakmis olabilir)
            self.ref_mode_var.set("abc2len")
            self._apply_ref_mode()
        for cb, lb in zip(self.abc_combos, "ABC"):
            cb.set(lb)
        for dst, val in ((self.abc_len_entries[0], ab), (self.abc_len_entries[1], ac)):
            dst.delete(0, "end")
            dst.insert(0, f"{val}")
        self.abc_right_angle_var.set(right)
        self.abc_angle_entry.delete(0, "end")
        if angle is not None:
            self.abc_angle_entry.insert(0, f"{angle}")
        self._recompute_plane(silent=True)
        if not self.plane_calibrated or self.plane_H is None:
            self._wizard_render("lengths", sub="Referans kurulamadi: A, B, C neredeyse ayni dogru uzerinde olabilir. "
                                               "'Geri al' ile noktalari yeniden secin.", sub_color="#b00")
            return
        self._wizard_refresh_measurements()
        self._wizard_go("measure")

    def _wizard_add_measurement(self, la, lb):
        snap = self._snapshot_current_plane()
        if snap is None:
            self._wizard_go("lengths")
            return
        snap["ref_label"] = self._current_ref_label(snap["corners"])
        n = 1
        names = {q["name"] for q in self.queries}
        while f"Olcum {n}" in names:
            n += 1
        self.queries.append({"name": f"Olcum {n}", "a": la, "b": lb, "c": None, "ground_truth_m": None,
                             "plane_snapshot": snap})
        self._refresh_query_list()
        self.compute()
        self._wizard_go("measure")

    def _wizard_refresh_measurements(self):
        """Referans degisince (uzunluk, yardimci kenar) sihirbazdaki olcumler
        guncel referansa tasinir ve yeniden hesaplanir."""
        snap = self._snapshot_current_plane()
        if snap is None or not self.queries:
            return
        snap["ref_label"] = self._current_ref_label(snap["corners"])
        for q in self.queries:
            q["plane_snapshot"] = dict(snap)
        self._refresh_query_list()
        self.compute()

    def _wizard_measure_text(self):
        lines = []
        if self.plane_H is not None and self.plane_calibrated:
            if getattr(self, "plane_model_type", None) == "projective":
                conf = {"YUKSEK": "yuksek", "ORTA": "orta", "DUSUK": "dusuk"}.get(self.plane_vp_confidence,
                                                                               self.plane_vp_confidence)
                lines.append(f"Referans hazir - perspektif duzeltildi (guven: {conf}).")
                if self.plane_vp_confidence != "YUKSEK":
                    lines.append("Daha dogru sonuc icin: fotografin UZAK bir bolgesinde A–B'ye ya da A–C'ye "
                                 "paralel, uzun ve net bir kenar ekleyin (asagidaki dugmeler).")
            else:
                lines.append("Referans hazir - ama perspektif bulunamadi; referanstan uzak olcumler hatali "
                             "olabilir. Asagidaki dugmelerle A–B'ye ve A–C'ye paralel birer kenar ekleyin.")
        results = [f"{q['name']}: {self._fmt(self.last_results[q['name']])}"
                   for q in self.queries if q["name"] in self.last_results]
        if results:
            lines.append("Sonuclar:  " + "   |   ".join(results[-6:]))
        return "\n".join(lines)

    def _wizard_undo(self):
        st = self.wizard_step
        if st == "measure":
            if self.wizard_pending is not None:
                self._wizard_remove_point(self.wizard_pending)
                self._wizard_go("measure")
            elif self.queries:
                q = self.queries.pop()
                self.last_results.pop(q["name"], None)
                for lb in (q["a"], q["b"]):
                    if lb.startswith("M"):
                        self._wizard_remove_point(lb)
                self._refresh_query_list()
                self._wizard_go("measure")
            else:
                self._wizard_go("lengths")
        elif st == "lengths":
            self._wizard_remove_point("C")
            self._wizard_go("C")
        elif st == "C":
            self._wizard_remove_point("B")
            self._wizard_go("B")
        elif st == "B":
            self._wizard_remove_point("A")
            self._wizard_go("A")

    def _wizard_restart(self):
        if self.pil_img is None:
            return
        self._reset_state_for_new_photo()
        self._refresh_all_display()
        self.wizard_start()

    def _wizard_add_edge(self, family):
        name = "A–B" if family == "ab" else "A–C"
        self.wizard_step = "edge"
        self._wizard_render("edge", title=f"{name}'ye paralel bir kenarin iki ucuna tiklayin",
                            sub=f"Gercekte {name} ile paralel, AYNI yuzeyde ve referanstan UZAK, uzun ve net bir "
                                f"kenar secin (ör. cati hatti, pencere sirasi, bina kosesi). Esc: vazgec.")
        self.start_helper_capture(family)

    def _wizard_after_edge(self):
        if self.easy_mode and self.wizard_step == "edge":
            self._wizard_refresh_measurements()
            self._wizard_go("measure" if self.plane_calibrated else "lengths")

    def toggle_advanced(self):
        self.advanced_visible = not self.advanced_visible
        if self.advanced_visible:
            for tb in self._adv_toolbars:
                tb.pack(fill="x", pady=(0, 6), before=self._hint_label)
            self.right_container.pack(side="left", fill="y", padx=(10, 0))
            self.advanced_btn.config(text="Gelismis ◂ (gizle)")
        else:
            for tb in self._adv_toolbars:
                tb.pack_forget()
            self.right_container.pack_forget()
            self.advanced_btn.config(text="Gelismis ▸")

    def _on_easy_mode_toggle(self):
        self.easy_mode = self.easy_mode_var.get()
        if self.easy_mode:
            self.wizard_frame.pack(fill="x", pady=(0, 6), after=self._toolbar_main)
            self._wizard_sync()
        else:
            self.wizard_frame.pack_forget()

    # ---------- Yardimci cizgiler (nokta akisi + Daha Yuksek Dogruluk paneli) ----------

    HELPER_SOURCE_LABELS = {"manual": "elle", "manual_magnifier": "elle (buyutec)",
                            "manual_refined": "elle + kenar", "point_pair": "nokta cifti"}

    def _choice_dialog(self, title, text, buttons, default=None):
        """Kucuk, modal secim penceresi. Enter/Esc/kapatma = default."""
        result = {"key": default}
        win = tk.Toplevel(self)
        win.title(title)
        win.transient(self)
        win.resizable(False, False)
        ttk.Label(win, text=text, justify="left", wraplength=480).pack(padx=12, pady=(12, 8), anchor="w")
        row = ttk.Frame(win)
        row.pack(padx=12, pady=(0, 12), fill="x")

        def choose(k):
            result["key"] = k
            win.destroy()

        for i, (key, label) in enumerate(buttons):
            b = ttk.Button(row, text=label, command=lambda k=key: choose(k))
            b.grid(row=i // 3, column=i % 3, padx=3, pady=2, sticky="ew")
            if key == default:
                b.focus_set()
        win.bind("<Return>", lambda e: choose(default))
        win.bind("<Escape>", lambda e: choose(default))
        win.protocol("WM_DELETE_WINDOW", lambda: choose(default))
        win.grab_set()
        self.wait_window(win)
        return result["key"]

    def _point_role(self, label):
        """Etiketin referanstaki rolu (A/B/C) - comboboxlardan, yoksa
        (henuz secim yapilmamissa) varsayilan A/B/C etiketlerinden."""
        combos = [cb.get() for cb in self.abc_combos]
        for role, lb in zip("ABC", combos):
            if lb == label:
                return role
        if not any(combos) and label in ("A", "B", "C"):
            return label
        return None

    def _offer_helper_after_point(self, label):
        """Nokta eklendikten SONRA hafif, ISTEGE BAGLI soru. Enter/Hayir ile
        akis eskisi gibi devam eder."""
        if self.pil_img is None or self.helper_capture is not None:
            return
        if not any(p["label"] == label for p in self.points):
            return
        role = self._point_role(label)
        rec = {"B": "ab", "C": "ac"}.get(role)
        hint = ""
        if role == "A":
            hint = ("\n\nA ortak kosedir - hem AB hem AC yonune katilir. Hangi yonde bir kenar "
                    "ekleyeceginizi acikca secin.")
        elif rec:
            hint = (f"\n\n{label} ile {FAMILY_NAMES[rec]} referans kenari tanimlandi; bu yonde baska bir "
                    f"kenar eklemek en dogal secimdir (kenar baska bir yerde de olabilir).")
        buttons = [("no", "Hayir"),
                   ("ab", "AB yonu" + (" (onerilen)" if rec == "ab" else "")),
                   ("ac", "AC yonu" + (" (onerilen)" if rec == "ac" else "")),
                   ("auto", "Otomatik"),
                   ("later", "Yonu daha sonra belirle")]
        choice = self._choice_dialog(
            "Yardimci cizgi ekle?",
            f"'{label}' eklendi. Bu nokta icin yardimci cizgi eklemek ister misiniz?\n\n"
            f"Yardimci cizgi, A-B veya A-C ile gercekte paralel olan baska bir kenardir. "
            f"Istemiyorsaniz Enter (Hayir) ile devam edin.{hint}",
            buttons, default="no")
        if choice in (None, "no"):
            return
        mode = self._choice_dialog(
            "Yardimci cizgi",
            f"Kenari nasil secmek istersiniz?\n\n"
            f"Bu noktadan baslat: '{label}' kenarin bir ucu olur; ayni gercek kenar uzerinde "
            f"ikinci bir nokta tiklayin.\n\n"
            f"Baska kenar sec: fotografin herhangi bir yerindeki bir kenarin iki ucunu tiklayin "
            f"(en faydalisi: referanstan UZAK, uzun ve net bir kenar).",
            [("anchor", "Bu noktadan baslat"), ("free", "Baska kenar sec"), ("cancel", "Iptal")],
            default="anchor")
        if mode in (None, "cancel"):
            return
        family = "auto" if choice in ("auto", "later") else choice
        self.start_helper_capture(family, anchor_label=label if mode == "anchor" else None,
                                  defer_family=(choice == "later"))

    def start_helper_capture(self, family, anchor_label=None, defer_family=False):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        # Diger tiklama modlariyla KARISMASIN - ayri, acik bir durum.
        if self.edge_mode:
            self.toggle_edge_mode()
        if self.line_calib_mode:
            self.toggle_line_calib_mode()
        pts, sigmas, srcs = [], [], []
        if anchor_label:
            p = next((q for q in self.points if q["label"] == anchor_label), None)
            if p is None:
                return
            pts.append((p["x"], p["y"]))
            sigmas.append(point_sigma_px(p.get("source", "manual")))
            srcs.append("anchor")
        self.helper_capture = {"family": family, "anchor_label": anchor_label, "points": pts,
                               "sigmas": sigmas, "srcs": srcs, "defer_family": defer_family}
        self._helper_capture_status()
        self._redraw()

    def _helper_capture_status(self):
        cap = self.helper_capture
        if cap is None:
            return
        name = {"ab": "AB yonu", "ac": "AC yonu"}.get(cap["family"], "Yonu belirlenecek")
        which = "ilk ucu" if not cap["points"] else "ikinci ucu"
        self.status_var.set(f"{name} yardimci cizgisi: {which} secin  (Esc / sag tik: iptal)")

    def cancel_helper_capture(self):
        if self.helper_capture is None:
            return
        self.helper_capture = None
        self.canvas.delete("helper_rubber")
        self.status_var.set("Yardimci cizgi iptal edildi.")
        self._redraw()
        self._wizard_after_edge()

    def _helper_capture_add_endpoint(self, x, y, source="manual"):
        cap = self.helper_capture
        if cap is None:
            return
        cap["points"].append((x, y))
        cap["sigmas"].append(LINE_ENDPOINT_SIGMA_PX.get(source, 1.0))
        cap["srcs"].append(source)
        if len(cap["points"]) < 2:
            self._helper_capture_status()
            self._redraw()
            return
        self.helper_capture = None
        self.canvas.delete("helper_rubber")
        self._finalize_helper_capture(cap)

    def _new_helper_id(self):
        existing = {h["id"] for h in self.helper_lines}
        while True:
            self._helper_counter += 1
            hid = f"HL{self._helper_counter}"
            if hid not in existing:
                return hid

    def _finalize_helper_capture(self, cap):
        p1, p2 = cap["points"]
        if dist(p1, p2) < 15:
            messagebox.showerror("Hata", "Yardimci cizgi cok kisa (en az ~15 piksel). Tekrar deneyin.")
            self._redraw()
            self._wizard_after_edge()
            return
        sig = math.sqrt(sum(s * s for s in cap["sigmas"]) / len(cap["sigmas"]))
        clicked = [s for s in cap["srcs"] if s != "anchor"]
        src = "manual_magnifier" if clicked and all(s == "manual_magnifier" for s in clicked) else "manual"
        hl = {"id": self._new_helper_id(), "p1": [float(p1[0]), float(p1[1])], "p2": [float(p2[0]), float(p2[1])],
              "family": cap["family"], "source": src, "anchor_label": cap["anchor_label"],
              "point_labels": None, "verified": True, "endpoint_sigma_px": sig, "n_support": 2, "note": ""}
        if self.helper_refine_var.get():
            try:
                gray = np.array(self.pil_img.convert("L"))
                ref, why = refine_line_to_edge(gray, p1, p2)
            except Exception as e:
                ref, why = None, str(e)
            if ref is not None:
                hl.update({"p1": list(ref["p1"]), "p2": list(ref["p2"]), "source": "manual_refined",
                           "endpoint_sigma_px": max(0.1, ref["rms_px"]), "n_support": ref["n_support"],
                           "note": f"kenara oturtuldu (rms {ref['rms_px']:.2f} px, {ref['n_support']} ornek)"})
            else:
                hl["note"] = f"kenara oturtulmadi ({why}) - tiklanan konum kullanildi"
        self._commit_helper_with_assessment(hl, defer_family=cap.get("defer_family", False))

    def _make_point_pair_helper(self, family, labels):
        lookup = {p["label"]: p for p in self.points}
        pa, pb = lookup[labels[0]], lookup[labels[1]]
        sig = math.sqrt((point_sigma_px(pa.get("source", "manual")) ** 2 +
                         point_sigma_px(pb.get("source", "manual")) ** 2) / 2.0)
        return {"id": f"P-{family.upper()}", "p1": [pa["x"], pa["y"]], "p2": [pb["x"], pb["y"]],
                "family": family, "source": "point_pair", "anchor_label": None,
                "point_labels": list(labels), "verified": True, "endpoint_sigma_px": sig,
                "n_support": 2, "note": "eski yontem: iki nokta etiketiyle"}

    @staticmethod
    def _normalize_helper_line(d):
        """JSON'dan gelen (ya da eksik alanli) bir kaydi guvenli bicime getirir."""
        fam = d.get("family", "auto")
        return {"id": str(d.get("id") or "HL?"), "p1": [float(d["p1"][0]), float(d["p1"][1])],
                "p2": [float(d["p2"][0]), float(d["p2"][1])],
                "family": fam if fam in ("ab", "ac", "auto") else "auto",
                "source": d.get("source", "manual"), "anchor_label": d.get("anchor_label"),
                "point_labels": d.get("point_labels"), "verified": bool(d.get("verified", True)),
                "endpoint_sigma_px": float(d.get("endpoint_sigma_px", 1.0)),
                "n_support": int(d.get("n_support", 2)), "note": d.get("note", "")}

    def _helper_to_observation(self, hl):
        o = LineObservation(tuple(hl["p1"]), tuple(hl["p2"]), source=hl.get("source", "manual"),
                            verified=bool(hl.get("verified", True)), family=hl.get("family", "auto"),
                            line_id=hl["id"], endpoint_sigma_px=float(hl.get("endpoint_sigma_px", 1.0)),
                            n_support=int(hl.get("n_support", 2)))
        hl["sigma_angle_deg"] = o.sigma_angle_deg
        return o

    def _sync_point_pair_helpers(self):
        """Nokta-cifti (eski yontem) yardimci cizgileri etiketlerin GUNCEL
        konumlarini izler; etiket artik yoksa bag koparilir (konum korunur)."""
        lookup = {p["label"]: p for p in self.points}
        for hl in self.helper_lines:
            labels = hl.get("point_labels")
            if not labels:
                continue
            if all(lb in lookup for lb in labels):
                fresh = self._make_point_pair_helper(hl["family"] if hl["family"] in ("ab", "ac") else "ab", labels)
                hl["p1"], hl["p2"] = fresh["p1"], fresh["p2"]
                hl["endpoint_sigma_px"] = fresh["endpoint_sigma_px"]
            else:
                hl["point_labels"] = None
                hl["source"] = "manual"
                hl["note"] = "nokta etiketi artik yok; kenar konumu korundu"

    def _on_legacy_helper_combo(self, family):
        combos = self.abc_helper_ab_combos if family == "ab" else self.abc_helper_ac_combos
        labels = [cb.get() for cb in combos]
        hid = f"P-{family.upper()}"
        had = any(h["id"] == hid for h in self.helper_lines)
        self.helper_lines = [h for h in self.helper_lines if h["id"] != hid]
        lookup = {p["label"] for p in self.points}
        if all(labels) and labels[0] != labels[1] and all(lb in lookup for lb in labels):
            self._commit_helper_with_assessment(self._make_point_pair_helper(family, labels))
        elif had:
            self._vp_stage_cache = (None, None)
            self._refresh_helper_tree()
            self._try_auto_compute_plane()

    def _current_abc_points(self):
        labels = [cb.get() for cb in self.abc_combos]
        if any(not lb for lb in labels) or len(set(labels)) != 3:
            return None
        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        if not all(lb in lookup for lb in labels):
            return None
        return tuple(lookup[lb] for lb in labels)

    def _current_abc_inputs(self):
        """Referans girdileri gecerliyse (mesaj GOSTERMEDEN) sozluk, degilse None."""
        if self.pil_img is None or self.ref_mode_var.get() != "abc2len":
            return None
        pts = self._current_abc_points()
        if pts is None:
            return None
        labels = [cb.get() for cb in self.abc_combos]
        A, B, C = pts
        if triangle_min_angle_deg(A, B, C) < MIN_TRIANGLE_ANGLE_DEG:
            return None
        ab_m = self._peek_len(self.abc_len_entries[0])
        ac_m = self._peek_len(self.abc_len_entries[1])
        if ab_m is None or ac_m is None:
            return None
        if self.abc_right_angle_var.get():
            angle_deg = 90.0
        else:
            try:
                angle_deg = float(self.abc_angle_entry.get().strip().replace(",", "."))
            except ValueError:
                return None
            if not (0 < angle_deg < 180):
                return None
        src = {p["label"]: p.get("source", "manual") for p in self.points}
        return {"labels": labels, "A": A, "B": B, "C": C, "sources": [src[lb] for lb in labels],
                "ab_m": ab_m, "ac_m": ac_m, "angle_deg": angle_deg}

    def _get_auto_line_observations(self):
        """Otomatik cizgi gozlemleri (LSD/Hough + gradyan gucu + sigma),
        fotograf basina bir kez hesaplanir."""
        if self.pil_img is None:
            return []
        key = id(self.pil_img)
        if getattr(self, "_auto_obs_cache_key", None) != key:
            try:
                self._auto_obs_cache = detect_line_observations(np.array(self.pil_img.convert("L")))
            except Exception:
                self._auto_obs_cache = []
            self._auto_obs_cache_key = key
        return self._auto_obs_cache[:AUTO_LINE_POOL_MAX]

    def _build_family_observations(self, inputs, helpers=None):
        """AB / AC aileleri icin gozlem havuzlari:
          - referans A-B / A-C (dogrulanmis, metrigi de tanimlar)
          - kullanicinin yardimci cizgileri (dogrulanmis, ailesi atanmis)
          - olcum sorgusu kenarlari ve otomatik cizgiler (DOGRULANMAMIS; her
            iki havuza da aday olarak girer - aile VP tutarliligiyla secilir)
        Dogrulanmis bir cizgiyle ayni goruntu dogrusu uzerindeki otomatik
        cizgiler (ör. referans kenarin kendisi) bagimsiz kanit olmadigi icin
        atilir."""
        A, B, C = inputs["A"], inputs["B"], inputs["C"]
        sA, sB, sC = (point_sigma_px(s) for s in inputs["sources"])
        ra = LineObservation(A, B, source="reference", verified=True, family="ab", line_id="REF-AB",
                             is_reference=True, endpoint_sigma_px=math.sqrt((sA * sA + sB * sB) / 2.0))
        rc = LineObservation(A, C, source="reference", verified=True, family="ac", line_id="REF-AC",
                             is_reference=True, endpoint_sigma_px=math.sqrt((sA * sA + sC * sC) / 2.0))
        obs_ab, obs_ac, verified_lines = [ra], [rc], [ra, rc]
        self._sync_point_pair_helpers()
        for hl in (self.helper_lines if helpers is None else helpers):
            if hl.get("family") not in ("ab", "ac"):
                continue
            o = self._helper_to_observation(hl)
            (obs_ab if hl["family"] == "ab" else obs_ac).append(o)
            verified_lines.append(o)

        lookup = {p["label"]: p for p in self.points}
        for q in self.queries:
            path = [q.get("a"), q.get("b")] + ([q["c"]] if q.get("c") else [])
            for k in range(len(path) - 1):
                pa, pb = lookup.get(path[k]), lookup.get(path[k + 1])
                if pa is None or pb is None:
                    continue
                sig = math.sqrt((point_sigma_px(pa.get("source", "manual")) ** 2 +
                                 point_sigma_px(pb.get("source", "manual")) ** 2) / 2.0)
                o = LineObservation((pa["x"], pa["y"]), (pb["x"], pb["y"]), source="query_edge", verified=False,
                                    line_id=f"Q:{q['name']}:{k}", endpoint_sigma_px=sig)
                if o.length_px < 15 or any(helper_duplicates_reference(o.p1, o.p2, v.p1, v.p2, 1.0, 3.0)
                                           for v in verified_lines):
                    continue
                obs_ab.append(o)
                obs_ac.append(o)
        for o in self._get_auto_line_observations():
            tol = max(3.0, 3.0 * o.endpoint_sigma_px)
            if any(helper_duplicates_reference(o.p1, o.p2, v.p1, v.p2, 1.0, tol) for v in verified_lines):
                continue
            obs_ab.append(o)
            obs_ac.append(o)
        return obs_ab, obs_ac

    def _known_segments(self):
        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        out = []
        for q in self.queries:
            if q.get("ground_truth_m") and not q.get("c") and q["a"] in lookup and q["b"] in lookup:
                out.append((lookup[q["a"]], lookup[q["b"]], q["ground_truth_m"]))
        return out

    def _vp_stage(self, A, obs_ab, obs_ac, img_size):
        """VP asamasi uzunluklardan/acidan BAGIMSIZDIR - uzunluk kutusuna
        yazarken her tus vurusunda yeniden hesaplanmasin diye onbellek."""
        def sig(obs):
            return tuple((o.line_id, round(o.p1[0], 3), round(o.p1[1], 3), round(o.p2[0], 3), round(o.p2[1], 3),
                          o.verified, round(o.endpoint_sigma_px, 4), o.n_support) for o in obs)
        key = (id(self.pil_img), sig(obs_ab), sig(obs_ac))
        if self._vp_stage_cache[0] == key:
            return self._vp_stage_cache[1]
        stage = estimate_family_vps(obs_ab, obs_ac, A, img_size=img_size)
        self._vp_stage_cache = (key, stage)
        return stage

    def _update_helper_status(self, stage):
        self.helper_status = {}
        if stage is not None:
            for fam, f in stage["families"].items():
                loo = {x["line_id"]: x for x in ((f.get("validation") or {}).get("loo", []))}
                for lid, st in (f.get("line_status") or {}).items():
                    if not st.get("verified") or lid.startswith("REF-"):
                        continue
                    entry = dict(st)
                    entry["family"] = fam
                    entry["loo_z"] = loo.get(lid, {}).get("z")
                    self.helper_status[lid] = entry
        self._refresh_helper_tree()

    def _commit_helper_with_assessment(self, hl, defer_family=False):
        """Yeni yardimci cizgiyi ONCE aday model olarak degerlendirir, eski
        modelle karsilastirir; H_final ancak dogrulama kotulesmiyorsa ya da
        kullanici ACIKCA kabul ederse degisir."""
        msgs = []
        pts = self._current_abc_points()
        if pts:
            A, B, C = pts
            for rp, rq, nm in ((A, B, "A-B"), (A, C, "A-C")):
                if helper_duplicates_reference(hl["p1"], hl["p2"], rp, rq):
                    msgs.append(f"Not: bu yardimci cizgi referans cizgisiyle ({nm}) neredeyse ayni konumda. "
                                f"Daha uzaktaki paralel bir kenar kacis noktasi tahminini daha fazla guclendirir.")
        inputs = self._current_abc_inputs()
        img_size = (self.pil_img.width, self.pil_img.height)

        if hl["family"] == "auto" and not defer_family:
            fam, zs = None, {}
            if inputs is not None:
                obs_ab, obs_ac = self._build_family_observations(inputs)
                res = compute_metric_homography_from_observations(
                    inputs["A"], inputs["B"], inputs["C"], inputs["ab_m"], inputs["ac_m"], inputs["angle_deg"],
                    img_size=img_size, stage=self._vp_stage(inputs["A"], obs_ab, obs_ac, img_size))
                fam, zs = suggest_line_family(self._helper_to_observation(hl), res)
            if fam is not None:
                hl["family"] = fam
                hl["note"] = (hl.get("note", "") + " | yon VP tutarliligiyla onerildi").strip(" |")
                msgs.append(f"Yon onerisi: {FAMILY_NAMES[fam]} (z_AB={zs['ab']:.1f}, z_AC={zs['ac']:.1f}). "
                            f"Yanlissa listeden degistirebilirsiniz.")
            else:
                detail = (f"\n\nAB yonune sapma z={zs['ab']:.1f}, AC yonune z={zs['ac']:.1f} "
                          f"(3'un alti tutarli).") if len(zs) == 2 else \
                    "\n\n(Henuz perspektif modeli yok - once A/B/C ve uzunluklari tamamlayin.)"
                c = self._choice_dialog("Yon belirsiz",
                                        "Yardimci cizginin yonu belirsiz. AB veya AC olarak secin." + detail,
                                        [("ab", "AB"), ("ac", "AC"), ("later", "Daha sonra")], default="later")
                if c in ("ab", "ac"):
                    hl["family"] = c

        if hl["family"] not in ("ab", "ac") or inputs is None:
            self.helper_lines.append(hl)
            self._vp_stage_cache = (None, None)
            self._refresh_helper_tree()
            self._try_auto_compute_plane()
            if hl["family"] not in ("ab", "ac"):
                msgs.insert(0, f"{hl['id']} kaydedildi, ancak yonu atanmadi - hesaplamada KULLANILMIYOR. "
                               f"Listeden AB/AC secin ya da 'Otomatik (oner)' deneyin.")
            else:
                msgs.insert(0, f"{hl['id']} ({FAMILY_NAMES[hl['family']]}) kaydedildi. Referans (A, B, C ve "
                               f"uzunluklar) tamamlaninca perspektif hesabina katilacak.")
            self.status_var.set(msgs[0])
            if len(msgs) > 1 and not self.easy_mode:
                messagebox.showinfo("Yardimci cizgi", "\n\n".join(msgs))
            self._redraw()
            self._wizard_after_edge()
            return

        obs_ab, obs_ac = self._build_family_observations(inputs)
        new_obs = self._helper_to_observation(hl)
        self.status_var.set("Yardimci cizgi degerlendiriliyor (onceki/sonraki model karsilastiriliyor)...")
        self.update_idletasks()
        a = assess_helper_addition(inputs["A"], inputs["B"], inputs["C"], inputs["ab_m"], inputs["ac_m"],
                                   inputs["angle_deg"], obs_ab, obs_ac, new_obs, img_size=img_size,
                                   known_segments=self._known_segments())
        text = self._format_assessment(a, hl)
        if msgs:
            text += "\n\n" + "\n".join(msgs)
        other = "ac" if hl["family"] == "ab" else "ab"
        swap_lbl = f"Yonu {FAMILY_NAMES[other]} yap"
        if a["verdict"] in ("accept", "accept_validated", "accept_unvalidated", "no_model") and self.easy_mode:
            choice = "keep"  # kolay mod: sorun yoksa soru sorma, sonucu seritte goster
        elif a["verdict"] in ("accept", "accept_validated", "accept_unvalidated", "no_model"):
            choice = self._choice_dialog("Yardimci cizgi", text,
                                         [("keep", "Tamam"), ("swap", swap_lbl), ("delete", "Sil")], default="keep")
        else:
            choice = self._choice_dialog("Yardimci cizgi - tutarsizlik", text,
                                         [("keep", "Yine de kullan"), ("swap", swap_lbl), ("delete", "Sil")],
                                         default="delete")
        if choice == "delete":
            self.status_var.set(f"{hl['id']} eklenmedi; model degismedi.")
            self._redraw()
            self._wizard_after_edge()
            return
        if choice == "swap":
            hl["family"] = other
            hl["note"] = (hl.get("note", "") + " | yon kullanici tarafindan degistirildi").strip(" |")
            self._commit_helper_with_assessment(hl)
            return
        if a["verdict"] not in ("accept", "accept_validated", "accept_unvalidated", "no_model"):
            hl["note"] = (hl.get("note", "") + " | tutarsizliga ragmen kullanici kabul etti").strip(" |")
        self.helper_lines.append(hl)
        self._vp_stage_cache = (None, None)
        self._recompute_plane(silent=True)
        self._refresh_helper_tree()
        self.status_var.set(f"{hl['id']} ({FAMILY_NAMES[hl['family']]}) eklendi ve modele katildi.")
        self._wizard_after_edge()

    def _format_assessment(self, a, hl):
        fam = a["family"]
        fn = FAMILY_NAMES[fam]
        verdict_txt = {
            "accept": "Mevcut modelle tutarli - model guncellendi.",
            "accept_validated": ("Mevcut kanitla catisiyor, ancak BAGIMSIZ veri (diger yardimci cizgiler / "
                                 "bilinen uzunluklar) yeni modeli destekliyor - model guncellendi."),
            "accept_unvalidated": ("Onceden tam perspektif modeli yoktu; bu cizgiyle kuruldu. Karsilastirma "
                                   "yapilamadi (bagimsiz dogrulama yok)."),
            "inconsistent": f"[!] Bu cizgi mevcut {fn} dogrultusuyla tutarsiz gorunuyor.",
            "worse": "[!] Bu cizgi dogrulama olcutlerini kotulestiriyor.",
            "rejected_by_validation": (f"[!] Bu cizgi mevcut {fn} dogrultusuyla tutarsiz; bagimsiz veri ESKI "
                                       f"modeli destekliyor."),
            "no_model": "Bu cizgiyle de tam perspektif modeli kurulamiyor (diger yonde yeterli kanit yok).",
        }[a["verdict"]]
        src = self.HELPER_SOURCE_LABELS.get(hl.get("source"), hl.get("source"))
        lines = [f"{fn} yardimci cizgisi {hl['id']} ({src})", verdict_txt]
        if hl.get("note"):
            lines.append(f"({hl['note']})")
        if a["z_before"] is not None:
            lines.append(f"Mevcut {fn} yonune sapma: {a['theta_before']:.2f}° (z={a['z_before']:.1f}; "
                         f"3'un uzeri tutarsiz sayilir)")
        b, af = a["before"], a["after"]

        def f(x, fmt="{:.3f}"):
            return fmt.format(x) if x is not None else "N/A"

        def pct(x):
            return f"%{x * 100:.1f}" if x is not None else "N/A"

        if af is not None:
            bb = b or {}
            lines += ["",
                      f"VP yon belirsizligi ({fn}):  once {f(bb.get(f'vp_unc_deg_{fam}'))}°  ->  "
                      f"sonra {f(af[f'vp_unc_deg_{fam}'])}°",
                      f"Bagimsiz aci kalintisi (hold-out RMS z):  once {f(bb.get(f'holdout_rms_z_{fam}'), '{:.2f}')}"
                      f"  ->  sonra {f(af[f'holdout_rms_z_{fam}'], '{:.2f}')}",
                      f"Uzamsal kapsama (dik yayilim):  once {pct(bb.get(f'spatial_{fam}'))}  ->  "
                      f"sonra {pct(af[f'spatial_{fam}'])}",
                      f"Uzak bolge olcek belirsizligi (1-sigma):  once {pct(bb.get('scale_unc_far'))}  ->  "
                      f"sonra {pct(af['scale_unc_far'])}"]
            if af.get("known_length_rel_err") is not None:
                lines.append(f"Bilinen uzunluk hatasi:  once {pct(bb.get('known_length_rel_err'))}  ->  "
                             f"sonra {pct(af['known_length_rel_err'])}")
            lines.append(f"Guven:  once {bb.get('confidence', 'N/A')}  ->  sonra {af['confidence']}")
        return "\n".join(lines)

    def _refresh_helper_tree(self):
        if not hasattr(self, "helper_tree"):
            return
        self.helper_tree.delete(*self.helper_tree.get_children())
        for hl in self.helper_lines:
            fam = FAMILY_NAMES.get(hl["family"], "?")
            st = self.helper_status.get(hl["id"])
            if hl["family"] not in ("ab", "ac"):
                status = "yon atanmadi (kullanilmiyor)"
            elif st is None:
                status = "-"
            elif not st.get("inlier", True):
                status = f"[!] aykiri (z={st['z']:.1f}) kullanilmadi"
            elif st.get("loo_z") is not None:
                status = f"bagimsiz z={st['loo_z']:.1f}" + ("  [!] tutarsiz" if st["loo_z"] > VP_GATE_Z else "")
            else:
                status = f"z={st['z']:.1f} (bagimsiz dogrulama yok)"
            self.helper_tree.insert("", "end", iid=hl["id"], values=(
                hl["id"], fam, self.HELPER_SOURCE_LABELS.get(hl.get("source"), hl.get("source")),
                hl.get("anchor_label") or "-", status))
        if self._selected_helper_id and self.helper_tree.exists(self._selected_helper_id):
            self.helper_tree.selection_set(self._selected_helper_id)

    def _on_helper_tree_select(self, event=None):
        sel = self.helper_tree.selection()
        new = sel[0] if sel else None
        if new != self._selected_helper_id:
            self._selected_helper_id = new
            self._redraw()

    def _selected_helper(self):
        sel = self.helper_tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Once listeden bir yardimci cizgi secin.")
            return None
        return next((h for h in self.helper_lines if h["id"] == sel[0]), None)

    def delete_selected_helper(self):
        hl = self._selected_helper()
        if hl is None:
            return
        self.helper_lines = [h for h in self.helper_lines if h["id"] != hl["id"]]
        if hl["id"] in ("P-AB", "P-AC"):
            for cb in (self.abc_helper_ab_combos if hl["id"] == "P-AB" else self.abc_helper_ac_combos):
                cb.set("")
        self._selected_helper_id = None
        self._vp_stage_cache = (None, None)
        self._refresh_helper_tree()
        self._try_auto_compute_plane()
        self.status_var.set(f"{hl['id']} silindi.")

    def set_selected_helper_family(self, family):
        hl = self._selected_helper()
        if hl is None or hl["family"] == family:
            return
        hl["family"] = family
        hl["note"] = (hl.get("note", "") + " | yon kullanici tarafindan degistirildi").strip(" |")
        self._vp_stage_cache = (None, None)
        self._try_auto_compute_plane()
        self._refresh_helper_tree()
        self.status_var.set(f"{hl['id']} artik {FAMILY_NAMES[family]} yonunde.")

    def suggest_selected_helper_family(self):
        hl = self._selected_helper()
        if hl is None:
            return
        inputs = self._current_abc_inputs()
        if inputs is None:
            messagebox.showinfo("Bilgi", "Oneri icin once referansi (A, B, C ve uzunluklar) tamamlayin.")
            return
        others = [h for h in self.helper_lines if h["id"] != hl["id"]]
        img_size = (self.pil_img.width, self.pil_img.height)
        obs_ab, obs_ac = self._build_family_observations(inputs, helpers=others)
        res = compute_metric_homography_from_observations(
            inputs["A"], inputs["B"], inputs["C"], inputs["ab_m"], inputs["ac_m"], inputs["angle_deg"],
            obs_ab, obs_ac, img_size=img_size)
        fam, zs = suggest_line_family(self._helper_to_observation(hl), res)
        detail = (f"AB yonune sapma z={zs['ab']:.1f}, AC yonune z={zs['ac']:.1f}." if len(zs) == 2
                  else "Diger kanitla perspektif modeli kurulamadi.")
        if fam is None:
            messagebox.showinfo("Yon belirsiz", "Yardimci cizginin yonu belirsiz. AB veya AC olarak secin.\n\n"
                                                + detail)
            return
        c = self._choice_dialog("Yon onerisi", f"Oneri: {FAMILY_NAMES[fam]}.\n{detail}\n\nUygulansin mi?",
                                [("yes", "Uygula"), ("no", "Vazgec")], default="yes")
        if c == "yes":
            self.set_selected_helper_family(fam)

    def _draw_helper_lines(self, draw, sc, width=2, font=None, dash=10, gap=6):
        cap = self.helper_capture
        if cap is not None and cap["points"]:
            x, y = sc(cap["points"][0])
            col = HELPER_COLORS.get(cap["family"], HELPER_COLORS["auto"])
            draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=col, width=3)
        if not self.show_helpers_var.get():
            return
        for hl in self.helper_lines:
            p, q = sc(hl["p1"]), sc(hl["p2"])
            col = HELPER_COLORS.get(hl["family"], HELPER_COLORS["auto"])
            st = self.helper_status.get(hl["id"]) or {}
            bad = (st.get("inlier") is False) or (st.get("loo_z") is not None and st["loo_z"] > VP_GATE_Z)
            w = width
            if hl["id"] == self._selected_helper_id:
                draw.line([p, q], fill=(255, 255, 255), width=width + 4)
                w = width + 1
            _draw_dashed_line(draw, p, q, col, w, dash, gap)
            for e, other in ((p, q), (q, p)):
                ux, uy = other[0] - e[0], other[1] - e[1]
                n = math.hypot(ux, uy) or 1.0
                tx, ty = -uy / n * 5 * w / 2, ux / n * 5 * w / 2
                draw.line([(e[0] - tx, e[1] - ty), (e[0] + tx, e[1] + ty)], fill=col, width=w)
            label = f"{FAMILY_NAMES.get(hl['family'], 'yonsuz')}-{hl['id']}" + (" !" if bad else "")
            mid = ((p[0] + q[0]) / 2 + 6, (p[1] + q[1]) / 2 + 4)
            draw.text(mid, label, fill=HELPER_WARN_COLOR if bad else col, font=font or self.font_small,
                      stroke_width=2, stroke_fill=(0, 0, 0))

    # ---------- Kenar Hizalama (subpixel) ----------

    def toggle_edge_mode(self):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        self.edge_mode = not self.edge_mode
        if self.edge_mode and self.line_calib_mode:
            self.line_calib_mode = False
            self.line_calib_current = []
            self.line_calib_btn.config(text="Duz Kenar Modu: KAPALI")
        self.edge_mode_btn.config(text=f"Kenar Hizalama Modu: {'ACIK' if self.edge_mode else 'KAPALI'}")
        if not self.edge_mode:
            self.edge_rough_points = []
        self._redraw()
        if self.edge_mode:
            self.status_var.set("Kenar Hizalama acik: kenar boyunca 2+ kaba nokta tiklayin.")

    def undo_edge_rough_point(self):
        if self.edge_rough_points:
            self.edge_rough_points.pop()
            self._redraw()

    def finalize_edge_alignment(self):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        if len(self.edge_rough_points) < 2:
            messagebox.showerror("Hata", "Once kenar boyunca en az 2 kaba nokta tiklayin "
                                          "(Kenar Hizalama Modunu acin).")
            return

        gray = np.array(self.pil_img.convert("L"))
        try:
            _, _, _, end1, end2 = refine_edge_points(gray, self.edge_rough_points)
        except Exception as e:
            messagebox.showerror("Hata", f"Kenar hizalanamadi: {e}")
            return

        existing = {p["label"] for p in self.points}
        new_points = []
        for i, pt in enumerate((end1, end2), start=1):
            suggestion = chr(ord('A') + len(self.points) + i - 1) if len(self.points) + i <= 26 \
                else f"P{len(self.points) + i}"
            while suggestion in existing:
                suggestion = suggestion + "'"
            label = simpledialog.askstring(
                "Nokta Etiketi", f"Hizalanmis kenarin {i}. uc noktasi icin bir etiket girin:",
                initialvalue=suggestion, parent=self)
            if not label:
                messagebox.showinfo("Iptal", "Kenar hizalama iptal edildi, nokta eklenmedi.")
                return
            if label in existing or label in [p["label"] for p in new_points]:
                messagebox.showerror("Hata", f"'{label}' etiketi zaten kullaniliyor. Tekrar deneyin.")
                return
            new_points.append({"label": label, "x": pt[0], "y": pt[1], "source": "subpixel_edge"})

        self.points.extend(new_points)
        self.edge_rough_points = []
        self._redraw()
        self._refresh_all_display()
        self.status_var.set(f"Kenar hizalandi: '{new_points[0]['label']}' ve "
                             f"'{new_points[1]['label']}' eklendi (subpixel hassasiyette).")

    # ---------- Noktalar paneli ----------

    def _refresh_points_tree(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.points:
            self.tree.insert("", "end", iid=p["label"], values=(p["label"], f"{p['x']:.0f}, {p['y']:.0f}"))

    def delete_point(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Once listeden bir nokta secin.")
            return
        label = sel[0]
        self.points = [p for p in self.points if p["label"] != label]
        self._remove_references_to(label)
        self._refresh_all_display()
        self._redraw()

    def _refresh_combos(self):
        labels = [p["label"] for p in self.points]
        self.combo_a["values"] = labels
        self.combo_b["values"] = labels
        self.combo_c["values"] = ("",) + tuple(labels)
        for cb in self.corner_combos:
            cb["values"] = labels
        for cb in self.tri_combos:
            cb["values"] = labels
        self.coords_point_combo["values"] = labels
        for cb in self.abc_combos:
            cb["values"] = labels
        for cb in self.abc_helper_ab_combos:
            cb["values"] = labels
        for cb in self.abc_helper_ac_combos:
            cb["values"] = labels

    def _on_unit_change(self, event=None):
        """Birim (m/cm/mm/...) degistiginde, Genislik/Yukseklik kutularina
        YAZILMIS SAYILARI, GERCEK ANLAMLARINI koruyacak sekilde yeniden
        yazar. ONEMLI: bu donusum olmadan, ornegin '3' yazip birimi
        'm'den 'cm'ye degistirmek, ayni '3' rakamini sessizce 100 kat
        farkli bir uzunluga (3 m -> 3 cm) donusturur ve duzlem tamamen
        yanlis hesaplanir - bu tam da yasanan '200 birim fark' turu
        hatalarin sebebidir."""
        old_unit = self._last_unit
        new_unit = self.unit_var.get()
        if old_unit != new_unit:
            for entry in (self.plane_width_entry, self.plane_height_entry, *self.tri_len_entries,
                          self.query_gt_entry, self.coords_x_entry, self.coords_y_entry,
                          *self.abc_len_entries):
                raw = entry.get().strip()
                if not raw:
                    continue
                try:
                    val = float(raw.replace(",", "."))
                except ValueError:
                    continue
                meters = to_meters(val, old_unit)
                new_val = from_meters(meters, new_unit)
                entry.delete(0, "end")
                entry.insert(0, f"{new_val:.4f}")
        self._last_unit = new_unit
        self._try_auto_compute_plane()
        self._refresh_all_display()

    # ---------- N-nokta (gercek duzlem koordinati) referans satirlari ----------

    def _refresh_coords_tree(self):
        self.coords_tree.delete(*self.coords_tree.get_children())
        for r in self.coords_rows:
            self.coords_tree.insert("", "end", values=(
                r["label"], self._fmt(r["x_m"]), self._fmt(r["y_m"])))

    def _add_coords_row(self):
        label = self.coords_point_combo.get()
        if not label:
            messagebox.showerror("Hata", "Bir nokta secin.")
            return
        if any(r["label"] == label for r in self.coords_rows):
            messagebox.showerror("Hata", f"'{label}' zaten eklendi. Once silin, sonra tekrar ekleyin.")
            return
        x_m = self._peek_coord(self.coords_x_entry)
        y_m = self._peek_coord(self.coords_y_entry)
        if x_m is None or y_m is None:
            messagebox.showerror("Hata", "Gercek X ve Y icin sayisal deger girin (0 ve negatif de olabilir).")
            return
        self.coords_rows.append({"label": label, "x_m": x_m, "y_m": y_m})
        self.coords_x_entry.delete(0, "end")
        self.coords_y_entry.delete(0, "end")
        self._refresh_coords_tree()
        self._try_auto_compute_plane()

    def _delete_coords_row(self):
        sel = self.coords_tree.selection()
        if not sel:
            return
        idx = self.coords_tree.index(sel[0])
        del self.coords_rows[idx]
        self._refresh_coords_tree()
        self._try_auto_compute_plane()

    # ---------- Duzlem (egim duzeltmesi) ----------

    def _peek_len(self, entry):
        """Bir Entry'den, hata mesaji GOSTERMEDEN, sayisal bir uzunluguu
        (metre cinsinden) okumaya calisir. Gecersiz/bos ise None doner -
        canli onizleme sirasinda yazarken gecici gecersiz durumlar
        rahatsiz edici hata kutusu acmasin diye."""
        raw = entry.get().strip()
        if not raw:
            return None
        try:
            val = float(raw.replace(",", "."))
        except ValueError:
            return None
        if val <= 0:
            return None
        return to_meters(val, self.unit_var.get())

    def _peek_coord(self, entry):
        """_peek_len ile ayni, ama duzlem KOORDINATI icin - 0 ve negatif
        degerler de gecerlidir (bir referans noktasi orijin (0,0) olabilir,
        ya da baska bir noktaya gore negatif yonde olabilir)."""
        raw = entry.get().strip()
        if not raw:
            return None
        try:
            val = float(raw.replace(",", "."))
        except ValueError:
            return None
        return to_meters(val, self.unit_var.get())

    def _on_corner_combo_change(self, event=None):
        """Bir Kose/Nokta kutusunun secimi degistiginde cagrilir. ONEMLI:
        uzunluk kutularindaki sayilari BURADA temizliyoruz - aksi halde,
        ornegin Nokta3'u farkli bir noktaya degistirdiginizde, ESKI kenar
        icin girilmis uzunluk sessizce YENI (farkli) kenara uygulanir ve
        tamamen yanlis (genelde cok sismis/kucuk) bir sonuc uretir. Bu,
        daha once fotograf/birim degisince yasanan 'eski deger sessizce
        yeniden kullanilir' hatasinin ayni sinifidan bir baska ornegidir."""
        self.plane_width_entry.delete(0, "end")
        self.plane_height_entry.delete(0, "end")
        for e in self.tri_len_entries:
            e.delete(0, "end")
        for e in self.abc_len_entries:
            e.delete(0, "end")
        self.abc_angle_entry.delete(0, "end")
        self.status_var.set("Referans noktasi degisti - uzunluklari tekrar girin.")
        self._try_auto_compute_plane()

    def _apply_ref_mode(self):
        # TEK gorunur akis: 3 Nokta + 2 Uzunluk ("Referans Olustur"). Eski
        # afin(3-nokta)/4-kose/N-nokta panelleri kod icinde korunuyor
        # (regresyon testleri/olasi arka plan kullanimi icin) ama ASLA
        # goruntulenmiyor - kullaniciya birden fazla yontem arasinda secim
        # yaptirmiyoruz.
        mode = self.ref_mode_var.get()
        self.affine3_frame.pack_forget()
        self.quad4_frame.pack_forget()
        self.coords_frame.pack_forget()
        self.abc2len_frame.pack_forget()
        if mode == "affine3":
            self.affine3_frame.pack(fill="x", pady=(0, 8), after=self.pts_frame)
        elif mode == "quad4":
            self.quad4_frame.pack(fill="x", pady=(0, 8), after=self.pts_frame)
        elif mode == "coords":
            self.coords_frame.pack(fill="x", pady=(0, 8), after=self.pts_frame)
        else:
            self.abc2len_frame.pack(fill="x", pady=(0, 8), after=self.pts_frame)
        self.plane_H = None
        self.plane_Hinv = None
        self.plane_corners = None
        self.plane_calibrated = False
        self.last_results = {}
        self._update_plane_status()
        self._redraw()

    def _try_auto_compute_plane(self, event=None):
        """Kose kutulari/uzunluk alanlari her degistiginde otomatik cagrilir.
        4 kose secilir secilmez uygulama, o noktalardan iki KACIS NOKTASI
        (vanishing point) bulup dikdortgenin GERCEK SEKLINI (aci/oran
        olarak) matematiksel olarak cikarir - bu sayede ölçek icin sadece
        TEK bir bilinen uzunluk yeterlidir (Genislik VEYA Yukseklik/Egim).
        Ikisi de girilirse tutarliliklari karsilastirilir. Bu goruntude
        yeterli perspektif yoksa (kacis noktasi bulunamazsa) eski yonteme
        donulur ve o zaman iki uzunluk da gerekir."""
        self._recompute_plane(silent=True)

    def compute_plane(self):
        """Elle 'Duzlemi Hesapla' benzeri bir eylem icin (artik cogunlukla
        otomatik tetiklenir) - basarisiz olursa nedenini acikca gosterir."""
        self._recompute_plane(silent=False)

    def _recompute_plane(self, silent):
        if self.pil_img is None:
            return
        mode = self.ref_mode_var.get()
        if mode == "affine3":
            self._recompute_plane_affine3(silent)
        elif mode == "quad4":
            self._recompute_plane_quad4(silent)
        elif mode == "coords":
            self._recompute_plane_coords(silent)
        else:
            self._recompute_plane_abc2len(silent)

    def _recompute_plane_affine3(self, silent):
        """3 referans noktasi + uzunluklar -> afin donusum.
        - 1-2 VE 2-3 uzunlugu verilip 1-3 verilMEMISse: Nokta 2'de 90
          derece (dik aci) varsayilir (SAS) - hizli/kolay, 1-3'u olcmenize
          gerek yok.
        - Ucu de verilirse: HICBIR ACI VARSAYIMI YAPILMADAN (SSS, kosinus
          teoremi) tam sekil kurulur - en dogru sonuc, ama Nokta 2'deki
          acinin gercekte 90 derece olmasi gerekmez."""
        labels = [cb.get() for cb in self.tri_combos]
        if any(not lb for lb in labels) or len(set(labels)) != 3:
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", "3 nokta icin de farkli bir nokta secmelisiniz.")
            return

        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        img_pts = [lookup[lb] for lb in labels]

        min_angle = triangle_min_angle_deg(*img_pts)
        if min_angle < MIN_TRIANGLE_ANGLE_DEG:
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            msg = (f"Secilen 3 nokta fotografta neredeyse ayni dogru uzerinde "
                   f"(en kucuk ic aci sadece {min_angle:.1f} derece). Bu, hesaplamayi "
                   f"sayisal olarak COK KARARSIZ yapar - kucuk bir tiklama sapmasi bile "
                   f"tamamen yanlis/saçma bir sonuc uretebilir (sizin gordugunuz "
                   f"'ters yonde yukselen izgara' ve 'cok kotu tahmin' TAM OLARAK bu belirtidir). "
                   f"Lutfen birbirinden daha 'yayilmis', gercek bir ucgene benzeyen 3 nokta secin "
                   f"(ör. ayni kenar uzerinde 3 nokta degil, farkli kenarlardan/koselerden).")
            self.plane_status_var.set(msg)
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", msg)
            return

        d12 = self._peek_len(self.tri_len_entries[0])
        d23 = self._peek_len(self.tri_len_entries[1])
        d13 = self._peek_len(self.tri_len_entries[2])

        if d12 is not None and d23 is not None and d13 is not None:
            try:
                world_pts = triangle_from_sides(d12, d23, d13)
            except ValueError as e:
                if not silent:
                    messagebox.showerror("Hata", str(e))
                self._build_plane(labels, img_pts, None, None, None, silent, False, str(e))
                return
            note = "3 referans uzunluktan (SSS) afin donusum kullanildi - aci varsayimi yok."
            self._build_plane(labels, img_pts, world_pts, d12, d23, silent, True, note)
            return

        if d12 is not None and d23 is not None:
            # 1-3 girilmedi - Nokta 2'de dik aci (90 derece) varsayilir.
            world_pts = [(0.0, 0.0), (d12, 0.0), (d12, d23)]
            note = "2 uzunluktan hesaplandi (Nokta 2'de 90 derece varsayildi). Daha kesin sonuc icin 1-3 uzunlugunu da girebilirsiniz."
            self._build_plane(labels, img_pts, world_pts, d12, d23, silent, True, note)
            return

        # Henuz yeterli uzunluk girilmedi - sadece kaba tiklanan
        # noktalarin PIKSEL oranlarindan bir sekil onizlemesi goster.
        px12 = dist(img_pts[0], img_pts[1])
        px23 = dist(img_pts[1], img_pts[2])
        px13 = dist(img_pts[0], img_pts[2])
        if px12 <= 1e-6:
            self._build_plane(labels, img_pts, None, None, None, silent, False,
                               "Nokta 1 ve 2 ayni yerde olamaz.")
            return
        scale_preview = 3.0 / px12
        try:
            world_pts = triangle_from_sides(px12 * scale_preview, px23 * scale_preview, px13 * scale_preview)
        except ValueError:
            world_pts = None
        note = ("On izleme: sekil piksel oranlarindan gosteriliyor. Olcek icin "
                "en az 1-2 VE 2-3 uzunluklarini girin.")
        width_m = px12 * scale_preview
        height_m = px23 * scale_preview
        self._build_plane(labels, img_pts, world_pts, width_m, height_m, silent, False, note)

    def _recompute_plane_quad4(self, silent):
        labels = [cb.get() for cb in self.corner_combos]
        if any(not lb for lb in labels) or len(set(labels)) != 4:
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", "4 kose icin de farkli bir nokta secmelisiniz.")
            return

        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        img_pts = [lookup[lb] for lb in labels]
        img_w, img_h = self.pil_img.size

        if quad_is_self_intersecting(*img_pts):
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            msg = ("Secilen 4 kose, 1->2->3->4 sirasiyla KENDI KENDINI KESEN "
                   "('kelebek' seklinde) bir dortgen olusturuyor - kosegen atlanmis "
                   "olabilir. 'Genislik' ve 'Yukseklik' artik gercek kenarlara degil "
                   "kosegenlere karsilik gelir ve sonuc anlamsiz cikar. Lutfen "
                   "koseleri dortgenin cevresi boyunca SIRAYLA (saat yonunde veya "
                   "tersi, ama atlamadan) secin.")
            self.plane_status_var.set(msg)
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", msg)
            return

        w_m = self._peek_len(self.plane_width_entry)
        h_m = self._peek_len(self.plane_height_entry)

        note = ""

        if w_m is not None and h_m is not None:
            # Iki uzunluk da bilindiginde HICBIR TAHMINE/KACIS NOKTASINA
            # gerek yok - dogrudan TAM DIKDORTGEN yontemi kullanilir (4
            # kose, tam olarak bu iki uzunluga sahip bir dikdortgene
            # esleniyor). Bu, sifir aspect-ratio belirsizligi demektir ve
            # HER ZAMAN tek-referans (kacis noktasi tahmini) yontemden
            # daha dogrudur. ONEMLI DUZELTME: eskiden burada iki uzunluk
            # da girilmis olsa bile kacis noktasindan tahmin edilen sekil
            # kullanilip iki uzunluk sadece "ortalama olcek" olarak
            # karistiriliyordu - bu da koselerden uzaklastikca buyuyen
            # sistematik hataya yol aciyordu. Artik iki uzunluk varsa
            # dogrudan ve tam kullaniliyor.
            world_pts = [(0.0, 0.0), (w_m, 0.0), (w_m, h_m), (0.0, h_m)]
            calibrated = True
            note = "Iki uzunluk da girildi - tam dikdortgen yontemi kullanildi (tahmin yok, en dogru sonuc)."

            # TUTARLILIK KONTROLU: bu yontem, 4 kosenin GERCEKTE tam bir
            # dikdortgen (90 derece acili) oldugunu VARSAYAR - tikladiginiz
            # dortgenin gercek seklini kontrol etmez. Fiziksel referans tam
            # dikdortgen degilse (ör. cerceve hafif carpiksa) ya da kose
            # tiklamalari kaymissa, bu varsayim referanstan uzaklastikca
            # BUYUYEN bir sistematik hataya yol acar. metric_rectify_quad,
            # kacis noktalarindan BAGIMSIZ bir en/boy orani tahmini yapar;
            # bu tahmin girilen Genislik/Yukseklik oranindan onemli olcude
            # sapiyorsa, referansin gercekten dikdortgen olmadigina dair
            # somut bir isarettir. (Sentetik dogrulama: bu iki oran arasindaki
            # fark ile asagi akan olcum hatasi arasinda guclu bir korelasyon
            # var - Spearman rho=0.61, n=968 sahne, bkz. regression_suite.py;
            # dogru referanslarda bu fark hep <%1.3 kaliyor.)
            raw_check = metric_rectify_quad(img_pts, img_w, img_h)
            if raw_check is not None:
                w_chk = dist(raw_check[0], raw_check[1])
                h_chk = dist(raw_check[1], raw_check[2])
                if w_chk > 1e-9 and h_chk > 1e-9:
                    entered_aspect = w_m / h_m
                    est_aspect = w_chk / h_chk
                    aspect_diff_pct = abs(est_aspect - entered_aspect) / entered_aspect * 100
                    if aspect_diff_pct > 3.0:
                        note += (f"\n[!] Tutarlilik uyarisi: kacis noktalarindan bagimsiz olarak "
                                 f"tahmin edilen en/boy orani, girdiginiz Genislik/Yukseklik oranindan "
                                 f"~%{aspect_diff_pct:.1f} farkli. Bu, secili 4 kosenin fiziksel olarak "
                                 f"tam dikdortgen olmayabilecegini (ya da kose tiklamalarindan birinin "
                                 f"kaymis olabilecegini) gosterir - sonuc, ozellikle bu referanstan uzak "
                                 f"bolgelerde, sistematik olarak yanlis olabilir. Koseleri kenar "
                                 f"cizgilerinin gercek kesisim noktalarina daha hassas tiklamayi veya "
                                 f"fiziksel olarak daha 'kare' bir referans secmeyi deneyin.")
                    elif aspect_diff_pct > 1.5:
                        note += (f"\n(bilgi: kacis noktasi tahmini ile girilen oran arasinda ~%"
                                 f"{aspect_diff_pct:.1f} fark var - gurultu sinirinin biraz ustunde, "
                                 f"izlemeye deger.)")
        else:
            raw = metric_rectify_quad(img_pts, img_w, img_h)
            if raw is not None:
                w_raw, h_raw = dist(raw[0], raw[1]), dist(raw[1], raw[2])
                if w_m is not None and w_raw > 1e-9:
                    s = w_m / w_raw
                    calibrated = True
                    note = "Otomatik egim tespiti - TEK referans uzunluktan (Genislik) hesaplandi."
                elif h_m is not None and h_raw > 1e-9:
                    s = h_m / h_raw
                    calibrated = True
                    note = "Otomatik egim tespiti - TEK referans uzunluktan (Yukseklik/Egim) hesaplandi."
                else:
                    s = 3.0 / max(w_raw, 1e-9)
                    calibrated = False
                    note = "On izleme: sekil/egim otomatik tespit edildi. Olcek icin Genislik VEYA Yukseklik/Egim uzunluklarindan birini girin."
                world_pts = [(u * s, v * s) for u, v in raw]
            else:
                # Bu acidan/yonden kacis noktasi bulunamadi (perspektif cok
                # az - ör. neredeyse tam karsidan cekim). Otomatik tek-uzunluk
                # tespiti guvenilir degil ve henuz tek uzunluk da girilmemis.
                pts = img_pts
                w_px = (dist(pts[0], pts[1]) + dist(pts[3], pts[2])) / 2
                h_px = (dist(pts[0], pts[3]) + dist(pts[1], pts[2])) / 2
                aspect = w_px / h_px if h_px > 1e-6 else 1.0
                width_m = 3.0
                height_m = 3.0 / aspect if aspect > 1e-6 else 3.0
                world_pts = [(0.0, 0.0), (width_m, 0.0), (width_m, height_m), (0.0, height_m)]
                calibrated = False
                note = ("On izleme. Bu goruntude otomatik egim tespiti yapilamadigi icin "
                        "olcum yapabilmeniz icin HEM Genislik HEM Yukseklik/Egim uzunluklarini girmeniz gerekiyor.")

        width_m = dist(world_pts[0], world_pts[1])
        height_m = dist(world_pts[1], world_pts[2])
        self._build_plane(labels, img_pts, world_pts, width_m, height_m, silent, calibrated, note)

    def _recompute_plane_coords(self, silent):
        """N-nokta (gercek duzlem koordinati) referans modu: her nokta icin
        kullanicinin dogrudan girdigi gercek (x,y) duzlem koordinati
        kullanilir - quad4'un aksine HICBIR SEKIL (dikdortgen vb.) VARSAYILMAZ.
        En az 4 nokta gerekir; 5+ girilirse compute_homography zaten en
        kucuk kareler ile cozer (bkz. fonksiyonun docstring'i). Bu, orijinal
        measure_from_photo.py CLI script'inin yaklasimiyla ayni ve genel
        olarak en saglam yontemdir - cunku referansi TEK KUCUK BIR
        DIKDORTGENE degil, kullanicinin bildigi HER YERE yayabilir, bu da
        kucuk bir referanstan uzak bolgelerde buyuyen ekstrapolasyon
        hatasini dogrudan azaltir (bkz. regression_suite.py genel testleri)."""
        if len(self.coords_rows) < 4:
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", f"En az 4 nokta gerekli (su an {len(self.coords_rows)}).")
            return

        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        labels = [r["label"] for r in self.coords_rows]
        if any(lb not in lookup for lb in labels):
            self.plane_H = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", "Bazi referans noktalari artik mevcut degil.")
            return

        img_pts = [lookup[lb] for lb in labels]
        world_pts = [(r["x_m"], r["y_m"]) for r in self.coords_rows]

        try:
            H = compute_homography(img_pts, world_pts)
            # ONEMLI: Hinv'i AYRI bir DLT ile degil, H'nin TAM matris
            # tersini alarak kuruyoruz. N>4 (en kucuk kareler) durumunda
            # world->image ve image->world yonlerinde AYRI AYRI fit edilen
            # iki homografi, gurultu varliginda BIRBIRININ TAM tersi
            # OLMAYABILIR (iki farkli optimizasyon problemi cozuluyor) -
            # bu, ör. izgara cizimi (Hinv kullanir) ile olcum (H kullanir)
            # arasinda kucuk ama gercek bir tutarsizliga yol acabilirdi.
            # np.linalg.inv(H) matematiksel olarak GARANTILI tam ters.
            Hinv = np.linalg.inv(H)
        except (ValueError, np.linalg.LinAlgError) as e:
            self.plane_H = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", f"Duzlem hesaplanamadi: {e}\n"
                                              "(noktalar ayni dogru uzerinde olmamali.)")
            return

        # Reprojeksiyon hatasi: her referans noktasinin H ile geri hesaplanan
        # dunya konumu, GIRILEN gercek konumdan ne kadar sapiyor? Tam 4
        # nokta icin bu HER ZAMAN ~0'dir (DLT tam cozer); 5+ nokta icin ise
        # en-kucuk-kareler fit'inin ne kadar TUTARLI oldugunu - yani
        # noktalarin gercekten ayni duzlemde olup olmadigini / tiklamalarin
        # ne kadar hassas oldugunu - gosteren somut, sayisal bir kalite
        # olcusudur (orijinal CLI script'teki fikirle ayni).
        errs = []
        for lb, ip, wp in zip(labels, img_pts, world_pts):
            est = apply_transform(H, ip)
            errs.append((lb, dist(est, wp)))
        max_err = max(e for _, e in errs)
        note_lines = ["Referans noktasi uyum kontrolu (fit ne kadar iyi):"]
        for lb, e in errs:
            note_lines.append(f"  {lb}: {self._fmt(e)} hata")
        if len(labels) > 4 and max_err > 0.02:
            note_lines.append(f"[!] En kucuk kareler fit'i {self._fmt(max_err)} kadar hata birakti - "
                               f"bazi noktalar ayni duzlemde olmayabilir ya da tiklamalar hassas degil.")
        note = "\n".join(note_lines)

        self.plane_corners = labels
        self.plane_width_m = dist(world_pts[0], world_pts[1])
        self.plane_height_m = dist(world_pts[1], world_pts[2]) if len(world_pts) > 2 else self.plane_width_m
        self.plane_H = H
        self.plane_Hinv = Hinv
        self.plane_img_pts = [tuple(p) for p in img_pts]
        self.plane_world_pts = [tuple(p) for p in world_pts]
        self.plane_calibrated = True
        self.plane_origin = np.array(world_pts[0], dtype=np.float64)
        self.plane_axis1 = np.array(world_pts[1], dtype=np.float64) - self.plane_origin
        self.plane_axis2 = (np.array(world_pts[2], dtype=np.float64) - np.array(world_pts[1], dtype=np.float64)
                             if len(world_pts) > 2 else np.array([-self.plane_axis1[1], self.plane_axis1[0]]))
        self._update_plane_status(note)
        self.last_results = {}
        self._redraw()
        if not silent:
            messagebox.showinfo("Duzlem hazir", note)

    def _get_auto_detected_lines(self):
        """Aktif fotografta OTOMATIK tespit edilen dogru parcalarini (bkz.
        detect_line_segments) DONDURUR - fotograf basina BIR KEZ hesaplanir
        ve onbelleklenir (LSD/Hough her tus vurusunda yeniden calismasin -
        bu maliyetli bir islemdir, referans alanlarina yazarken canli
        onizleme COK YAVASLARDI)."""
        if self.pil_img is None:
            return []
        cache_key = id(self.pil_img)
        if getattr(self, "_auto_lines_cache_key", None) != cache_key:
            try:
                gray = np.array(self.pil_img.convert("L"))
                self._auto_lines_cache = detect_line_segments(gray)
            except Exception:
                self._auto_lines_cache = []
            self._auto_lines_cache_key = cache_key
        return self._auto_lines_cache

    def _gather_auto_lines_for_direction(self, ref_dir_angle_deg, angle_tolerance_deg=35.0):
        """Onbelleklenmis otomatik-tespit cizgilerinden, KABACA (genis bir
        tolerans) referans yonune yakin acidaki adaylari filtreler. Bu SADECE
        bir ON-filtre - GERCEK dogrulama (bir kacis noktasiyla tutarli olup
        olmadigi) RANSAC asamasinda (_ransac_vanishing_point icinde,
        _resolve_vanishing_point tarafindan cagirilir) yapilir. Genis tolerans
        kasitli: guclu perspektifte GERCEKTEN ayni yondeki cizgiler, farkli
        konumlarda goruntude onemli olcude farkli acilarda gorunebilir."""
        candidates = []
        for p, q in self._get_auto_detected_lines():
            ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
            diff = abs(ang - ref_dir_angle_deg) % 180.0
            if diff > 90.0:
                diff = 180.0 - diff
            if diff <= angle_tolerance_deg:
                candidates.append((p, q))
        return candidates

    def _gather_extra_parallel_lines(self, lookup, baseline_kind, baseline_vp, ref_dir_angle_deg,
                                      exclude_pts):
        """SU ANA KADAR eklenmis olcum sorgularinin (self.queries) uc
        noktalari arasinda, AYNI GERCEK DUNYA YONUNE ait olabilecek
        kenarlari toplar - boylece kacis noktasi tahmini TEK bir yardimci
        cizgiye degil, mevcut TUM kanitlara dayanir.

        ONEMLI (duzeltme): eskiden bu fonksiyon sadece GORUNTU ACISI
        yakinligina (±10°) bakiyordu - ama GERCEK dunyada paralel iki
        cizgi, PERSPEKTIF altinda goruntude FARKLI yerel acilarda
        gorunebilir (bu, tam da kacis noktasi yakinsamasinin nedenidir).
        Acisi benzer diye ayni yonde saymak GEOMETRIK OLARAK YANLIS,
        acisi FARKLI diye ayni yonde OLMADIGINI da SOYLEMEZ.

        DOGRU KRITER: adayin GORUNTU CIZGISI, referans+yardimci cizginin
        ZATEN belirledigi (baseline) kacis noktasina ACISAL OLARAK
        tutarli mi (bkz. _angular_residual_deg)? ONEMLI: bu ESKIDEN
        piksel-mesafesi tabanli bir kriterdi (adayin dogrusunun VP'ye
        PIKSEL uzakligi) - ama VP UZAKTAYKEN (zayif perspektif, SIK
        rastlanan bir durum) bu metrik mesafeyle ORANTILI buyudugunden,
        GERCEK ama kucuk (elle tiklamadan kaynaklanan) bir aci sapmasi
        bile adayi 'aykiri deger' gibi gosteriyordu - bu oturumda
        sentetik click-noise testiyle SOMUT olarak tespit edilen GERCEK
        bir bug (bkz. _angular_residual_deg dokumantasyonu). Aci-tabanli
        kriter OLCEK-BAGIMSIZDIR. baseline_kind "near_infinity" ise
        (kacis noktasi pratikte sonsuzda - kanitlanmis), zaten aci testi
        kullanilir (asagida, ayri dalda)."""
        extra = []
        exclude_set = {tuple(p) for p in exclude_pts}
        for q in self.queries:
            a_lbl, b_lbl = q.get("a"), q.get("b")
            if a_lbl not in lookup or b_lbl not in lookup:
                continue
            p, qp = lookup[a_lbl], lookup[b_lbl]
            if p in exclude_set and qp in exclude_set:
                continue
            v = (qp[0] - p[0], qp[1] - p[1])
            length = math.hypot(*v)
            if length < 1e-6:
                continue

            if baseline_kind in _FINITE_KINDS and baseline_vp is not None:
                # Aday cizginin, bilinen kacis noktasina ACISAL tutarliligi
                # (bkz. yukaridaki docstring notu ve _angular_residual_deg).
                if _angular_residual_deg(p, qp, baseline_vp) <= VP_RANSAC_ANGLE_TOL_DEG:
                    extra.append((p, qp))
            else:
                # baseline "near_infinity" (ya da henuz bilinmiyor) - bu
                # durumda doğru test GORUNTU ACISI yakinligidir (yukaridaki
                # docstring'e bakin).
                ang = math.degrees(math.atan2(v[1], v[0]))
                diff = abs(ang - ref_dir_angle_deg) % 180.0
                if diff > 90.0:
                    diff = 180.0 - diff
                if diff <= 10.0:
                    extra.append((p, qp))
        return extra

    def _recompute_plane_abc2len(self, silent):
        """3 Nokta + 2 Uzunluk modu: A ortak kose, AB ve AC uzunluklari
        biliniyor. D otomatik olusturulur - eger fotografta AB ve AC
        yonlerinde birer YARDIMCI CIZGI (baska bir yerde gorunen, ayni
        dunya yonundeki gercek bir kenar) belirtilmisse GERCEK KACIS
        NOKTALARINDAN (tam projektif, dogru); belirtilmemisse - D'nin
        gercek konumu matematiksel olarak belirlenemeyecegi icin (bkz.
        compute_fourth_point_projective docstring) - mevcut 3-nokta
        AFIN yaklasimina ACIKCA belirtilerek geri donulur."""
        self.plane_strat_result = None  # her cagride SIFIRLA - eski bir hesaptan kalan STALE sonuc kalmasin
        labels = [cb.get() for cb in self.abc_combos]
        if any(not lb for lb in labels) or len(set(labels)) != 3:
            self.plane_H = None
            self.plane_Hinv = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", "A, B ve C icin farkli uc nokta secmelisiniz.")
            return

        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        lookup_source = {p["label"]: p.get("source", "manual") for p in self.points}
        A_lbl, B_lbl, C_lbl = labels
        A, B, C = lookup[A_lbl], lookup[B_lbl], lookup[C_lbl]

        min_angle = triangle_min_angle_deg(A, B, C)
        if min_angle < MIN_TRIANGLE_ANGLE_DEG:
            self.plane_H = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", f"A, B, C neredeyse ayni dogru uzerinde "
                                              f"(en kucuk ic aci {min_angle:.1f} derece) - "
                                              f"fit sayisal olarak kararsiz. Farkli noktalar secin.")
            return

        ab_m = self._peek_len(self.abc_len_entries[0])
        ac_m = self._peek_len(self.abc_len_entries[1])
        if ab_m is None or ac_m is None:
            self.plane_H = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", "AB ve AC icin gecerli (pozitif) uzunluk girin.")
            return

        if self.abc_right_angle_var.get():
            angle_deg = 90.0
        else:
            angle_raw = self.abc_angle_entry.get().strip()
            try:
                angle_deg = float(angle_raw.replace(",", "."))
            except ValueError:
                angle_deg = None
            if angle_deg is None or not (0 < angle_deg < 180):
                self.plane_H = None
                self.plane_corners = None
                self.plane_calibrated = False
                self._update_plane_status()
                self._redraw()
                if not silent:
                    messagebox.showerror("Hata", "Dikdortgen degilse A'daki gercek aciyi "
                                                  "(0-180 derece arasi) girin.")
                return
        angle_rad = math.radians(angle_deg)

        # YARDIMCI CIZGILER: tek veri modeli (self.helper_lines) - nokta
        # akisiyla eklenenler, bagimsiz kenarlar ve eski nokta-cifti
        # secimleri. Hepsi DOGRULANMIS gozlem olarak, referans A-B/A-C ve
        # dogrulanmamis adaylarla (otomatik cizgiler, olcum kenarlari)
        # birlikte gozlem-tabanli saglam VP kestiricisine girer.
        inputs = {"labels": labels, "A": A, "B": B, "C": C,
                  "sources": [lookup_source.get(lb, "manual") for lb in labels],
                  "ab_m": ab_m, "ac_m": ac_m, "angle_deg": angle_deg}
        obs_ab, obs_ac = self._build_family_observations(inputs)
        img_size = (self.pil_img.width, self.pil_img.height) if self.pil_img is not None else None
        vp_stage = self._vp_stage(A, obs_ab, obs_ac, img_size)
        self._update_helper_status(vp_stage)

        # Yedek (JOINT) rota icin eski bicimdeki girdiler - ayni yardimci cizgilerden.
        helpers_ab = [(tuple(h["p1"]), tuple(h["p2"])) for h in self.helper_lines if h["family"] == "ab"]
        helpers_ac = [(tuple(h["p1"]), tuple(h["p2"])) for h in self.helper_lines if h["family"] == "ac"]
        helper_ab = helpers_ab[0] if helpers_ab else None
        helper_ac = helpers_ac[0] if helpers_ac else None
        extra_ab, extra_ac = helpers_ab[1:], helpers_ac[1:]
        ang_ab_ref = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
        ang_ac_ref = math.degrees(math.atan2(C[1] - A[1], C[0] - A[0]))
        auto_ab = self._gather_auto_lines_for_direction(ang_ab_ref)
        auto_ac = self._gather_auto_lines_for_direction(ang_ac_ref)
        if vp_stage.get("ambiguous_families"):
            # Otomatik kanit belirsiz bulunduysa yedek rota da onu KULLANMAMALI
            # (ayni yanlis kumeyi baska bir yoldan secebilir).
            auto_ab, auto_ac = [], []

        world_A = (0.0, 0.0)
        world_B = (ab_m, 0.0)
        world_C = (ac_m * math.cos(angle_rad), ac_m * math.sin(angle_rad))
        world_D = (world_B[0] + world_C[0], world_B[1] + world_C[1])

        # ROUTE A: kacis noktasi/yardimci cizgi bile GEREKMEDEN, EXIF'ten
        # yaklasik K + 3 noktadan kamera pozu (SQPNP) ile D icin bir aday
        # bulmaya calisir. K yoksa ya da poz belirsizse (bkz.
        # compute_fourth_point_camera_pose dokumantasyonu) sessizce None
        # doner. ONEMLI (Bolum 8): bu aday ARTIK TEK BASINA H'yi belirlemez -
        # asagida compute_global_homography'ye BAGIMSIZ bir dorduncu nokta
        # GOZLEMI olarak verilir; nihai H yine de (varsa) VP/cizgi
        # kisitlariyla BIRLIKTE, TEK bir en-kucuk-kareler sisteminde cozulur.
        img_w = self.pil_img.width if self.pil_img is not None else None
        img_h = self.pil_img.height if self.pil_img is not None else None
        K_exif = (estimate_camera_intrinsics_from_exif(getattr(self, "photo_exif", None), img_w, img_h)
                  if img_w and img_h else None)
        camera_pose_seed = (compute_fourth_point_camera_pose(A, B, C, K_exif, ab_m, ac_m, angle_deg)
                             if K_exif is not None else None)
        # BOLUM 4: gercek bir kalibrasyon profili YOK (henuz uygulanmadi) -
        # K_exif varsa bile bu SADECE EXIF 35mm-esdegerinden yaklasik bir
        # baslangic tahmini, gercek olcum degil - durumu ACIKCA etiketle.
        self.plane_camera_status = "EXIF YAKLASIK" if K_exif is not None else "BILINMIYOR"

        # ANA YONTEM: kademeli (stratified) PROJEKTIF->AFIN->METRIK
        # rektifikasyon, gozlem tabanli (bkz.
        # compute_metric_homography_from_observations): v_AB, v_AC belirsizlik-
        # agirlikli ve dogrulanmis-kisitli saglam kestiriciden; l_inf = v_AB x
        # v_AC; metrik olcek A,B,C'den TAM. D HICBIR ASAMADA girdi degildir.
        # Karsilastirma olcumleri: tests/benchmark_helper_lines.py.
        self.plane_strat_result = compute_metric_homography_from_observations(
            A, B, C, ab_m, ac_m, angle_deg, img_size=img_size, stage=vp_stage,
            known_segments=self._known_segments())

        # JOINT rota (bir onceki mimari - A,B,C VE yon kisitlarini TEK
        # sistemde cozer, kamera pozunu ek nokta olarak katabilir) SADECE
        # kademeli cozucu YETERLI kanit bulamadiysa (ör. iki yonden birinde
        # HICBIR ikinci cizgi kaniti yoksa) YEDEK olarak denenir - bu,
        # Route A'nin (kamera pozu) hala katkida bulunabilmesini saglar
        # (kademeli cozucu camera_pose_seed KULLANMAZ, bkz. Bolum 20).
        point_sources_abc = [lookup_source.get(A_lbl, "manual"), lookup_source.get(B_lbl, "manual"),
                             lookup_source.get(C_lbl, "manual")]
        global_result = None
        if self.plane_strat_result is None:
            global_result = compute_global_homography(A, B, C, ab_m, ac_m, angle_deg,
                                                        helper_ab, helper_ac, extra_ab, extra_ac,
                                                        auto_ab, auto_ac, camera_pose_seed,
                                                        point_sources=point_sources_abc,
                                                        img_size=(img_w, img_h) if img_w and img_h else None)

        self.plane_vanishing_points = {"ab": None, "ac": None}
        self.plane_d_route = "affine_fallback"
        self.plane_line_residuals = {"ab": None, "ac": None}
        self.plane_point_reproj = None
        if self.plane_strat_result is not None:
            sr = self.plane_strat_result
            D_img = sr["D_img"]
            img_pts = [A, B, C, D_img]
            world_pts = [world_A, world_B, world_C, world_D]
            self.plane_H = sr["H"]
            self.plane_Hinv = sr["Hinv"]
            self.plane_model_type = "projective"
            self.plane_d_route = "stratified"

            note = self._stratified_note(sr)
        elif global_result is not None:
            D_img = global_result["D_img"]
            img_pts = [A, B, C, D_img]
            world_pts = [world_A, world_B, world_C, world_D]
            kind_ab, vp_ab = global_result["kind_ab"], global_result["vp_ab"]
            kind_ac, vp_ac = global_result["kind_ac"], global_result["vp_ac"]
            used_camera_pose = global_result["used_camera_pose"]
            self.plane_vanishing_points = {"ab": (kind_ab, vp_ab), "ac": (kind_ac, vp_ac)}
            self.plane_model_type = "projective"
            self.plane_d_route = ("camera_pose" if used_camera_pose and kind_ab not in _FINITE_KINDS
                                   and kind_ac not in _FINITE_KINDS else "vanishing_point")
            self.plane_line_residuals = {"ab": global_result["line_residuals_ab"],
                                          "ac": global_result["line_residuals_ac"]}
            self.plane_point_reproj = global_result["point_reproj"]

            CONF = {"finite_strong": "YUKSEK", "finite_weak": "ORTA"}
            n_extra = len(extra_ab) + len(extra_ac)
            extra_note = (f" ({n_extra} ek olcum kenari da kacis noktasi tahminine dahil "
                           f"edildi - daha kararli.)") if n_extra else ""
            auto_only_ab = helper_ab is None and kind_ab in _FINITE_KINDS
            auto_only_ac = helper_ac is None and kind_ac in _FINITE_KINDS
            if auto_only_ab or auto_only_ac:
                which = "AB ve AC" if auto_only_ab and auto_only_ac else ("AB" if auto_only_ab else "AC")
                extra_note += (f" [{which} yonunde yardimci cizgi VERILMEDI - kacis noktasi "
                               f"TAMAMEN otomatik cizgi tespiti (LSD/Hough+RANSAC) ile bulundu.]")
            cam_note = (" Kamera pozu (EXIF+P3P/SQPNP) tahmini de BAGIMSIZ bir dorduncu nokta "
                        "gozlemi olarak sisteme dahil edildi." if used_camera_pose else "")

            if kind_ab in _FINITE_KINDS and kind_ac in _FINITE_KINDS:
                self.plane_vp_confidence = CONF[kind_ab] if kind_ab == "finite_weak" or kind_ac == "finite_weak" else "YUKSEK"
                note = (f"H, A/B/C + HER IKI yonun GERCEK kacis noktasi kisitlari DOGRUDAN "
                        f"(D ARA DEGISKENI OLMADAN) BIRLIKTE cozuldu, D* bu H'den SONRADAN "
                        f"turetildi - TAM PROJEKTIF (AB={CONF[kind_ab]}, AC={CONF[kind_ac]})." +
                        extra_note + cam_note)
            elif kind_ab in _FINITE_KINDS or kind_ac in _FINITE_KINDS:
                finite_kind = kind_ab if kind_ab in _FINITE_KINDS else kind_ac
                finite_yon = "AB" if kind_ab in _FINITE_KINDS else "AC"
                parallel_yon = "AC" if finite_yon == "AB" else "AB"
                # Karma durumda GENEL guven en fazla ORTA sayilir - cunku
                # tek bir yon gercek kacis noktasindan geliyor, diger yon
                # (kanitlanmis da olsa) bir varsayima dayaniyor.
                self.plane_vp_confidence = "ORTA"
                note = (f"H, {finite_yon} yonundeki GERCEK kacis noktasi ({CONF[finite_kind]}) + "
                        f"{parallel_yon} yonunde SAYISAL OLARAK KANITLANMIS uzak/sonsuz yon "
                        f"kisitiyla DOGRUDAN BIRLIKTE cozuldu - KISMI PROJEKTIF (guclu "
                        f"perspektifin oldugu {finite_yon} yonu dogru modellendi)." +
                        extra_note + cam_note)
            else:
                # SADECE kamera pozu (hicbir VP kaniti YOK). Bolum 8:
                # yaklasik EXIF K TEK BASINA asla YUKSEK guven URETEMEZ.
                self.plane_vp_confidence = "ORTA"
                note = ("H, SADECE kamera pozu kestirimiyle (EXIF+P3P/SQPNP) kuruldu - hicbir "
                        "kacis noktasi/cizgi kaniti yok, bu yuzden guven ORTA ile sinirlandirildi "
                        "(yaklasik EXIF odak uzunlugu TEK BASINA YUKSEK guvenli bir global model "
                        "uretemez). DAHA YUKSEK GUVEN ICIN: 'Daha Yuksek Dogruluk' bolumune bir "
                        "yardimci cizgi ekleyin.")

            lr_ab, lr_ac = global_result["line_residuals_ab"], global_result["line_residuals_ac"]
            if lr_ab:
                note += (f"\nAB cizgi tutarliligi (n={lr_ab['n']}, BAGIMSIZ dogrulama): "
                         f"ortalama={lr_ab['mean_deg']:.2f}°, medyan={lr_ab['median_deg']:.2f}°, "
                         f"max={lr_ab['max_deg']:.2f}°")
            if lr_ac:
                note += (f"\nAC cizgi tutarliligi (n={lr_ac['n']}, BAGIMSIZ dogrulama): "
                         f"ortalama={lr_ac['mean_deg']:.2f}°, medyan={lr_ac['median_deg']:.2f}°, "
                         f"max={lr_ac['max_deg']:.2f}°")
            ortho = global_result.get("orthogonality")
            if ortho is not None and not ortho["consistent"]:
                note += f"\n[!] {ortho['message']}"
        else:
            img_pts = [A, B, C]
            world_pts = [world_A, world_B, world_C]
            self.plane_model_type = "affine_local"
            self.plane_vp_confidence = "N/A"
            note = ("[!] Yeterli kanit yok - D'nin GERCEK projektif konumu hesaplanamiyor (bu, "
                    "sadece A,B,C+2 uzunluktan MATEMATIKSEL OLARAK belirlenemez - kamera odak "
                    "uzakligi bilinse bile birden fazla gecerli kamera pozu farkli D verir). "
                    "Yaklasik (afin) sonuc kullaniliyor - gercek perspektif/kacis noktasi YOK "
                    "sayiliyor, uzak bolgelerde hata buyuyebilir. DAHA DOGRU SONUC ICIN: asagidaki "
                    "'Daha Yuksek Dogruluk' bolumune, AB veya AC yonunde fotografta baska bir "
                    "yerde (ör. baska bir pencere kenari) gorunen bir kenarin 2 ucunu secin.")
            for r in vp_stage.get("reasons", []):
                note += "\n  - " + r

        try:
            if self.plane_strat_result is not None:
                # H, kademeli rektifikasyondan (T_metric @ H_p) DOGRUDAN
                # geliyor - bu 4 noktadan (A,B,C,D) YENIDEN KURULMUYOR.
                # cond SADECE tanisal/goruntuleme amacli.
                H = self.plane_strat_result["H"]
                Hinv = self.plane_strat_result["Hinv"]
                cond = homography_condition_number(img_pts, world_pts)
            elif global_result is not None:
                # H ARTIK bu 4 noktadan YENIDEN kurulmuyor - compute_global_
                # homography'nin (nokta+yon kisitlarini BIRLIKTE cozen, sonra
                # nonlineer inceltilen) SONUCU DOGRUDAN kullanilir. cond,
                # SADECE tanisal/goruntuleme amacli (bu 4 noktanin nasil bir
                # kosulluluk gosterdigi) - H'yi belirlemiyor.
                H = global_result["H"]
                Hinv = global_result["Hinv"]
                cond = homography_condition_number(img_pts, world_pts)
            else:
                H = fit_affine(img_pts, world_pts)
                Hinv = np.linalg.inv(H)
                cond = affine_condition_number(img_pts, world_pts)
        except (ValueError, np.linalg.LinAlgError) as e:
            self.plane_H = None
            self.plane_corners = None
            self.plane_calibrated = False
            self._update_plane_status()
            self._redraw()
            if not silent:
                messagebox.showerror("Hata", f"Duzlem hesaplanamadi: {e}")
            return

        # Kosul sayisi (bkz. classify_condition_quality dokumantasyonu, sentetik
        # olcumlerle kalibre edildi): referans noktalari neredeyse ayni dogru
        # uzerindeyse ya da asiri carpik bir sekil olusturuyorsa, bu deger hizla
        # buyur - kucuk tiklama hatalarinin ne kadar buyutulecegini gosterir.
        quality = classify_condition_quality(cond)
        self.plane_condition_number = cond
        self.plane_quality = quality
        if quality in ("Zayif", "Kararsiz"):
            note += (f"\n[!] Referans geometrisi kalitesi: {quality} (kosul sayisi={cond:.1f}) - "
                     f"A, B, C neredeyse ayni dogru uzerinde olabilir ya da referans sekli asiri "
                     f"carpik. Kucuk tiklama hatalari sonucu orantisiz etkileyebilir.")
        else:
            note += f"\nReferans geometrisi kalitesi: {quality} (kosul sayisi={cond:.1f})"

        self.plane_corners = [A_lbl, B_lbl, C_lbl]
        self.plane_width_m = ab_m
        self.plane_height_m = ac_m
        self.plane_H = H
        self.plane_Hinv = Hinv
        self.plane_img_pts = [tuple(p) for p in img_pts]
        self.plane_world_pts = [tuple(p) for p in world_pts]
        # D (varsa) gercek bir tiklama degil, kacis noktalarindan TUREYEN
        # sentetik bir noktadir - Monte Carlo belirsizligi bunu diger
        # manuel noktalar gibi degil, "derived_projective" (bkz.
        # POINT_SOURCE_SIGMA_PX) olarak agirlikladirmali.
        self.plane_point_sources = ([lookup_source.get(A_lbl, "manual"), lookup_source.get(B_lbl, "manual"),
                                      lookup_source.get(C_lbl, "manual")] +
                                     (["derived_projective"] if len(img_pts) == 4 else []))
        self.plane_calibrated = True
        # Izgara tabani: A ortak kose (origin), AB ve AC GERCEK kenar
        # yonleri (quad4/afin'in aksine, burada "axis2" ikinci kenardan
        # degil DOGRUDAN A'dan cikan AC yonunden alinir - cunku A ortak
        # kosedir, B degil).
        self.plane_origin = np.array(world_A, dtype=np.float64)
        self.plane_axis1 = np.array(world_B, dtype=np.float64) - self.plane_origin
        self.plane_axis2 = np.array(world_C, dtype=np.float64) - self.plane_origin
        self._update_plane_status(note)
        self.last_results = {}
        self._redraw()
        if not silent:
            messagebox.showinfo("Duzlem hazir", note)

    def _stratified_note(self, sr):
        """Kademeli cozumun durum notu: guven ve BILESENLERI ayri ayri
        (tek bir opak skor yerine), yetersiz kanit varsa somut oneri."""
        self.plane_vp_confidence = sr["confidence"]
        su = sr.get("scale_unc_far")
        lines = ["H, KADEMELI REKTIFIKASYON ile kuruldu (kacis cizgisi -> afin -> metrik; olcek A/B/C'den "
                 "TAM) - D* sadece SONRADAN turetildi.",
                 f"Guven: {sr['confidence']}" +
                 (f"  (uzak bolgelerde olcek belirsizligi ~%{su * 100:.1f}, 1-sigma)" if su is not None else "")]
        suggest = []
        for fam in ("ab", "ac"):
            f = sr["families"][fam]
            fn = FAMILY_NAMES[fam]
            sp = f["spatial"] or {}
            val = f.get("validation") or {}
            loo = [x for x in val.get("loo", []) if x.get("z") is not None]
            vtxt = []
            if loo:
                vtxt.append(f"yardimci LOO en buyuk z={max(x['z'] for x in loo):.1f}")
            if val.get("cv_rms_z") is not None:
                vtxt.append(f"otomatik CV RMS z={val['cv_rms_z']:.1f}")
            unc = f["unc_deg"]
            lines.append(f"{fn} yonu: {'SONSUZDA (paralel)' if f['is_infinite'] else 'sonlu VP'}, "
                         f"{f['n_inliers']} cizgi (referans + {f['n_verified_helpers']} yardimci + "
                         f"{f['n_unverified']} otomatik/diger), yon belirsizligi="
                         f"{f'{unc:.2f}°' if unc is not None else 'N/A'}, dik yayilim=%"
                         f"{sp.get('perp_span_frac', 0) * 100:.0f}, bagimsiz dogrulama: {', '.join(vtxt) or 'YOK'}")
            if f["verified_outlier_ids"]:
                lines.append(f"[!] {fn}: {', '.join(f['verified_outlier_ids'])} diger kanitla tutarsiz - "
                             f"hesaba KATILMADI. Listeden silin ya da yonunu degistirin.")
            if (sp.get("perp_span_frac", 0) < 0.15 or (unc is not None and unc > 0.5) or
                    (not loo and val.get("cv_rms_z") is None)):
                suggest.append(fn)
        for r in sr.get("confidence_reasons", []):
            lines.append(f"[!] {r}")
        if suggest:
            lines.append(f"Oneri: {' ve '.join(suggest)} yonunde, fotografin referanstan UZAK bir bolgesindeki "
                         f"uzun ve net bir paralel kenari yardimci cizgi olarak ekleyin.")
        lines.append(f"AB/AC geri-kazanim (T_metric TAM olmali): {sr['ab_recovered']:.5f} (girdi "
                     f"{sr['ab_input']:.5f}), {sr['ac_recovered']:.5f} (girdi {sr['ac_input']:.5f})")
        return "\n".join(lines)

    def _build_plane(self, labels, img_pts, world_pts, width_m, height_m, silent, calibrated, note):
        if world_pts is None:
            if not silent:
                messagebox.showerror("Hata", note or "Duzlem hesaplanamadi.")
            self._redraw()
            return
        try:
            if len(img_pts) == 3:
                H = fit_affine(img_pts, world_pts)
                Hinv = np.linalg.inv(H)
            else:
                H = compute_homography(img_pts, world_pts)
                Hinv = np.linalg.inv(H)  # AYNI H'nin tam tersi - bkz. yukaridaki not
        except (ValueError, np.linalg.LinAlgError) as e:
            if not silent:
                messagebox.showerror("Hata", f"Duzlem hesaplanamadi: {e}\n"
                                              "(noktalar ayni dogru uzerinde olmamali.)")
            self._redraw()
            return

        self.plane_corners = labels
        self.plane_width_m = width_m
        self.plane_height_m = height_m
        self.plane_H = H
        self.plane_Hinv = Hinv
        self.plane_calibrated = calibrated
        # Izgara TABANI: 1->2 kenari ve 2->3 kenari (dunya vektorleri).
        # Bunlar 4-kose modunda zaten birbirine dik (dikdortgen varsayimi),
        # ama 3-nokta (afin/SSS) modunda GENELDE DIK DEGILDIR - izgara bu
        # gercek kenarlari takip etmeli, kese kese (ortonormal) bir
        # varsayilan eksen takimini degil.
        self.plane_origin = np.array(world_pts[0], dtype=np.float64)
        self.plane_axis1 = np.array(world_pts[1], dtype=np.float64) - self.plane_origin
        self.plane_axis2 = np.array(world_pts[2], dtype=np.float64) - np.array(world_pts[1], dtype=np.float64)
        self._update_plane_status(note)
        self.last_results = {}
        self._redraw()
        if not silent and calibrated:
            messagebox.showinfo("Duzlem hazir", note)
        elif not silent:
            messagebox.showerror("Hata", note)

    def _update_plane_status(self, note=""):
        if self.plane_H is None or self.plane_corners is None:
            self.plane_status_var.set("Duzlem henuz ayarlanmadi.")
        elif self.ref_mode_var.get() == "coords":
            self.plane_status_var.set(
                f"Duzlem ayarlandi ({len(self.plane_corners)} nokta, gercek koordinat).\n"
                f"Noktalar: {' , '.join(self.plane_corners)}\n{note}"
            )
        elif self.plane_calibrated:
            model_type = getattr(self, "plane_model_type", None)
            if model_type == "projective":
                d_route = getattr(self, "plane_d_route", None)
                cam_status = getattr(self, "plane_camera_status", "BILINMIYOR")
                if d_route == "stratified":
                    model_line = (f"Model: TAM PROJEKTIF HOMOGRAFI [KADEMELI REKTIFIKASYON: "
                                   f"kacis cizgisi -> afin -> metrik] (Guven: {self.plane_vp_confidence})"
                                   f"\nKamera: {cam_status}")
                elif d_route == "camera_pose":
                    model_line = (f"Model: TAM PROJEKTIF HOMOGRAFI [ROUTE A: KAMERA POZU, P3P/SQPNP] "
                                   f"(Guven: {self.plane_vp_confidence})\nKamera: {cam_status}")
                else:
                    vps = getattr(self, "plane_vanishing_points", {}) or {}
                    vp_ab_kind = (vps.get("ab") or (None,))[0]
                    vp_ac_kind = (vps.get("ac") or (None,))[0]
                    model_line = (f"Model: TAM PROJEKTIF HOMOGRAFI [ROUTE B: KACIS NOKTASI] "
                                   f"(Guven: {self.plane_vp_confidence} - "
                                   f"AB={vp_ab_kind or '-'}, AC={vp_ac_kind or '-'})\nKamera: {cam_status}")
            elif model_type == "affine_local":
                model_line = ("Model: SADECE YEREL AFIN (perspektif COZULEMEDI) - izgara ve uzak "
                               "olcumler SADECE referansa yakin bolgede guvenilir, bkz. asagidaki not.")
            else:
                model_line = "Model: bilinmiyor"
            self.plane_status_var.set(
                f"{model_line}\n"
                f"Duzlem ayarlandi: Genislik={self._fmt(self.plane_width_m)}  "
                f"Yukseklik/Egim={self._fmt(self.plane_height_m)}\n"
                f"Kose sirasi: {' -> '.join(self.plane_corners)}\n{note}"
            )
        else:
            self.plane_status_var.set(
                "On izleme: egim/perspektif gosteriliyor (olcek HENUZ DOGRU DEGIL).\n"
                f"Kose sirasi: {' -> '.join(self.plane_corners)}\n{note}"
            )

    # ---------- Kayitli duzlemler (birden fazla alan/yuzey icin) ----------

    def _snapshot_current_plane(self):
        """Su an aktif olan (kalibre edilmis) duzlemin bir 'anlik goruntusunu'
        alir - bu, bir sorguya veya kayitli duzlem listesine gomulup, o
        sorgu/duzlem SONRADAN baska bir referans kurulsa bile KENDI
        kalibrasyonunu hatirlamaya devam eder. ONEMLI: kose PIKSEL
        konumlarini da (corner_coords) donduruyoruz - sadece etiketleri
        degil - boylece bir etiket SONRADAN silinip baska bir noktaya
        yeniden verilirse (ör. "A" silinip farkli bir yerde yeni bir "A"
        eklenirse), bunu tespit edip kullaniciyi uyarabiliriz; aksi halde
        kayitli duzlem sessizce yanlis noktadan yeniden kurulurdu."""
        if self.plane_H is None or not self.plane_calibrated:
            return None
        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        img_pts = getattr(self, "plane_img_pts", None)
        world_pts = getattr(self, "plane_world_pts", None)
        point_sources = getattr(self, "plane_point_sources", None)
        return {
            "mode": self.ref_mode_var.get(),
            "corners": list(self.plane_corners),
            "corner_coords": [lookup[lb] for lb in self.plane_corners],
            "H": self.plane_H.copy(),
            "Hinv": self.plane_Hinv.copy() if self.plane_Hinv is not None else None,
            "width_m": self.plane_width_m,
            "height_m": self.plane_height_m,
            "origin": self.plane_origin.copy() if self.plane_origin is not None else None,
            "axis1": self.plane_axis1.copy() if self.plane_axis1 is not None else None,
            "axis2": self.plane_axis2.copy() if self.plane_axis2 is not None else None,
            # ONEMLI: H'yi kuran TAM (img_pts, world_pts) cifti - Monte Carlo
            # olcum belirsizligi (bkz. monte_carlo_uncertainty) bu referansi
            # AYNEN yeniden kurup perturbe edebilmek icin buna ihtiyac duyar.
            # Eski (bu alanlar olmadan) kaydedilmis config'ler icin None kalir
            # ve belirsizlik hesaplanamaz - geri kalan her sey calismaya devam eder.
            "img_pts": [list(p) for p in img_pts] if img_pts else None,
            "world_pts": [list(p) for p in world_pts] if world_pts else None,
            "point_sources": list(point_sources) if point_sources else None,
            "condition_number": getattr(self, "plane_condition_number", None),
            "quality": getattr(self, "plane_quality", None),
            # model_type: "projective" (D gercek/kismi kacis noktasindan) ya
            # da "affine_local" (D=B+C-A yaklasimi, perspektif YOK sayildi).
            # Bu ayrim, olcum sonuclarinda ve grid cizerken KRITIK -
            # affine_local model, referanstan uzak bolgelerde YANLIS
            # olabilir ve bunu acikca isaretlememiz gerekir.
            "model_type": getattr(self, "plane_model_type", None),
            "vp_confidence": getattr(self, "plane_vp_confidence", "N/A"),
            "d_route": getattr(self, "plane_d_route", None),
            "camera_status": getattr(self, "plane_camera_status", "BILINMIYOR"),
            "line_residuals": getattr(self, "plane_line_residuals", None),
            "point_reproj": getattr(self, "plane_point_reproj", None),
            **self._helper_evidence_snapshot(),
        }

    def _helper_evidence_snapshot(self):
        """Bu duzlemi KURAN yardimci-cizgi kanitini (geometri, aile, kaynak,
        guven), VP tahminlerini, belirsizligi ve dogrulama bilesenlerini
        JSON-uyumlu olarak saklar. Kayitli duzlem yeniden yuklendiginde
        dondurulmus H kullanilir - cizgiler yeniden TESPIT EDILMEZ."""
        sr = self.plane_strat_result if getattr(self, "plane_d_route", None) == "stratified" else None
        if sr is None:
            return {"helper_lines": [], "vp": None, "vp_uncertainty_deg": None, "validation": None}
        used = []
        for hl in self.helper_lines:
            if hl["family"] not in ("ab", "ac"):
                continue
            st = self.helper_status.get(hl["id"], {})
            used.append({**self._normalize_helper_line(hl),
                         "sigma_angle_deg": hl.get("sigma_angle_deg"),
                         "inlier": st.get("inlier"), "z": st.get("z"), "loo_z": st.get("loo_z")})
        return {
            "helper_lines": used,
            "vp": {"ab": [float(x) for x in sr["v_ab_hom"]], "ac": [float(x) for x in sr["v_ac_hom"]]},
            "vp_uncertainty_deg": {"ab": sr["families"]["ab"]["unc_deg"], "ac": sr["families"]["ac"]["unc_deg"]},
            "validation": summarize_model_validation(sr),
        }

    def _current_ref_label(self, corners):
        """Ayni koseler arka arkaya kullanilirsa ayni 'RefN' etiketini
        tekrar kullanir; degisirse yeni bir numara verir. Sadece
        sorgu listesinde hangi referansin kullanildigini gostermek icin."""
        if corners == self._last_ref_corners:
            return self._last_ref_label
        self._ref_counter += 1
        label = f"Ref{self._ref_counter}"
        self._last_ref_corners = list(corners)
        self._last_ref_label = label
        return label

    def save_named_plane(self):
        snap = self._snapshot_current_plane()
        if snap is None:
            messagebox.showerror("Hata", "Once gecerli (kalibre edilmis) bir referans/duzlem kurun.")
            return
        name = simpledialog.askstring("Duzlemi Kaydet", "Bu duzlem icin bir isim girin (ör. 'Bina', 'Pencere'):",
                                       parent=self)
        if not name:
            return
        if any(p["name"] == name for p in self.saved_planes):
            messagebox.showerror("Hata", f"'{name}' isimli kayitli duzlem zaten var.")
            return

        if snap["mode"] == "affine3":
            lengths_m = {
                "d12": self._peek_len(self.tri_len_entries[0]),
                "d23": self._peek_len(self.tri_len_entries[1]),
                "d13": self._peek_len(self.tri_len_entries[2]),
            }
        else:
            lengths_m = {
                "width": self._peek_len(self.plane_width_entry),
                "height": self._peek_len(self.plane_height_entry),
            }
        self.saved_planes.append({**snap, "name": name, "lengths_m": lengths_m})
        self._refresh_saved_planes_list()
        messagebox.showinfo("Kaydedildi", f"'{name}' duzlemi kaydedildi.")

    def _refresh_saved_planes_list(self):
        self.saved_planes_list.delete(0, "end")
        for p in self.saved_planes:
            mode_label = "3N" if p["mode"] == "affine3" else "4K"
            self.saved_planes_list.insert("end", f"{p['name']} [{mode_label}] {' -> '.join(p['corners'])}")

    def load_named_plane(self):
        """ONEMLI DUZELTME: eskiden burada duzlem, LABEL'lerin su anki
        (canli) piksel konumlarindan YENIDEN HESAPLANIYORDU. Bir etiket
        (ör. 'A') silinip baska bir noktaya yeniden verilmisse, bu SESSIZCE
        yanlis bir konumdan duzlem kurardi - ayni fiziksel referans icin
        farkli sonuclar almanizin nedenlerinden biri buydu. Artik kaydedildigi
        andaki DONDURULMUS H matrisi DOGRUDAN uygulaniyor - etiketler ne
        olursa olsun, kaydedilen kalibrasyon degismeden korunuyor. Etiket
        konumlari degismisse de acikca uyariyoruz."""
        sel = self.saved_planes_list.curselection()
        if not sel:
            messagebox.showinfo("Bilgi", "Once listeden bir duzlem secin.")
            return
        p = self.saved_planes[sel[0]]

        lookup = {pt["label"]: (pt["x"], pt["y"]) for pt in self.points}
        saved_coords = p.get("corner_coords")
        mismatched = []
        if saved_coords:
            for lb, (sx, sy) in zip(p["corners"], saved_coords):
                cur = lookup.get(lb)
                if cur is None or math.hypot(cur[0] - sx, cur[1] - sy) > 2.0:
                    mismatched.append(lb)
        if mismatched:
            if not messagebox.askyesno(
                    "Uyari - Etiket Uyusmazligi",
                    f"'{p['name']}' duzlemi kaydedildiginden beri su etiketler farkli bir "
                    f"konuma tasinmis veya silinip yeniden kullanilmis gorunuyor: "
                    f"{', '.join(mismatched)}.\n\n"
                    f"Yine de kaydedildigi ANDAKI orijinal kalibrasyonu (o zamanki nokta "
                    f"konumlariyla, mevcut noktalari GORMEZDEN gelerek) kullanmak "
                    f"istiyor musunuz?"):
                return

        self.ref_mode_var.set(p["mode"])
        self._apply_ref_mode()

        # Duzlemi CANLI noktalardan degil, kaydedilen DONDURULMUS
        # matristen dogrudan geri yukle.
        self.plane_H = p["H"].copy()
        self.plane_Hinv = (p["Hinv"].copy() if p.get("Hinv") is not None
                            else np.linalg.inv(self.plane_H))
        self.plane_corners = list(p["corners"])
        self.plane_width_m = p["width_m"]
        self.plane_height_m = p["height_m"]
        self.plane_calibrated = True
        self.plane_origin = p["origin"].copy() if p.get("origin") is not None else None
        self.plane_axis1 = p["axis1"].copy() if p.get("axis1") is not None else None
        self.plane_axis2 = p["axis2"].copy() if p.get("axis2") is not None else None

        # Sadece GORUNUM/bilgi amacli - kutulari doldur ama YENIDEN
        # HESAPLATMA (bu, az once yukledigimiz dondurulmus matrisi ezerdi).
        if p["mode"] == "affine3":
            for cb, lb in zip(self.tri_combos, p["corners"]):
                cb.set(lb)
            for entry, key in zip(self.tri_len_entries, ("d12", "d23", "d13")):
                entry.delete(0, "end")
                val = p["lengths_m"].get(key)
                if val is not None:
                    entry.insert(0, f"{from_meters(val, self.unit_var.get()):.4f}")
        else:
            for cb, lb in zip(self.corner_combos, p["corners"]):
                cb.set(lb)
            self.plane_width_entry.delete(0, "end")
            self.plane_height_entry.delete(0, "end")
            w = p["lengths_m"].get("width")
            h = p["lengths_m"].get("height")
            if w is not None:
                self.plane_width_entry.insert(0, f"{from_meters(w, self.unit_var.get()):.4f}")
            if h is not None:
                self.plane_height_entry.insert(0, f"{from_meters(h, self.unit_var.get()):.4f}")

        note = f"'{p['name']}' KAYITLI duzlem yuklendi (kaydedildigi andaki kalibrasyon aynen kullaniliyor)."
        if p.get("helper_lines"):
            note += (f" Bu duzlem {len(p['helper_lines'])} yardimci cizgi kanitiyla kurulmustu; cizgiler "
                     f"yeniden tespit edilmedi.")
        self._update_plane_status(note)
        self._redraw()
        self.status_var.set(f"'{p['name']}' duzlemi yuklendi.")

    def delete_named_plane(self):
        sel = self.saved_planes_list.curselection()
        if not sel:
            return
        del self.saved_planes[sel[0]]
        self._refresh_saved_planes_list()

    # ---------- Sorgular ----------

    def _refresh_query_list(self):
        self.query_list.delete(0, "end")
        for q in self.queries:
            gt = f"  (gercek: {self._fmt(q['ground_truth_m'])})" if q.get("ground_truth_m") is not None else ""
            snap = q.get("plane_snapshot")
            ref = f"[{snap.get('ref_label', '?')}] " if snap else "[eski/referanssiz] "
            path = f"{q['a']} - {q['b']} - {q['c']}" if q.get("c") else f"{q['a']} - {q['b']}"
            self.query_list.insert("end", f"{ref}{q['name']}: {path}{gt}")

    def add_query(self):
        a, b = self.combo_a.get(), self.combo_b.get()
        c = self.combo_c.get().strip() or None
        name = self.query_name_entry.get().strip()
        gt_raw = self.query_gt_entry.get().strip()

        if not a or not b:
            messagebox.showerror("Hata", "En az A ve B noktalarini secmelisiniz.")
            return
        if a == b or (c is not None and c in (a, b)):
            messagebox.showerror("Hata", "A, B (ve varsa C) birbirinden farkli olmali.")
            return
        if not name:
            messagebox.showerror("Hata", "Sorgu icin bir isim girin.")
            return
        if any(q["name"] == name for q in self.queries):
            messagebox.showerror("Hata", f"'{name}' isimli sorgu zaten var.")
            return

        # ONEMLI: sorgu, EKLENDIGI ANDA aktif olan referans/duzlemin bir
        # kopyasini kendi icine gomer. Boylece siz baska bir alan (ör.
        # calinin yanindaki duvar, pencere) icin YENI bir referans
        # kursaniz bile, bu sorgu HALA KENDI dogru referansini kullanir -
        # farkli alanlar arasinda gecis yaparken eski olcumleri kaybetmezsiniz.
        snap = self._snapshot_current_plane()
        if snap is None:
            messagebox.showerror("Hata", "Once gecerli (kalibre edilmis) bir referans/duzlem kurun\n"
                                          "('Referans Olustur' panelinde, 'Duzlem ayarlandi' durumunu gorene kadar).")
            return

        # GUVENLIK KONTROLU: bu sorgu, TAM SU ANDA dondurulecek referans
        # degerlerini KALICI olarak icine gomecek. Referans alanlari canli
        # (her tus vurusunda) yeniden hesaplandigi icin, kullanici bir
        # uzunluk alanina yazarken (ör. "1.418" yazarken henuz "1" iken)
        # TAM O ANDA "Ekle"ye basarsa, sorgu bu EKSIK/YANLIS degeri sonsuza
        # dek dondurur - sonradan alani duzeltmek bu sorguyu ETKILEMEZ
        # (somut olarak dogrulandi: AC="1" iken donmus bir sorgu, AC
        # sonradan 1.418'e duzeltilse bile 1.000 sonuc vermeye devam eder).
        # Bu yuzden, referans degerleri SON ONAYLANANDAN farkliysa, dondurmadan
        # ONCE kullaniciya TAM OLARAK hangi degerlerin kullanilacagini
        # gosterip onay istiyoruz - boylece yaziminizi bitirmeden eklerseniz
        # bunu HEMEN fark edersiniz.
        ref_signature = (tuple(snap["corners"]), round(snap["width_m"], 6), round(snap["height_m"], 6))
        if ref_signature != getattr(self, "_last_confirmed_ref_signature", None):
            proceed = messagebox.askyesno(
                "Referans degerlerini onayla",
                f"Bu sorgu, SU AN icin gecerli olan asagidaki referansi KALICI olarak "
                f"kullanacak:\n\n"
                f"  Noktalar: {' -> '.join(snap['corners'])}\n"
                f"  1. uzunluk: {self._fmt(snap['width_m'])}\n"
                f"  2. uzunluk: {self._fmt(snap['height_m'])}\n\n"
                f"Bu degerler yanlissa (ör. uzunluk alanina yazmayi henuz "
                f"BITIRMEDIYSENIZ), HAYIR deyip once 'Referans Olustur' "
                f"panelindeki alanlari tamamlayin, sonra tekrar 'Ekle'ye basin.\n\n"
                f"Devam edilsin mi?")
            if not proceed:
                return
            self._last_confirmed_ref_signature = ref_signature

        snap["ref_label"] = self._current_ref_label(snap["corners"])

        ground_truth_m = None
        if gt_raw:
            ground_truth_m = self._parse_len(gt_raw, "Gercek deger sayisal olmali.")
            if ground_truth_m is None:
                return

        self.queries.append({"name": name, "a": a, "b": b, "c": c, "ground_truth_m": ground_truth_m,
                              "plane_snapshot": snap})
        self.query_name_entry.delete(0, "end")
        self.query_gt_entry.delete(0, "end")
        self.combo_c.set("")
        self._refresh_query_list()

    def delete_query(self):
        sel = self.query_list.curselection()
        if not sel:
            return
        del self.queries[sel[0]]
        self._refresh_query_list()

    def refresh_query_reference(self):
        """Secili sorgunun 'dondurulmus' referansini, SU AN aktif olan
        referansla DEGISTIRIR. Ornek kullanim: bir sorguyu 3-nokta
        modundayken eklediniz, sonra o alan icin daha guvenilir bir
        4-kose duzlemi kurdunuz - bu sorgu eski (daha az dogru) referansi
        kullanmaya devam eder, cunku her sorgu EKLENDIGI ANDAKI referansi
        bilerek/kasitli olarak dondurur (farkli alanlar icin farkli
        referanslari kaybetmemek amaciyla). Bu buton, o donmus referansi
        BILINCLI OLARAK guncellemenizi saglar."""
        sel = self.query_list.curselection()
        if not sel:
            messagebox.showinfo("Bilgi", "Once listeden bir sorgu secin.")
            return
        snap = self._snapshot_current_plane()
        if snap is None:
            messagebox.showerror("Hata", "Once gecerli (kalibre edilmis) bir referans/duzlem kurun.")
            return
        q = self.queries[sel[0]]
        snap["ref_label"] = self._current_ref_label(snap["corners"])
        q["plane_snapshot"] = snap
        self._refresh_query_list()
        messagebox.showinfo("Guncellendi", f"'{q['name']}' sorgusu artik [{snap['ref_label']}] referansini "
                                            f"kullaniyor. Sonucu gormek icin HESAPLA'ya basin.")

    # ---------- Hesaplama ----------

    def compute(self):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        if not self.queries:
            messagebox.showerror("Hata", "En az bir olcum sorgusu ekleyin.")
            return

        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
        lines = [
            "Not: Her sorgu, EKLENDIGI ANDA aktif olan kendi referansini kullanir\n"
            "(farkli alanlar icin farkli referanslar kurmus olabilirsiniz - koseli\n"
            "parantezdeki [RefN] etiketi hangi referansin kullanildigini gosterir).",
            "",
            "Olcum sonuclari:",
        ]
        results = {}
        for q in self.queries:
            snap = q.get("plane_snapshot")
            if snap is None:
                messagebox.showerror("Hata", f"'{q['name']}' icin referans bilgisi eksik "
                                              "(eski bir kayittan gelmis olabilir). Sorguyu silip "
                                              "tekrar ekleyin.")
                return
            try:
                pa = apply_transform(snap["H"], lookup[q["a"]])
                pb = apply_transform(snap["H"], lookup[q["b"]])
                if q.get("c"):
                    pc = apply_transform(snap["H"], lookup[q["c"]])
            except ValueError as e:
                messagebox.showerror("Hata", f"'{q['name']}' hesaplanamadi: {e}")
                return
            if q.get("c"):
                # 3 nokta = kirikli/koseli uzunluk: A->B->C, IKI PARCANIN TOPLAMI
                # (duz A-C mesafesi degil). Ör. bir koseden donen bir duvarin
                # veya mahyanin toplam uzunlugunu olcmek icin.
                meters = dist(pa, pb) + dist(pb, pc)
            else:
                meters = dist(pa, pb)
            results[q["name"]] = meters
            path_label = f"{q['a']}-{q['b']}-{q['c']}" if q.get("c") else f"{q['a']}-{q['b']}"

            # MONTE CARLO OLCUM BELIRSIZLIGI: referans (ve sorgu) noktalarini
            # KAYNAKLARINA gore (bkz. point_sigma_px - manuel/buyutecli/subpixel
            # farkli guven agirligi tasir) tekrar tekrar rastgele perturbe edip
            # duzlemi YENIDEN kurarak, bu sorgu sonucunun ne kadar GUVENILIR
            # oldugunu (tek bir sayi degil, bir DAGILIM olarak) kestiriyoruz.
            # Eski (bu bilgiyi icermeyen) config'lerden gelen sorgularda bu
            # atlanir - sonuc yine dogru hesaplanir, sadece belirsizlik verilmez.
            ci_text = ""
            snap_img_pts = snap.get("img_pts")
            snap_world_pts = snap.get("world_pts")
            if snap_img_pts and snap_world_pts:
                is_affine = len(snap_img_pts) == 3
                sources = snap.get("point_sources") or ["manual"] * len(snap_img_pts)
                sigmas = [point_sigma_px(s) for s in sources]
                q_pts = [lookup[q["a"]], lookup[q["b"]]] + ([lookup[q["c"]]] if q.get("c") else [])
                mc = monte_carlo_uncertainty(snap_img_pts, snap_world_pts, q_pts, is_affine,
                                              point_sigmas_px=sigmas, n_iter=300, seed=None)
                if mc is not None and mc["n_success"] >= 30:
                    ci_text = f"  ±{self._fmt(mc['std'] * 1.96)} (95% GA)"

            # UYARI: bu sorgu, referans noktalarinin kapladigi bolgenin
            # DISINA ne kadar "ekstrapolasyon" yapiyor? Homografi/afin
            # donusumler, kalibre edilen bolgeden uzaklastikca kucuk
            # tiklama/model hatalarini (ör. hafif lens distorsiyonu, kucuk
            # kose tiklama sapmasi) orantisiz buyutebilir - "farkli
            # yerlerde farkli uzunluk cikmasi" sikayetinin en sik nedeni
            # budur. Referans koseleri kucuk bir bolgede toplanmisken sorgu
            # cok uzaktaysa, kullaniciyi acikca uyariyoruz.
            ref_labels = snap.get("corners") or []
            ref_pts = [lookup[c] for c in ref_labels if c in lookup]
            query_pts = [lookup[q["a"]], lookup[q["b"]]] + ([lookup[q["c"]]] if q.get("c") else [])
            ratio = extrapolation_ratio(ref_pts, query_pts) if len(ref_pts) >= 2 else None
            coverage_durum = None
            if len(ref_pts) >= 3:
                coverage_durum, coverage_rel = reference_coverage_report(ref_pts, query_pts)

            # GUVENILIRLIK ETIKETI: model turu (projective/affine_local) ile
            # ekstrapolasyon durumunu BIRLIKTE degerlendirir. Afin modelde
            # perspektif hic modellenmedigi icin, GUCLU ekstrapolasyon
            # durumunda sonuc "kesin" gibi gosterilmemeli - acikca
            # UNRELIABLE olarak isaretlenir (sonuc yine de HESAPLANIR ve
            # gosterilir, sadece gizlenmez/sessizce yanlis kalmaz).
            model_type = snap.get("model_type")
            strong_extrap = (ratio is not None and ratio > 1.5) or coverage_durum == "guclu ekstrapolasyon"
            mild_extrap = (ratio is not None and ratio > 0.5) and not strong_extrap
            reliability_tag = ""
            if model_type == "affine_local" and strong_extrap:
                reliability_tag = "  [GUVENILMEZ: afin ekstrapolasyonu]"
            elif model_type == "affine_local" and mild_extrap:
                reliability_tag = "  [DUSUK GUVEN: afin, referanstan uzak]"
            elif model_type == "projective" and strong_extrap:
                reliability_tag = "  [DIKKAT: guclu ekstrapolasyon]"

            line = (f"  [{snap.get('ref_label', '?')}] {q['name']:16s} ({path_label}): "
                    f"{self._fmt(meters)}{ci_text}{reliability_tag}")
            if q.get("ground_truth_m") is not None:
                line += f"   (gercek: {self._fmt(q['ground_truth_m'])}, hata: {self._fmt_err(meters, q['ground_truth_m'])})"
            lines.append(line)

            if ratio is not None and ratio > 1.5:
                lines.append(f"      [!] Bu nokta(lar) referans bolgesinden ~{ratio:.1f}x uzakta - "
                             f"dogruluk azalmis olabilir. Bu bolgeye yakin ek bir referans "
                             f"(koseli parantezdeki referansi bu alana tasiyin ya da yeni bir "
                             f"'Kayitli Duzlem' kurun) eklemeniz onerilir.")
            elif ratio is not None and ratio > 0.5:
                lines.append(f"      (bilgi: referans bolgesinden ~{ratio:.1f}x uzakta)")

            if coverage_durum == "guclu ekstrapolasyon":
                lines.append(f"      [!] Kapsama: {coverage_durum} (referans govdesinden goreli uzaklik={coverage_rel:.2f})")

            if model_type == "affine_local" and (strong_extrap or mild_extrap):
                lines.append("      [!] Bu referans TAM PROJEKTIF degil (afin/yerel model) - "
                              "perspektif yakinsamasi modellenmedi. Bu sorgu icin daha guvenilir "
                              "sonuc icin: (a) AB/AC yonunde bir yardimci cizgi ekleyin, ya da "
                              "(b) bu bolgeye yakin ayri bir referans kurun.")

            cond = snap.get("condition_number")
            quality = snap.get("quality")
            if quality in ("Zayif", "Kararsiz"):
                lines.append(f"      [!] Bu referansin geometrik kalitesi '{quality}' "
                             f"(kosul sayisi={cond:.1f}) - sonuc guvenilirligi dusuk olabilir.")

        # BOLUM 1/24 (METRIK OLCEK TESHISI): "gercek deger" (ground_truth_m)
        # girilmis sorgular varsa - AYNI referansa ait olanlari birlikte -
        # yatay/dikey eksene gore siniflandirip r_x, r_y, global_scale_ratio,
        # axis_anisotropy hesapla ve ayri bir bolum olarak raporla. Bu,
        # HERHANGI bir duzeltme UYGULAMAZ - sadece kalan bir sapmanin
        # (varsa) global mi yoksa eksene mi ozel oldugunu GORUNUR kilar
        # (bkz. compute_axis_scale_diagnostics dokumantasyonu).
        gt_by_ref = {}
        for q in self.queries:
            if q.get("ground_truth_m") is None:
                continue
            snap = q.get("plane_snapshot")
            if snap is None or snap.get("model_type") != "projective" or not snap.get("img_pts"):
                continue
            key = id(snap)
            entry = gt_by_ref.setdefault(key, {"snap": snap, "segs": []})
            axis = classify_query_axis(snap, lookup[q["a"]], lookup[q["b"]])
            entry["segs"].append({"name": q["name"], "p": lookup[q["a"]], "q": lookup[q["b"]],
                                   "true_length_m": q["ground_truth_m"], "axis": axis})

        diag_lines = []
        for entry in gt_by_ref.values():
            segs = entry["segs"]
            if len(segs) < 2:
                continue
            diag = compute_axis_scale_diagnostics(entry["snap"]["H"], segs)
            ref_lbl = entry["snap"].get("ref_label", "?")
            diag_lines.append(f"\n[{ref_lbl}] Metrik olcek teshisi ({len(segs)} bilinen uzunluklu sorgu):")
            if diag["r_x"] is not None:
                cv_txt = f"  (konum-ici CV=%{diag['r_x_cv']*100:.1f})" if diag["r_x_cv"] is not None else ""
                diag_lines.append(f"   r_x (yatay oran) = {diag['r_x']:.4f}{cv_txt}")
            if diag["r_y"] is not None:
                cv_txt = f"  (konum-ici CV=%{diag['r_y_cv']*100:.1f})" if diag["r_y_cv"] is not None else ""
                diag_lines.append(f"   r_y (dikey oran) = {diag['r_y']:.4f}{cv_txt}")
            if diag["global_scale_ratio"] is not None:
                diag_lines.append(f"   global_scale_ratio = {diag['global_scale_ratio']:.4f}")
            if diag["axis_anisotropy"] is not None:
                diag_lines.append(f"   axis_anisotropy (r_y/r_x) = {diag['axis_anisotropy']:.4f}")
            diag_lines.append(f"   -> {diag['classification']}")
        if diag_lines:
            lines.append("")
            lines.append("=== Metrik Olcek Teshisi ===")
            lines.append("(bilinen uzunluklu sorgular kullanildi - bkz. 'Ölçüm Sorguları' bölümündeki "
                          "'gercek deger' alani)")
            lines.extend(diag_lines)

        self.last_results = results
        self._set_results_text("\n".join(lines))
        self._redraw()

    # ---------- Birim / bicimlendirme yardimcilari ----------

    def _parse_len(self, raw, err_prompt):
        if not raw:
            messagebox.showerror("Hata", err_prompt)
            return None
        try:
            val = float(raw.replace(",", "."))
        except ValueError:
            messagebox.showerror("Hata", "Deger sayisal olmali.")
            return None
        if val <= 0:
            messagebox.showerror("Hata", "Deger pozitif olmali.")
            return None
        return to_meters(val, self.unit_var.get())

    def _fmt(self, value_m):
        return f"{from_meters(value_m, self.unit_var.get()):.3f} {self.unit_var.get()}"

    def _fmt_err(self, computed_m, gt_m):
        err_m = abs(computed_m - gt_m)
        return f"{from_meters(err_m, self.unit_var.get()):.3f} {self.unit_var.get()}"

    def _refresh_all_display(self):
        self._refresh_points_tree()
        self._refresh_combos()
        self._refresh_query_list()
        self._update_plane_status()
        self._redraw()

    def _set_results_text(self, text):
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
        self.results_text.config(state="disabled")

    # ---------- Config / gorsel kaydet-yukle ----------

    _SNAPSHOT_ARRAY_FIELDS = ("H", "Hinv", "origin", "axis1", "axis2")

    @staticmethod
    def _snapshot_to_json(snap):
        """H/Hinv/origin/axis1/axis2 - hepsi numpy array olabilir; JSON'a
        yazilabilmesi icin listeye ceviriyoruz (None olanlari atlayarak)."""
        if snap is None:
            return None
        out = dict(snap)
        for key in MeasureApp._SNAPSHOT_ARRAY_FIELDS:
            if out.get(key) is not None:
                out[key] = out[key].tolist()
        return out

    @staticmethod
    def _snapshot_from_json(data):
        if data is None:
            return None
        out = dict(data)
        for key in MeasureApp._SNAPSHOT_ARRAY_FIELDS:
            if out.get(key) is not None:
                out[key] = np.array(out[key], dtype=np.float64)
        return out

    def save_config(self):
        if not self.points:
            messagebox.showinfo("Bilgi", "Kaydedilecek nokta yok.")
            return
        plane_data = None
        if self.plane_corners and self.plane_calibrated:
            mode = self.ref_mode_var.get()
            if mode == "affine3":
                d12 = self._peek_len(self.tri_len_entries[0])
                d23 = self._peek_len(self.tri_len_entries[1])
                d13 = self._peek_len(self.tri_len_entries[2])
                if d12 is not None and d23 is not None:
                    plane_data = {"mode": "affine3", "labels": self.plane_corners,
                                  "d12_m": d12, "d23_m": d23, "d13_m": d13}
            elif mode == "quad4":
                plane_data = {"mode": "quad4", "labels": self.plane_corners,
                              "width_m": self.plane_width_m, "height_m": self.plane_height_m}
            elif mode == "coords":
                plane_data = {"mode": "coords", "labels": self.plane_corners,
                              "coords_rows": [dict(r) for r in self.coords_rows]}
            else:
                angle_deg = 90.0 if self.abc_right_angle_var.get() else self._peek_coord(self.abc_angle_entry)
                helper_ab_labels = [cb.get() for cb in self.abc_helper_ab_combos]
                helper_ac_labels = [cb.get() for cb in self.abc_helper_ac_combos]
                plane_data = {
                    "mode": "abc2len", "labels": self.plane_corners,
                    "ab_m": self.plane_width_m, "ac_m": self.plane_height_m,
                    "angle_deg": angle_deg,
                    # eski surumlerle uyumluluk icin hala yaziliyor; asil kaynak "helper_lines"
                    "helper_ab_labels": helper_ab_labels if all(helper_ab_labels) else None,
                    "helper_ac_labels": helper_ac_labels if all(helper_ac_labels) else None,
                    # Kaydedilen kalibrasyonun AYNEN geri yuklenebilmesi icin
                    "H_final": self.plane_H.tolist() if self.plane_H is not None else None,
                    "model_type": getattr(self, "plane_model_type", None),
                    "d_route": getattr(self, "plane_d_route", None),
                    **self._helper_evidence_snapshot(),
                }

        queries_out = [{**q, "plane_snapshot": self._snapshot_to_json(q.get("plane_snapshot"))}
                       for q in self.queries]
        saved_planes_out = [self._snapshot_to_json(p) for p in self.saved_planes]

        cfg = {
            "photo_path": self.photo_path,
            "pdf_page": self.pdf_page,
            "image_size": list(self.pil_img.size) if self.pil_img is not None else None,
            "ref_mode": self.ref_mode_var.get(),
            "image_points": [{"label": p["label"], "x": p["x"], "y": p["y"],
                              "source": p.get("source", "manual")} for p in self.points],
            "helper_lines": [self._normalize_helper_line(h) for h in self.helper_lines],
            "queries": queries_out,
            "plane": plane_data,
            "saved_planes": saved_planes_out,
        }
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Kaydedildi", f"Config kaydedildi:\n{path}")

    def load_config(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:
            messagebox.showerror("Hata", f"Config okunamadi:\n{e}")
            return

        photo_path = cfg.get("photo_path")
        loaded = bool(photo_path and os.path.exists(photo_path)
                      and self._load_photo(photo_path, pdf_page=cfg.get("pdf_page")))
        if not loaded:
            messagebox.showinfo("Fotograf gerekli", "Bu config icin bir fotograf secin.")
            path2 = filedialog.askopenfilename(
                filetypes=IMAGE_FILETYPES)
            if not path2 or not self._load_photo(path2):
                return

        # ONEMLI GUVENLIK KONTROLU: config'teki tum piksel koordinatlari
        # (noktalar, referans koseleri) KAYIT ANINDAKI goruntu cozunurlugune
        # gore verilmistir. Su an acilan fotograf - AYNI dosya yolu olsa bile
        # (ör. telefon/bulut senkronu dosyayi farkli bir cozunurlukte yeniden
        # kaydetmis olabilir, ya da kullanici "baska bir fotograf sec" ile
        # farkli boyutlu bir dosya secmis olabilir) - FARKLI boyuttaysa, bu
        # koordinatlar SESSIZCE yanlis yerlere isaret eder ve olcumler
        # konuma bagli, ongorulemez sekilde hatali cikar. Eski config'ler
        # icin (image_size henuz kaydedilmemisken olusturulmus) bu kontrol
        # atlanir - o durumda kullanicinin kendi gozlemine guveniyoruz.
        saved_size = cfg.get("image_size")
        if saved_size and self.pil_img is not None and tuple(saved_size) != tuple(self.pil_img.size):
            proceed = messagebox.askyesno(
                "Cozunurluk uyusmuyor",
                f"Bu config, {saved_size[0]}x{saved_size[1]} piksel boyutundaki bir goruntude "
                f"kaydedilmis, ama su an acilan fotograf {self.pil_img.size[0]}x{self.pil_img.size[1]} "
                f"piksel.\n\nBu durumda config'teki tum nokta/referans koordinatlari YANLIS yerlere "
                f"isaret eder ve olcumler sessizce hatali cikar (konuma bagli, ongorulemez bir hata).\n\n"
                f"Yine de yuklemeye devam etmek istiyor musunuz? (Onerilmez - once ayni cozunurluktegi "
                f"orijinal fotografi bulun.)")
            if not proceed:
                self.status_var.set("Config yuklenmedi (cozunurluk uyusmazligi).")
                return

        self._reset_state_for_new_photo()

        self.ref_mode_var.set(cfg.get("ref_mode", "affine3"))
        self._apply_ref_mode()

        self.points = [{"label": p["label"], "x": float(p["x"]), "y": float(p["y"]),
                        "source": p.get("source", "manual")}
                       for p in cfg.get("image_points", [])]
        # "helper_lines" yoksa (eski config) bos liste - eski projeler bozulmaz.
        self.helper_lines = []
        for d in cfg.get("helper_lines") or []:
            try:
                self.helper_lines.append(self._normalize_helper_line(d))
            except (KeyError, TypeError, ValueError, IndexError):
                continue
        nums = [int(h["id"][2:]) for h in self.helper_lines if h["id"].startswith("HL") and h["id"][2:].isdigit()]
        self._helper_counter = max(nums) if nums else 0
        self._vp_stage_cache = (None, None)
        self._refresh_helper_tree()
        self.queries = [{**q, "plane_snapshot": self._snapshot_from_json(q.get("plane_snapshot"))}
                        for q in cfg.get("queries", [])]
        self.saved_planes = [self._snapshot_from_json(p) for p in cfg.get("saved_planes", [])]
        self._ref_counter = 0
        self._last_ref_corners = None
        self._last_ref_label = None
        self._refresh_saved_planes_list()

        restored_note = None
        plane = cfg.get("plane")
        if plane and plane.get("labels"):
            lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}
            labels = plane["labels"]
            mode = plane.get("mode", "quad4")
            if all(lb in lookup for lb in labels):
                img_pts = [lookup[lb] for lb in labels]
                try:
                    if mode == "affine3":
                        d12, d23, d13 = plane["d12_m"], plane["d23_m"], plane.get("d13_m")
                        if d13 is not None:
                            world_pts = triangle_from_sides(d12, d23, d13)
                        else:
                            world_pts = [(0.0, 0.0), (d12, 0.0), (d12, d23)]
                        self.plane_H = fit_affine(img_pts, world_pts)
                        self.plane_Hinv = np.linalg.inv(self.plane_H)
                        self.plane_width_m = d12
                        self.plane_height_m = d23
                        for cb, lb in zip(self.tri_combos, labels):
                            cb.set(lb)
                        for entry, val in zip(self.tri_len_entries, (d12, d23, d13)):
                            if val is not None:
                                entry.insert(0, f"{from_meters(val, self.unit_var.get()):.4f}")
                    elif mode == "quad4":
                        width_m, height_m = plane["width_m"], plane["height_m"]
                        world_pts = [(0.0, 0.0), (width_m, 0.0), (width_m, height_m), (0.0, height_m)]
                        self.plane_H = compute_homography(img_pts, world_pts)
                        self.plane_Hinv = np.linalg.inv(self.plane_H)
                        self.plane_width_m = width_m
                        self.plane_height_m = height_m
                        for cb, lb in zip(self.corner_combos, labels):
                            cb.set(lb)
                        self.plane_width_entry.insert(0, f"{from_meters(width_m, self.unit_var.get()):.4f}")
                        self.plane_height_entry.insert(0, f"{from_meters(height_m, self.unit_var.get()):.4f}")
                    elif mode == "coords":
                        self.coords_rows = [dict(r) for r in plane.get("coords_rows", [])]
                        world_pts = [(r["x_m"], r["y_m"]) for r in self.coords_rows]
                        self.plane_H = compute_homography(img_pts, world_pts)
                        self.plane_Hinv = np.linalg.inv(self.plane_H)
                        self.plane_width_m = dist(world_pts[0], world_pts[1])
                        self.plane_height_m = dist(world_pts[1], world_pts[2])
                        self._refresh_coords_tree()
                        self.plane_corners = labels
                        self.plane_calibrated = True
                        self.plane_origin = np.array(world_pts[0], dtype=np.float64)
                        self.plane_axis1 = np.array(world_pts[1], dtype=np.float64) - self.plane_origin
                        self.plane_axis2 = np.array(world_pts[2], dtype=np.float64) - np.array(world_pts[1], dtype=np.float64)
                    else:
                        # abc2len: arayuz alanlari doldurulur, sonra INTERAKTIF akisla
                        # AYNI kod (_recompute_plane_abc2len) calisir - ikinci bir kopya yok.
                        ab_m, ac_m = plane["ab_m"], plane["ac_m"]
                        angle_deg = plane.get("angle_deg") or 90.0
                        is_right_angle = abs(angle_deg - 90.0) < 1e-9
                        for cb, lb in zip(self.abc_combos, labels):
                            cb.set(lb)
                        self.abc_len_entries[0].insert(0, f"{from_meters(ab_m, self.unit_var.get()):.4f}")
                        self.abc_len_entries[1].insert(0, f"{from_meters(ac_m, self.unit_var.get()):.4f}")
                        self.abc_right_angle_var.set(is_right_angle)
                        if not is_right_angle:
                            self.abc_angle_entry.insert(0, f"{angle_deg:.4f}")
                        # ESKI config: helper_*_labels -> ayni veri modeline (nokta cifti).
                        for fam, key, combos in (("ab", "helper_ab_labels", self.abc_helper_ab_combos),
                                                 ("ac", "helper_ac_labels", self.abc_helper_ac_combos)):
                            hl_labels = plane.get(key)
                            if hl_labels and len(hl_labels) == 2 and all(lb in lookup for lb in hl_labels):
                                for cb, lb in zip(combos, hl_labels):
                                    cb.set(lb)
                                if not any(h["id"] == f"P-{fam.upper()}" for h in self.helper_lines):
                                    self.helper_lines.append(self._make_point_pair_helper(fam, hl_labels))
                        self._vp_stage_cache = (None, None)
                        self._recompute_plane_abc2len(silent=True)
                        # Kayitli H_final varsa ve yeniden hesaplama FARKLI sonuc
                        # veriyorsa (ör. farkli OpenCV surumu farkli otomatik cizgi
                        # buldu), kaydedilen kalibrasyon AYNEN korunur.
                        stored_H = plane.get("H_final")
                        if stored_H is not None and self.plane_H is not None:
                            Hs = np.array(stored_H, dtype=np.float64)
                            Hs = Hs / Hs[2, 2]
                            Hc = self.plane_H / self.plane_H[2, 2]
                            if not np.allclose(Hs, Hc, rtol=1e-6, atol=1e-9):
                                self.plane_H = Hs
                                self.plane_Hinv = np.linalg.inv(Hs)
                                if self.plane_img_pts and len(self.plane_img_pts) == 4 and self.plane_world_pts:
                                    self.plane_img_pts[3] = tuple(apply_transform(self.plane_Hinv,
                                                                                  self.plane_world_pts[3]))
                                restored_note = ("Kayitli kalibrasyon (H_final) AYNEN geri yuklendi - mevcut "
                                                 "kanitla yeniden hesaplama farkli sonuc veriyordu.")
                        self._refresh_helper_tree()

                    if mode in ("affine3", "quad4"):
                        self.plane_corners = labels
                        self.plane_calibrated = True
                        self.plane_origin = np.array(world_pts[0], dtype=np.float64)
                        self.plane_axis1 = np.array(world_pts[1], dtype=np.float64) - self.plane_origin
                        self.plane_axis2 = np.array(world_pts[2], dtype=np.float64) - np.array(world_pts[1], dtype=np.float64)
                except (ValueError, np.linalg.LinAlgError):
                    pass

        self.last_results = {}
        self._refresh_all_display()
        self._set_results_text("")
        self.status_var.set(f"Config yuklendi: {os.path.basename(path)}" +
                            (f"  [{restored_note}]" if restored_note else ""))
        self._wizard_sync()

    def save_annotated(self):
        if self.pil_img is None:
            messagebox.showinfo("Bilgi", "Once bir fotograf acin.")
            return
        out_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                  filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if not out_path:
            return

        full = self.pil_img.copy().convert("RGBA")
        draw = ImageDraw.Draw(full, "RGBA")
        lookup = {p["label"]: (p["x"], p["y"]) for p in self.points}

        if self.plane_H is not None and self.plane_calibrated:
            is_full_confidence = getattr(self, "plane_model_type", None) == "projective"
            if self.show_grid_var.get():
                self._draw_grid(draw, lambda pt: pt, color=(GRID_COLOR if is_full_confidence else PREVIEW_GRID_COLOR))
            if self.plane_corners:
                pts = [lookup[c] for c in self.plane_corners]
                draw.line(pts + [pts[0]], fill=PLANE_COLOR, width=4)

        if self.last_results:
            for q in self.queries:
                if q["name"] not in self.last_results:
                    continue
                path_pts = [lookup[q["a"]], lookup[q["b"]]]
                if q.get("c") and q["c"] in lookup:
                    path_pts.append(lookup[q["c"]])
                draw.line(path_pts, fill=QUERY_COLOR, width=4)
                mid_idx = len(path_pts) // 2
                mp1, mp2 = path_pts[mid_idx - 1], path_pts[mid_idx]
                mid = ((mp1[0] + mp2[0]) / 2, (mp1[1] + mp2[1]) / 2)
                draw.text(mid, f"{q['name']}: {self._fmt(self.last_results[q['name']])}", fill=QUERY_COLOR,
                          font=load_font(20), stroke_width=3, stroke_fill=(0, 0, 0))

        line_w = max(3, full.size[0] // 800)
        self._draw_helper_lines(draw, lambda pt: (pt[0], pt[1]), width=line_w, font=load_font(22),
                                dash=6 * line_w, gap=4 * line_w)

        for p in self.points:
            x, y = p["x"], p["y"]
            is_corner = self.plane_corners is not None and p["label"] in self.plane_corners
            color = PLANE_COLOR if is_corner else POINT_COLOR
            r = 8
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=3)
            draw.text((x + 12, y - 14), p["label"], fill=color, font=load_font(22),
                      stroke_width=3, stroke_fill=(0, 0, 0))

        # Okunakli bir "sonuc raporu" kutusu - goruntunun uzerine gomulu,
        # tum olcum sonuclarini (hangi referansi kullandiklarini da
        # belirterek) tek bir yerden okunabilir sekilde listeler.
        if self.last_results:
            img_w, img_h = full.size
            font_size = max(16, img_w // 100)
            rep_font = load_font(font_size)
            report_lines = ["Olcum Sonuclari:"]
            for q in self.queries:
                if q["name"] not in self.last_results:
                    continue
                ref = q.get("plane_snapshot", {}).get("ref_label", "?")
                line = f"[{ref}] {q['name']}: {self._fmt(self.last_results[q['name']])}"
                if q.get("ground_truth_m") is not None:
                    line += f"  (gercek: {self._fmt(q['ground_truth_m'])})"
                report_lines.append(line)

            pad = font_size
            line_h = int(font_size * 1.4)
            text_w = max(draw.textlength(t, font=rep_font) for t in report_lines)
            box_w = text_w + pad * 2
            box_h = line_h * len(report_lines) + pad * 2
            box_x0, box_y0 = pad, img_h - box_h - pad
            draw.rectangle([box_x0, box_y0, box_x0 + box_w, box_y0 + box_h], fill=(255, 255, 255, 220))
            y = box_y0 + pad
            for i, t in enumerate(report_lines):
                fill = (20, 20, 20, 255) if i > 0 else (0, 0, 0, 255)
                draw.text((box_x0 + pad, y), t, fill=fill, font=rep_font)
                y += line_h

        full = full.convert("RGB")

        full.save(out_path)
        messagebox.showinfo("Kaydedildi", f"Isaretli gorsel kaydedildi:\n{out_path}")

    def show_help(self):
        messagebox.showinfo("Nasil kullanilir?", __doc__)


if __name__ == "__main__":
    app = MeasureApp()
    app.mainloop()

"""Sentetik cephe sahnesi uretici (testler ve benchmark icin).

Dunya: cephe duzlemi Z=0, X saga (AB yonu), Y yukari (AC yonu), metre.
Kamera: cephe merkezine bakan, rastgele azimut/yukseklik/roll/uzaklik;
odak uzakligi cephe goruntuye sigacak sekilde secilir. Gercek VP'ler
v_AB = K R e_X, v_AC = K R e_Y (sonsuzda olabilir - gecerli).

Hicbir fonksiyon belirli bir fotografa gore ayarlanmamistir; tum
parametreler rastgele orneklenir.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import measure_from_photo_gui as m  # noqa: E402


class Scene:
    def __init__(self, rng, img_size=None, az_deg=None, el_deg=None, roll_deg=None,
                 dist_factor=None, facade=None, vertical_infinite=False):
        sizes = [(4000, 3000), (3000, 4000), (1600, 1200), (2400, 1800)]
        self.W, self.H = img_size or sizes[rng.integers(len(sizes))]
        self.FW, self.FH = facade or (float(rng.uniform(12, 30)), float(rng.uniform(8, 20)))
        az = math.radians(az_deg if az_deg is not None else rng.uniform(-40, 40))
        el = math.radians(el_deg if el_deg is not None else rng.uniform(-25, 5))
        if vertical_infinite:
            el = 0.0
        roll = math.radians(roll_deg if roll_deg is not None else rng.uniform(-4, 4))
        d = (dist_factor if dist_factor is not None else rng.uniform(0.8, 2.5)) * max(self.FW, self.FH)
        target = np.array([self.FW / 2, self.FH / 2, 0.0])
        if vertical_infinite:
            target[1] = 1.6
        Cc = target + d * np.array([math.sin(az) * math.cos(el), math.sin(el), -math.cos(az) * math.cos(el)])
        if not vertical_infinite:
            Cc[1] = max(Cc[1], 1.0)
        z = target - Cc
        z /= np.linalg.norm(z)
        up = np.array([0.0, 1.0, 0.0])
        x = np.cross(up, z)
        x /= np.linalg.norm(x)
        y = -np.cross(z, x)
        cr, sr = math.cos(roll), math.sin(roll)
        x, y = cr * x + sr * y, -sr * x + cr * y
        self.R = np.vstack([x, y, z])
        self.Cc = Cc
        corners = [(0, 0), (self.FW, 0), (self.FW, self.FH), (0, self.FH)]
        nc = [self._cam(p) for p in corners]
        if any(c[2] <= 0.1 for c in nc):
            raise ValueError("cephe kameranin arkasinda")
        xs = [c[0] / c[2] for c in nc]
        ys = [c[1] / c[2] for c in nc]
        cx0, cy0 = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        self.f = 0.92 * min(self.W / (max(xs) - min(xs)), self.H / (max(ys) - min(ys)))
        self.cx = self.W / 2 - self.f * cx0
        self.cy = self.H / 2 - self.f * cy0
        self.K = np.array([[self.f, 0, self.cx], [0, self.f, self.cy], [0, 0, 1.0]])

    def _cam(self, XY):
        return self.R @ (np.array([XY[0], XY[1], 0.0]) - self.Cc)

    def project(self, XY):
        c = self._cam(XY)
        return (self.f * c[0] / c[2] + self.cx, self.f * c[1] / c[2] + self.cy)

    def project3(self, P):
        c = self.R @ (np.asarray(P, dtype=float) - self.Cc)
        if c[2] <= 0.05:
            return None
        return (self.f * c[0] / c[2] + self.cx, self.f * c[1] / c[2] + self.cy)

    def vp(self, fam):
        e = np.array([1.0, 0.0, 0.0]) if fam == "ab" else np.array([0.0, 1.0, 0.0])
        v = self.K @ (self.R @ e)
        return v / np.linalg.norm(v)

    def in_image(self, p, margin=0):
        return p is not None and -margin <= p[0] <= self.W + margin and -margin <= p[1] <= self.H + margin


def _noisy(p, q, sigma, rng):
    """Uc noktalara (her iki eksende) Gauss gurultusu."""
    return ((p[0] + rng.normal(0, sigma), p[1] + rng.normal(0, sigma)),
            (q[0] + rng.normal(0, sigma), q[1] + rng.normal(0, sigma)))


def _rotate_about_mid(p, q, deg):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    def r(pt):
        dx, dy = pt[0] - mx, pt[1] - my
        return (mx + ca * dx - sa * dy, my + sa * dx + ca * dy)
    return r(p), r(q)


def make_reference(scene, rng, ab_len=None, ac_len=None):
    ab = ab_len or float(rng.uniform(0.8, 2.5))
    ac = ac_len or float(rng.uniform(0.8, 2.5))
    xa = float(rng.uniform(0.5, scene.FW - ab - 0.5))
    ya = float(rng.uniform(0.5, scene.FH - ac - 0.5))
    Aw, Bw, Cw = (xa, ya), (xa + ab, ya), (xa, ya + ac)
    return Aw, Bw, Cw, ab, ac


def facade_segments(scene, rng, fam, n, region=None, min_len=0.5, max_len=4.0):
    """Cephe uzerinde gercek AB (yatay) ya da AC (dusey) parcalari (dunya)."""
    x0, x1, y0, y1 = region or (0.0, scene.FW, 0.0, scene.FH)
    segs = []
    for _ in range(n):
        Lm = float(rng.uniform(min_len, max_len))
        if fam == "ab":
            y = float(rng.uniform(y0, y1))
            xs = float(rng.uniform(x0, max(x0, x1 - Lm)))
            segs.append(((xs, y), (min(x1, xs + Lm), y)))
        else:
            x = float(rng.uniform(x0, x1))
            ys = float(rng.uniform(y0, max(y0, y1 - Lm)))
            segs.append(((x, ys), (x, min(y1, ys + Lm))))
    return segs


def auto_observations(scene, rng, n_true=12, n_wrong=12, noise_px=0.5, bias_deg=0.0, region=None):
    """'Otomatik tespit edilmis' cizgiler: gercek cephe cizgileri (gurultulu,
    istege bagli sistematik aci sapmasi) + yanlis cizgiler (yan duvar, zemin,
    rastgele)."""
    obs = []
    k = 0
    for fam in ("ab", "ac"):
        for pw, qw in facade_segments(scene, rng, fam, n_true, region=region):
            p, q = scene.project(pw), scene.project(qw)
            if m.dist(p, q) < 25:
                continue
            p, q = _noisy(p, q, noise_px, rng)
            if bias_deg:
                p, q = _rotate_about_mid(p, q, bias_deg)
            obs.append(m.LineObservation(p, q, source="auto", verified=False, line_id=f"AUTO{k}",
                                         endpoint_sigma_px=0.7, n_support=max(2, int(m.dist(p, q)))))
            k += 1
    wrong = 0
    tries = 0
    while wrong < n_wrong and tries < 200:
        tries += 1
        kind = rng.integers(3)
        if kind == 0:  # yan duvar (X=FW duzlemi) - Z yonunde yatay cizgiler, farkli VP
            y = float(rng.uniform(0, scene.FH))
            z0 = float(rng.uniform(0.2, 6))
            P, Q = (scene.FW, y, -z0), (scene.FW, y, -z0 - float(rng.uniform(1, 4)))
        elif kind == 1:  # zemin (Y=0) - Z yonunde cizgiler
            x = float(rng.uniform(0, scene.FW))
            z0 = float(rng.uniform(0.5, 6))
            P, Q = (x, 0.0, -z0), (x, 0.0, -z0 - float(rng.uniform(1, 4)))
        else:  # rastgele dokusal cizgi
            p = (float(rng.uniform(0, scene.W)), float(rng.uniform(0, scene.H)))
            a = float(rng.uniform(0, math.pi))
            Lp = float(rng.uniform(40, 300))
            q = (p[0] + Lp * math.cos(a), p[1] + Lp * math.sin(a))
            obs.append(m.LineObservation(p, q, source="auto", verified=False, line_id=f"AUTO{k}",
                                         endpoint_sigma_px=0.7, n_support=int(Lp)))
            k += 1
            wrong += 1
            continue
        p, q = scene.project3(P), scene.project3(Q)
        if not (scene.in_image(p) and scene.in_image(q)) or m.dist(p, q) < 25:
            continue
        obs.append(m.LineObservation(p, q, source="auto", verified=False, line_id=f"AUTO{k}",
                                     endpoint_sigma_px=0.7, n_support=int(m.dist(p, q))))
        k += 1
        wrong += 1
    return obs


def manual_helper(scene, rng, fam, world_seg, noise_px=1.0, line_id="HL"):
    pw, qw = world_seg
    p, q = _noisy(scene.project(pw), scene.project(qw), noise_px, rng)
    return m.LineObservation(p, q, source="manual", verified=True, family=fam, line_id=line_id,
                             endpoint_sigma_px=noise_px)


def far_helper_segment(scene, fam, Aw, rng):
    """Referanstan UZAK, uzun bir gercek kenar (ör. cati hatti / cephe kosesi)."""
    if fam == "ab":
        y = scene.FH * 0.95 if Aw[1] < scene.FH / 2 else scene.FH * 0.05
        return (scene.FW * 0.1, y), (scene.FW * 0.9, y)
    x = scene.FW * 0.95 if Aw[0] < scene.FW / 2 else scene.FW * 0.05
    return (x, scene.FH * 0.1), (x, scene.FH * 0.9)


def reference_observations(A, B, C, sigma_px=1.0):
    ra = m.LineObservation(A, B, source="reference", verified=True, family="ab", line_id="REF-AB",
                           is_reference=True, endpoint_sigma_px=sigma_px)
    rc = m.LineObservation(A, C, source="reference", verified=True, family="ac", line_id="REF-AC",
                           is_reference=True, endpoint_sigma_px=sigma_px)
    return ra, rc


def measurement_errors(scene, H, n=5):
    """Cephe boyunca 1 m'lik yatay ve dusey parcalarin goreli olcum hatalari."""
    hor, ver = [], []
    for i in range(n):
        for j in range(n):
            x = scene.FW * (0.05 + 0.85 * i / (n - 1))
            y = scene.FH * (0.05 + 0.85 * j / (n - 1))
            for fam, (dx, dy), bucket in (("ab", (1.0, 0.0), hor), ("ac", (0.0, 1.0), ver)):
                p, q = scene.project((x, y)), scene.project((x + dx, y + dy))
                try:
                    meas = m.dist(m.apply_transform(H, p), m.apply_transform(H, q))
                except ValueError:
                    meas = float("nan")
                bucket.append(meas / 1.0 - 1.0)
    return np.array(hor), np.array(ver)


def vp_angle_error_deg(v_true, v_est, at):
    a = m.vp_direction_angle_at(v_true, at)
    b = m.vp_direction_angle_at(v_est, at)
    d = abs(a - b) % math.pi
    return math.degrees(min(d, math.pi - d))


def vanishing_line_error(scene, l_est, A_img, n=5):
    """Kacis cizgisi hatasi: cephe noktalarinda goreli projektif derinlik
    w(x)=l.x'in (A'ya normalize) gercek degere gore en buyuk sapmasi."""
    l_true = np.cross(scene.vp("ab"), scene.vp("ac"))
    a = np.array([A_img[0], A_img[1], 1.0])
    worst = 0.0
    for i in range(n):
        for j in range(n):
            p = scene.project((scene.FW * i / (n - 1), scene.FH * j / (n - 1)))
            x = np.array([p[0], p[1], 1.0])
            r = (l_est @ x / (l_est @ a)) / (l_true @ x / (l_true @ a))
            worst = max(worst, abs(r - 1.0))
    return worst


def world_to_image_homography(scene):
    """Cephe duzlemi (X, Y metre) -> goruntu pikseli homografisi: K [r1 r2 t]."""
    t = -scene.R @ scene.Cc
    return scene.K @ np.column_stack([scene.R[:, 0], scene.R[:, 1], t])


def render_facade_image(scene, rng, ppm=60, n_cols=6, n_rows=4):
    """Pencereli bir cephe dokusu cizip perspektifle goruntuye isler
    (gercek LSD tespiti ile uctan uca testler icin). Doner: gri numpy dizi."""
    import cv2
    TW, TH = int(scene.FW * ppm), int(scene.FH * ppm)
    tex = np.full((TH, TW), 150, np.uint8)
    noise = rng.normal(0, 6, tex.shape)
    tex = np.clip(tex + noise, 0, 255).astype(np.uint8)
    cw, rh = scene.FW / n_cols, scene.FH / n_rows
    for i in range(n_cols):
        for j in range(n_rows):
            x0, y0 = (i + 0.25) * cw, (j + 0.25) * rh
            x1, y1 = (i + 0.75) * cw, (j + 0.7) * rh
            u0, u1 = int(x0 * ppm), int(x1 * ppm)
            v0, v1 = int(TH - y1 * ppm), int(TH - y0 * ppm)
            cv2.rectangle(tex, (u0, v0), (u1, v1), 40, -1)
            cv2.rectangle(tex, (u0, v0), (u1, v1), 230, 3)
    cv2.rectangle(tex, (0, 0), (TW - 1, TH - 1), 230, 4)
    T = np.array([[1.0 / ppm, 0, 0], [0, -1.0 / ppm, scene.FH], [0, 0, 1]])
    Htot = world_to_image_homography(scene) @ T
    img = cv2.warpPerspective(tex, Htot, (scene.W, scene.H), flags=cv2.INTER_LINEAR, borderValue=90)
    return cv2.GaussianBlur(img, (3, 3), 0.8)


def make_scene(rng, **kw):
    for _ in range(50):
        try:
            return Scene(rng, **kw)
        except ValueError:
            continue
    raise RuntimeError("sahne uretilemedi")

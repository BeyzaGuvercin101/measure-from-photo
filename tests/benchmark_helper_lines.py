"""Yardimci cizgi / VP dogruluk benchmark'i (sentetik, rastgele sahneler).

Senaryolar:
  A: sadece otomatik cizgi kaniti
  B: otomatik + aile basina 1 elle yardimci cizgi (referanstan uzak, uzun)
  C: otomatik + aile basina 3 elle yardimci cizgi (cepheye yayilmis)

Her senaryo hem ESKI cozucuyle (compute_metric_homography_stratified - bu
degisiklikten onceki ana yol) hem YENI gozlem-tabanli cozucuyle
(compute_metric_homography_from_observations) cozulur. Cozucu None donerse
uygulamadaki gibi yerel afin modele dusulur (basarisizlik orani raporlanir).

Kosullar (her biri ayri tabloda):
  clean        : otomatik dogru cizgiler tum cepheye yayilmis, 12/aile, 12 yanlis cizgi
  local_biased : otomatik dogru cizgiler referans cevresinde (yerel), 6/aile,
                 aile basina sistematik +0.3° aci sapmasi (ör. artik lens
                 distorsiyonu), 15 yanlis cizgi
  sparse       : 2 yerel otomatik cizgi/aile, 15 yanlis cizgi

Sahnelerin %25'inde dusey VP tam sonsuzdadir (kamera egimsiz).

Kullanim:  python tests/benchmark_helper_lines.py [N]   (varsayilan N=120)
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import synthetic_scene as ss  # noqa: E402
m = ss.m

CONDITIONS = {
    "clean": dict(n_true=12, n_wrong=12, bias_deg=0.0, local=False),
    "local_biased": dict(n_true=6, n_wrong=15, bias_deg=0.3, local=True),
    "sparse": dict(n_true=2, n_wrong=15, bias_deg=0.0, local=True),
}


def build_case(rng, cond):
    vert_inf = rng.random() < 0.25
    sc = ss.make_scene(rng, vertical_infinite=vert_inf)
    Aw, Bw, Cw, ab, ac = ss.make_reference(sc, rng)
    A, B, C = (ss._noisy(sc.project(w), sc.project(w), 1.0, rng)[0] for w in (Aw, Bw, Cw))
    region = None
    if cond["local"]:
        r = 0.25
        region = (max(0, Aw[0] - r * sc.FW), min(sc.FW, Aw[0] + r * sc.FW),
                  max(0, Aw[1] - r * sc.FH), min(sc.FH, Aw[1] + r * sc.FH))
    autos = ss.auto_observations(sc, rng, n_true=cond["n_true"], n_wrong=cond["n_wrong"],
                                 noise_px=0.7, bias_deg=cond["bias_deg"], region=region)
    helpers = {"ab": [], "ac": []}
    for fam in ("ab", "ac"):
        segs = [ss.far_helper_segment(sc, fam, Aw, rng)]
        # iki ek, cepheye yayilmis uzun kenar (C senaryosu)
        for frac in (0.35, 0.65):
            if fam == "ab":
                y = sc.FH * frac
                segs.append(((sc.FW * 0.15, y), (sc.FW * 0.85, y)))
            else:
                x = sc.FW * frac
                segs.append(((x, sc.FH * 0.15), (x, sc.FH * 0.85)))
        helpers[fam] = [ss.manual_helper(sc, rng, fam, s, noise_px=1.0, line_id=f"HL-{fam}{k}")
                        for k, s in enumerate(segs)]
    return sc, (A, B, C, ab, ac), autos, helpers, vert_inf


def solve_new(ref, autos, hab, hac, img_size):
    A, B, C, ab, ac = ref
    ra, rc = ss.reference_observations(A, B, C)
    return m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra] + hab + autos,
                                                         [rc] + hac + autos, img_size=img_size)


def solve_old(ref, autos, hab, hac):
    """Degisiklik oncesi uygulama akisi: ilk yardimci = helper, digerleri
    extra; otomatik cizgiler referans acisina +-35° on-filtreyle."""
    A, B, C, ab, ac = ref

    def prefilter(p, q):
        ref_ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        out = []
        for o in autos:
            d = abs(o.angle_deg - ref_ang % 180.0) % 180.0
            if min(d, 180 - d) <= 35.0:
                out.append((o.p1, o.p2))
        return out
    seg = lambda o: (o.p1, o.p2)  # noqa: E731
    return m.compute_metric_homography_stratified(
        A, B, C, ab, ac, 90.0,
        seg(hab[0]) if hab else None, seg(hac[0]) if hac else None,
        [seg(o) for o in hab[1:]], [seg(o) for o in hac[1:]],
        prefilter(A, B), prefilter(A, C))


def evaluate(sc, ref, res):
    A, B, C, ab, ac = ref
    if res is None:
        H = m.fit_affine([A, B, C], [(0, 0), (ab, 0), (0, ac)])
        vp_ab = vp_ac = vl = None
    else:
        H = res["H"]
        vp_ab = ss.vp_angle_error_deg(sc.vp("ab"), res["v_ab_hom"], A)
        vp_ac = ss.vp_angle_error_deg(sc.vp("ac"), res["v_ac_hom"], A)
        vl = ss.vanishing_line_error(sc, res["l_inf"], A)
    h, v = ss.measurement_errors(sc, H)
    allr = np.concatenate([h, v])
    return {"failed": res is None, "conf": (res or {}).get("confidence"), "vp_ab": vp_ab, "vp_ac": vp_ac, "vl": vl,
            "mae_h": float(np.mean(np.abs(h))), "mae_v": float(np.mean(np.abs(v))),
            "drift": float(np.max(allr) - np.min(allr)), "p95": float(np.percentile(np.abs(allr), 95))}


def aggregate(rows):
    out = {"n": len(rows), "fail_rate": float(np.mean([r["failed"] for r in rows]))}
    calib = {}
    for r in rows:
        key = r["conf"] or "AFIN (yedek)"
        calib.setdefault(key, []).append(max(r["mae_h"], r["mae_v"]))
    out["calibration"] = {k: {"n": len(v), "median_mae": float(np.median(v)),
                              "frac_over_5pct": float(np.mean(np.array(v) > 0.05))} for k, v in calib.items()}
    for k in ("vp_ab", "vp_ac", "vl", "mae_h", "mae_v", "drift", "p95"):
        vals = np.array([r[k] for r in rows if r[k] is not None], dtype=float)
        vals = vals[np.isfinite(vals)]
        out[k] = {"mean": float(np.mean(vals)) if len(vals) else None,
                  "median": float(np.median(vals)) if len(vals) else None,
                  "p95": float(np.percentile(vals, 95)) if len(vals) else None}
    return out


def run(n=120, seed=12345):
    results = {}
    for cname, cond in CONDITIONS.items():
        rng = np.random.default_rng(seed)
        rows = {(s, solver): [] for s in "ABC" for solver in ("old", "new")}
        t0 = time.time()
        for _ in range(n):
            sc, ref, autos, helpers, _vi = build_case(rng, cond)
            img_size = (sc.W, sc.H)
            for s, k in (("A", 0), ("B", 1), ("C", 3)):
                hab, hac = helpers["ab"][:k], helpers["ac"][:k]
                rows[(s, "old")].append(evaluate(sc, ref, solve_old(ref, autos, hab, hac)))
                rows[(s, "new")].append(evaluate(sc, ref, solve_new(ref, autos, hab, hac, img_size)))
        results[cname] = {f"{s}/{solver}": aggregate(r) for (s, solver), r in rows.items()}
        results[cname]["_seconds"] = time.time() - t0
    return results


def print_tables(results):
    def f(x, scale=1.0, nd=3):
        return "-" if x is None else f"{x * scale:.{nd}f}"
    for cname, res in results.items():
        print(f"\n### {cname}  (N={res['A/old']['n']}, {res['_seconds']:.0f}s)")
        print("| senaryo/cozucu | afin yedege dustu | VP_AB ort/p95 (°) | VP_AC ort/p95 (°) | kacis cizgisi hatasi "
              "medyan (%) | MAE yatay ort/medyan (%) | MAE dusey ort/medyan (%) | olcek kaymasi medyan (%) "
              "| sahne-ici p95 |hata| medyan (%) |")
        print("|---|---|---|---|---|---|---|---|---|")
        for key in ("A/old", "A/new", "B/old", "B/new", "C/old", "C/new"):
            r = res[key]
            print(f"| {key} | {r['fail_rate'] * 100:.0f}% | {f(r['vp_ab']['mean'])} / {f(r['vp_ab']['p95'])} "
                  f"| {f(r['vp_ac']['mean'])} / {f(r['vp_ac']['p95'])} | {f(r['vl']['median'], 100, 2)} "
                  f"| {f(r['mae_h']['mean'], 100, 1)} / {f(r['mae_h']['median'], 100, 2)} "
                  f"| {f(r['mae_v']['mean'], 100, 1)} / {f(r['mae_v']['median'], 100, 2)} "
                  f"| {f(r['drift']['median'], 100, 2)} | {f(r['p95']['median'], 100, 2)} |")
        print("\nYeni cozucunun guven etiketi kalibrasyonu (sahne basina max(MAE yatay, MAE dusey)):")
        for key in ("A/new", "B/new", "C/new"):
            cal = res[key]["calibration"]
            parts = [f"{k}: n={v['n']}, medyan %{v['median_mae'] * 100:.2f}, >%5 hata orani %{v['frac_over_5pct'] * 100:.0f}"
                     for k, v in sorted(cal.items())]
            print(f"  {key}: " + " | ".join(parts))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    res = run(n)
    print_tables(res)
    out = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(f"\nJSON: {out}")

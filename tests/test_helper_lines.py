"""Yardimci cizgi + saglam VP testleri.

Calistirma:  python -m pytest tests -q
Cekirdek testler sentetik, rastgele sahnelerde calisir (fotografa ozel
ayar yok). Uygulama (Tk) testleri ekran gerektirir; Tk acilamazsa atlanir.
"""
import json
import math
import os
import re
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(__file__))
import synthetic_scene as ss  # noqa: E402
import benchmark_helper_lines as bh  # noqa: E402

m = ss.m
ACCEPT = ("accept", "accept_validated", "accept_unvalidated")


# ---------------------------------------------------------------- cekirdek

def test_line_sigma_reflects_measurement_uncertainty():
    short = m.LineObservation((0, 0), (100, 0), endpoint_sigma_px=1.0)
    long_ = m.LineObservation((0, 0), (1000, 0), endpoint_sigma_px=1.0)
    refined = m.LineObservation((0, 0), (1000, 0), endpoint_sigma_px=0.3, n_support=300)
    auto = m.LineObservation((0, 0), (1000, 0), endpoint_sigma_px=1.0, verified=False)
    assert long_.sigma_angle_deg < short.sigma_angle_deg
    assert refined.sigma_angle_deg < long_.sigma_angle_deg
    assert auto.sigma_angle_deg > long_.sigma_angle_deg  # dogrulanmamis -> model belirsizligi tabani
    # cok uzun bir cizgi bile sifir belirsizlige inmez (uzun != otomatik dogru)
    huge = m.LineObservation((0, 0), (1e6, 0), verified=False)
    assert huge.sigma_angle_deg >= m.LINE_MODEL_SIGMA_DEG_UNVERIFIED


def test_vanishing_point_at_infinity_is_valid():
    obs = [m.LineObservation((0, y), (1000, y + 0.0), line_id=f"L{k}", is_reference=(k == 0))
           for k, y in enumerate((0, 200, 400, 650))]
    est = m.estimate_vp_weighted(obs)
    assert est is not None, "paralel aile None'a cevrilmemeli"
    v = est["v"]
    assert abs(v[2]) < 1e-6 and abs(v[1]) < 1e-6  # ideal nokta (1,0,0)
    assert est["n_inliers"] == 4


def _case(rng, cond="clean", **scene_kw):
    sc = ss.make_scene(rng, **scene_kw)
    Aw, Bw, Cw, ab, ac = ss.make_reference(sc, rng)
    A, B, C = (ss._noisy(sc.project(w), sc.project(w), 1.0, rng)[0] for w in (Aw, Bw, Cw))
    c = bh.CONDITIONS[cond]
    region = None
    if c["local"]:
        region = (max(0, Aw[0] - 0.25 * sc.FW), min(sc.FW, Aw[0] + 0.25 * sc.FW),
                  max(0, Aw[1] - 0.25 * sc.FH), min(sc.FH, Aw[1] + 0.25 * sc.FH))
    autos = ss.auto_observations(sc, rng, n_true=c["n_true"], n_wrong=c["n_wrong"], noise_px=0.7,
                                 bias_deg=c["bias_deg"], region=region)
    return sc, Aw, (A, B, C, ab, ac), autos


def test_abc_d_workflow_preserved():
    """A/B/C + iki uzunluk -> T_metric TAM, D sadece H'den SONRA turetilir."""
    rng = np.random.default_rng(1)
    for _ in range(10):
        sc, Aw, (A, B, C, ab, ac), autos = _case(rng)
        ra, rc = ss.reference_observations(A, B, C)
        res = m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra] + autos, [rc] + autos,
                                                            img_size=(sc.W, sc.H))
        assert res is not None
        assert abs(res["ab_recovered"] - ab) < 1e-6 and abs(res["ac_recovered"] - ac) < 1e-6
        assert abs(res["angle_recovered_deg"] - 90.0) < 1e-6
        D_expected = m.apply_transform(res["Hinv"], (ab, ac))
        assert m.dist(D_expected, res["D_img"]) < 1e-6
        # l_inf = v_AB x v_AC (kademeli mimari)
        l = np.cross(res["v_ab_hom"], res["v_ac_hom"])
        l = l / math.hypot(l[0], l[1])
        assert np.allclose(np.abs(l), np.abs(res["l_inf"]), atol=1e-9)


def test_legacy_stratified_solver_unchanged_interface():
    rng = np.random.default_rng(2)
    sc, Aw, (A, B, C, ab, ac), autos = _case(rng)
    segs = [(o.p1, o.p2) for o in autos]
    res = m.compute_metric_homography_stratified(A, B, C, ab, ac, 90.0, None, None, [], [], segs, segs)
    assert res is not None and abs(res["ab_recovered"] - ab) < 1e-6


def test_auto_family_suggestion_uses_vp_consistency():
    rng = np.random.default_rng(3)
    ok, ambiguous_right = 0, 0
    for t in range(12):
        sc, Aw, (A, B, C, ab, ac), autos = _case(rng)
        ra, rc = ss.reference_observations(A, B, C)
        res = m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra] + autos, [rc] + autos,
                                                            img_size=(sc.W, sc.H))
        fam = "ab" if t % 2 == 0 else "ac"
        line = ss.manual_helper(sc, rng, "auto", ss.far_helper_segment(sc, fam, Aw, rng), line_id="X")
        sug, zs = m.suggest_line_family(line, res)
        ok += sug == fam
        # rastgele yonlu bir cizgi icin oneri YAPILMAMALI (belirsiz)
        p = (sc.W * 0.3, sc.H * 0.3)
        a = math.radians(45 + 90 * (t % 2))
        rnd = m.LineObservation(p, (p[0] + 400 * math.cos(a), p[1] + 400 * math.sin(a)), line_id="R")
        s2, _ = m.suggest_line_family(rnd, res)
        ambiguous_right += s2 is None
    assert ok >= 11, ok
    assert ambiguous_right >= 10, ambiguous_right


def test_one_correct_far_helper_improves_biased_auto_vp():
    """Bolum 33: otomatik VP hafif yanli + referanstan uzak, dogru, uzun bir
    yardimci cizgi -> gercek VP hatasi ve olcum hatasi azalmali; yeni modelin
    tahmini belirsizligi ya da bagimsiz kalintisi iyilesmeli."""
    rng = np.random.default_rng(33)
    vp_better, mae_b, mae_a, unc_or_val_better, verdicts, n = 0, [], [], 0, [], 0
    while n < 25:
        sc, Aw, (A, B, C, ab, ac), autos = _case(rng, "local_biased")
        ra, rc = ss.reference_observations(A, B, C)
        helper = ss.manual_helper(sc, rng, "ab", ss.far_helper_segment(sc, "ab", Aw, rng), line_id="HL1")
        a = m.assess_helper_addition(A, B, C, ab, ac, 90.0, [ra] + autos, [rc] + autos, helper,
                                     img_size=(sc.W, sc.H))
        if a["before_result"] is None or a["after_result"] is None:
            continue
        n += 1
        verdicts.append(a["verdict"])
        b, af = a["before_result"], a["after_result"]
        vp_far_b = ss.vp_angle_error_deg(sc.vp("ab"), b["v_ab_hom"], helper.midpoint)
        vp_far_a = ss.vp_angle_error_deg(sc.vp("ab"), af["v_ab_hom"], helper.midpoint)
        vp_better += (vp_far_a < vp_far_b)
        hb, _ = ss.measurement_errors(sc, b["H"])
        ha, _ = ss.measurement_errors(sc, af["H"])
        mae_b.append(np.mean(np.abs(hb)))
        mae_a.append(np.mean(np.abs(ha)))
        sb, sa = a["before"], a["after"]
        better_unc = sa["vp_unc_deg_ab"] < sb["vp_unc_deg_ab"]
        better_val = (sa["holdout_rms_z_ab"] is not None and sb["holdout_rms_z_ab"] is not None
                      and sa["holdout_rms_z_ab"] <= sb["holdout_rms_z_ab"])
        unc_or_val_better += better_unc or better_val
    print("verdicts:", {v: verdicts.count(v) for v in set(verdicts)})
    print(f"MAE yatay once {np.mean(mae_b) * 100:.2f}% -> sonra {np.mean(mae_a) * 100:.2f}%")
    assert np.mean(mae_a) < np.mean(mae_b)
    assert vp_better >= 0.7 * n, (vp_better, n)
    assert unc_or_val_better >= 0.8 * n, (unc_or_val_better, n)


def test_wrong_helper_is_flagged_and_does_not_replace_model():
    """Bolum 34: kasitli yanlis yardimci cizgi (yan duvarin yatay kenari /
    cepheye gore 4° egik bir kenar) tespit edilmeli; aday model degerlendirilir
    ama otomatik kabul edilmez."""
    rng = np.random.default_rng(34)
    flagged, n = 0, 0
    while n < 30:
        sc, Aw, (A, B, C, ab, ac), autos = _case(rng)
        ra, rc = ss.reference_observations(A, B, C)
        good = ss.manual_helper(sc, rng, "ab", ss.far_helper_segment(sc, "ab", Aw, rng), line_id="HL1")
        if n % 2 == 0:  # yan duvar (X=FW duzlemi) uzerinde Z yonunde kenar
            y = float(rng.uniform(0.2, 0.8)) * sc.FH
            p, q = sc.project3((sc.FW, y, -0.3)), sc.project3((sc.FW, y, -6.0))
            if p is None or q is None or m.dist(p, q) < 80:
                continue
        else:  # cephe uzerinde ama 4° egik (gercekte paralel olmayan) kenar
            y = sc.FH * 0.5
            p, q = sc.project((sc.FW * 0.1, y)), sc.project((sc.FW * 0.9, y + math.tan(math.radians(4)) * sc.FW * 0.8))
        wrong = m.LineObservation(p, q, family="ab", line_id="HLX", endpoint_sigma_px=1.0)
        before = m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra, good] + autos,
                                                               [rc] + autos, img_size=(sc.W, sc.H))
        a = m.assess_helper_addition(A, B, C, ab, ac, 90.0, [ra, good] + autos, [rc] + autos, wrong,
                                     img_size=(sc.W, sc.H))
        n += 1
        flagged += a["verdict"] not in ACCEPT
        # degerlendirme mevcut modeli DEGISTIRMEZ (yan etkisiz)
        assert np.allclose(before["H"], a["before_result"]["H"])
    assert flagged >= 0.9 * n, (flagged, n)


def test_distributed_helpers_beat_clustered_helpers():
    """Bolum 35: 100x100 px icinde toplanmis 3 yardimci cizgi vs cepheye
    yayilmis 3 yardimci cizgi (otomatik kanit YOK, sadece referans+yardimci)."""
    rng = np.random.default_rng(35)
    unc_better, err_better, n = 0, 0, 0
    while n < 25:
        sc = ss.make_scene(rng)
        Aw, Bw, Cw, ab, ac = ss.make_reference(sc, rng)
        A, B, C = (ss._noisy(sc.project(w), sc.project(w), 1.0, rng)[0] for w in (Aw, Bw, Cw))
        ra, rc = ss.reference_observations(A, B, C)

        def helpers(fam, spread):
            out = []
            for k in range(3):
                if spread:
                    if fam == "ab":
                        y = sc.FH * (0.1 + 0.4 * k)
                        seg = ((sc.FW * 0.1, y), (sc.FW * 0.9, y))
                    else:
                        x = sc.FW * (0.1 + 0.4 * k)
                        seg = ((x, sc.FH * 0.1), (x, sc.FH * 0.9))
                    out.append(ss.manual_helper(sc, rng, fam, seg, line_id=f"{fam}{k}"))
                else:  # 100x100 px kume (referansin yaninda)
                    c0 = (A[0] + 60, A[1] - 60)
                    vtrue = sc.vp(fam)
                    ang = m.vp_direction_angle_at(vtrue, (c0[0], c0[1] + 30 * k))
                    p = (c0[0], c0[1] + 30 * k)
                    q = (p[0] + 90 * math.cos(ang), p[1] + 90 * math.sin(ang))
                    p, q = ss._noisy(p, q, 1.0, rng)
                    out.append(m.LineObservation(p, q, family=fam, line_id=f"{fam}{k}"))
            return out
        rs = m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra] + helpers("ab", True),
                                                           [rc] + helpers("ac", True), img_size=(sc.W, sc.H))
        rcl = m.compute_metric_homography_from_observations(A, B, C, ab, ac, 90.0, [ra] + helpers("ab", False),
                                                            [rc] + helpers("ac", False), img_size=(sc.W, sc.H))
        if rs is None or rcl is None:
            continue
        n += 1
        unc_better += (rs["scale_unc_far"] or 9) < (rcl["scale_unc_far"] or 9)
        es = np.concatenate(ss.measurement_errors(sc, rs["H"]))
        ec = np.concatenate(ss.measurement_errors(sc, rcl["H"]))
        err_better += np.percentile(np.abs(es), 95) < np.percentile(np.abs(ec), 95)
        assert rs["families"]["ab"]["spatial"]["perp_span_frac"] > rcl["families"]["ab"]["spatial"]["perp_span_frac"]
    assert unc_better >= 0.9 * n, (unc_better, n)
    assert err_better >= 0.8 * n, (err_better, n)


def test_ambiguous_sparse_auto_evidence_is_not_trusted():
    """Seyrek otomatik kanit + yanlis duzlem cizgileri: aile 'belirsiz'
    isaretlenmeli ve projektif model KURULMAMALI (yardimci cizgi istenir)."""
    rng = np.random.default_rng(5)
    declined, n = 0, 0
    for _ in range(20):
        sc, Aw, (A, B, C, ab, ac), autos = _case(rng, "sparse")
        ra, rc = ss.reference_observations(A, B, C)
        stage = m.estimate_family_vps([ra] + autos, [rc] + autos, A, img_size=(sc.W, sc.H))
        n += 1
        if not stage["ok"]:
            declined += 1
            assert stage["reasons"]
    assert declined >= 0.8 * n, (declined, n)


def _step_edge_image(w, h, line, lo=60.0, hi=190.0, ss_factor=8, noise=2.0, seed=0):
    """Bilinen (subpixel) dogru l.x=0 boyunca keskin basamak kenari - alan
    ornekleme (supersampling) ile antialias, hafif Gauss gurultusu."""
    ys, xs = np.mgrid[0:h * ss_factor, 0:w * ss_factor]
    X = (xs + 0.5) / ss_factor - 0.5
    Y = (ys + 0.5) / ss_factor - 0.5
    side = (line[0] * X + line[1] * Y + line[2]) > 0
    frac = side.reshape(h, ss_factor, w, ss_factor).mean(axis=(1, 3))
    img = lo + (hi - lo) * frac + np.random.default_rng(seed).normal(0, noise, (h, w))
    return np.clip(img, 0, 255).astype(np.uint8)


def test_subpixel_refinement_on_known_edge():
    l_true = m._line_through((40.0, 200.3), (560.0, 248.9))
    l_true = l_true / math.hypot(l_true[0], l_true[1])
    gray = _step_edge_image(600, 400, l_true)
    p, q = (60.0, 202.2 + 1.6), (540.0, 247.0 - 1.4)  # kaba tiklama: ~1.5 px hata
    ref, why = m.refine_line_to_edge(gray, p, q)
    assert ref is not None, why
    d_rough = max(abs(l_true @ np.array([x, y, 1.0])) for x, y in (p, q))
    d_ref = max(abs(l_true @ np.array([x, y, 1.0])) for x, y in (ref["p1"], ref["p2"]))
    assert d_rough > 1.0 and d_ref < 0.25, (d_rough, d_ref)
    # inceltilmis cizginin aci belirsizligi daha kucuk olmali
    o_r = m.LineObservation(ref["p1"], ref["p2"], source="manual_refined", endpoint_sigma_px=max(0.1, ref["rms_px"]),
                            n_support=ref["n_support"])
    o_m = m.LineObservation(p, q, source="manual", endpoint_sigma_px=1.0)
    assert o_r.sigma_angle_deg < o_m.sigma_angle_deg
    # duz, dokusuz bir bolgede inceltme ZORLANMAMALI
    flat = np.full((400, 400), 120, np.uint8)
    ref2, why2 = m.refine_line_to_edge(flat, (50, 200), (350, 210))
    assert ref2 is None and why2


def test_no_image_specific_scale_corrections_in_source():
    src = open(m.__file__, encoding="utf-8").read()
    assert not re.search(r"(vertical|horizontal)_scale\s*\*=", src)
    assert "current_photo" not in src


# ---------------------------------------------------------------- uygulama (Tk)

@pytest.fixture(scope="module")
def app(tmp_path_factory):
    try:
        m.messagebox.askyesno = lambda *a, **k: True
        m.messagebox.showinfo = lambda *a, **k: None
        m.messagebox.showerror = lambda *a, **k: None
        a = m.MeasureApp()
    except Exception as e:  # ekran yok
        pytest.skip(f"Tk acilamadi: {e}")
    a.withdraw()
    a.helper_prompt_var.set(False)
    a.magnifier_var.set(False)
    a._answers = []
    a._choice_dialog = lambda title, text, buttons, default=None: a._answers.pop(0) if a._answers else default
    rng = np.random.default_rng(11)
    sc = ss.make_scene(rng, img_size=(1600, 1200), az_deg=30, el_deg=-12, facade=(20, 12))
    from PIL import Image
    path = str(tmp_path_factory.mktemp("img") / "facade.png")
    Image.fromarray(ss.render_facade_image(sc, rng)).save(path)
    assert a._load_photo(path)
    a._scene = sc
    a._img_path = path
    yield a
    a.destroy()


def _setup_reference(app):
    sc = app._scene
    app._reset_state_for_new_photo()
    cw, rh = 20 / 6, 12 / 4
    W = {"A": (1.25 * cw, 1.25 * rh), "B": (1.75 * cw, 1.25 * rh), "C": (1.25 * cw, 1.7 * rh)}
    for lb, w in W.items():
        x, y = sc.project(w)
        app.points.append({"label": lb, "x": x, "y": y, "source": "manual"})
    app._refresh_all_display()
    for cb, lb in zip(app.abc_combos, "ABC"):
        cb.set(lb)
    app.abc_len_entries[0].insert(0, f"{W['B'][0] - W['A'][0]:.4f}")
    app.abc_len_entries[1].insert(0, f"{W['C'][1] - W['A'][1]:.4f}")
    app._recompute_plane(silent=True)
    return W


def test_app_helper_lines_are_separate_from_points(app):
    _setup_reference(app)
    n_points = len(app.points)
    sc = app._scene
    app.start_helper_capture("ab")
    assert app.helper_capture is not None
    app._helper_capture_add_endpoint(*sc.project((1.0, 11.0)), "manual")
    app._answers[:] = ["keep"]
    app._helper_capture_add_endpoint(*sc.project((19.0, 11.0)), "manual")
    assert len(app.points) == n_points
    assert len(app.helper_lines) == 1 and app.helper_lines[0]["family"] == "ab"
    assert app.helper_capture is None
    assert app.plane_d_route == "stratified"
    st = app.plane_strat_result["families"]["ab"]
    assert st["n_verified_helpers"] == 1  # yardimci cizgi gercekten cozucuye girdi


def test_app_escape_cancels_capture(app):
    _setup_reference(app)
    app.start_helper_capture("ac")
    app._helper_capture_add_endpoint(100.0, 100.0, "manual")
    app.cancel_helper_capture()
    assert app.helper_capture is None and not app.helper_lines


def test_app_wrong_helper_rejected_keeps_model(app):
    _setup_reference(app)
    H0 = app.plane_H.copy()
    sc = app._scene
    app.start_helper_capture("ab")
    app._helper_capture_add_endpoint(*sc.project((10.0, 0.5)), "manual")  # dusey kenar, AB diye
    app._answers[:] = ["delete"]
    app._helper_capture_add_endpoint(*sc.project((10.0, 11.0)), "manual")
    assert not app.helper_lines
    assert np.allclose(H0, app.plane_H)


def test_app_anchor_detached_on_point_delete(app):
    _setup_reference(app)
    sc = app._scene
    app.start_helper_capture("ab", anchor_label="B")
    app._answers[:] = ["keep"]
    app._helper_capture_add_endpoint(*sc.project((15.0, 3.75)), "manual")
    hl = app.helper_lines[0]
    p1_before = list(hl["p1"])
    assert hl["anchor_label"] == "B"
    app.tree.selection_set("B")
    app.delete_point()
    assert hl["anchor_label"] is None and hl["p1"] == p1_before and "silindi" in hl["note"]


def test_app_json_roundtrip_and_old_config(app, tmp_path):
    _setup_reference(app)
    sc = app._scene
    app.start_helper_capture("ac")
    app._helper_capture_add_endpoint(*sc.project((19.9, 0.5)), "manual")
    app._answers[:] = ["keep"]
    app._helper_capture_add_endpoint(*sc.project((19.9, 11.5)), "manual")
    H_saved = app.plane_H.copy()
    p = str(tmp_path / "cfg.json")
    m.filedialog.asksaveasfilename = lambda **k: p
    app.save_config()
    cfg = json.load(open(p, encoding="utf-8"))
    assert cfg["helper_lines"] and cfg["plane"]["H_final"] and cfg["plane"]["vp"]
    m.filedialog.askopenfilename = lambda **k: p
    app.load_config()
    assert [h["id"] for h in app.helper_lines] == [h["id"] for h in cfg["helper_lines"]]
    assert np.allclose(H_saved / H_saved[2, 2], app.plane_H / app.plane_H[2, 2])

    # ESKI bicim: "helper_lines" alani yok, yardimci cizgi nokta etiketleriyle
    pts = [{"label": q["label"], "x": q["x"], "y": q["y"]} for q in app.points]
    for lb, w in (("E", (1.0, 11.0)), ("F", (19.0, 11.0))):
        x, y = sc.project(w)
        pts.append({"label": lb, "x": x, "y": y})
    old = {"photo_path": app._img_path, "image_size": list(app.pil_img.size), "ref_mode": "abc2len",
           "image_points": pts, "queries": [], "saved_planes": [],
           "plane": {"mode": "abc2len", "labels": ["A", "B", "C"], "ab_m": cfg["plane"]["ab_m"],
                     "ac_m": cfg["plane"]["ac_m"], "angle_deg": 90.0,
                     "helper_ab_labels": ["E", "F"], "helper_ac_labels": None}}
    p2 = str(tmp_path / "old.json")
    json.dump(old, open(p2, "w"))
    m.filedialog.askopenfilename = lambda **k: p2
    app.load_config()
    assert [h["id"] for h in app.helper_lines] == ["P-AB"]
    assert app.helper_lines[0]["point_labels"] == ["E", "F"]
    assert [cb.get() for cb in app.abc_helper_ab_combos] == ["E", "F"]
    assert app.plane_calibrated and app.plane_corners == ["A", "B", "C"]
    assert app.plane_strat_result["families"]["ab"]["n_verified_helpers"] == 1

    # tamamen bos/eksik alanli bir eski config de cokmemeli
    p3 = str(tmp_path / "older.json")
    json.dump({"photo_path": app._img_path, "image_points": pts, "queries": []}, open(p3, "w"))
    m.filedialog.askopenfilename = lambda **k: p3
    app.load_config()
    assert app.helper_lines == []

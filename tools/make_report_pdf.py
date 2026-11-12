"""Builds the final PDF report (A4, page border, header/footer, aligned tables)."""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

OUT = r"C:\Users\aryan\OneDrive\Desktop\weather_module\satellite_module\docs\Drought_Early_Warning_Final_Report.pdf"

pdfmetrics.registerFont(TTFont("Cal", r"C:\Windows\Fonts\calibri.ttf"))
pdfmetrics.registerFont(TTFont("CalB", r"C:\Windows\Fonts\calibrib.ttf"))
pdfmetrics.registerFont(TTFont("CalI", r"C:\Windows\Fonts\calibrii.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Cal", normal="Cal", bold="CalB", italic="CalI", boldItalic="CalB")

NAVY = colors.HexColor("#1F3A5F")
ACCENT = colors.HexColor("#2E6DA4")
LIGHT = colors.HexColor("#EAF1F8")
GRID = colors.HexColor("#9DB3CC")
INK = colors.HexColor("#1A1A1A")
GREY = colors.HexColor("#5A5A5A")

PW, PH = A4
MARGIN = 2.2 * cm
FRAME_W = PW - 2 * MARGIN

S = {
    "title": ParagraphStyle("title", fontName="CalB", fontSize=24, leading=30, textColor=NAVY, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", fontName="Cal", fontSize=13, leading=18, textColor=GREY, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="CalB", fontSize=15, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="CalB", fontSize=11.5, leading=15, textColor=ACCENT, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    "body": ParagraphStyle("body", fontName="Cal", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=5, alignment=4),
    "intro": ParagraphStyle("intro", fontName="Cal", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=5,
                            alignment=4, keepWithNext=1),
    "lead": ParagraphStyle("lead", fontName="CalI", fontSize=10.5, leading=14.5, textColor=GREY, spaceAfter=6, alignment=4),
    "bullet": ParagraphStyle("bullet", fontName="Cal", fontSize=10.5, leading=14, textColor=INK, leftIndent=14,
                             bulletIndent=3, spaceAfter=2.5, alignment=TA_LEFT),
    "ref": ParagraphStyle("ref", fontName="Cal", fontSize=9.5, leading=12.5, textColor=INK, leftIndent=24,
                          bulletIndent=0, bulletFontName="Cal", spaceAfter=2),
    "cell": ParagraphStyle("cell", fontName="Cal", fontSize=9, leading=11.5, textColor=INK),
    "cellc": ParagraphStyle("cellc", fontName="Cal", fontSize=9, leading=11.5, textColor=INK, alignment=TA_CENTER),
    "head": ParagraphStyle("head", fontName="CalB", fontSize=9, leading=11.5, textColor=colors.white),
    "headc": ParagraphStyle("headc", fontName="CalB", fontSize=9, leading=11.5, textColor=colors.white, alignment=TA_CENTER),
    "cap": ParagraphStyle("cap", fontName="CalI", fontSize=9, leading=12, textColor=GREY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8),
    "key": ParagraphStyle("key", fontName="Cal", fontSize=10.5, leading=14.5, textColor=INK),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


def table(rows, widths, center_from=1, bold_rows=(), zebra=True):
    """rows[0] = header. widths in fractions of the frame width (sum 1). Text wraps inside cells."""
    w = [f * FRAME_W for f in widths]
    data = []
    for i, r in enumerate(rows):
        out = []
        for j, c in enumerate(r):
            if i == 0:
                st = "headc" if j >= center_from else "head"
            else:
                st = "cellc" if j >= center_from else "cell"
            txt = f"<b>{c}</b>" if (i in bold_rows and i > 0) else str(c)
            out.append(Paragraph(txt, S[st]))
        data.append(out)
    t = Table(data, colWidths=w, repeatRows=1, hAlign="CENTER")
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("BOX", (0, 0), (-1, -1), 0.9, NAVY),
             ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if zebra:
        for i in range(1, len(rows)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def keybox(lines):
    t = Table([[Paragraph("<b>Key results</b>", S["h2"])]] + [[Paragraph("• " + l, S["key"])] for l in lines],
              colWidths=[FRAME_W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.1, ACCENT), ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def system_diagram():
    w, h = FRAME_W, 150
    d = Drawing(w, h)
    bw, bh, gap = (w - 2 * 36) / 3, 72, 36
    ys = h - bh - 6
    titles = [("1  Weather: predict", ["AgERA5, 6 cells, 1979-2026", "Physics + ML hybrid", "Output: drought alarm"]),
              ("2  Satellite: confirm", ["Sentinel-2, 240 fields", "Crop SVI every 5 days", "Output: stressed fields"]),
              ("3  UAV: quantify", ["Drone survey of flagged", "fields (UAV team)", "Output: damaged area"])]
    for i, (t, lines) in enumerate(titles):
        x = i * (bw + gap)
        fill = LIGHT if i == 1 else colors.white
        stroke = ACCENT if i == 1 else NAVY
        r = Rect(x, ys, bw, bh, rx=6, ry=6, fillColor=fill, strokeColor=stroke, strokeWidth=1.6 if i == 1 else 1)
        if i == 2:
            r.strokeDashArray = [4, 3]
        d.add(r)
        d.add(String(x + 9, ys + bh - 17, t, fontName="CalB", fontSize=11, fillColor=NAVY))
        for k, l in enumerate(lines):
            d.add(String(x + 9, ys + bh - 34 - 13 * k, l, fontName="Cal", fontSize=9.5,
                         fillColor=INK if k == 2 else GREY))
        if i < 2:
            x1, x2, yy = x + bw + 4, x + bw + gap - 4, ys + bh / 2
            d.add(Line(x1, yy, x2 - 6, yy, strokeColor=NAVY, strokeWidth=1.2))
            d.add(Polygon([x2, yy, x2 - 7, yy + 4, x2 - 7, yy - 4], fillColor=NAVY, strokeColor=NAVY))
    cx = bw + gap + bw / 2
    d.add(Line(cx, ys - 4, cx, 36, strokeColor=NAVY, strokeWidth=1.2))
    d.add(Polygon([cx, 30, cx - 4, 37, cx + 4, 37], fillColor=NAVY, strokeColor=NAVY))
    d.add(Rect(cx - 95, 2, 190, 26, rx=6, ry=6, fillColor=colors.HexColor("#F2F2F2"), strokeColor=NAVY, strokeWidth=1))
    d.add(String(cx, 11, "Checked: AP and Karnataka drought orders", fontName="Cal", fontSize=9.5,
                 fillColor=INK, textAnchor="middle"))
    return d


def weather_chart():
    hz = ["7 days", "15 days", "30 days"]
    series = [("Persistence", [0.662, 0.515, 0.424], "#B8B8B8"),
              ("Physics only (water balance)", [0.783, 0.592, 0.375], "#8FB3D9"),
              ("Hybrid (physics + ML)", [0.819, 0.651, 0.424], "#1F3A5F")]
    fig, ax = plt.subplots(figsize=(6.6, 2.9), dpi=200)
    x = range(3)
    bw = 0.26
    for k, (n, v, c) in enumerate(series):
        pos = [i + (k - 1) * bw for i in x]
        b = ax.bar(pos, v, bw, label=n, color=c, edgecolor="white")
        for p_, val in zip(pos, v):
            ax.text(p_, val + 0.012, f"{val:.2f}", ha="center", va="bottom", fontsize=7.5, color="#1A1A1A")
    ax.set_xticks(list(x))
    ax.set_xticklabels(hz, fontsize=9)
    ax.set_ylim(0, 0.95)
    ax.set_ylabel("Macro-F1 (test 2019-2026)", fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", color="#E0E0E0", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.13))
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img = Image(buf, width=FRAME_W * 0.84, height=FRAME_W * 0.84 * 2.9 / 6.6)
    img.hAlign = "CENTER"
    return img


def on_page(c, doc):
    c.saveState()
    inset = 1.1 * cm
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.4)
    c.rect(inset, inset, PW - 2 * inset, PH - 2 * inset)
    c.setLineWidth(0.4)
    c.rect(inset + 3, inset + 3, PW - 2 * inset - 6, PH - 2 * inset - 6)
    if doc.page > 1:
        c.setFont("Cal", 8.5)
        c.setFillColor(GREY)
        c.drawString(MARGIN, PH - 1.65 * cm, "Weather-to-Satellite Drought Early Warning, Rayalaseema")
        c.drawRightString(PW - MARGIN, PH - 1.65 * cm, "DeepDroughtUAV project | November 2026")
        c.setStrokeColor(GRID)
        c.line(MARGIN, PH - 1.8 * cm, PW - MARGIN, PH - 1.8 * cm)
        c.line(MARGIN, 1.85 * cm, PW - MARGIN, 1.85 * cm)
        c.drawCentredString(PW / 2, 1.5 * cm, f"Page {doc.page}")
    c.restoreState()


def build():
    import os
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=2.3 * cm,
                            bottomMargin=2.3 * cm, title="Weather-to-Satellite Drought Early Warning: Final Results",
                            author="Aryan Rajesh Gadam")
    st = []
    # ---------------- title page
    st += [Spacer(1, 4.2 * cm), P("Weather-to-Satellite Drought Early Warning<br/>for Rayalaseema", "title"),
           Spacer(1, 10), P("Final results of stages 1-2: weather forecasting and satellite confirmation", "sub"),
           Spacer(1, 1.2 * cm)]
    meta = Table([[P("<b>Project</b>", "cell"), P("DeepDroughtUAV: drought-area estimation in the Anantapur cluster", "cell")],
                  [P("<b>Prepared by</b>", "cell"), P("Aryan Rajesh Gadam", "cell")],
                  [P("<b>Date</b>", "cell"), P("12 November 2026", "cell")],
                  [P("<b>Study area</b>", "cell"), P("8 farming areas in Sri Sathya Sai and Kurnool (Andhra Pradesh) and Tumakuru (Karnataka)", "cell")],
                  [P("<b>Code and data</b>", "cell"), P("github.com/ARYAN3012-G/weather_time_series<br/>github.com/ARYAN3012-G/Sentinel2-Drought-Confirmation", "cell")]],
                 colWidths=[0.27 * FRAME_W, 0.73 * FRAME_W], hAlign="CENTER")
    meta.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, NAVY), ("INNERGRID", (0, 0), (-1, -1), 0.4, GRID),
                              ("BACKGROUND", (0, 0), (0, -1), LIGHT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    st += [meta, PageBreak()]

    # ---------------- 1 summary
    st += [P("1. Summary", "h1"),
           P("A weather-to-satellite early-warning chain for rainfed farmland confirmed every severe drought season "
             "declared in 2023-2026 (9 of 9, Andhra Pradesh and Karnataka) and stayed silent in 10 of 11 seasons with no "
             "declaration. All results are on held-out years, with leakage tests, physical and statistical baselines and "
             "confidence intervals."),
           keybox(["<b>Weather stage:</b> drought class 7 days ahead with 85.6% balanced accuracy (68.3% at 15 days); "
                   "macro-F1 0.819 / 0.651 vs 0.662 / 0.515 for persistence.",
                   "<b>Physics matters:</b> a water-balance ensemble alone reaches 0.783 at 7 days; machine learning adds "
                   "significant skill at 15 days; nothing is skilful at 30 days.",
                   "<b>Crops follow weather:</b> rainfed crop greenness (SVI) follows 30-day SPEI 10 days earlier "
                   "(ρ 0.48 in training, 0.45 on unseen years 2024-2026).",
                   "<b>Early warning:</b> fields about to fall below normal within 15 days are ranked at ROC-AUC 0.76, "
                   "+0.02 to +0.07 over a fair statistical baseline.",
                   "<b>Operational replay:</b> severe 9/9 confirmed, 10/11 undeclared seasons quiet, 8 of 15 declared "
                   "seasons confirmed before the government order (median 7 days earlier).",
                   "<b>Honest negatives:</b> weather adds no significant skill to crop forecasts beyond satellite history; "
                   "single-date agreement with UAV verdicts is weak (3 of 10 fields clear, 2 mixed)."]),
           Spacer(1, 8),
           P("2. Study design", "h1"),
           P("The weather alarm says where to look, the satellite says which fields were actually hit, and the drone "
             "measures the damaged area. This report covers stages 1-2; stage 3 is the UAV segmentation work of the "
             "DeepDroughtUAV team."),
           KeepTogether([system_diagram(), P("Figure 1. The three-stage system.", "cap")])]

    st += [PageBreak(), P("Each site centre is a UAV survey field; the satellite uses farmland within 3 km of it. Names and mandals "
             "were checked against the coordinates."),
           table([["Site", "Village", "Mandal (district)", "Centre (°N, °E)", "Weather cell"],
                  ["Somandepalle", "Tungodu", "Somandepalle (Sri Sathya Sai)", "13.9988, 77.6247", "14.0, 77.6"],
                  ["Lepakshi", "Mamidimakalapalli", "Lepakshi (Sri Sathya Sai)", "13.7998, 77.6194", "13.8, 77.6*"],
                  ["Cholasamudram", "Cholasamudram", "Lepakshi (Sri Sathya Sai)", "13.8118, 77.5687", "13.8, 77.6*"],
                  ["Sira", "Gidaganahalli", "Sira taluk (Tumakuru, KA)", "13.7975, 76.9750", "13.8, 77.0"],
                  ["Peddakadubur", "Pedda Thumbalam", "Adoni / Peddakadubur (Kurnool)", "15.7826, 77.2528", "15.8, 77.3"],
                  ["Kurnool - Dinnedevarapadu", "Dinnedevarapadu", "Kurnool Rural", "15.7715, 78.0471", "15.8, 78.0"],
                  ["Kurnool - Balaji Villas", "Kurnool outskirts", "Kurnool Urban", "15.7834, 78.0561", "15.8, 78.1*"],
                  ["Kurnool - Pullaiah College", "Venkayyapalle", "Kurnool Urban", "15.7982, 78.0806", "15.8, 78.1*"]],
                 [0.23, 0.17, 0.25, 0.19, 0.16], center_from=3),
           P("Table 1. Sites. * = weather cell shared by two sites (6 independent cells). Periods: weather training "
             "1979-2011, validation 2012-2018, test 2019-2026; satellite training 2019-2023, validation 2024, test 2025-2026.", "cap")]

    # ---------------- 3 data
    st += [P("3. Data and official records", "h1"),
           table([["Source", "Content", "Period", "Use"],
                  ["AgERA5 v2.0 (Copernicus CDS)", "Daily rain, FAO-56 ET0, temperature, humidity, radiation, wind (0.1° cell of each site)", "1979 - Nov 2026", "Weather inputs, SPEI"],
                  ["Sentinel-2 SR (Earth Engine)", "B2-B12, NDVI, NDMI, EVI per field and date; Cloud Score+ and SCL masks", "2019 - Oct 2026", "Crop condition (SVI)"],
                  ["ESA WorldCover, Dynamic World", "10 m land cover", "2019-2023", "Finding farmland"],
                  ["UAV dataset (DeepDroughtUAV)", "10 surveyed fields, 2,254 images, drought / healthy labels", "Nov 2025 - Jan 2026", "Field check"],
                  ["AP G.O.Ms. 4/2023, 15/2024, 6/2025, 4 & 5/2026; Karnataka 2023 order", "Drought mandal / taluk lists, severe / moderate", "Kharif 2023-2026", "Independent check"]],
                 [0.24, 0.40, 0.16, 0.20], center_from=2),
           P("Table 2. Data. All inputs are public; nothing is simulated.", "cap")]

    # ---------------- 4 weather
    st += [PageBreak(), P("4. Stage 1: weather module", "h1"),
           P("The module forecasts the SPEI-30 drought class (normal ≥ 0, moderate -1.5 to 0, severe < -1.5) 7, 15 and "
             "30 days ahead. SPEI is calibrated on 1979-2011 only and frozen; the split is chronological and purged, and "
             "models are chosen on validation data. The <b>water-balance ensemble</b> is a physical baseline: on forecast "
             "day t part of the 30-day window is already observed, and the unknown days are filled with each 1979-2011 "
             "year's water balance in turn. The <b>hybrid</b> adds its three class probabilities to the weather, SPEI and "
             "season inputs."),
           KeepTogether([weather_chart(), P("Figure 2. Weather-module test scores, all sites.", "cap")]),
           table([["Model", "7 days", "15 days", "30 days"],
                  ["Persistence (no change)", "0.662", "0.515", "0.424"],
                  ["Water-balance ensemble (physics only)", "0.783", "0.592", "0.375"],
                  ["Best model without physics (XGBoost)", "0.755", "0.613", "0.424"],
                  ["Hybrid, ensemble of 4 models", "0.819", "0.651", "0.424"],
                  ["Hybrid vs physics, Δ [95% CI]", "[-0.007, +0.088]", "[+0.010, +0.099]", "[+0.023, +0.084]"],
                  ["Balanced accuracy, hybrid", "85.6%", "68.3%", "42.5%"],
                  ["ROC-AUC, hybrid", "0.97", "0.90", "0.68"]],
                 [0.40, 0.20, 0.20, 0.20], bold_rows=(4,)),
           P("Table 3. Macro-F1 on test years 2019-2026 unless stated. 30 days: no model beats persistence.", "cap")]
    st += bullets(["<b>7 days:</b> physics is hard to beat; the hybrid gain over it is not significant, but both beat persistence widely.",
                   "<b>15 days:</b> the hybrid significantly beats physics and persistence.",
                   "<b>Unseen regions</b> (leave-one-cluster-out): the hybrid holds up (mean 0.811 / 0.633 / 0.381).",
                   "<b>Marusov et al. protocol</b> (binary SPEI < -1): weather inputs raise 15-day ROC-AUC from 0.81 to 0.89; at 30 days a logistic model on the last SPEI is as good as anything."])

    # ---------------- 5 satellite
    st += [PageBreak(), P("5. Stage 2: satellite module", "h1"),
           P("Farmland is found automatically in Earth Engine from training years 2019-2023 only: ESA WorldCover "
             "cropland, minus built-up, tree and water pixels (Dynamic World), with a crop cycle in at least 2 of 5 "
             "years. SNIC splits it into 13,750 field segments; 20 rainfed and 10 irrigated fields are sampled per site "
             "(240 fields). The label is the <b>Standardized Vegetation Index</b> (SVI = NDVI departure from the field's "
             "own normal / its spread), with normals from images up to 31 Dec 2023 and the scored year fully removed."),
           P("Leakage controls, each covered by automated tests (42 across both modules):", "body")]
    st += bullets(["model inputs use only images up to the forecast date; spike cleaning (which looks ahead) is applied to labels only;",
                   "normals never see later years or the scored year; samples are purged when inputs, target or label support cross a period boundary;",
                   "an independent code review found five look-ahead and selection issues in an earlier version; all are fixed and every result here is from the corrected pipeline."])

    # ---------------- 6 lag
    st += [P("6. Result: crops follow weather drought within about 10 days", "h1"),
           P("The SPEI scale and lag were chosen on 2019-2023 only, then measured on 2024-2026."),
           table([["Fields", "Chosen on 2019-2023", "ρ training", "ρ 2024-2026 (median, range)"],
                  ["Rainfed", "SPEI-30, 10-day lag", "0.48", "0.45 (0.16-0.58)"],
                  ["Irrigated", "SPEI-60, 15-day lag", "0.24", "0.29 (0.12-0.46)"]],
                 [0.22, 0.30, 0.18, 0.30]),
           P("Table 4. Spearman correlation of crop SVI with SPEI. Rainfed minus irrigated on 2024-2026: [-0.02, +0.24].", "cap"),
           P("Weather alarms (SPEI-30 below -1) were followed by rainfed crop stress within 60 days in 22 of 44 cases, "
             "clearly above the base rate at Balaji Villas, Dinnedevarapadu and Cholasamudram.")]

    # ---------------- 7 forecasts
    st += [PageBreak(), P("7. Result: crop forecasts and early warning of stress", "h1"),
           table([["Version", "15 days", "Δ vs persistence [95% CI]", "30 days"],
                  ["Persistence (no change)", "0.648", "", "0.520"],
                  ["1  Satellite history", "0.668", "[-0.004, +0.036]", "0.555"],
                  ["2  + past weather", "0.677", "[+0.011, +0.038]", "0.553"],
                  ["3  + weather-module forecast", "0.677", "[+0.013, +0.041]", "0.553"],
                  ["4  + actual future weather (upper bound)", "0.685", "[+0.016, +0.052]", "0.575"]],
                 [0.42, 0.16, 0.26, 0.16]),
           P("Table 5. Macro-F1 on test years 2025-2026 (XGBoost, 5 seeds).", "cap")]
    st += bullets(["Weather versions beat persistence at 15 days (also with 90-day bootstrap blocks) but not satellite history alone; the weather forecast adds nothing beyond past weather.",
                   "<b>Onset warning</b>: among fields normal today, the models rank those falling below normal by day 15 at ROC-AUC 0.76 (30 days: 0.70), vs 0.72 for a logistic baseline on current SVI and its trend.",
                   "Interpretation: crop stress at 15-30 days is set mostly by water already lost, so the weather stage's value is the earlier meteorological alarm."])

    # ---------------- 8 replay
    st += [P("8. Result: operational replay against government declarations", "h1"),
           P("Every 5 days from 1 June to 30 November, with weather 7 days late and satellite 2 days late. Alarm: "
             "SPEI-30 < -1 or a severe +15-day forecast. Confirmed: median rainfed SVI < -1 from at least 5 clear "
             "fields; fewer fields = 'insufficient data'. No crop model is used, so all seasons are out of sample.", "intro"),
           table([["Site", "2023", "2024", "2025", "2026"],
                  ["Somandepalle", "Moderate: 2 d before", "none: quiet", "Moderate: missed", "Severe: after order"],
                  ["Lepakshi", "Moderate: 7 d before", "none: quiet", "Moderate: missed", "Severe: 7 d before"],
                  ["Cholasamudram", "Moderate: 12 d before", "none: quiet", "Moderate: missed", "Severe: after order"],
                  ["Sira (Karnataka)", "Severe: 5 d before", "none found", "none found", "likely declared"],
                  ["Kurnool - Balaji Villas", "Severe: 2 d before", "none: quiet", "none: quiet", "Severe: 22 d before"],
                  ["Kurnool - Dinnedevarapadu", "none: confirmed", "none: quiet", "none: quiet", "Severe: 22 d before"],
                  ["Kurnool - Pullaiah", "Severe: after order", "none: quiet", "none: quiet", "Severe: after order"],
                  ["Peddakadubur", "ambiguous mandal", "ambiguous", "none: quiet", "ambiguous"]],
                 [0.24, 0.19, 0.19, 0.19, 0.19]),
           P("Table 6. Official declaration and system result per site and season.", "cap"),
           table([["Official declaration", "System confirmed", "Not confirmed"],
                  ["Severe (9 site-seasons)", "9", "0"],
                  ["Moderate (6)", "3", "3 (all 2025)"],
                  ["Not declared (11)", "1", "10"]],
                 [0.40, 0.30, 0.30]),
           P("Table 7. Agreement. 8 of 15 declared site-seasons were confirmed before the order (median 7 days). "
             "Thresholds -0.75 / -1.25 leave the false-alarm count unchanged.", "cap")]

    # ---------------- 9 mismatches
    st += [PageBreak(), P("9. Mismatches and the UAV fields", "h1"),
           table([["Case", "Observation", "Likely reason (to verify)"],
                  ["2025: Lepakshi, Somandepalli declared Moderate", "Rain above normal; crops normal or greener June-October", "Late-season stress from November-December, after the replay window"],
                  ["2023: Dinnedevarapadu not declared", "53% of fields below normal", "Mandal-level assessment vs a 3 km urban-fringe area"],
                  ["2026: Peddakadubur", "Driest season (-57% rain), only 25% of fields below normal", "Deep black soils may hold water longer (check soil map)"],
                  ["UAV fields", "Clear agreement at 3 of 10 fields, 2 mixed", "Post-harvest flights; drone sees mm patches, Sentinel-2 averages 10 m"]],
                 [0.27, 0.36, 0.37], center_from=9),
           P("Table 8. Cases that do not fit. At the southern 'drought' maize fields (15 Nov 2025) Sentinel-2 showed "
             "crops greener than normal in September-October and below normal only from December: a field with 40% dry "
             "patches can look normal at 10 m. This is why the UAV stage is needed after satellite confirmation.", "cap")]

    # ---------------- 10 novelty
    st += [P("10. What is new", "h1"),
           table([["Aspect", "Common practice", "This work"],
                  ["Baselines", "Other ML models", "Persistence, Markov, climatology and a physical water-balance ensemble"],
                  ["Calibration", "Full record", "SPEI frozen on 1979-2011; SVI normals on 2019-2023, scored year removed"],
                  ["Leakage", "Rarely tested", "42 automated tests, independent review, purging by label support"],
                  ["Fields", "Hand-picked or district averages", "Automatic farmland from training years; 240 random fields"],
                  ["Validation", "Index vs index", "Four seasons of government orders, live replay with data delays, UAV fields"],
                  ["Weather + satellite", "Studied separately", "Linked; direct test of whether forecasts improve crop forecasts"]],
                 [0.20, 0.26, 0.54], center_from=9),
           P("Table 9. Comparison with common practice. The Marusov et al. comparison is a Marusov-inspired protocol, "
             "not a claim of beating their monthly PDSI results.", "cap")]

    # ---------------- 11 limitations
    st += [PageBreak(), P("11. Limitations", "h1")]
    st += bullets(["Short satellite record: normals rest on five years and the test years hold one full drought season (2026).",
                   "Few events: 3-7 alarms per site and 15 declared site-seasons; agreement figures are case evidence.",
                   "Monsoon clouds often leave fewer than 5 clear fields in August-September, delaying confirmation.",
                   "SVI classes are index categories, not measured damage; irrigation is inferred from dry-season greenness.",
                   "Spatial mismatch between mandals, 3 km areas and single fields; for Sira only 2023 is confirmed by name.",
                   "AgERA5 is about a week late, so 7-day forecasts give little real warning; 15 days gives about a week.",
                   "No skill beyond persistence at 30 days; UAV comparison uses post-harvest flights and no field boundaries."])

    # ---------------- 12 references
    st += [P("12. References", "h1")]
    refs = ["Achanta, R. & Süsstrunk, S. (2017). Superpixels and polygons using simple non-iterative clustering. CVPR.",
            "Boogaard, H. et al. AgERA5: agrometeorological indicators from 1979 to present. Copernicus Climate Change Service.",
            "Brown, C. F. et al. (2022). Dynamic World, near real-time global 10 m land cover mapping. Scientific Data 9, 251.",
            "Government of Andhra Pradesh, Revenue (DM) Dept. G.O.Ms. 4 (2023), 15 (2024), 6 (2025), 4 and 5 (2026).",
            "Government of India (2016). Manual for Drought Management. Ministry of Agriculture and Farmers Welfare.",
            "Kogan, F. N. (1995). Vegetation index and brightness temperature for drought detection. Adv. Space Res. 15(11).",
            "Marusov, A. et al. Long-term drought prediction using deep neural networks. Environ. Model. Softw.; arXiv:2309.06212.",
            "Pasquarella, V. J. et al. (2023). Cloud Score+: cloud and cloud-shadow masking for Sentinel-2. CVPR Workshops.",
            "Peters, A. J. et al. (2002). Drought monitoring with NDVI-based Standardized Vegetation Index. PE&RS 68(1).",
            "Vicente-Serrano, S. M. et al. (2010). A multiscalar drought index sensitive to global warming: the SPEI. J. Climate 23.",
            "Zanaga, D. et al. (2021, 2022). ESA WorldCover 10 m v100 / v200."]
    st += [Paragraph(r, S["ref"], bulletText=f"[{i + 1}]") for i, r in enumerate(refs)]

    # keep every table together with its caption (no table split across pages)
    out, i = [], 0
    while i < len(st):
        it = st[i]
        if isinstance(it, Table) and i + 1 < len(st) and isinstance(st[i + 1], Paragraph)                 and st[i + 1].style.name == "cap":
            out.append(KeepTogether([it, st[i + 1]]))
            i += 2
        else:
            out.append(it)
            i += 1
    final = out
    doc.build(final, onFirstPage=on_page, onLaterPages=on_page)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()


import os
import pathlib
import io
import base64
import matplotlib
matplotlib.use("Agg")  # backend sin ventana para CI
import matplotlib.pyplot as plt
import pandas as pd
from elasticsearch import Elasticsearch, helpers

ES_URL   = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "penguins")

if not ES_URL or not ES_API_KEY:
    raise SystemExit("Faltan ES_URL o ES_API_KEY en variables de entorno.")

es = Elasticsearch(ES_URL, api_key=ES_API_KEY)

# --- Descargar datos (hasta ~10k docs) ---
docs = helpers.scan(es, index=ES_INDEX, query={"query": {"match_all": {}}})
rows = []
for d in docs:
    src = d["_source"]
    rows.append(src)
df = pd.DataFrame(rows)

if df.empty:
    raise SystemExit("El DataFrame está vacío. ¿Cargaste datos al índice?")

# Normaliza nombres por si vienen como strings con espacios
df = df.rename(columns={
    "bill_length_mm":"bill_length_mm",
    "bill_depth_mm":"bill_depth_mm",
    "flipper_length_mm":"flipper_length_mm",
    "body_mass_g":"body_mass_g",
    "species":"species",
    "sex":"sex",
    "island":"island",
})

# Crea carpeta de salida
site = pathlib.Path("site")
imgd = site / "img"
imgd.mkdir(parents=True, exist_ok=True)

# Utilidad para guardar y devolver ruta
def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=140, bbox_inches="tight")
    plt.close()

# 1) Conteo por especie (barras)
ax = df["species"].value_counts().sort_index().plot(kind="bar")
ax.set_title("Conteo por especie")
ax.set_xlabel("Especie")
ax.set_ylabel("Conteo")
savefig(imgd/"by_species.png")

# 2) Dispersión: flipper vs body_mass, coloreado por especie
fig, ax = plt.subplots()
for sp, g in df.groupby("species"):
    ax.scatter(g["flipper_length_mm"], g["body_mass_g"], s=18, label=sp, alpha=0.7)
ax.set_xlabel("Flipper length (mm)")
ax.set_ylabel("Body mass (g)")
ax.set_title("Masa corporal vs largo de aleta")
ax.legend(title="Especie")
savefig(imgd/"scatter_flipper_mass.png")

# 3) Boxplot de body mass por especie
fig, ax = plt.subplots()
order = sorted(df["species"].dropna().unique())
data = [df.loc[df["species"]==sp, "body_mass_g"].dropna() for sp in order]
ax.boxplot(data, labels=order)
ax.set_title("Distribución de masa corporal por especie")
ax.set_ylabel("Body mass (g)")
savefig(imgd/"box_body_mass.png")

# --- Genera index.html ---
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Penguins – Elasticsearch → GitHub Pages</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 32px; }}
    h1, h2 {{ margin: 0 0 12px; }}
    .grid {{ display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }}
    figure {{ margin: 0; background:#fafafa; border:1px solid #eee; padding:16px; border-radius:12px; }}
    figcaption {{ margin-top:8px; color:#666; font-size:14px; }}
    img {{ max-width:100%; height:auto; display:block; }}
    .muted {{ color:#6b7280; }}
  </style>
</head>
<body>
  <h1>Penguins – Elasticsearch → GitHub Pages</h1>
  <p class="muted">Dataset ingestado en Elasticsearch y graficado automáticamente con GitHub Actions.</p>

  <div class="grid">
    <figure>
      <img src="img/by_species.png" alt="Conteo por especie">
      <figcaption>Conteo por especie</figcaption>
    </figure>
    <figure>
      <img src="img/scatter_flipper_mass.png" alt="Flipper vs masa">
      <figcaption>Masa corporal vs largo de aleta</figcaption>
    </figure>
    <figure>
      <img src="img/box_body_mass.png" alt="Boxplot de masa por especie">
      <figcaption>Distribución de masa corporal por especie</figcaption>
    </figure>
  </div>

  <p class="muted">Índice: <code>{ES_INDEX}</code> | Registros: <b>{len(df):,}</b></p>
</body>
</html>
"""
(site / "index.html").write_text(html, encoding="utf-8")
print("OK: sitio generado en ./site")

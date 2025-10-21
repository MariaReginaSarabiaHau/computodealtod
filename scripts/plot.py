import os
import pathlib
from datetime import datetime
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import pandas as pd

ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "penguins")

if not ES_URL or not ES_API_KEY:
    raise SystemExit("Faltan ES_URL o ES_API_KEY en variables de entorno.")

es = Elasticsearch(ES_URL, api_key=ES_API_KEY)

# 1) Agregación: conteo por especie
agg = {"size": 0, "aggs": {"by_species": {"terms": {"field": "species", "size": 10}}}}
r = es.search(index=ES_INDEX, body=agg)
buckets = r["aggregations"]["by_species"]["buckets"]
labels = [b["key"] for b in buckets]
values = [b["doc_count"] for b in buckets]

# 2) Graficar
out_dir = pathlib.Path("site")
img_dir = out_dir / "img"
img_dir.mkdir(parents=True, exist_ok=True)

plt.figure()
plt.bar(labels, values)
plt.title("Conteo de especímenes por especie (Penguins)")
plt.xlabel("Especie")
plt.ylabel("Conteo")
plt.tight_layout()
plt.savefig(img_dir / "species_counts.png", dpi=150)
plt.close()

# 3) Agregación de promedios por especie
agg2 = {
    "size": 0,
    "aggs": {
        "by_species": {
            "terms": {"field": "species", "size": 10},
            "aggs": {
                "avg_bill_length": {"avg": {"field": "bill_length_mm"}},
                "avg_bill_depth": {"avg": {"field": "bill_depth_mm"}},
                "avg_flipper": {"avg": {"field": "flipper_length_mm"}},
                "avg_mass": {"avg": {"field": "body_mass_g"}}
            }
        }
    }
}
r2 = es.search(index=ES_INDEX, body=agg2)
rows = []
for b in r2["aggregations"]["by_species"]["buckets"]:
    rows.append({
        "species": b["key"],
        "avg_bill_length_mm": round(b["avg_bill_length"]["value"], 2),
        "avg_bill_depth_mm": round(b["avg_bill_depth"]["value"], 2),
        "avg_flipper_length_mm": round(b["avg_flipper"]["value"], 2),
        "avg_body_mass_g": round(b["avg_mass"]["value"], 2),
        "count": b["doc_count"]
    })
df = pd.DataFrame(rows)

# 4) HTML
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
table_html = df.to_html(index=False)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Penguins × Elasticsearch</title>
  <style>
    body {{ font-family: system-ui, Arial, sans-serif; margin: 2rem; }}
    .wrap {{ max-width: 900px; margin: auto; }}
    img {{ max-width: 100%; height: auto; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #ddd; padding: .5rem; text-align: center; }}
    th {{ background: #f3f3f3; }}
    .muted {{ color: #666; font-size: .9rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Visualización desde Elasticsearch (Penguins)</h1>
    <p>Gráfica generada con GitHub Actions (Python) y publicada en GitHub Pages.</p>
    <h2>Conteo por especie</h2>
    <img src="img/species_counts.png" alt="Conteo por especie" />
    <h2>Promedios por especie</h2>
    {table_html}
    <p class="muted">Última actualización: {now} · Índice: <code>{ES_INDEX}</code></p>
  </div>
</body>
</html>"""

out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "index.html").write_text(html, encoding="utf-8")
print("Sitio generado en site/")

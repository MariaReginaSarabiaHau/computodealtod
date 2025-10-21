import os
import pandas as pd
from elasticsearch import Elasticsearch, helpers

ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "penguins")

if not ES_URL or not ES_API_KEY:
    raise SystemExit("Faltan ES_URL o ES_API_KEY en variables de entorno.")

# Conexión a Elasticsearch con API Key
es = Elasticsearch(ES_URL, api_key=ES_API_KEY)

# Dataset Penguins (seaborn)
CSV_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
df = pd.read_csv(CSV_URL)

# Limpieza básica
df = df.dropna(subset=[
    "species", "island", "bill_length_mm", "bill_depth_mm",
    "flipper_length_mm", "body_mass_g", "sex"
])

# Crear índice si no existe
if es.indices.exists(index=ES_INDEX):
    print(f"Índice '{ES_INDEX}' ya existe.")
else:
    mapping = {
        "mappings": {
            "properties": {
                "species": {"type": "keyword"},
                "island": {"type": "keyword"},
                "sex": {"type": "keyword"},
                "bill_length_mm": {"type": "float"},
                "bill_depth_mm": {"type": "float"},
                "flipper_length_mm": {"type": "integer"},
                "body_mass_g": {"type": "integer"},
                "year": {"type": "integer"}
            }
        }
    }
    es.indices.create(index=ES_INDEX, body=mapping)
    print(f"Índice '{ES_INDEX}' creado.")

# Bulk index
actions = []
for _, row in df.iterrows():
    doc = {
        "species": row["species"],
        "island": row["island"],
        "sex": row["sex"],
        "bill_length_mm": float(row["bill_length_mm"]),
        "bill_depth_mm": float(row["bill_depth_mm"]),
        "flipper_length_mm": int(row["flipper_length_mm"]),
        "body_mass_g": int(row["body_mass_g"]),
    }
    actions.append({"_index": ES_INDEX, "_source": doc})

helpers.bulk(es, actions)
print(f"Ingestados {len(actions)} documentos en '{ES_INDEX}'.")

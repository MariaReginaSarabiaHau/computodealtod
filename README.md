# Elasticsearch → GitHub Pages (Penguins)
Tarea: cargar dataset a Elasticsearch y publicar gráfica con GitHub Actions.

## Workflows
- **Load dataset to Elasticsearch** (manual): crea índice y sube datos.
- **Build & Deploy GitHub Pages**: consulta ES, genera `site/` y publica.

## Secrets requeridos
- `ES_URL` — endpoint de Elasticsearch (Elastic Cloud recomendado).
- `ES_API_KEY` — API Key con permisos de lectura/escritura.
- `ES_INDEX` — nombre del índice (e.g., `penguins`).

## Página
Se publica mediante GitHub Actions → Pages (source: GitHub Actions).

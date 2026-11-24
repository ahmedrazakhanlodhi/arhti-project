# Deploying the app (Streamlit Community Cloud)

The app (`app/app.py`) reads only files in the repository: `app/data/` (written by `scripts/18_export_web.py`),
`app/content/*.md`, `docs/human_checklist.md` and `docs/data_inventory.md` (seven pages; district disbursement amounts are mapped only on the Reporting geography page). It needs no raw data, QGIS or API keys, and the
maps use no third-party tiles.

## 1. Check locally
```bash
bash run_all.sh --from 13                      # rerun scripts 13-16 (reporting geography, cost, key numbers, app data)
.venv/bin/python -I -m pytest tests -q
.venv/bin/streamlit run app/app.py             # http://localhost:8501 ; presentation mode: add ?present=1
```

## 2. Public GitHub repository
Commit everything except what `.gitignore` excludes (`private/`, `.venv/`, `data/raw/`, `data/interim/`, large rasters).
Before the first push, check `git status` to confirm that no file from `private/` is listed.

## 3. Create the app
1. https://share.streamlit.io → sign in with GitHub → **Create app** → deploy from the repository.
2. Branch `main`; **Main file path `app/app.py`**; Python **3.11** under Advanced settings.
3. Streamlit Cloud installs `app/requirements.txt` (next to the main file) and reads `.streamlit/config.toml` (theme and fonts).
4. Optional: set a custom subdomain under Settings → General.

## 4. Updating
Rerun the pipeline (or `scripts/17_key_numbers.py` and `scripts/18_export_web.py`), run the tests, commit and push; the app
redeploys. Edits to `app/content/narrative.md` show up without code changes.

## 5. Before the presentation
Community Cloud apps go to sleep after a period without visitors (see Streamlit's documentation on app hibernation for the
current limit). Open the URL 10–15 minutes before presenting, wake it if needed (usually under a minute), and click through
each page once. Keep a local copy running as a fallback (`streamlit run app/app.py`); its maps need internet because the
map library loads from a CDN. Screenshots of every page are in `docs/app_screenshots/`.

## 6. Presentation mode
`?present=1` (or the sidebar toggle): navigation moves to the top, the sidebar collapses, menus are hidden and type is larger.

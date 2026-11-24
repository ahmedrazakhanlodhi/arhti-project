# Source this to run PyQGIS headless with the bundled QGIS (macOS). Adjust QGIS_APP if your QGIS is elsewhere.
QGIS_APP="${QGIS_APP:-$(ls -d /Applications/QGIS*.app 2>/dev/null | head -1)}"
export QGIS_PY="$QGIS_APP/Contents/MacOS/python3.12"
R="$QGIS_APP/Contents/Resources"
export PYTHONHOME="$R"
export PYTHONPATH="$R/python3.12:$R/python3.12/lib-dynload:$R/python3.12/site-packages:$R/qgis/python:$R/qgis/python/plugins"
export PROJ_DATA="$R/qgis/proj"
export QT_QPA_PLATFORM=offscreen

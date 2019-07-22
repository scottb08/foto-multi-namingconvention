@echo on
rem The path to output all built .py files to:
set UI_PYTHON_PATH=../python/app/ui

pyside-uic --from-imports dialog.ui -o dialog.py
sed -i "s/from PySide import/from tank.platform.qt import/g" dialog.py
move dialog.py %UI_PYTHON_PATH%

pyside-rcc resources.qrc > resources_rc.py
sed -i "s/from PySide import/from tank.platform.qt import/g" resources_rc.py
move resources_rc.py %UI_PYTHON_PATH%

set UI_PYTHON_PATH=

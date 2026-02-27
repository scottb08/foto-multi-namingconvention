#!/usr/bin/env bash
# This script requires tk-toolchain utility to build the QT resources
# For more information:
# https://github.com/shotgunsoftware/tk-toolchain?tab=readme-ov-file#tk-build-qt-resources.
# This currently only works with PySide2 (not PySide6) with Python 3.10.x (not Python 3.11.x that ships with SG Desktop)

# This script has to be run from the directory that contains the build_resource.yml file

tk-build-qt-resources --yamlfile ".\build_resources.yml" --rcc "pyside2-rcc.exe" --uic "pyside2-uic.exe"

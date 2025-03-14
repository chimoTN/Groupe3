# tests/conftest.py
import sys
from pathlib import Path

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
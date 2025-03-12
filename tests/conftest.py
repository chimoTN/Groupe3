# conftest.py (à placer dans GROUPE3/)
import sys
import os
from pathlib import Path

# Obtenez le chemin absolu du répertoire du projet
project_root = Path(__file__).parent.absolute()

# Ajoutez le répertoire du projet au chemin d'importation Python
sys.path.insert(0, str(project_root))

print(f"Added {project_root} to Python path")
print(f"Current Python path: {sys.path}")
"""Configuracion basica del proyecto PEC4."""

from datetime import datetime
from pathlib import Path


STUDENT_NAME: str = "Pablo_Witold_Martinez"
EXECUTION_TIMESTAMP: str = datetime.now().strftime("%Y%m%d_%H%M%S")

SRC_DIR: Path = Path(__file__).resolve().parent
PROJECT_DIR: Path = SRC_DIR.parent
DATA_DIR: Path = SRC_DIR / "data"
IMG_DIR: Path = SRC_DIR / "img"
DOC_DIR: Path = PROJECT_DIR / "doc"
SCREENSHOTS_DIR: Path = PROJECT_DIR / "screenshots"

CSV_PATH: Path = DATA_DIR / "LaLiga_Matches.csv"


def build_image_name(exercise_number: int, description: str = "figura") -> Path:
    """Construye una ruta de imagen con ejercicio, alumno y timestamp."""
    del description
    file_name = f"grafica_ex{exercise_number}_{STUDENT_NAME}_{EXECUTION_TIMESTAMP}.png"
    return IMG_DIR / file_name

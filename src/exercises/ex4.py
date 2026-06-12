"""Ejercicio 4: distribucion del resultado final de los partidos."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import build_image_name


matplotlib.use("Agg")

import matplotlib.pyplot as plt

RESULT_DESCRIPTIONS: dict[str, str] = {
    "H": "Victoria local",
    "A": "Victoria visitante",
    "D": "Empate",
}


def FTR(data: pd.DataFrame) -> pd.DataFrame:  # pylint: disable=invalid-name
    """Calcula la distribucion de resultados finales."""
    result_counts = data["FTR"].value_counts()
    distribution = pd.DataFrame(
        {
            "resultado": ["H", "A", "D"],
            "descripcion": [
                RESULT_DESCRIPTIONS["H"],
                RESULT_DESCRIPTIONS["A"],
                RESULT_DESCRIPTIONS["D"],
            ],
        }
    )
    distribution["partidos"] = (
        distribution["resultado"].map(result_counts).fillna(0).astype(int)
    )
    return distribution


def calculate_result_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la distribucion de resultados finales."""
    return FTR(df)


def calculate_home_win_percentage(result_distribution: pd.DataFrame) -> float:
    """Calcula el porcentaje de victorias locales sobre el total."""
    total_matches = result_distribution["partidos"].sum()
    home_wins = result_distribution.loc[
        result_distribution["resultado"] == "H", "partidos"
    ].iloc[0]
    return home_wins / total_matches * 100


def plot_FTR(ftr: pd.DataFrame) -> Path:  # pylint: disable=invalid-name
    """Genera y guarda una grafica de distribucion de resultados."""
    image_path = build_image_name(4, "distribucion_resultados")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 5))
    plt.bar(ftr["resultado"], ftr["partidos"])
    plt.title("Distribucion del resultado final")
    plt.xlabel("Resultado")
    plt.ylabel("Numero de partidos")
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def save_result_distribution_chart(result_distribution: pd.DataFrame) -> Path:
    """Genera y guarda una grafica de distribucion de resultados."""
    return plot_FTR(result_distribution)


def run(df: pd.DataFrame) -> tuple[pd.DataFrame, float, Path]:
    """Ejecuta el ejercicio 4 a partir del DataFrame limpio."""
    result_distribution = FTR(df)
    home_win_percentage = calculate_home_win_percentage(result_distribution)
    image_path = plot_FTR(result_distribution)
    return result_distribution, home_win_percentage, image_path

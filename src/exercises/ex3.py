"""Ejercicio 3: distribucion de goles locales y visitantes."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import build_image_name


matplotlib.use("Agg")

import matplotlib.pyplot as plt


def calculate_goal_distribution(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calcula cuantos partidos hubo para cada cantidad de goles."""
    distribution = df[column].value_counts().sort_index().to_frame(name="partidos")
    distribution.index.name = "goles"
    return distribution


def goals_distribution(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula las distribuciones de goles locales y visitantes."""
    distr_goals_home = calculate_goal_distribution(data, "FTHG")
    distr_goals_away = calculate_goal_distribution(data, "FTAG")
    return distr_goals_home, distr_goals_away


def plot_goals_ditribution(
    distr_goals_home: pd.DataFrame, distr_goals_away: pd.DataFrame
) -> Path:
    """Genera y guarda una grafica comparando distribuciones de goles."""
    image_path = build_image_name(3, "distribucion_goles")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.plot(
        distr_goals_home.index,
        distr_goals_home["partidos"],
        marker="o",
        label="Goles locales",
    )
    plt.plot(
        distr_goals_away.index,
        distr_goals_away["partidos"],
        marker="o",
        label="Goles visitantes",
    )
    plt.title("Distribucion de goles locales y visitantes")
    plt.xlabel("Goles")
    plt.ylabel("Numero de partidos")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def save_goal_distribution_chart(
    home_distribution: pd.DataFrame, away_distribution: pd.DataFrame
) -> Path:
    """Genera y guarda una grafica comparando distribuciones de goles."""
    return plot_goals_ditribution(home_distribution, away_distribution)


def run(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 3 a partir del DataFrame limpio."""
    home_distribution, away_distribution = goals_distribution(df)
    image_path = plot_goals_ditribution(home_distribution, away_distribution)
    return home_distribution, away_distribution, image_path

"""Ejercicio 2: partidos jugados por cada equipo."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import build_image_name


matplotlib.use("Agg")

import matplotlib.pyplot as plt


def total_matches(data: pd.DataFrame) -> pd.DataFrame:
    """Cuenta partidos como local, visitante y total por equipo."""
    home_matches = data["HomeTeam"].value_counts()
    away_matches = data["AwayTeam"].value_counts()

    result = pd.DataFrame(
        {
            "equipo": sorted(set(home_matches.index) | set(away_matches.index)),
        }
    )
    result["partidos_local"] = result["equipo"].map(home_matches).fillna(0).astype(int)
    result["partidos_visitante"] = (
        result["equipo"].map(away_matches).fillna(0).astype(int)
    )
    result["partidos_total"] = (
        result["partidos_local"] + result["partidos_visitante"]
    )

    return result.sort_values(
        by=["partidos_total", "equipo"], ascending=[False, True]
    ).reset_index(drop=True)


def count_matches_by_team(df: pd.DataFrame) -> pd.DataFrame:
    """Cuenta partidos como local, visitante y total por equipo."""
    return total_matches(df)


def get_teams_with_max_matches(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el equipo o equipos con mas partidos jugados."""
    max_matches = matches_df["partidos_total"].max()
    return matches_df[matches_df["partidos_total"] == max_matches]


def plot_matches_team_total(matches_team_total: pd.DataFrame) -> Path:
    """Genera y guarda una grafica de partidos totales por equipo."""
    image_path = build_image_name(2, "partidos_totales_por_equipo")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    ordered_df = matches_team_total.sort_values("partidos_total", ascending=True)

    plt.figure(figsize=(10, 12))
    plt.barh(ordered_df["equipo"], ordered_df["partidos_total"])
    plt.title("Partidos totales por equipo")
    plt.xlabel("Partidos totales")
    plt.ylabel("Equipo")
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def save_total_matches_chart(matches_df: pd.DataFrame) -> Path:
    """Genera y guarda una grafica de partidos totales por equipo."""
    return plot_matches_team_total(matches_df)


def run(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 2 a partir del DataFrame limpio."""
    matches_df = total_matches(df)
    max_teams_df = get_teams_with_max_matches(matches_df)
    image_path = plot_matches_team_total(matches_df)
    return matches_df, max_teams_df, image_path

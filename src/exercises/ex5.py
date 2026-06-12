"""Ejercicio 5: clasificacion historica por puntos."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import build_image_name


matplotlib.use("Agg")

import matplotlib.pyplot as plt


def add_points(data: pd.DataFrame) -> pd.DataFrame:
    """Anade columnas de puntos para local y visitante segun el resultado."""
    df_points = data.copy()
    df_points["points_home"] = 0
    df_points["points_away"] = 0

    df_points.loc[df_points["FTR"] == "H", "points_home"] = 3
    df_points.loc[df_points["FTR"] == "A", "points_away"] = 3
    df_points.loc[df_points["FTR"] == "D", ["points_home", "points_away"]] = 1

    return df_points


def add_points_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Anade columnas de puntos para local y visitante segun el resultado."""
    return add_points(df)


def fun_total_points(data: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """Calcula los puntos historicos por equipo como local y visitante."""
    df_points = add_points(data)

    home_points = df_points.groupby("HomeTeam")["points_home"].sum()
    away_points = df_points.groupby("AwayTeam")["points_away"].sum()

    classification = pd.DataFrame(
        {
            "equipo": sorted(set(home_points.index) | set(away_points.index)),
        }
    )
    classification["puntos_local"] = (
        classification["equipo"].map(home_points).fillna(0).astype(int)
    )
    classification["puntos_visitante"] = (
        classification["equipo"].map(away_points).fillna(0).astype(int)
    )
    classification["puntos_total"] = (
        classification["puntos_local"] + classification["puntos_visitante"]
    )

    classification = classification.sort_values(
        by=["puntos_total", "equipo"], ascending=[False, True]
    ).reset_index(drop=True)

    total_points_by_team = classification.set_index("equipo")["puntos_total"]
    return total_points_by_team, classification


def calculate_historical_classification(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula los puntos historicos por equipo como local y visitante."""
    _, classification = fun_total_points(df)
    return classification


def alltime_winner(df_total_points: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el equipo o equipos con mas puntos historicos."""
    max_points = df_total_points["puntos_total"].max()
    return df_total_points[df_total_points["puntos_total"] == max_points]


def get_top_team(classification: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el equipo o equipos con mas puntos historicos."""
    return alltime_winner(classification)


def save_historical_points_chart(classification: pd.DataFrame) -> Path:
    """Genera y guarda una grafica de puntos totales por equipo."""
    image_path = build_image_name(5, "clasificacion_historica")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    ordered_df = classification.sort_values("puntos_total", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 12))
    ax.barh(ordered_df["equipo"], ordered_df["puntos_total"])
    ax.set_title("Clasificacion historica por puntos")
    ax.set_xlabel("Puntos totales")
    ax.set_ylabel("Equipo")
    fig.tight_layout()
    fig.savefig(image_path)
    plt.close(fig)

    return image_path


def run(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 5 a partir del DataFrame limpio."""
    _, classification = fun_total_points(df)
    top_team = alltime_winner(classification)
    image_path = save_historical_points_chart(classification)
    return classification, top_team, image_path

"""Ejercicio 6: resumen historico de puntos y goles."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import build_image_name
from exercises import ex5


matplotlib.use("Agg")

import matplotlib.pyplot as plt


def fun_total_goals(data: pd.DataFrame) -> tuple[int, int, int]:
    """Calcula goles locales, visitantes y totales del dataset."""
    total_home_goals = int(data["FTHG"].sum())
    total_away_goals = int(data["FTAG"].sum())
    total_goals = total_home_goals + total_away_goals

    return total_home_goals, total_away_goals, total_goals


def fun_total_goals_by_team(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calcula goles como local, visitante y total por equipo."""
    home_goals = data.groupby("HomeTeam")["FTHG"].sum()
    away_goals = data.groupby("AwayTeam")["FTAG"].sum()

    goals_df = pd.DataFrame(
        {
            "equipo": sorted(set(home_goals.index) | set(away_goals.index)),
        }
    )
    goals_df["goles_local"] = goals_df["equipo"].map(home_goals).fillna(0).astype(int)
    goals_df["goles_visitante"] = (
        goals_df["equipo"].map(away_goals).fillna(0).astype(int)
    )
    goals_df["goles_total"] = goals_df["goles_local"] + goals_df["goles_visitante"]

    home_goals_by_team = goals_df[["equipo", "goles_local"]].copy()
    away_goals_by_team = goals_df[["equipo", "goles_visitante"]].copy()
    total_goals_by_team = goals_df[["equipo", "goles_total"]].copy()

    return home_goals_by_team, away_goals_by_team, total_goals_by_team


def calculate_goals_by_team(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula goles como local, visitante y total por equipo."""
    home_goals_by_team, away_goals_by_team, total_goals_by_team = (
        fun_total_goals_by_team(df)
    )
    return home_goals_by_team.merge(away_goals_by_team, on="equipo").merge(
        total_goals_by_team, on="equipo"
    )


def fun_summary_1996_2025(
    total_points_by_team: pd.Series,
    home_goals_by_team: pd.DataFrame,
    away_goals_by_team: pd.DataFrame,
    total_goals_by_team: pd.DataFrame,
) -> pd.DataFrame:
    """Construye el resumen historico de puntos y goles por equipo."""
    points_df = (
        total_points_by_team.rename("puntos_total")
        .rename_axis("equipo")
        .reset_index()
    )

    summary = (
        points_df.merge(home_goals_by_team, on="equipo", how="left")
        .merge(away_goals_by_team, on="equipo", how="left")
        .merge(total_goals_by_team, on="equipo", how="left")
    )
    return summary.sort_values(
        by=["puntos_total", "equipo"], ascending=[False, True]
    ).reset_index(drop=True)


def build_historical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Combina puntos historicos y goles por equipo."""
    total_points_by_team, _ = ex5.fun_total_points(df)
    home_goals_by_team, away_goals_by_team, total_goals_by_team = (
        fun_total_goals_by_team(df)
    )
    return fun_summary_1996_2025(
        total_points_by_team,
        home_goals_by_team,
        away_goals_by_team,
        total_goals_by_team,
    )


def get_top_three_teams(summary: pd.DataFrame) -> pd.DataFrame:
    """Obtiene los tres primeros equipos del resumen historico."""
    return summary.head(3)


def podium(summary_1996_2025: pd.DataFrame) -> Path:
    """Genera y guarda una grafica tipo podium con el top 3."""
    image_path = build_image_name(6, "podium_top_3")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    top_three = get_top_three_teams(summary_1996_2025)
    podium_df = top_three.iloc[[1, 0, 2]].copy()
    podium_df["altura"] = [2, 3, 1]
    podium_df["puesto"] = ["2", "1", "3"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        [0, 1, 2],
        podium_df["altura"],
        color=["#7ea6c4", "#d8b64c", "#c9826b"],
        width=0.8,
    )

    for podium_bar, (_, row) in zip(bars, podium_df.iterrows()):
        x_position = podium_bar.get_x() + podium_bar.get_width() / 2
        ax.text(
            x_position,
            podium_bar.get_height() + 0.08,
            row["equipo"],
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )
        ax.text(
            x_position,
            podium_bar.get_height() / 2,
            row["puesto"],
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
            color="white",
        )

    ax.set_title("Podium historico por puntos")
    ax.set_ylim(0, 3.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    fig.savefig(image_path)
    plt.close(fig)

    return image_path


def save_podium_chart(top_three: pd.DataFrame) -> Path:
    """Genera y guarda una grafica tipo podium con el top 3."""
    return podium(top_three)


def run(
    df: pd.DataFrame,
) -> tuple[tuple[int, int, int], pd.DataFrame, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 6 a partir del DataFrame limpio."""
    total_goals = fun_total_goals(df)
    total_points_by_team, _ = ex5.fun_total_points(df)
    home_goals_by_team, away_goals_by_team, total_goals_by_team = (
        fun_total_goals_by_team(df)
    )
    summary = fun_summary_1996_2025(
        total_points_by_team,
        home_goals_by_team,
        away_goals_by_team,
        total_goals_by_team,
    )
    top_three = get_top_three_teams(summary)
    image_path = podium(summary)
    return total_goals, summary, top_three, image_path

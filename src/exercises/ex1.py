"""Ejercicio 1: carga, limpieza inicial y visualizacion del dataset."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import pandas as pd

from config import CSV_PATH, build_image_name


DROP_COLUMNS: list[str] = ["HTHG", "HTAG", "HTR"]

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def load_and_eda(file: str | Path) -> pd.DataFrame:
    """Carga el CSV indicado y elimina las columnas del descanso."""
    df = pd.read_csv(file)
    return df.drop(columns=DROP_COLUMNS)


def plot_home_away_goals(data: pd.DataFrame) -> Path:
    """Genera y guarda un boxplot de goles locales y visitantes."""
    image_path = build_image_name(1, "boxplot_goles")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    data[["FTHG", "FTAG"]].boxplot()
    plt.title("Distribucion de goles locales y visitantes")
    plt.ylabel("Goles")
    plt.xticks([1, 2], ["Goles locales", "Goles visitantes"])
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def load_clean_dataset() -> pd.DataFrame:
    """Carga el CSV de LaLiga y elimina las columnas del descanso."""
    return load_and_eda(CSV_PATH)


def save_goals_boxplot(df: pd.DataFrame) -> Path:
    """Genera y guarda un boxplot de goles locales y visitantes."""
    return plot_home_away_goals(df)


def get_basic_info(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve informacion basica del DataFrame en formato tabular."""
    return pd.DataFrame(
        {
            "columna": df.columns,
            "tipo": [str(dtype) for dtype in df.dtypes],
            "valores_no_nulos": df.notna().sum().to_list(),
        }
    )


def run() -> tuple[pd.DataFrame, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 1 y devuelve datos limpios, info e imagen."""
    df = load_and_eda(CSV_PATH)
    image_path = plot_home_away_goals(df)
    info_df = get_basic_info(df)
    return df, info_df, image_path

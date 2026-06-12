"""Punto de entrada principal para la PEC4."""

import argparse
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from config import CSV_PATH, EXECUTION_TIMESTAMP, PROJECT_DIR, STUDENT_NAME
from exercises import ex1, ex2, ex3, ex4, ex5, ex6, ex7


def relative_path(path: Path) -> Path:
    """Devuelve una ruta relativa al proyecto para mostrarla por pantalla."""
    return path.relative_to(PROJECT_DIR)


def print_project_info() -> None:
    """Muestra informacion basica del proyecto."""
    print("PEC4 - Programacion para la Ciencia de Datos")
    print(f"Alumno: {STUDENT_NAME}")
    print(f"Timestamp de ejecucion: {EXECUTION_TIMESTAMP}")
    print("Directorio del proyecto: .")
    print(f"Dataset: {relative_path(CSV_PATH)}")
    print()


def print_exercise_1() -> pd.DataFrame:
    """Muestra los resultados principales del ejercicio 1."""
    df, info_df, image_path = ex1.run()

    print("Ejercicio 1 - Carga, limpieza inicial y boxplot de goles")
    print()
    print("Primeros registros:")
    print(df.head())
    print()
    print("Ultimos registros:")
    print(df.tail())
    print()
    print("Columnas disponibles:")
    print(list(df.columns))
    print()
    print("Dimensiones del DataFrame:")
    print(f"{df.shape[0]} filas x {df.shape[1]} columnas")
    print()
    print("Informacion basica del DataFrame:")
    print(info_df)
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()
    return df


def print_exercise_2(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 2."""
    matches_df, max_teams_df, image_path = ex2.run(df)

    print("Ejercicio 2 - Partidos jugados por cada equipo")
    print()
    print("Primeras filas del resultado:")
    print(matches_df.head(10))
    print()
    print("Equipo o equipos con mas partidos:")
    print(max_teams_df)
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


def print_exercise_3(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 3."""
    home_distribution, away_distribution, image_path = ex3.run(df)

    print("Ejercicio 3 - Distribucion de goles locales y visitantes")
    print()
    print("Distribucion de goles locales:")
    print(home_distribution)
    print()
    print("Distribucion de goles visitantes:")
    print(away_distribution)
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


def print_exercise_4(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 4."""
    result_distribution, home_win_percentage, image_path = ex4.run(df)

    print("Ejercicio 4 - Distribucion del resultado final")
    print()
    print("Distribucion de resultados:")
    print(result_distribution)
    print()
    print(f"Porcentaje de victorias locales: {home_win_percentage:.2f}%")
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


def print_exercise_5(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 5."""
    classification, top_team, image_path = ex5.run(df)

    print("Ejercicio 5 - Clasificacion historica por puntos")
    print()
    print("Primeras filas de la clasificacion historica:")
    print(classification.head(10))
    print()
    print("Equipo con mayor puntuacion historica:")
    print(top_team)
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


def print_exercise_6(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 6."""
    total_goals, summary, top_three, image_path = ex6.run(df)

    print("Ejercicio 6 - Resumen historico de puntos y goles")
    print()
    home_goals, away_goals, goals_total = total_goals
    print(f"Total de goles locales: {home_goals}")
    print(f"Total de goles visitantes: {away_goals}")
    print(f"Total global de goles: {goals_total}")
    print()
    print("Primeras filas del resumen historico:")
    print(summary.head(10).to_string())
    print()
    print("Top 3 de equipos:")
    print(top_three.to_string())
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


def print_exercise_7(df: pd.DataFrame) -> None:
    """Muestra los resultados principales del ejercicio 7."""
    top_five_teams, selected_matches, graph, edges_df, image_path = ex7.run(df)

    print("Ejercicio 7 - Grafo entre los 5 mejores equipos historicos")
    print()
    print("Equipos seleccionados:")
    print(top_five_teams)
    print()
    print(f"Numero de partidos filtrados: {len(selected_matches)}")
    print()
    print("Nodos del grafo:")
    print(list(graph.nodes()))
    print()
    print("Aristas del grafo:")
    print(edges_df.to_string(index=False))
    print()
    print(f"Imagen generada: {relative_path(image_path)}")
    print()


EXERCISE_PRINTERS: dict[int, Callable[[pd.DataFrame], None]] = {
    2: print_exercise_2,
    3: print_exercise_3,
    4: print_exercise_4,
    5: print_exercise_5,
    6: print_exercise_6,
    7: print_exercise_7,
}


def run_exercise(
    exercise_number: int, df: pd.DataFrame | None = None
) -> pd.DataFrame | None:
    """Ejecuta el ejercicio indicado si esta implementado."""
    if exercise_number == 1:
        return print_exercise_1()

    exercise_printer = EXERCISE_PRINTERS.get(exercise_number)
    if exercise_printer is None:
        print(f"Ejercicio {exercise_number}: pendiente de implementacion.")
        print()
        return df

    if df is None:
        df = ex1.load_and_eda(CSV_PATH)
    exercise_printer(df)
    return df


def parse_args() -> argparse.Namespace:
    """Procesa los argumentos de la linea de comandos."""
    parser = argparse.ArgumentParser(
        description="Ejecuta los ejercicios de la PEC4 de forma incremental."
    )
    parser.add_argument(
        "-ex",
        type=int,
        choices=range(1, 8),
        required=True,
        metavar="{1,2,3,4,5,6,7}",
        help="numero de ejercicio hasta el que se desea ejecutar",
    )
    return parser.parse_args()


def main() -> None:
    """Ejecuta el programa principal."""
    args = parse_args()

    print_project_info()

    df = None
    for exercise_number in range(1, args.ex + 1):
        df = run_exercise(exercise_number, df)


if __name__ == "__main__":
    main()

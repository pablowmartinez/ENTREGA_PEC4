"""Ejercicio 7: grafo de partidos entre los 5 mejores equipos."""
# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports

from pathlib import Path

import matplotlib
import networkx as nx
import pandas as pd

from config import build_image_name
from exercises import ex5


matplotlib.use("Agg")

import matplotlib.pyplot as plt


def get_top_five_teams(df: pd.DataFrame) -> list[str]:
    """Obtiene los 5 equipos con mayor puntuacion historica."""
    classification = ex5.calculate_historical_classification(df)
    return classification.head(5)["equipo"].to_list()


def filter_matches_between_teams(df: pd.DataFrame, teams: list[str]) -> pd.DataFrame:
    """Filtra partidos disputados entre los equipos seleccionados."""
    selected_matches = df[
        df["HomeTeam"].isin(teams) & df["AwayTeam"].isin(teams)
    ].copy()
    return selected_matches


def build_matches_graph(teams: list[str], matches_df: pd.DataFrame) -> nx.Graph:
    """Construye un grafo no dirigido con partidos entre equipos."""
    graph = nx.Graph()
    graph.add_nodes_from(teams)

    for _, row in matches_df.iterrows():
        home_team = row["HomeTeam"]
        away_team = row["AwayTeam"]

        if graph.has_edge(home_team, away_team):
            graph[home_team][away_team]["partidos"] += 1
        else:
            graph.add_edge(home_team, away_team, partidos=1)

    return graph


def graph_edges_to_dataframe(graph: nx.Graph) -> pd.DataFrame:
    """Convierte las aristas del grafo en un DataFrame legible."""
    edges = [
        {
            "equipo_1": team_1,
            "equipo_2": team_2,
            "partidos": data["partidos"],
        }
        for team_1, team_2, data in graph.edges(data=True)
    ]
    return pd.DataFrame(edges).sort_values(
        by=["partidos", "equipo_1", "equipo_2"], ascending=[False, True, True]
    ).reset_index(drop=True)


def save_graph_image(graph: nx.Graph) -> Path:
    """Genera y guarda una imagen del grafo."""
    image_path = build_image_name(7, "grafo_top_5")
    image_path.parent.mkdir(parents=True, exist_ok=True)

    positions = nx.spring_layout(graph, seed=7)
    edge_labels = nx.get_edge_attributes(graph, "partidos")

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(graph, positions, node_size=1800)
    nx.draw_networkx_edges(graph, positions, width=1.5)
    nx.draw_networkx_labels(graph, positions, font_size=9)
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels, font_size=8)
    plt.title("Grafo de partidos entre el top 5 historico")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def graf(data: pd.DataFrame, selected_teams: list[str]) -> Path:
    """Genera el grafo de partidos entre equipos seleccionados y guarda la imagen."""
    selected_matches = filter_matches_between_teams(data, selected_teams)
    graph = build_matches_graph(selected_teams, selected_matches)
    return save_graph_image(graph)


def run(
    df: pd.DataFrame,
) -> tuple[list[str], pd.DataFrame, nx.Graph, pd.DataFrame, Path]:
    """Ejecuta el ejercicio 7 a partir del DataFrame limpio."""
    top_five_teams = get_top_five_teams(df)
    selected_matches = filter_matches_between_teams(df, top_five_teams)
    graph = build_matches_graph(top_five_teams, selected_matches)
    edges_df = graph_edges_to_dataframe(graph)
    image_path = graf(df, top_five_teams)
    return top_five_teams, selected_matches, graph, edges_df, image_path

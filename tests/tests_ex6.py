"""Tests unitarios para el ejercicio 6."""

import importlib
import sys
import unittest
from pathlib import Path

import pandas as pd


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

fun_total_goals = importlib.import_module("exercises.ex6").fun_total_goals


class TestFunTotalGoals(unittest.TestCase):
    """Tests para la funcion fun_total_goals."""

    def test_calculates_total_home_away_and_global_goals(self) -> None:
        """Comprueba goles locales, visitantes y totales."""
        df = pd.DataFrame(
            {
                "FTHG": [2, 0, 3],
                "FTAG": [1, 4, 2],
            }
        )

        home_goals, away_goals, total_goals = fun_total_goals(df)

        self.assertEqual(home_goals, 5)
        self.assertEqual(away_goals, 7)
        self.assertEqual(total_goals, 12)


if __name__ == "__main__":
    unittest.main()

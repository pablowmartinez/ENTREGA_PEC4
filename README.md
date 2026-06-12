# PEC4 - Programacion para la Ciencia de Datos

Alumno: Pablo Witold Martinez

Este proyecto contiene una practica academica de analisis de partidos de LaLiga usando Python, pandas, matplotlib y networkx. El programa carga el dataset, realiza distintos analisis sobre partidos, goles, resultados y equipos, genera graficas y permite ejecutar los ejercicios de forma incremental desde consola.

## Estructura del proyecto

```text
PEC4/
+-- src/
|   +-- main.py
|   +-- config.py
|   +-- data/
|   |   +-- LaLiga_Matches.csv
|   +-- exercises/
|   |   +-- ex1.py
|   |   +-- ex2.py
|   |   +-- ex3.py
|   |   +-- ex4.py
|   |   +-- ex5.py
|   |   +-- ex6.py
|   |   +-- ex7.py
|   +-- img/
+-- tests/
|   +-- tests_ex6.py
+-- doc/
+-- screenshots/
+-- README.md
+-- requirements.txt
+-- LICENSE
+-- .gitignore
```

## Requisitos

- Python
- pandas
- matplotlib
- networkx

## Entorno virtual en Windows

Crear el entorno virtual:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.venv\Scripts\activate
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecucion del programa

Mostrar ayuda:

```powershell
.venv\Scripts\python.exe src\main.py --help
```

Ejecutar solo hasta el ejercicio 1:

```powershell
.venv\Scripts\python.exe src\main.py -ex 1
```

Ejecutar todos los ejercicios:

```powershell
.venv\Scripts\python.exe src\main.py -ex 7
```

El parametro `-ex` ejecuta los ejercicios de forma incremental. Por ejemplo, `-ex 4` ejecuta los ejercicios 1, 2, 3 y 4.

## Resumen de ejercicios

1. Carga el dataset, elimina columnas del descanso y genera un boxplot de goles locales y visitantes.
2. Calcula el total de partidos jugados por cada equipo como local y visitante.
3. Analiza la distribucion de goles locales y visitantes.
4. Calcula la distribucion de resultados finales y el porcentaje de victorias locales.
5. Construye una clasificacion historica por puntos.
6. Combina puntos historicos y goles por equipo, calcula goles totales y genera un podium con el top 3.
7. Crea un grafo con networkx para los partidos entre los 5 equipos con mayor puntuacion historica.

Algunos resultados obtenidos:

- Dataset limpio: 11664 filas x 7 columnas.
- Porcentaje de victorias locales: 47.15%.
- Goles totales: 31093.
- Top 3 del ejercicio 6: Barcelona, Real Madrid, Ath Madrid.
- Top 5 del ejercicio 7: Barcelona, Real Madrid, Ath Madrid, Valencia, Ath Bilbao.

## Tests

El proyecto incluye un test unitario con `unittest` para la funcion `fun_total_goals(df)` del ejercicio 6.

Ejecutar tests:

```powershell
.venv\Scripts\python.exe -m unittest discover tests -v
```

## Pylint

`pylint` se usa como herramienta de desarrollo y no forma parte de las dependencias funcionales del proyecto. Si no esta instalado, se puede instalar aparte:

```powershell
.venv\Scripts\python.exe -m pip install pylint
```

Ejecutar revision de calidad con pylint:

```powershell
.venv\Scripts\python.exe -m pylint src tests
```

Durante la revision del proyecto se obtuvo una puntuacion de `10.00/10`.

## Documentacion con pydoc

La documentacion HTML generada con `pydoc` se encuentra en la carpeta `doc/`.

Ejemplo de generacion de documentacion:

```powershell
cd doc
$env:PYTHONPATH='..\src;..'
& ..\.venv\Scripts\python.exe -m pydoc -w main
& ..\.venv\Scripts\python.exe -m pydoc -w config
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex1
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex2
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex3
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex4
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex5
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex6
& ..\.venv\Scripts\python.exe -m pydoc -w exercises.ex7
& ..\.venv\Scripts\python.exe -m pydoc -w tests.tests_ex6
```

Se generaron documentos para `main`, `config`, los ejercicios `ex1` a `ex7` y el test `tests_ex6`.

## Preparacion del ZIP

La carpeta `.venv/` no debe incluirse en el ZIP final de entrega.

## Git y GitHub

Comandos basicos para preparar y subir la entrega:

```powershell
git init
git add .
git commit -m "Entrega final PEC4"
git branch -M main
git remote add origin git@github.com:pablowmartinez/ENTREGA_PEC4.git
git push -u origin main
```

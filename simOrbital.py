# By: Johanna Olivera y Ailin Ferrari

"""
- Elige caso (frío/caliente), simula 1 órbita y grafica resultados.
- Menos repetición: lista de ecuaciones por nodo y lazo compacto.
- AFT tomadas desde constants.py (en °C).
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple
from constants import (
    ORBITAL_PERIOD, T_VENUS, T_SPACE, C_COND, F_VIEW,
    get_propiedades_caso,
    AFT_OBC_MIN, AFT_OBC_MAX, AFT_BAT_MIN, AFT_BAT_MAX
)

# ----------------------------
# Configuración de simulación
# ----------------------------
T_TOTAL: float = 6000.0    # [s]
DT: float = 1.0            # [s]
NODES_TOTAL: int = 15      # 13 nodos físicos + Venus (14) + espacio (15)
NODES_SOLVE: int = 13      # resolvemos 1..13

# Paleta
COLORS = [
    "#d35e60", "#d35e60", "#7293cb", "#7293cb", "#84ba5b", "#84ba5b",
    "#ff974c", "#ff974c", "#808585", "#9067a7", "#fc91ad", "#00a99a", "#8a6d3f"
]

# ----------------------------
# Utilidades
# ----------------------------
def theta_deg(step: int, dt: float, period: float) -> float:
    """Ángulo orbital en grados, normalizado a [0,360)."""
    theta = (360.0 / period) * step * dt
    return theta % 360.0

def pick_case() -> Tuple[str, object]:
    """Pregunta por consola y retorna ('frio'|'caliente', módulo de ecuaciones)."""
    op = -1
    while op not in (1, 2):
        print("\n==== Menú ====\n< 1 > Caso frío\n< 2 > Caso caliente")
        try:
            op = int(input("\n>> Ingrese la opción a simular: "))
        except Exception:
            op = -1
    if op == 2:
        import ecNodales_Caliente as ecs
        return "caliente", ecs
    else:
        import ecNodales_Frio as ecs
        return "frio", ecs

def build_node_funcs(ecs_mod) -> List[Callable]:
    """Devuelve [ecNodo1, ..., ecNodo13] desde el módulo de ecuaciones."""
    return [
        ecs_mod.ecNodo1, ecs_mod.ecNodo2, ecs_mod.ecNodo3, ecs_mod.ecNodo4,
        ecs_mod.ecNodo5, ecs_mod.ecNodo6, ecs_mod.ecNodo7, ecs_mod.ecNodo8,
        ecs_mod.ecNodo9, ecs_mod.ecNodo10, ecs_mod.ecNodo11, ecs_mod.ecNodo12,
        ecs_mod.ecNodo13
    ]

def simulate(caso: str, ecs_mod) -> Tuple[np.ndarray, np.ndarray]:
    """Corre la simulación y devuelve (temps[K], t[s])."""
    props = get_propiedades_caso(caso)
    T0 = np.asarray(props["T_inicial"], dtype=float)  # [K]

    steps = int(T_TOTAL // DT)
    temps = np.zeros((NODES_TOTAL, steps), dtype=float)
    temps[:, 0] = T0

    node_funcs = build_node_funcs(ecs_mod)

    # Pre-alisto vistas de matrices para evitar repetir list() en cada llamada
    cond_rows = [list(C_COND[i]) for i in range(NODES_SOLVE)]
    fv_rows   = [list(F_VIEW[i])  for i in range(NODES_SOLVE)]

    for p in range(1, steps):
        prev = temps[:, p - 1]
        theta = theta_deg(p, DT, ORBITAL_PERIOD)
        # Avance explícito de nodos 1..13
        for i in range(NODES_SOLVE):
            temps[i, p] = node_funcs[i](prev, DT, cond_rows[i], fv_rows[i], theta)
        # Nodos "fuente": Venus y espacio
        temps[13, p] = T_VENUS
        temps[14, p] = T_SPACE

    t_axis = np.arange(0.0, T_TOTAL, DT)
    return temps, t_axis

# ----------------------------
# Gráficos
# ----------------------------
def plot_all_nodes(temps_K: np.ndarray, t_axis: np.ndarray) -> None:
    """Gráfico general de todos los nodos (en °C)."""
    fig, ax = plt.subplots()
    # pares: (0,1), (2,3), (4,5), (6,7)
    for i in range(NODES_SOLVE):
        if i in (1, 3, 5, 7):
            continue
        label = f"Nodo {i+1}" if i not in (0, 2, 4, 6) else f"Nodo {i+1} y {i+2}"
        ax.plot(t_axis, temps_K[i] - 273.15, color=COLORS[i], label=label)

    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Temperatura [°C]")
    ax.legend(ncol=2, loc="best", borderaxespad=0.0)
    ax.grid(True)
    fig.tight_layout()

def plot_aft_windows(temps_K: np.ndarray, t_axis: np.ndarray) -> None:
    """Subplots para nodos 12 y 13 con líneas AFT desde constants.py."""
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    # Nodo 12 (OBC/AOCS)
    ax1.plot(t_axis, temps_K[11] - 273.15, color="#00a99a", label="Nodo 12 (OBC/AOCS)")
    ax1.plot(t_axis, np.full_like(t_axis, AFT_OBC_MIN - 273.15), label="AFT min", linestyle="--")
    ax1.plot(t_axis, np.full_like(t_axis, AFT_OBC_MAX - 273.15), label="AFT max", linestyle="--")
    ax1.set_xlabel("Tiempo [s]")
    ax1.set_ylabel("Temperatura [°C]")
    ax1.legend(loc="best")
    ax1.grid(True)

    # Nodo 13 (Batería/Tanque)
    ax2.plot(t_axis, temps_K[12] - 273.15, color="#d35e60", label="Nodo 13 (Batería/Tanque)")
    ax2.plot(t_axis, np.full_like(t_axis, AFT_BAT_MIN - 273.15), label="AFT min", linestyle="--")
    ax2.plot(t_axis, np.full_like(t_axis, AFT_BAT_MAX - 273.15), label="AFT max", linestyle="--")
    ax2.set_xlabel("Tiempo [s]")
    ax2.set_ylabel("Temperatura [°C]")
    ax2.legend(loc="best")
    ax2.grid(True)

    fig.tight_layout()

def print_extremes(temps_K: np.ndarray) -> None:
    """Imprime Tmax/Tmin para nodos 1..13 en °C."""
    for i in range(NODES_SOLVE):
        node = i + 1
        t_c = temps_K[i] - 273.15
        print(f"> Tmax nodo {node}: {np.max(t_c):.3f} °C")
        print(f"> Tmin nodo {node}: {np.min(t_c):.3f} °C")

# ----------------------------
# Main
# ----------------------------
def main() -> None:
    caso, ecs_mod = pick_case()
    temps_K, t_axis = simulate(caso, ecs_mod)

    # Gráficos
    plot_all_nodes(temps_K, t_axis)
    plot_aft_windows(temps_K, t_axis)
    plt.show()

    # Logs
    print("\nTemperaturas iniciales de una órbita (K):\n", temps_K[:, 0], "\n")
    print_extremes(temps_K)

if __name__ == "__main__":
    main()

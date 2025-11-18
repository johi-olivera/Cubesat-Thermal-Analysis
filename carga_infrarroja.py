# By: Johanna Olivera y Ailin Ferrari

"""

- Calcula y grafica el flujo IR (incidente/absorbido) por cara.
- IR independiente de θ → curvas constantes vs. ángulo orbital.
- Grupos: Z+, Z−, X± (solar array), Y± (white coating).
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple
from constants import (
    SIGMA, T_VENUS,
    F_PLANET_ZPLUS, F_PLANET_LATERAL,
    EPS_SA_BOL, EPS_SA_EOL, EPS_WTC_BOL, EPS_WTC_EOL,
    AREA_CARA_Y,
    THETA_C1, THETA_C2, THETA_C3, THETA_C4
)

"""
Configuración “de escenario”
----------------------------
'INC' = flujo incidente [W/m^2]
'BOL' = flujo absorbido BOL [W/m^2]
'EOL' = flujo absorbido EOL [W/m^2]
"""
STATE = "INC"

# ----------------------------
# Dominio y ejes
# ----------------------------
th = np.linspace(0.0, 2.0 * np.pi, 1000)

# ----------------------------
# Parámetros por STATE
# ----------------------------
def get_params(state: str):
    """
    Devuelve:
      - funciones de emisividad por material (sa, wtc) o 1.0 si 'INC'
      - Ai (área efectiva de plot)
      - título del gráfico
    """
    st = state.upper().strip()
    if st == "INC":
        # Incidente: sin emisividad/área (por unidad de área)
        eps_sa = lambda: 1.0
        eps_wtc = lambda: 1.0
        Ai = 1.0
        title = "Flujo infrarrojo incidente"
    elif st == "BOL":
        eps_sa = lambda: EPS_SA_BOL
        eps_wtc = lambda: EPS_WTC_BOL
        Ai = 1.0
        title = "Flujo infrarrojo absorbido en BOL"
    elif st == "EOL":
        eps_sa = lambda: EPS_SA_EOL
        eps_wtc = lambda: EPS_WTC_EOL
        Ai = 1.0
        title = "Flujo infrarrojo absorbido en EOL"
    else:
        raise ValueError(f"STATE inválido: {state}")
    return eps_sa, eps_wtc, Ai, title

# ----------------------------
# Ley general IR por grupo
# ----------------------------
def ir_power(F_i: float, eps_i: float, Ai: float, npts: int) -> np.ndarray:
    """
    q = ε_i * F_i * σ T_V^4  (flujo, W/m², constante en θ)
    Devuelve array constante para graficar vs. θ.
    """
    value = eps_i * F_i * SIGMA * (T_VENUS ** 4)
    return np.full(npts, value, dtype=float)

# ----------------------------
# Grupos y factores de vista
# ----------------------------
# Nota: Z- no ve planeta --> F = 0
GROUPS: Dict[str, Tuple[float, str]] = {
    "Cara Z+": (F_PLANET_ZPLUS, "sa"),
    "Cara Z-": (0.0,             "sa"),   # Material irrelevante (F=0), mantenemos consistencia
    "Cara X±": (F_PLANET_LATERAL, "sa"),
    "Cara Y±": (F_PLANET_LATERAL, "wtc"),
}

# ----------------------------
# Plot
# ----------------------------
def main() -> None:
    eps_sa_fn, eps_wtc_fn, Ai, title = get_params(STATE)

    plt.figure(figsize=(10, 6), dpi=96)
    ax = plt.gca()
    ax.grid(True, alpha=0.35)
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(0, 150)
    ax.set_xlabel("Ángulo orbital [deg]")
    ax.set_xticks(
        [0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3, 5*np.pi/6, np.pi,
         7*np.pi/6, 4*np.pi/3, 3*np.pi/2, 5*np.pi/3, 11*np.pi/6, 2*np.pi]
    )
    ax.set_xticklabels(
        [r"$0$", r"$30$", r"$60$", r"$90$", r"$120$", r"$150$", r"$180$",
         r"$210$", r"$240$", r"$270$", r"$300$", r"$330$", r"$360$"]
    )
    ax.set_title(title)
    ax.set_ylabel("Flujo de calor [W/m²]")

    # Dibujar cada grupo con su emisividad correspondiente
    for label, (F_i, mat) in GROUPS.items():
        eps = eps_sa_fn() if mat == "sa" else eps_wtc_fn()
        Q = ir_power(F_i=F_i, eps_i=eps, Ai=Ai, npts=th.size)
        ax.plot(th, Q, label=label)

    ax.legend(loc="best")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

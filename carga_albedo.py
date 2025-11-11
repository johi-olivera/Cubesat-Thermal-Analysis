# By: Johanna Olivera y Ailin Ferrari

"""
- Calcula y grafica el flujo por albedo (incidente/absorbido) por cara.
- Una sola ley general: Q(θ) = α_s * γ * S_V * F_i * A_i * f_Aeff * η * cos(θ),
  enmascarada fuera del rango sin eclipse (0–θ_c1 y θ_c4–360).
- Evita repeticiones con un mapeo de “grupo de caras → F_i”.
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple
from constants import (
    SCV, GAMMA, F_PLANET_ZPLUS, F_PLANET_LATERAL,
    F_AEFF, ETA_ELEC, AREA_CARA_Y,
    ALPHA_S_BOL, ALPHA_S_EOL,
    THETA_C1, THETA_C2, THETA_C3, THETA_C4
)

"""
Configuración “de escenario”
----------------------------
'INC' = flujo incidente [W/m^2]
'BOL' = absorbido BOL [W]
'EOL' = absorbido EOL [W]
"""
STATE = "INC"

# ----------------------------
# Dominio angular y máscaras
# ----------------------------
c1 = np.radians(THETA_C1)  # Inicio de eclipse (115° aprox)
c4 = np.radians(THETA_C4)  # Fin de eclipse (270° aprox)
th = np.linspace(0.0, 2.0 * np.pi, 1000)

# Albedo distinto de 0 solo fuera del eclipse
mask_out_eclipse = (th <= c1) | (th >= c4)

# ----------------------------
# Parámetros por STATE
# ----------------------------
def get_params(state: str) -> Tuple[float, float, float, float, str]:
    """
    Devuelve (alpha_s, A_i, f_Aeff, eta, titulo) según el modo.
    'INC' devuelve magnitudes por unidad de área (A_i=f_Aeff=eta=1).
    """
    st = state.upper().strip()
    if st == "INC":
        return 1.0, 1.0, 1.0, 1.0, "Flujo por albedo incidente"
    elif st == "BOL":
        return ALPHA_S_BOL, AREA_CARA_Y, F_AEFF, ETA_ELEC, "Flujo por albedo absorbido en BOL"
    elif st == "EOL":
        return ALPHA_S_EOL, AREA_CARA_Y, F_AEFF, ETA_ELEC, "Flujo por albedo absorbido en EOL"
    else:
        raise ValueError(f"STATE inválido: {state}")

# ----------------------------
# Ley general de albedo por cara
# ----------------------------
def albedo_power_group(alpha_s: float, Ai: float, f_Aeff: float, eta: float,
                       F_i: float, theta: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Q(θ) = α_s * γ * S_V * F_i * A_i * f_Aeff * η * cos(θ), θ ∈ fuera-de-eclipse; 0 si no.
    """
    base = alpha_s * GAMMA * SCV * F_i * Ai * f_Aeff * eta
    Q = base * np.cos(theta)
    Q[~mask] = 0.0
    return Q

# ----------------------------
# Grupos de caras y factores F_i
# ----------------------------
# Z- no ve planeta --> F = 0
GROUPS: Dict[str, float] = {
    "Cara Z+": F_PLANET_ZPLUS,
    "Cara Z-": 0.0,
    "Cara X±/Y±": F_PLANET_LATERAL,  # X+, X-, Y+, Y- comparten F_lateral
}

# ----------------------------
# Plot
# ----------------------------
def main() -> None:
    alpha_s, Ai, f_Aeff, eta, title = get_params(STATE)

    plt.figure(figsize=(10, 6), dpi=96)
    ax = plt.gca()
    ax.grid(True, alpha=0.35)
    ax.set_xlim(0, 2*np.pi)
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

    if STATE.upper() == "INC":
        ax.set_ylabel("Flujo de calor [W/m²]")
    else:
        ax.set_ylabel("Flujo de calor [W]")
        if STATE.upper() == "BOL":
            ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
            ax.set_yticklabels(
                [r"$0$", r"$10$", r"$20$", r"$30$", r"$40$", r"$50$",
                 r"$60$", r"$70$", r"$80$", r"$90$"]
            )
        elif STATE.upper() == "EOL":
            ax.set_yticks([0, 20, 40, 60, 80, 100, 120, 140])
            ax.set_yticklabels(
                [r"$0$", r"$20$", r"$40$", r"$60$", r"$80$",
                 r"$100$", r"$120$", r"$140$"]
            )

    # Dibujar cada grupo
    for label, F_i in GROUPS.items():
        Q = albedo_power_group(alpha_s, Ai, f_Aeff, eta, F_i, th, mask_out_eclipse)
        ax.plot(th, Q, label=label)

    ax.legend(loc="best")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

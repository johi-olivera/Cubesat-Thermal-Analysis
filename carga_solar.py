# By: Johanna Olivera y Ailin Ferrari

"""
- Calcula y grafica flujo solar incidente/absorbido por cara.
- Reduce repetición con un mapeo cara --> (cos(phi), condición angular).
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict, Tuple
from constants import (
    SCV, F_AEFF, ETA_ELEC, AREA_PANEL,
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
STATE = "BOL"

# ----------------------------
# Utilidades y dominio angular
# ----------------------------
c1 = np.radians(THETA_C1)
c2 = np.radians(THETA_C2)
c3 = np.radians(THETA_C3)
c4 = np.radians(THETA_C4)

th = np.linspace(0.0, 2.0 * np.pi, 1000)

BoolFunc = Callable[[np.ndarray], np.ndarray]
CosFunc  = Callable[[np.ndarray], np.ndarray]

def _zero(th: np.ndarray) -> np.ndarray:
    return np.zeros_like(th)

# Ventanas angulares
cond_Z_plus: BoolFunc = lambda t: ((t >= c1) & (t <= c2)) | ((t >= c3) & (t <= c4))
cond_Z_minus: BoolFunc = lambda t: (t <= c1) | (t >= c4)
cond_X_plus: BoolFunc = lambda t: (t >= c3)
cond_X_minus: BoolFunc = lambda t: (t <= c2)
cond_Y: BoolFunc = lambda t: np.zeros_like(t, dtype=bool)  # Ya que nunca recibe Sol directo

# Cosenos por orientación
cos_Z_plus: CosFunc  = lambda t: -np.cos(t)
cos_Z_minus: CosFunc = lambda t:  np.cos(t)
cos_X_plus: CosFunc  = lambda t: -np.sin(t)
cos_X_minus: CosFunc = lambda t:  np.sin(t)
cos_Y: CosFunc       = _zero

# Mapeo “cara --> (cos(phi), condición angular, etiqueta)”
FACES: Dict[str, Tuple[CosFunc, BoolFunc, str]] = {
    "Z+": (cos_Z_plus,  cond_Z_plus,  "Cara Z+"),
    "Z-": (cos_Z_minus, cond_Z_minus, "Cara Z-"),
    "X+": (cos_X_plus,  cond_X_plus,  "Cara X+"),
    "X-": (cos_X_minus, cond_X_minus, "Cara X-"),
    "Y+": (cos_Y,       cond_Y,       "Cara Y+"),
    "Y-": (cos_Y,       cond_Y,       "Cara Y-"),
}

# ----------------------------
# Parámetros según STATE
# ----------------------------
def get_params(state: str) -> Tuple[float, float, float, float, str]:
    """
    Devuelve (alpha_s, A_i, f_Aeff, eta, titulo) según el modo.
    'INC' devuelve magnitudes por unidad de área (A_i=f_Aeff=eta=1).
    """
    st = state.upper().strip()
    if st == "INC":
        return 1.0, 1.0, 1.0, 1.0, "Flujo solar incidente"
    elif st == "BOL":
        return ALPHA_S_BOL, AREA_PANEL*2, F_AEFF, ETA_ELEC, "Flujo solar absorbido en BOL"
    elif st == "EOL":
        return ALPHA_S_EOL, AREA_PANEL*2, F_AEFF, ETA_ELEC, "Flujo solar absorbido en EOL"
    else:
        raise ValueError(f"STATE inválido: {state}")

# ----------------------------
# Modelo general por cara
# ----------------------------
def solar_power_face(alpha_s: float, Ai: float, f_Aeff: float, eta: float,
                     cos_fn: CosFunc, cond_fn: BoolFunc, theta: np.ndarray) -> np.ndarray:
    """
    Q(theta) = alpha_s * SCV * Ai * f_Aeff * eta * cos(phi(theta)) con máscara por ventana angular.
    Nota: cos(phi) ya incluye el signo por orientación.
    """
    base = alpha_s * SCV * Ai * f_Aeff * eta
    cos_term = cos_fn(theta)
    mask = cond_fn(theta)
    Q = base * cos_term
    Q[~mask] = 0.0
    return Q

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
        # Escala similar a la tuya original
        ax.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500])
        ax.set_yticklabels(
            [r"$0$", r"$250$", r"$500$", r"$750$", r"$1000$", r"$1250$",
             r"$1500$", r"$1750$", r"$2000$", r"$2250$", r"$2500$"]
        )
    else:
        ax.set_ylabel("Flujo de calor [W]")
        if STATE.upper() == "EOL":
            ax.set_yticks([0, 30, 60, 90, 120, 150, 180, 210])
            ax.set_yticklabels(
                [r"$0$", r"$30$", r"$60$", r"$90$", r"$120$", r"$150$", r"$180$", r"$210$"]
            )

    # Dibujar cada cara
    for key in ["Z+", "Z-", "X+", "X-", "Y+", "Y-"]:
        cos_fn, cond_fn, label = FACES[key]
        Q = solar_power_face(alpha_s, Ai, f_Aeff, eta, cos_fn, cond_fn, th)
        ax.plot(th, Q, label=label)

    ax.legend(loc="best")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

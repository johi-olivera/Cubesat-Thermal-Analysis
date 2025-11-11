# By: Johanna Olivera y Ailin Ferrari

# Caso FRÍO (BOL)

import numpy as np
from constants import *

# Props del caso frío
props = get_propiedades_caso('frio')
eps_sa = props['eps_sa']
alpha_s = props['alpha_s']
eps_wc = props['eps_wc']
alpha_wc = props['alpha_wc']
get_potencia = props['get_potencia']  # devuelve 0 en frío

# ----------------------------
# Helpers de ventanas angulares
# ----------------------------
def _theta_mask_sol(theta_deg: float) -> bool:
    # Iluminación directa (Z+ en cuadraturas, Z- afuera de eclipse); tu lógica original:
    return ((THETA_C1 < theta_deg < THETA_C2) or (THETA_C3 < theta_deg < THETA_C4))

def _theta_mask_alb(theta_deg: float) -> bool:
    # Albedo activo fuera de eclipse
    return ((0 < theta_deg < THETA_C1) or (THETA_C4 < theta_deg < 360))

def _cos_phi(theta_deg: float) -> float:
    # Mantengo tu cosφ = -cos(theta) usado en todos los nodos externos
    return -np.cos(np.radians(theta_deg))

# ----------------------------
# Núcleo de cálculo por tipo
# ----------------------------
def _panel_step(T, dt, cond_row, fv_row, theta_deg, F_planet):
    """
    Nodos 1..8 (paneles): usan eps/alpha de SA y AREA_PANEL.
    Incluye F_AEFF/ETA_ELEC en q_sol, q_alb e IR como en tu código.
    """
    Ti = T[0]  # placeholder, se sobreescribe por caller (ver wrappers)
    raise RuntimeError("No llamar directo; usar wrappers ecNodoX")

def _panel_common(i, T, dt, cond_row, fv_row, theta_deg, F_planet):
    Ti = T[i]
    cos_phi = _cos_phi(theta_deg)
    F_planet_cos = F_planet * np.cos(np.radians(theta_deg))

    # IR planetaria
    q_ir = F_planet * eps_sa * AREA_PANEL * SIGMA * (T[13]**4) * F_AEFF
    # Al espacio
    q_esp = eps_sa * AREA_PANEL * SIGMA * (T[14]**4 - Ti**4)

    # Solar directa
    q_sol = cos_phi * SCV * AREA_PANEL * alpha_s * ETA_ELEC * F_AEFF if _theta_mask_sol(theta_deg) else 0.0
    # Albedo
    q_alb = F_planet_cos * SCV * AREA_PANEL * alpha_s * GAMMA * ETA_ELEC * F_AEFF if _theta_mask_alb(theta_deg) else 0.0

    # Conducción interna
    q_cond = 0.0
    for n, c in enumerate(cond_row):
        q_cond += c * (T[n] - Ti)

    # Radiación interna
    q_rad = 0.0
    for n, fv in enumerate(fv_row):
        q_rad += EPS_AL * SIGMA * fv * AREA_PANEL * (T[n]**4 - Ti**4)

    return Ti + (dt / (MASA_PANEL * CP_PANEL)) * (q_ir + q_esp + q_sol + q_alb + q_cond + q_rad)

def _yface_common(i, T, dt, cond_row, fv_row, theta_deg, F_planet):
    """
    Nodos 9..10 (tapas Y± con white coating).
    Sin F_AEFF/ETA_ELEC (respetando tu implementación).
    """
    Ti = T[i]
    cos_phi = _cos_phi(theta_deg)
    F_planet_cos = F_planet * np.cos(np.radians(theta_deg))

    q_ir = F_planet * eps_wc * AREA_CARA_Y * SIGMA * (T[13]**4)
    q_esp = eps_wc * AREA_CARA_Y * SIGMA * (T[14]**4 - Ti**4)
    q_sol = cos_phi * SCV * AREA_CARA_Y * alpha_wc if _theta_mask_sol(theta_deg) else 0.0
    q_alb = F_planet_cos * SCV * AREA_CARA_Y * alpha_wc * GAMMA if _theta_mask_alb(theta_deg) else 0.0

    q_cond = sum(c * (T[n] - Ti) for n, c in enumerate(cond_row))
    q_rad  = sum(EPS_AL * SIGMA * fv * AREA_CARA_Y * (T[n]**4 - Ti**4) for n, fv in enumerate(fv_row))

    return Ti + (dt / (MASA_CARA_Y * CP_CARA_Y)) * (q_ir + q_esp + q_sol + q_alb + q_cond + q_rad)

def _bandeja_common(i, T, dt, cond_row, fv_row):
    Ti = T[i]
    q_cond = sum(c * (T[n] - Ti) for n, c in enumerate(cond_row))
    q_rad  = sum(EPS_AL * SIGMA * fv * AREA_BANDEJA * (T[n]**4 - Ti**4) for n, fv in enumerate(fv_row))
    return Ti + (dt / (MASA_BANDEJA * CP_BANDEJA)) * (q_cond + q_rad)

def _box_common(i, T, dt, cond_row, fv_row, area, masa, cp, nodo_id, theta_deg):
    Ti = T[i]
    q_cond = sum(c * (T[n] - Ti) for n, c in enumerate(cond_row))
    q_rad  = sum(EPS_AL * SIGMA * fv * area * (T[n]**4 - Ti**4) for n, fv in enumerate(fv_row))
    pot_dis = get_potencia(theta_deg, nodo_id)  # en frío devuelve 0
    return Ti + (dt / (masa * cp)) * (q_cond + q_rad + pot_dis)

# ----------------------------
# Wrappers públicos ecNodo1..13
# ----------------------------
def ecNodo1(T, dt, cond_row, fv_row, theta):  # Z+ panel
    return _panel_common(0, T, dt, cond_row, fv_row, theta, F_PLANET_ZPLUS)

def ecNodo2(T, dt, cond_row, fv_row, theta):  # Z+ panel
    return _panel_common(1, T, dt, cond_row, fv_row, theta, F_PLANET_ZPLUS)

def ecNodo3(T, dt, cond_row, fv_row, theta):  # X- panel (lateral)
    return _panel_common(2, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo4(T, dt, cond_row, fv_row, theta):  # X- panel (lateral)
    return _panel_common(3, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo5(T, dt, cond_row, fv_row, theta):  # Z- panel (no ve Venus)
    return _panel_common(4, T, dt, cond_row, fv_row, theta, F_PLANET_ZMINUS)

def ecNodo6(T, dt, cond_row, fv_row, theta):  # Z- panel
    return _panel_common(5, T, dt, cond_row, fv_row, theta, F_PLANET_ZMINUS)

def ecNodo7(T, dt, cond_row, fv_row, theta):  # X+ panel (lateral)
    return _panel_common(6, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo8(T, dt, cond_row, fv_row, theta):  # X+ panel (lateral)
    return _panel_common(7, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo9(T, dt, cond_row, fv_row, theta):  # Y+ coating
    return _yface_common(8, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo10(T, dt, cond_row, fv_row, theta):  # Y- coating
    return _yface_common(9, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)

def ecNodo11(T, dt, cond_row, fv_row, theta):  # Bandeja
    return _bandeja_common(10, T, dt, cond_row, fv_row)

def ecNodo12(T, dt, cond_row, fv_row, theta):  # OBC/AOCS
    return _box_common(11, T, dt, cond_row, fv_row, AREA_OBC, MASA_OBC, CP_OBC, 12, theta)

def ecNodo13(T, dt, cond_row, fv_row, theta):  # Batería/Tanque
    return _box_common(12, T, dt, cond_row, fv_row, AREA_BAT, MASA_BAT, CP_BAT, 13, theta)

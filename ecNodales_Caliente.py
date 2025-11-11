# By: Johanna Olivera y Ailin Ferrari

# Caso CALIENTE (EOL)

import numpy as np
from constants import *

# Props del caso caliente
props = get_propiedades_caso('caliente')
eps_sa = props['eps_sa']
alpha_s = props['alpha_s']
eps_wc = props['eps_wc']
alpha_wc = props['alpha_wc']
get_potencia = props['get_potencia']  # devuelve potencia para nodos 12/13 según θ

# ----------------------------
# Helpers de ventanas angulares
# ----------------------------
def _theta_mask_sol(theta_deg: float) -> bool:
    return ((THETA_C1 < theta_deg < THETA_C2) or (THETA_C3 < theta_deg < THETA_C4))

def _theta_mask_alb(theta_deg: float) -> bool:
    return ((0 < theta_deg < THETA_C1) or (THETA_C4 < theta_deg < 360))

def _cos_phi(theta_deg: float) -> float:
    return -np.cos(np.radians(theta_deg))

# ----------------------------
# Núcleo por tipo (idéntico a nodeC, cambia get_potencia y props)
# ----------------------------
def _panel_common(i, T, dt, cond_row, fv_row, theta_deg, F_planet):
    Ti = T[i]
    cos_phi = _cos_phi(theta_deg)
    F_planet_cos = F_planet * np.cos(np.radians(theta_deg))

    q_ir = F_planet * eps_sa * AREA_PANEL * SIGMA * (T[13]**4) * F_AEFF
    q_esp = eps_sa * AREA_PANEL * SIGMA * (T[14]**4 - Ti**4)
    q_sol = cos_phi * SCV * AREA_PANEL * alpha_s * ETA_ELEC * F_AEFF if _theta_mask_sol(theta_deg) else 0.0
    q_alb = F_planet_cos * SCV * AREA_PANEL * alpha_s * GAMMA * ETA_ELEC * F_AEFF if _theta_mask_alb(theta_deg) else 0.0

    q_cond = sum(c * (T[n] - Ti) for n, c in enumerate(cond_row))
    q_rad  = sum(EPS_AL * SIGMA * fv * AREA_PANEL * (T[n]**4 - Ti**4) for n, fv in enumerate(fv_row))

    return Ti + (dt / (MASA_PANEL * CP_PANEL)) * (q_ir + q_esp + q_sol + q_alb + q_cond + q_rad)

def _yface_common(i, T, dt, cond_row, fv_row, theta_deg, F_planet):
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
    pot_dis = get_potencia(theta_deg, nodo_id)
    return Ti + (dt / (masa * cp)) * (q_cond + q_rad + pot_dis)

# ----------------------------
# Wrappers públicos
# ----------------------------
def ecNodo1(T, dt, cond_row, fv_row, theta):  return _panel_common(0, T, dt, cond_row, fv_row, theta, F_PLANET_ZPLUS)
def ecNodo2(T, dt, cond_row, fv_row, theta):  return _panel_common(1, T, dt, cond_row, fv_row, theta, F_PLANET_ZPLUS)
def ecNodo3(T, dt, cond_row, fv_row, theta):  return _panel_common(2, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo4(T, dt, cond_row, fv_row, theta):  return _panel_common(3, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo5(T, dt, cond_row, fv_row, theta):  return _panel_common(4, T, dt, cond_row, fv_row, theta, F_PLANET_ZMINUS)
def ecNodo6(T, dt, cond_row, fv_row, theta):  return _panel_common(5, T, dt, cond_row, fv_row, theta, F_PLANET_ZMINUS)
def ecNodo7(T, dt, cond_row, fv_row, theta):  return _panel_common(6, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo8(T, dt, cond_row, fv_row, theta):  return _panel_common(7, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo9(T, dt, cond_row, fv_row, theta):  return _yface_common(8, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo10(T, dt, cond_row, fv_row, theta): return _yface_common(9, T, dt, cond_row, fv_row, theta, F_PLANET_LATERAL)
def ecNodo11(T, dt, cond_row, fv_row, theta): return _bandeja_common(10, T, dt, cond_row, fv_row)
def ecNodo12(T, dt, cond_row, fv_row, theta): return _box_common(11, T, dt, cond_row, fv_row, AREA_OBC, MASA_OBC, CP_OBC, 12, theta)
def ecNodo13(T, dt, cond_row, fv_row, theta): return _box_common(12, T, dt, cond_row, fv_row, AREA_BAT, MASA_BAT, CP_BAT, 13, theta)

# By: Johanna Olivera y Ailin Ferrari

"""
Constantes del sistema de análisis térmico del CubeSat
Todas las constantes físicas y parámetros del modelo térmico
"""

import numpy as np

# ==========================================
# CONSTANTES FÍSICAS UNIVERSALES
# ==========================================
SIGMA = 5.67e-8  # Constante de Stefan-Boltzmann [W/m²K⁴]

# ==========================================
# PARÁMETROS ORBITALES Y AMBIENTALES
# ==========================================
ORBITAL_PERIOD = 5980.55  # Período orbital [s]
T_VENUS = 228  # Temperatura de Venus [K]
T_SPACE = 3  # Temperatura del espacio [K]
SCV = 2611  # Constante solar en Venus [W/m²]
GAMMA = 0.77  # Factor de albedo de Venus

# ==========================================
# TEMPERATURAS OPERACIONALES (AFT)
# ==========================================
# OBC/AOCS (Nodo 12)
AFT_OBC_MIN = -25 + 273.15  # [K]
AFT_OBC_MAX = 65 + 273.15  # [K]

# Batería (Nodo 13)
AFT_BAT_MIN = -10 + 273.15  # [K]
AFT_BAT_MAX = 50 + 273.15  # [K]

# Tanque de butano (Nodo 13)
AFT_TANK_MIN = 0 + 273.15  # [K]
AFT_TANK_MAX = 35 + 273.15  # [K]

# ==========================================
# FACTORES DE VISTA CON VENUS
# ==========================================
F_PLANET_ZPLUS = 0.8277  # Factor de vista Z+ con Venus
F_PLANET_LATERAL = 0.3638  # Factor de vista caras laterales con Venus
F_PLANET_ZMINUS = 0  # Factor de vista Z- con Venus (sin vista directa)

# ==========================================
# PROPIEDADES DE MATERIALES
# ==========================================
# Aluminio
EPS_AL = 0.125  # Emisividad del aluminio

# Solar Array - BOL (Beginning of Life)
EPS_SA_BOL = 0.95  # Emisividad panel solar BOL
ALPHA_S_BOL = 0.65  # Absortividad solar BOL

# Solar Array - EOL (End of Life)
EPS_SA_EOL = 0.85  # Emisividad panel solar EOL
ALPHA_S_EOL = 0.92  # Absortividad solar EOL

# White Thermal Coating - BOL
EPS_WTC_BOL = 0.89  # Emisividad coating BOL
ALPHA_WTC_BOL = 0.212  # Absortividad coating BOL

# White Thermal Coating - EOL
EPS_WTC_EOL = 0.852  # Emisividad coating EOL
ALPHA_WTC_EOL = 0.38  # Absortividad coating EOL

# ==========================================
# FACTORES DE EFICIENCIA
# ==========================================
ETA_ELEC = 1  # Factor de rendimiento energético
F_AEFF = 1  # Factor de área efectiva

# ==========================================
# PROPIEDADES TÉRMICAS DE NODOS
# ==========================================
# Nodos 1-8 (Paneles solares/caras externas)
MASA_PANEL = 0.20565  # [kg]
CP_PANEL = 1156.57  # [J/kgK]
AREA_PANEL = 0.045  # [m²]

# Nodos 9-10 (Caras Y+ y Y- con coating)
MASA_CARA_Y = 0.2493  # [kg]
CP_CARA_Y = 937  # [J/kgK]
AREA_CARA_Y = 0.09  # [m²]

# Nodo 11 (Bandeja)
MASA_BANDEJA = 0.2493  # [kg]
CP_BANDEJA = 937  # [J/kgK]
AREA_BANDEJA = 0.09  # [m²]

# Nodo 12 (OBC/AOCS)
MASA_OBC = 5  # [kg]
CP_OBC = 960  # [J/kgK]
AREA_OBC = 0.2 * 0.2  # [m²]

# Nodo 13 (Batería/Tanque)
MASA_BAT = 5  # [kg]
CP_BAT = 2000  # [J/kgK]
AREA_BAT = 0.2 * 0.2  # [m²]

# ==========================================
# MATRIZ DE CONDUCTANCIAS [W/K]
# ==========================================
C_COND = np.array([
    [0, 0.352, 0.0872, 0, 0, 0, 0.0872, 0, 0.2241, 0, 0.2265, 0, 0],
    [0.352, 0, 0, 0.0872, 0, 0, 0, 0.0872, 0, 0.2241, 0.2265, 0, 0],
    [0.0872, 0, 0, 0.352, 0.0872, 0, 0, 0, 0.2241, 0, 0.2265, 0, 0],
    [0, 0.0872, 0.352, 0, 0, 0.0872, 0, 0, 0, 0.2241, 0.2265, 0, 0],
    [0, 0, 0.0872, 0, 0, 0.352, 0.0872, 0, 0.2241, 0, 0.2265, 0, 0],
    [0, 0, 0, 0.0872, 0.352, 0, 0, 0.0872, 0, 0.2241, 0.2265, 0, 0],
    [0.0872, 0, 0, 0, 0.0872, 0, 0, 0.352, 0.2241, 0, 0.2265, 0, 0],
    [0, 0.0872, 0, 0, 0, 0.0872, 0.352, 0, 0, 0.2241, 0.2265, 0, 0],
    [0.2241, 0, 0.2241, 0, 0.2241, 0, 0.2241, 0, 0, 0, 0, 0, 0],
    [0, 0.2241, 0, 0.2241, 0, 0.2241, 0, 0.2241, 0, 0, 0, 0, 0],
    [0.2265, 0.2265, 0.2265, 0.2265, 0.2265, 0.2265, 0.2265, 0.2265, 0, 0, 0, 110.94, 100.94],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100.94, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100.94, 0, 0]
])

# ==========================================
# MATRIZ DE FACTORES DE VISTA
# ==========================================
F_VIEW = np.array([
    [0, 0, 0.15, 0, 0.015, 0, 0.15, 0, 0.33, 0, 0.37, 0.16, 0],
    [0, 0, 0, 0.15, 0, 0.015, 0, 0.15, 0, 0.33, 0.37, 0, 0.16],
    [0.15, 0, 0, 0, 0.15, 0, 0.015, 0, 0.33, 0, 0.37, 0.16, 0],
    [0, 0.15, 0, 0, 0, 0.15, 0, 0.015, 0, 0.33, 0.37, 0, 0.16],
    [0.015, 0, 0.15, 0, 0, 0, 0.15, 0, 0.33, 0, 0.37, 0.16, 0],
    [0, 0.015, 0, 0.15, 0, 0, 0, 0.15, 0, 0.33, 0.37, 0, 0.16],
    [0.15, 0, 0.015, 0, 0.15, 0, 0, 0, 0.33, 0, 0.37, 0.16, 0],
    [0, 0.15, 0, 0.015, 0, 0.15, 0, 0, 0, 0.33, 0.37, 0, 0.16],
    [0.33, 0, 0.33, 0, 0.33, 0, 0.33, 0, 0, 0, 0.37, 0.39, 0],
    [0, 0.33, 0, 0.33, 0, 0.33, 0, 0.33, 0, 0, 0.37, 0, 0.39],
    [0.37, 0.37, 0.37, 0.37, 0.37, 0.37, 0.37, 0.37, 0.37, 0.37, 0, 0.08, 0.08],
    [0.16, 0, 0.16, 0, 0.16, 0, 0.16, 0, 0.39, 0, 0.08, 0, 0],
    [0, 0.16, 0, 0.16, 0, 0.16, 0, 0.16, 0, 0.39, 0.08, 0, 0]
])

# ==========================================
# CONDICIONES INICIALES - CASO CALIENTE [K]
# ==========================================
T_INICIAL_CALIENTE = [
    273.15 + 51.768380887451315,   # Nodo 1
    273.15 + 51.766202110884535,   # Nodo 2
    273.15 + 23.43624663704486,    # Nodo 3
    273.15 + 23.43346705086799,    # Nodo 4
    273.15 + 13.159464848627977,   # Nodo 5
    273.15 + 13.157062190410727,   # Nodo 6
    273.15 + 23.43624663704486,    # Nodo 7
    273.15 + 23.43346705086799,    # Nodo 8
    273.15 + 17.688041454037204,   # Nodo 9
    273.15 + 17.679055033100724,   # Nodo 10
    273.15 + 22.106952394620237,   # Nodo 11
    273.15 + 22.414968196217615,   # Nodo 12
    273.15 + 22.153055266061358,   # Nodo 13
    T_VENUS,                        # Nodo 14 (Venus)
    T_SPACE                         # Nodo 15 (Espacio)
]

# ==========================================
# CONDICIONES INICIALES - CASO FRÍO [K]
# ==========================================
T_INICIAL_FRIO = [
    273.15 + 3.304536468119295,     # Nodo 1
    273.15 + 3.304204908677832,     # Nodo 2
    273.15 - 19.958827414203995,    # Nodo 3
    273.15 - 19.959197582088336,    # Nodo 4
    273.15 - 29.881899035517677,    # Nodo 5
    273.15 - 29.88200030554924,     # Nodo 6
    273.15 - 19.958827414203995,    # Nodo 7
    273.15 - 19.959197582088336,    # Nodo 8
    273.15 - 22.423850457711808,    # Nodo 9
    273.15 - 22.425049514203266,    # Nodo 10
    273.15 - 34.28890318418789,     # Nodo 11
    273.15 - 34.291808049396565,    # Nodo 12
    273.15 - 34.30208303181928,     # Nodo 13
    T_VENUS,                         # Nodo 14 (Venus)
    T_SPACE                          # Nodo 15 (Espacio)
]

# ==========================================
# ÁNGULOS CRÍTICOS ORBITALES [grados]
# ==========================================
THETA_C1 = 90
THETA_C2 = 115
THETA_C3 = 245
THETA_C4 = 270

# ==========================================
# POTENCIAS DISIPADAS - CASO CALIENTE
# ==========================================
def get_potencia_disipada_caliente(theta, nodo):
    """
    Retorna la potencia disipada para el caso caliente
    
    Parameters:
    -----------
    theta : float
        Ángulo orbital [grados]
    nodo : int
        Número de nodo (12 o 13)
    
    Returns:
    --------
    float : Potencia disipada [W]
    """
    if nodo == 12:  # OBC/AOCS
        if 0 < theta < 108:
            return 50
        elif 236 < theta < 272:
            return 15
        else:
            return 0
    elif nodo == 13:  # Batería/Tanque
        return 15
    else:
        return 0

# ==========================================
# POTENCIAS DISIPADAS - CASO FRÍO
# ==========================================
def get_potencia_disipada_frio(theta, nodo):
    """
    Retorna la potencia disipada para el caso frío
    
    Parameters:
    -----------
    theta : float
        Ángulo orbital [grados]
    nodo : int
        Número de nodo (12 o 13)
    
    Returns:
    --------
    float : Potencia disipada [W]
    """
    # En caso frío no hay potencia disipada
    return 0

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def get_propiedades_caso(caso='caliente'):
    """
    Retorna un diccionario con las propiedades según el caso (BOL/EOL)
    
    Parameters:
    -----------
    caso : str
        'caliente' para EOL o 'frio' para BOL
    
    Returns:
    --------
    dict : Diccionario con propiedades del material
    """
    if caso.lower() == 'caliente':
        return {
            'eps_sa': EPS_SA_EOL,
            'alpha_s': ALPHA_S_EOL,
            'eps_wc': EPS_WTC_EOL,
            'alpha_wc': ALPHA_WTC_EOL,
            'T_inicial': T_INICIAL_CALIENTE,
            'get_potencia': get_potencia_disipada_caliente
        }
    else:  # caso frío
        return {
            'eps_sa': EPS_SA_BOL,
            'alpha_s': ALPHA_S_BOL,
            'eps_wc': EPS_WTC_BOL,
            'alpha_wc': ALPHA_WTC_BOL,
            'T_inicial': T_INICIAL_FRIO,
            'get_potencia': get_potencia_disipada_frio
        }

def get_factor_planeta(nodo):
    """
    Retorna el factor de vista con Venus según el nodo
    
    Parameters:
    -----------
    nodo : int
        Número de nodo (1-13)
    
    Returns:
    --------
    float : Factor de vista con Venus
    """
    if nodo in [1, 2]:  # Z+
        return F_PLANET_ZPLUS
    elif nodo in [5, 6]:  # Z-
        return F_PLANET_ZMINUS
    else:  # Caras laterales
        return F_PLANET_LATERAL
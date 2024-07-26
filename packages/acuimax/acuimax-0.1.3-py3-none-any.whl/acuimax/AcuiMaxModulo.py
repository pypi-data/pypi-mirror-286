# Importar las funciones del archivo funciones_acuiferos.py
from AcuiMax import calcular_capacidad_carga, calcular_tiempo_agotamiento

# Datos del acuífero A (ejemplo)
T_A = 2000   # Transmisividad del acuífero A [m^2/día]
R_A = 0.5    # Recarga anual del acuífero A [m/día]
alpha_A = 0.9  # Factor de seguridad para el acuífero A
V_A = 1000000  # Volumen total del acuífero A [m³]

# Datos del acuífero B (ejemplo)
T_B = 5000   # Transmisividad del acuífero B [m^2/día]
R_B = 0.8    # Recarga anual del acuífero B [m/día]
alpha_B = 0.95  # Factor de seguridad para el acuífero B
V_B = 2000000  # Volumen total del acuífero B [m³]

# Calcular la capacidad de carga y el tiempo de agotamiento para el acuífero A
Q_max_A = calcular_capacidad_carga(T_A, R_A, alpha_A)
t_agot_A = calcular_tiempo_agotamiento(V_A, Q_max_A)

# Calcular la capacidad de carga y el tiempo de agotamiento para el acuífero B
Q_max_B = calcular_capacidad_carga(T_B, R_B, alpha_B)
t_agot_B = calcular_tiempo_agotamiento(V_B, Q_max_B)

# Impresión de los resultados
print("Los resultados son:")
print(f"Acuífero A: Capacidad de carga máxima = {Q_max_A:.2f} m³/día, Tiempo de agotamiento = {t_agot_A:.2f} días")
print(f"Acuífero B: Capacidad de carga máxima = {Q_max_B:.2f} m³/día, Tiempo de agotamiento = {t_agot_B:.2f} días")


from AcuiMax import capacidad_carga_maxima, tiempo_agotamiento
import numpy as np

# Datos de los acuíferos A y B
transmisividad = np.array([2000, 5000])  # Ejemplos: [A, B]
recarga_anual = np.array([0.5, 0.8])
factor_seguridad = np.array([0.9, 0.95])
volumen = np.array([1000000, 2000000])

# Cálculo de la capacidad de carga máxima para ambos acuíferos
qmax = capacidad_carga_maxima(transmisividad, recarga_anual, factor_seguridad)

# Cálculo del tiempo de agotamiento para ambos acuíferos
tagot = tiempo_agotamiento(volumen, qmax)

# Imprimir resultados
print("Los resultados son:")
print(f"Capacidad de carga máxima del acuífero A: {qmax[0]:.2f} m³/día")
print(f"Capacidad de carga máxima del acuífero B: {qmax[1]:.2f} m³/día")
print(f"Tiempo de agotamiento del acuífero A: {tagot[0]:.2f} días")
print(f"Tiempo de agotamiento del acuífero B: {tagot[1]:.2f} días")

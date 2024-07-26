def calcular_capacidad_carga(T, R, alpha):
    return alpha * R * T

def calcular_tiempo_agotamiento(V, Q_max):
    return V / Q_max

def capacidad_carga_maxima(transmisividad, recarga_anual, factor_seguridad):
    return factor_seguridad * recarga_anual * transmisividad

def tiempo_agotamiento(volumen, capacidad_carga_maxima):
    return volumen / capacidad_carga_maxima

import matplotlib.pyplot as plt
import numpy as np

# Definir funciones para cálculos
def capacidad_carga_maxima(transmitividad, recarga_anual, factor_seguridad):
    return transmitividad * recarga_anual * factor_seguridad

def tiempo_agotamiento(volumen, capacidad_carga_maxima):
    return volumen / capacidad_carga_maxima

def graficar_acuiferos(acuiferos, capacidades, tiempos):
    # Crear la figura y los ejes
    fig, ax1 = plt.subplots()

    # Graficar la capacidad de carga máxima (barras)
    color ='tab:blue'
    ax1.set_xlabel("Acuiferos")
    ax1.set_ylabel("Capacidad de Carga maxima (m3/dia)", color=color)
    ax1.bar(acuiferos, capacidades, color=color, alpha=0.6)
    ax1.tick_params(axis="y", labelcolor=color)

    # Crear un segundo eje para el tiempo
    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.plot(acuiferos, tiempos, color=color, marker='o')
    ax2.set_ylabel('Tiempo de Agotamiento (días)', color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    # Ajustar el diseño
    fig.tight_layout()
    plt.title("Capacidad de carga maxima y tiempo de agotamiento de los acuideros")

    # Mostrar el gráfico
    plt.show()

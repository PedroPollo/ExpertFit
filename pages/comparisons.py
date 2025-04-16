import flet as ft  # type: ignore
import numpy as np
import pandas as pd # type: ignore
import matplotlib # type: ignore
from scipy import stats # type: ignore
import matplotlib.pyplot as plt # type: ignore
from flet.matplotlib_chart import MatplotlibChart # type: ignore
import warnings
from components import navbar, appbar

warnings.filterwarnings("ignore", category=DeprecationWarning)

matplotlib.use("svg")

def ComparisonsScreen(page):
    mejor_modelo = page.best_model
    intervalos = page.current_intervals
    data = page.dataframe
    parametros = page.best_model_params
    
    #Funcion para crear la comparacion
    def create_comparison_chart(data, num_bins, model_name=None, model_params=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Verificar que los datos sean numéricos
        try:
            data = np.array(data, dtype=float)
        except (ValueError, TypeError):
            ax.text(0.5, 0.5, "Error: Los datos no son numéricos", 
                    ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Crear histograma normalizado (density=True para que el área = 1)
        counts, bins, patches = ax.hist(data, bins=num_bins, density=True, 
                                        alpha=0.6, color='skyblue', label='Datos')
        
        # Si tenemos el mejor modelo, graficar su PDF
        if model_name and model_params:
            try:
                # Crear rango de valores para la curva
                x = np.linspace(float(np.min(data)), float(np.max(data)), 1000)
                
                # Obtener la distribución
                dist = getattr(stats, model_name)
                
                # Asegurar que los parámetros sean numéricos
                if isinstance(model_params, (list, tuple, np.ndarray)):
                    # Convertir explícitamente a array de floats
                    params = np.array([float(p) if isinstance(p, (int, float, np.number)) else p 
                                    for p in model_params], dtype=float)
                else:
                    params = np.array([float(model_params)], dtype=float)
                
                # Calcular la función de densidad de probabilidad (PDF)
                pdf = dist.pdf(x, *params)
                
                # Graficar la curva del modelo
                ax.plot(x, pdf, 'r-', linewidth=2, label=f'Modelo {model_name}')
                
                ax.set_title(f'Comparación: Histograma vs Modelo {model_name}')
            except Exception as e:
                import traceback
                traceback.print_exc()
                ax.set_title('Histograma de datos (error al cargar modelo)')
        else:
            ax.set_title('Histograma de datos (sin modelo seleccionado)')
        
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad')
        ax.legend()
        
        return fig
    
    fig = create_comparison_chart(data, intervalos, mejor_modelo, parametros)
    chart = MatplotlibChart(fig, expand = True)
    
    return ft.View(
        "/comparisons",
        [
            appbar.appBar(page, "Comparasiones"),
            chart,
            navbar.NavigationBar(page)
        ]
    )
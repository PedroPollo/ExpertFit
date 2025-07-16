import flet as ft  # type: ignore
import numpy as np
from scipy import stats  # type: ignore
from components import navbar, appbar

def ModelsScreen(page):
    data = page.dataframe
    
    # Inicializar estado si no existe
    if not hasattr(page, 'distribution_results'):
        page.distribution_results = {}
    
    if not hasattr(page, 'selected_model'):
        page.selected_model = None
    
    # Asegurarse de que best_model_params exista
    if not hasattr(page, 'best_model_params'):
        page.best_model_params = None
    
    # Diccionario con descripciones de las distribuciones
    descripciones_distribuciones = {
        'norm': "Distribución Normal (Gaussiana): Distribución simétrica en forma de campana. Útil para modelar variables que son resultado de muchos efectos aleatorios pequeños e independientes.",
        'expon': "Distribución Exponencial: Describe el tiempo entre eventos en un proceso de Poisson. Útil para modelar tiempos de espera o la vida útil de componentes.",
        'gamma': "Distribución Gamma: Generalización de la exponencial. Útil para modelar variables que representan el tiempo hasta que ocurran n eventos.",
        'weibull_min': "Distribución Weibull: Comúnmente usada en análisis de confiabilidad y supervivencia. Describe el tiempo hasta el fallo de sistemas.",
        'lognorm': "Distribución Log-Normal: Útil cuando el logaritmo de la variable sigue una distribución normal. Común en fenómenos de crecimiento o procesos multiplicativos.",
        'beta': "Distribución Beta: Usada para modelar proporciones y probabilidades. Es muy versátil y puede tomar diversas formas según sus parámetros.",
        't': "Distribución t de Student: Similar a la normal pero con colas más pesadas. Útil en inferencia estadística con muestras pequeñas.",
        'cauchy': "Distribución de Cauchy: Tiene colas muy pesadas. Útil para modelar fenómenos con valores extremos frecuentes.",
        'pareto': "Distribución de Pareto: Sigue el principio de Pareto (80-20). Útil para modelar distribuciones de riqueza, tamaño de ciudades, etc.",
        'loglaplace': "Distribución Log-Laplace: Variación de la distribución de Laplace donde el logaritmo de la variable sigue una distribución de Laplace.",
        'weibull_max': "Distribución Weibull Máxima: Versión de la distribución Weibull utilizada para modelar valores máximos.",
        'gompertz': "Distribución Gompertz: Comúnmente utilizada en demografía y seguros para modelar la mortalidad humana.",
        'logistic': "Distribución Logística: Similar a la normal pero con colas más pesadas. Usada en modelos de crecimiento y regresión logística.",
        'invgauss': "Distribución Gaussiana Inversa: Modela el tiempo que tarda una partícula en alcanzar un umbral en movimiento browniano con deriva.",
        'genextreme': "Distribución de Valor Extremo Generalizada: Combina tres tipos de distribuciones para modelar valores máximos o mínimos.",
        'genpareto': "Distribución Pareto Generalizada: Extensión de la distribución de Pareto. Usada en el análisis de valores extremos.",
        'triang': "Distribución Triangular: Simple y limitada por mínimo, máximo y moda. Útil cuando se conocen estos tres valores.",
        'powerlaw': "Distribución Power Law: Describe fenómenos donde la probabilidad disminuye con una potencia de la variable."
    }
    
    # Texto para la descripción del modelo
    descripcion_modelo = ft.Text(
        value="", 
        size=16,
        selectable=True,
        text_align=ft.TextAlign.JUSTIFY,
        width=700,
    )
    
    result_text = ft.Text(
        value="", 
        size=18, 
        weight="bold", 
        color=ft.colors.GREEN,
        text_align=ft.TextAlign.CENTER,
        selectable=True
    )
    
    dropdown = ft.Dropdown(
        label="Seleccionar modelo",
        width=300,
        options=[],
        on_change=lambda e: actualizar_resultado(e)
    )
    
    # Recuperar resultados anteriores si existen
    distribuciones_resultado = page.distribution_results if hasattr(page, 'distribution_results') else {}
    
    # Texto para mostrar resultados generales
    resultados_generales = ft.Text(
        value="", 
        size=16,
        color=ft.colors.BLUE,
        selectable=True
    )
    
    def actualizar_resultado(e):
        seleccion = dropdown.value
        if seleccion in distribuciones_resultado:
            # Actualizar el texto mostrado
            result_text.value = distribuciones_resultado[seleccion]
            
            # Mostrar descripción del modelo seleccionado
            if seleccion in descripciones_distribuciones:
                descripcion_modelo.value = descripciones_distribuciones[seleccion]
            else:
                descripcion_modelo.value = "No hay descripción disponible para este modelo."
            
            # Guardar el modelo seleccionado en page
            page.best_model = seleccion
            page.selected_model = seleccion
            
            # Actualizar los parámetros del modelo seleccionado
            try:
                dist = getattr(stats, seleccion)
                # Calcular y guardar los parámetros del modelo seleccionado
                page.best_model_params = dist.fit(data)
            except Exception as ex:
                print(f"Error al actualizar parámetros: {ex}")
                # En caso de error, asegurarse de que haya un valor para best_model_params
                if not page.best_model_params:
                    page.best_model_params = None
            
        page.update()
    
    def evaluar_distribuciones(e):
        try:
            distribuciones = ['norm', 'expon', 'gamma', 'weibull_min', 'lognorm', 'beta', 't', 'cauchy', 'pareto', 'loglaplace', 'weibull_max', 'gompertz', 'logistic', 'invgauss', 'genextreme', 'genpareto', 'triang', 'powerlaw']
            resultados = []
            distribuciones_resultado.clear()
            
            for dist_name in distribuciones:
                try:
                    dist = getattr(stats, dist_name)
                    params = dist.fit(data)
                    
                    # Asegura que los parámetros estén bien pasados como tupla
                    D, p = stats.kstest(data, dist_name, args=tuple(params))
                    
                    # Verificar que p sea un número escalar, no un array
                    if isinstance(p, np.ndarray):
                        p_value = float(p[0])  # Convertir el primer elemento a float
                    else:
                        p_value = float(p)
                    
                    resultados.append((dist_name, p_value))
                    distribuciones_resultado[dist_name] = f"Distribución: {dist_name}\nD = {float(D):.4f}\np-valor = {p_value:.4f}"
                except Exception as ex:
                    resultados.append((dist_name, f"Error: {ex}"))
                    distribuciones_resultado[dist_name] = f"Distribución: {dist_name}\nError: {ex}"
            
            # Filtramos solo distribuciones con p válido
            p_validos = [(d, p) for d, p in resultados if isinstance(p, (float, int))]
            
            texto_general = "📊 Resultados del análisis:\n\n"
            
            if p_validos:
                # Buscar la distribución con el mejor p-valor (mayor es mejor)
                mejor_ajuste = max(p_validos, key=lambda x: x[1])
                mejor_dist = mejor_ajuste[0]
                texto_general += f"✅ Mejor distribución según p-valor: {mejor_dist} (p-valor: {mejor_ajuste[1]:.4f})\n\n"
                
                # Mostrar descripción del mejor modelo
                if mejor_dist in descripciones_distribuciones:
                    descripcion_modelo.value = descripciones_distribuciones[mejor_dist]
                else:
                    descripcion_modelo.value = "No hay descripción disponible para este modelo."
            else:
                mejor_dist = None
                texto_general += f"⚠️ No se encontró un p-valor válido.\n\n"
                descripcion_modelo.value = ""
            
            # Guardar resultados en page para persistencia
            page.distribution_results = distribuciones_resultado.copy()
            
            if mejor_dist:
                page.best_model = mejor_dist
                page.selected_model = mejor_dist
                # También podemos guardar los parámetros para usarlos en la pantalla de comparación
                try:
                    dist = getattr(stats, mejor_dist)
                    page.best_model_params = dist.fit(data)
                except Exception as ex:
                    print(f"Error al guardar parámetros del mejor modelo: {ex}")
                    page.best_model_params = None
            
            texto_general += "Todas las distribuciones evaluadas:\n"
            for d, p in resultados:
                if isinstance(p, (float, int)):
                    texto_general += f"- {d}: p-valor = {p:.4f}\n"
                else:
                    texto_general += f"- {d}: {p}\n"
            
            resultados_generales.value = texto_general
            
            # Actualizar el dropdown con las opciones de distribuciones válidas
            dropdown_options = []
            for d, p in resultados:
                if isinstance(p, (float, int)):
                    dropdown_options.append(ft.dropdown.Option(d))
            
            dropdown.options = dropdown_options
            
            # Mostrar mensaje si no hay opciones en el dropdown
            if not dropdown_options:
                result_text.value = "No se encontraron distribuciones válidas para mostrar en el dropdown"
                descripcion_modelo.value = ""
            elif mejor_dist:
                # Seleccionar el mejor ajuste por defecto
                dropdown.value = mejor_dist
                result_text.value = distribuciones_resultado[mejor_dist]
            
            page.update()
        
        except Exception as ex:
            result_text.value = f"Error al procesar los datos: {ex}"
            resultados_generales.value = ""
            descripcion_modelo.value = ""
            page.update()

    # Cargar estado previo cuando se vuelve a esta pantalla
    def cargar_estado_previo():
        # Si ya hay resultados guardados, cargar el dropdown
        if hasattr(page, 'distribution_results') and page.distribution_results:
            dropdown_options = []
            for dist_name in page.distribution_results:
                # Solo agregar si es un resultado válido (no contiene "Error:")
                if "Error:" not in page.distribution_results[dist_name]:
                    dropdown_options.append(ft.dropdown.Option(dist_name))
            
            dropdown.options = dropdown_options
            
            # Restaurar la selección anterior si existe
            if hasattr(page, 'selected_model') and page.selected_model:
                try:
                    dropdown.value = page.selected_model
                    result_text.value = page.distribution_results[page.selected_model]
                    
                    # Mostrar descripción del modelo restaurado
                    if page.selected_model in descripciones_distribuciones:
                        descripcion_modelo.value = descripciones_distribuciones[page.selected_model]
                    else:
                        descripcion_modelo.value = "No hay descripción disponible para este modelo."
                    
                    # Asegurarse de que los parámetros estén actualizados
                    if not hasattr(page, 'best_model_params') or page.best_model_params is None:
                        dist = getattr(stats, page.selected_model)
                        page.best_model_params = dist.fit(data)
                except Exception as ex:
                    print(f"Error al restaurar selección: {ex}")
            
            # Restaurar resultados generales si hay un mejor modelo
            if hasattr(page, 'best_model') and page.best_model:
                try:
                    mejor_dist = page.best_model
                    texto_general = "📊 Resultados del análisis:\n\n"
                    texto_general += f"✅ Mejor distribución según p-valor: {mejor_dist}\n\n"
                    texto_general += "Todas las distribuciones evaluadas:\n"
                    
                    for dist_name in page.distribution_results:
                        if "Error:" not in page.distribution_results[dist_name]:
                            # Extraer p-valor del texto guardado
                            texto = page.distribution_results[dist_name]
                            try:
                                p_valor = float(texto.split("p-valor = ")[1])
                                texto_general += f"- {dist_name}: p-valor = {p_valor:.4f}\n"
                            except:
                                texto_general += f"- {dist_name}\n"
                    
                    resultados_generales.value = texto_general
                except Exception as ex:
                    print(f"Error al restaurar resultados generales: {ex}")

    # Ejecutar la carga de estado previo al iniciar la vista
    try:
        cargar_estado_previo()
    except Exception as ex:
        print(f"Error al cargar estado previo: {ex}")

    return ft.View(
        "/models",
        [
            appbar.appBar(page, "Models"),
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton("Evaluar distribuciones", on_click=evaluar_distribuciones),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            result_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Nuevo elemento para mostrar la descripción del modelo
                    ft.Row(
                        [
                            descripcion_modelo,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            resultados_generales,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
                scroll="auto",
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            navbar.NavigationBar(page)
        ]
    )
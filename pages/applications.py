import flet as ft  # type: ignore
from components import navbar, appbar

def ApplicationsScreen(page):
    modelo = page.best_model
    parametros = page.best_model_params
    print(f"Modelo Seleccionado: {modelo}")
    print(f"Parametros del modelo: {parametros}")
    return ft.View(
        "/applications",
        [
            appbar.appBar(page, "Aplicaciones"),
            ft.Text("Applications"),
            navbar.NavigationBar(page)
        ]
    )
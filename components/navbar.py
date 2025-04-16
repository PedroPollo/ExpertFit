import flet as ft  # type: ignore

def NavigationBar(page):
    selected_index = page.client_storage.get("selected_index") or 0
    
    nav_bar =  ft.NavigationBar(
        selected_index=selected_index,
        destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.DATA_THRESHOLDING_ROUNDED, label="Data"),
            ft.NavigationBarDestination(icon=ft.Icons.MODEL_TRAINING_ROUNDED, label="Models"),
            ft.NavigationBarDestination(icon=ft.Icons.AUTO_GRAPH_ROUNDED, label="Comparaciones"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_APPLICATIONS_ROUNDED, label="Aplicacion"),
        ],
        on_change=lambda e: change_page(e, page, nav_bar)
    )
    
    return nav_bar

def change_page(e, page, nav_bar):
    index = e.control.selected_index
    routes = ["/data","/models","/comparisons","/applications"]
    
    page.client_storage.set("selected_index", index)
    
    page.go(routes[index])
import flet as ft # type: ignore
from pages import home, dataloaded, applications, comparisons, data, models


def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(home.HomeScreen(page))
        elif page.route == "/data":
            page.views.append(data.DataScreen(page))
        elif page.route == "/models":
            page.views.append(models.ModelsScreen(page))
        elif page.route == "/comparisons":
            page.views.append(comparisons.ComparisonsScreen(page))
        elif page.route == "/applications":
            page.views.append(applications.ApplicationsScreen(page))
        elif page.route == "/dataloaded":
            page.views.append(dataloaded.DataLoadedScreen(page))
        
        page.update()
        
    page.on_route_change = route_change
    page.go("/")


ft.app(main)

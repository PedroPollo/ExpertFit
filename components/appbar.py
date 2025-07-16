import flet as ft  # type: ignore

def appBar(page, texto):
    return ft.AppBar(
                title = ft.Text(texto),
                center_title = True,
                leading = ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: page.go("/dataloaded")),
            )
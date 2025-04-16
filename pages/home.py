import flet as ft  # type: ignore
from components.navbar import NavigationBar

def HomeScreen(page):
    trabajos = ["Trabajo 1","Trabajo 2","Trabajo 3"]
    return ft.View(
        "/",
        [
            ft.Column(
                [
                    ft.Text("Trabajos anteriores", size=20),
                    #Poner para mostrar los trabajos guardados
                    #Hacerlos botones para que cada uno nos lleve a poder editarlos
                    
                    ft.ListView(
                        [
                            ft.Container(
                                ft.ElevatedButton(t),
                                padding=10
                            )
                            for t in trabajos
                        ],
                        height="500"
                    ),
                    
                    
                    ft.ElevatedButton(text="Crear nuevo", on_click=lambda e: page.go("/dataloaded"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )
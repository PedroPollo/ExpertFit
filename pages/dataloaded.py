import flet as ft # type: ignore
import pandas as pd # type: ignore
import warnings
from components import navbar, appbar

warnings.filterwarnings("ignore", category=DeprecationWarning)

def DataLoadedScreen(page):

    infotxt = ft.Text()
    table_container = ft.Column()

    # Botón que solo se activa al cargar datos
    continuar_btn = ft.ElevatedButton(
        "Continuar",
        disabled=True,
        on_click=lambda e: page.go("/data"),  # Puedes cambiar la ruta
    )

    def cargar_tabla_desde_df(df, file_path=None):
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
            rows=[
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                )
                for _, row in df.iterrows()
            ]
        )

        table_container.controls.clear()
        table_container.controls.append(table)
        continuar_btn.disabled = False
        infotxt.value = f"Archivo cargado: {file_path}" if file_path else "Datos previamente cargados"
        page.update()

    def cargar_csv(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                df = pd.read_csv(file_path)
                page.dataframe = df
                cargar_tabla_desde_df(df, file_path)

            except Exception as ex:
                continuar_btn.disabled = True
                infotxt.value = f"Error al cargar CSV: {ex}"
                page.update()

    # Verificar si ya hay un dataframe previamente cargado
    if hasattr(page, "dataframe") and page.dataframe is not None:
        cargar_tabla_desde_df(page.dataframe)

    file_picker = ft.FilePicker(on_result=cargar_csv)
    page.overlay.append(file_picker)
    page.update()

    cargar_btn = ft.ElevatedButton(
        "Seleccionar archivo CSV",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["csv"]
        )
    )

    return ft.View(
        "/dataloaded",
        controls=[
            appbar.appBar(page, "Cargar Datos"),
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.TextField(label="Nombre del proyecto"),
                        ft.ElevatedButton(
                            "Volver", 
                            on_click=lambda e: (setattr(page, "dataframe", None), page.go("/"))
                            ),
                        cargar_btn,
                        infotxt,
                        table_container,
                        continuar_btn
                    ],
                    scroll="auto",
                    alignment="center",
                    horizontal_alignment="center",
                    expand=True,
                ),
            )
        ]
    )
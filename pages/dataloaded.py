import io
import pandas as pd
import flet as ft

def DataLoadedScreen(page):

    infotxt = ft.Text()
    table_container = ft.Column()

    continuar_btn = ft.ElevatedButton(
        "Continuar",
        disabled=True,
        on_click=lambda e: page.go("/data"),
    )

    def cargar_tabla_desde_df(df, file_name=None):
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
        infotxt.value = f"Archivo cargado: {file_name}" if file_name else "Datos previamente cargados"
        page.update()

    def cargar_csv(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        f = e.files[0]
        try:
            # ✅ Verificamos que sea CSV
            if not f.name.endswith(".csv"):
                infotxt.value = "Error: Solo se permiten archivos CSV"
                continuar_btn.disabled = True
                page.update()
                return

            df = None

            # ✅ Caso escritorio (tiene path real)
            if hasattr(f, "path") and f.path:
                df = pd.read_csv(f.path)

            # ✅ Caso web (usa contenido en memoria)
            elif hasattr(f, "content") and f.content:
                df = pd.read_csv(io.BytesIO(f.content))

            # ✅ Si no se pudo leer
            if df is None:
                raise ValueError("El archivo no tiene ni 'path' ni 'content' válidos")

            # Guardamos el dataframe en la página
            page.dataframe = df
            cargar_tabla_desde_df(df, f.name)

        except Exception as ex:
            continuar_btn.disabled = True
            infotxt.value = f"Error al cargar CSV: {ex}"
            page.update()

    file_picker = ft.FilePicker(on_result=cargar_csv)
    page.overlay.append(file_picker)
    page.update()

    cargar_btn = ft.ElevatedButton(
        "Seleccionar archivo CSV",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["csv"]  # ✅ Solo CSV
        )
    )

    if hasattr(page, "dataframe") and page.dataframe is not None:
        cargar_tabla_desde_df(page.dataframe)

    return ft.View(
        "/dataloaded",
        controls=[
            ft.AppBar(title=ft.Text("Cargar Datos")),
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

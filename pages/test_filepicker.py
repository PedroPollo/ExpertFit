import flet as ft

def main(page: ft.Page):
    def on_result(e: ft.FilePickerResultEvent):
        if e.files:
            page.dialog = ft.AlertDialog(title=ft.Text(f"Archivo seleccionado: {e.files[0].name}"))
            page.dialog.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=on_result)
    page.overlay.append(file_picker)
    page.update()

    page.add(
        ft.ElevatedButton("Seleccionar archivo", on_click=lambda _: file_picker.pick_files())
    )

ft.app(target=main)

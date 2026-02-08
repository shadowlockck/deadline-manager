import flet as ft
import datetime



def main(page: ft.Page):
    page.title = "Task manager"
    page.theme_mode = "dark"

    def date_changed(e):
        if date_picker.value:
            date_text.value = f"Дедайн через {(date_picker.value.date() - datetime.date.today()).days} днів"
            page.update()

    def open_picker(e):
        date_picker.open = True
        page.update()


    date_text = ft.Text("Дата не вибрана")


    date_picker = ft.DatePicker(
        first_date=datetime.datetime.now(),
        on_change=lambda e: date_changed(e)
    )

    page.overlay.append(date_picker)


    btn = ft.ElevatedButton("Вибрати дату", on_click=open_picker)

    page.add(btn, date_text)


ft.app(target=main)

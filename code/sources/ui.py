import flet as ft
import datetime


def main(page: ft.Page):
    page.title = "Task manager"
    page.theme_mode = "dark"

    selected_deadline = None 

    def date_changed(e):
        nonlocal selected_deadline
        selected_deadline = date_picker.value
        page.update()

    def open_picker(e):
        date_picker.open = True
        page.update()


    def task_created(e):
        if not name_of_task.value.strip() and selected_deadline is None:
            error.value = "Введи назву задачі і вибери дедлайн"
            
            page.update()
            return

        elif selected_deadline is None:
            error.value = "Спочатку вибери дедлайн"
            page.update()
            return
            
        elif not name_of_task.value.strip():
            error.value = "Введи назву задачі"
            page.update()
            return
        
        error.value = "Завдання Успішно створено!"
        error.color = "green"
        



    name_of_task = ft.TextField(label="Назва задачі")

    date_picker = ft.DatePicker(
        first_date=datetime.datetime.now(),
        last_date=datetime.datetime(2030, 12, 31),
        on_change=date_changed
    )

    page.overlay.append(date_picker)


    pick_btn = ft.ElevatedButton("Вибрати дедлайн", on_click=open_picker)
    create_btn = ft.ElevatedButton("Створити задачу", on_click=task_created)
    error = ft.Text("", color="red")
    

    page.add(
        name_of_task,
        pick_btn,
        create_btn,
        error,
    )


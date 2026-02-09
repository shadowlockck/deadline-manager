import flet as ft
import datetime
import sources.tasks as tasks


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
        no_name = not name_of_task.value.strip()
        no_deadline = selected_deadline is None
        no_priority = priority.value is None
        
        match (no_name, no_deadline, no_priority):

            case (True, True, True):
                error.value = "Введи назву задачі, вибери дедлайн та пріоритет"
                return

            case (True, True, False):
                error.value = "Введи назву задачі та вибери дедлайн"
                return

            case (True, False, True):
                error.value = "Введи назву задачі та вибери пріоритет"
                return

            case (False, True, True):
                error.value = "Вибери дедлайн та пріоритет"
                return

            case (True, False, False):
                error.value = "Введи назву задачі"
                return

            case (False, True, False):
                error.value = "Вибери дедлайн"
                return

            case (False, False, True):
                error.value = "Вибери пріоритет"
                return

            case (False, False, False):
                error.value = ""
                page.update()

        
        error.value = "Завдання Успішно створено!"
        error.color = "green"

        tasks.create_task(name_of_task.value, selected_deadline.strftime("%Y-%m-%d"), priority.value)
        



    name_of_task = ft.TextField(label="Назва задачі")

    date_picker = ft.DatePicker(
        first_date=datetime.datetime.now(),
        last_date=datetime.datetime(2030, 12, 31),
        on_change=date_changed
    )

    page.overlay.append(date_picker)


    pick_btn = ft.ElevatedButton("Вибрати дедлайн", on_click=open_picker)
    create_btn = ft.ElevatedButton("Створити задачу", on_click=task_created)
    priority = ft.Dropdown(
        options=[
            ft.dropdown.Option("P3"),
            ft.dropdown.Option("P2"),
            ft.dropdown.Option("P1"),
        ],
        label="Пріоритет"


    )
    error = ft.Text("", color="red")
    

    page.add(
        name_of_task,
        pick_btn,
        priority,
        create_btn,
        error,
    )


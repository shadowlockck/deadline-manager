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

    def load_tasks():
        tasks_column.controls.clear()

        db = tasks.import_db()

        for task in db:
            name = task["name"]
            deadline = task["deadline"]
            priority_value = task["priority"]

            deadline_date = datetime.datetime.fromisoformat(deadline).date()
            days = (deadline_date - datetime.date.today()).days

            if days < 0:
                subtitle = f"Прострочено на {abs(days)} днів | {priority_value}"
            else:
                subtitle = f"{days} днів | {priority_value}"

            tile = ft.ListTile(
                title=ft.Text(name),
                subtitle=ft.Text(subtitle)
            )

            tasks_column.controls.append(tile)

        page.update()



    def task_created(e):
        no_name = not name_of_task.value.strip()
        no_deadline = selected_deadline is None
        no_priority = priority.value is None
          
        match (no_name, no_deadline, no_priority):

            case (True, True, True):
                error.value = "Введи назву задачі, вибери дедлайн та пріоритет"
                name_of_task.border_color = "red"
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
                name_of_task.border_color = "red"
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

        
        error.value = "Завдання Успішно створено!",
        error.color = "green"

        tasks.create_task(name_of_task.value, selected_deadline.strftime("%Y-%m-%d"), priority.value)
        load_tasks()
        


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

    sort_tasks = ft.Dropdown(
        options=[
            ft.dropdown.Option("За назвою"),
            ft.dropdown.Option("За дедлайном"),
            ft.dropdown.Option("За пріоритетом"),
        ],
        label="Сортувати задачі"
    )

    filter_tasks = ft.Dropdown(
        options=[
            ft.dropdown.Option("Всі задачі"),
            ft.dropdown.Option("Прострочені"),
            ],
        label="Сортувати задачі"
    )

    error = ft.Text("", color="red")
    tasks_column = ft.Column(
        scroll="auto",
        expand=True,
        spacing=10
    )


    sort_tasks.width=150
    filter_tasks.width=150

    left_panel = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(sort_tasks, expand=True),
                        ft.Container(filter_tasks, expand=True),
                    ],
                    spacing=10
                ),
                ft.Divider(),
                tasks_column
            ],
            expand=True,
            spacing=10
        ),
        width=350,
        padding=15,
    )


    create_panel = ft.Container(
        content=ft.Column(
            [
                name_of_task,
                pick_btn,
                create_btn,
                error,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=40
    )



    page.add(
    ft.Row(
        [
            left_panel,
            ft.VerticalDivider(width=1),
            create_panel
        ],
        expand=True
    )
)


    

    load_tasks()
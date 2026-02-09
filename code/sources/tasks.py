import json
import os

def import_db():
    try:
        with open("code/data/task.json", "r", encoding="utf-8") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = []

    return db

def save_db(db):
    os.makedirs("data", exist_ok=True)

    with open("code/data/task.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)


def create_task(name_of_task, deadline, priority):
    db = import_db()

    new_task = {
        "name": name_of_task,
        "deadline": deadline,
        "priority": priority
    }

    db.append(new_task)
    save_db(db)

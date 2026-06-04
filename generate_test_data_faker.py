#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор тестових даних для БД it_project_management.

Як використовувати:
1. Спочатку виконай CREATE TABLE скрипт у MySQL Workbench.
2. Запусти цей файл: python generate_test_data.py
3. У результаті буде створено файл test_data.sql.
4. Відкрий test_data.sql у MySQL Workbench і виконай його.

Скрипт використовує бібліотеку Faker: pip install faker
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
import random

try:
    from faker import Faker
except ImportError as exc:
    raise SystemExit("Потрібно встановити Faker: pip install faker") from exc

random.seed(42)
Faker.seed(42)
fake = Faker(["uk_UA", "en_US"])

OUTPUT_FILE = "test_data_faker.sql"
SCHEMA_NAME = "it_project_management"

# Для навантажувального тестування: 8 проєктів × 130–180 задач ≈ 1000–1400 задач.
# Якщо потрібно менше даних, наприклад для швидкої перевірки, постав 7 і 12.
TASKS_PER_PROJECT_MIN = 130
TASKS_PER_PROJECT_MAX = 180


def sql_value(value):
    """Перетворює Python-значення в SQL-значення."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, datetime):
        return f"'{value.isoformat(sep=' ')}'"
    if isinstance(value, date):
        return f"'{value.isoformat()}'"
    text = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{text}'"


def insert_many(table: str, columns: list[str], rows: list[tuple]) -> str:
    """Формує INSERT INTO з кількома рядками."""
    cols = ", ".join(f"`{c}`" for c in columns)
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_value(v) for v in row) + ")")
    return f"INSERT INTO `{table}` ({cols}) VALUES\n" + ",\n".join(values) + ";\n"


def d(y, m, day):
    return date(y, m, day)


def dt(day: date, hour: int = 10, minute: int = 0):
    return datetime(day.year, day.month, day.day, hour, minute, 0)


def rand_date(start: date, end: date) -> date:
    if end < start:
        return start
    return start + timedelta(days=random.randint(0, (end - start).days))


# -------------------------
# Довідники
# -------------------------

project_statuses = [
    (1, "Planned", 0),
    (2, "Active", 0),
    (3, "Paused", 0),
    (4, "Completed", 1),
    (5, "Archived", 1),
]

task_statuses = [
    (1, "Backlog", 0, 1),
    (2, "To Do", 0, 2),
    (3, "In Progress", 0, 3),
    (4, "Code Review", 0, 4),
    (5, "Testing", 0, 5),
    (6, "Done", 1, 6),
]

task_priorities = [
    (1, "Low", 72),
    (2, "Medium", 48),
    (3, "High", 24),
    (4, "Critical", 8),
]

task_types = [
    (1, "Feature", "Нова функціональність системи"),
    (2, "Bug", "Виправлення помилки"),
    (3, "Task", "Технічна або організаційна задача"),
    (4, "Improvement", "Покращення існуючої функціональності"),
    (5, "Research", "Дослідження або аналіз технічного рішення"),
    (6, "Documentation", "Підготовка або оновлення документації"),
]

employee_roles = [
    (1, "Project Manager", 45.00, "Керує проєктом, строками та комунікацією з клієнтом"),
    (2, "Scrum Master", 38.00, "Координує роботу команди в межах Agile-процесу"),
    (3, "Backend Developer", 35.00, "Розробляє серверну частину системи"),
    (4, "Frontend Developer", 32.00, "Розробляє клієнтську частину системи"),
    (5, "QA Engineer", 25.00, "Перевіряє якість функціональності"),
    (6, "DevOps Engineer", 40.00, "Підтримує інфраструктуру, CI/CD та середовища"),
    (7, "Business Analyst", 30.00, "Аналізує вимоги клієнтів і формує задачі"),
    (8, "UI/UX Designer", 28.00, "Проєктує інтерфейси та користувацький досвід"),
]

departments = [
    (1, "Project Management Office", None),
    (2, "Software Development", None),
    (3, "Quality Assurance", None),
    (4, "DevOps and Infrastructure", None),
    (5, "Business Analysis and Design", None),
]

skills = [
    (1, "Python", "Programming", "Розробка серверної логіки та автоматизація"),
    (2, "Java", "Programming", "Розробка корпоративних застосунків"),
    (3, "JavaScript", "Programming", "Клієнтська та серверна веброзробка"),
    (4, "React", "Programming", "Розробка SPA-інтерфейсів"),
    (5, "Node.js", "Programming", "Серверна розробка на JavaScript"),
    (6, "MySQL", "Database", "Проєктування та адміністрування реляційних БД"),
    (7, "PostgreSQL", "Database", "Робота з реляційними БД"),
    (8, "Docker", "DevOps", "Контейнеризація застосунків"),
    (9, "Kubernetes", "DevOps", "Оркестрація контейнерів"),
    (10, "GitLab CI/CD", "DevOps", "Автоматизація збірки та деплою"),
    (11, "Manual Testing", "QA", "Ручне тестування функціональності"),
    (12, "Automated Testing", "QA", "Автоматизація тестування"),
    (13, "Figma", "Design", "Проєктування інтерфейсів"),
    (14, "UX Research", "Design", "Дослідження користувацького досвіду"),
    (15, "Scrum", "Management", "Організація роботи за Scrum"),
    (16, "Kanban", "Management", "Візуалізація та оптимізація потоку задач"),
    (17, "Requirements Analysis", "Management", "Збір та аналіз вимог"),
    (18, "Communication", "Soft Skills", "Командна комунікація"),
    (19, "Problem Solving", "Soft Skills", "Пошук рішень у складних ситуаціях"),
    (20, "Technical Writing", "Other", "Підготовка технічної документації"),
]

industries = [
    "FinTech",
    "Healthcare",
    "Education",
    "Logistics",
    "Retail",
    "Public Sector",
    "E-commerce",
    "Telecommunications",
]

countries = ["Ukraine", "Poland", "Germany", "Romania", "Moldova", "Czech Republic"]

company_prefixes = [
    "Green", "Smart", "Nova", "Core", "Digital", "Cloud", "Urban", "Global",
    "Prime", "Next", "Data", "Bright", "Soft", "Agile", "City"
]

company_suffixes = [
    "Pay", "Med", "Edu", "Track", "Retail", "Gov", "Market", "Telecom",
    "Logix", "CRM", "Analytics", "Services", "Systems", "Hub"
]


def fake_phone(country: str = "Ukraine") -> str:
    """Створює короткий тестовий телефон у безпечному форматі."""
    if country == "Ukraine":
        return "+380" + "".join(str(random.randint(0, 9)) for _ in range(9))
    if country == "Poland":
        return "+48" + "".join(str(random.randint(0, 9)) for _ in range(9))
    if country == "Germany":
        return "+49" + "".join(str(random.randint(0, 9)) for _ in range(10))
    if country == "Romania":
        return "+40" + "".join(str(random.randint(0, 9)) for _ in range(9))
    return "+" + "".join(str(random.randint(0, 9)) for _ in range(11))


def build_clients(count: int = 8):
    """Генерує клієнтів через Faker та власні IT-шаблони."""
    rows = []
    used_names = set()

    for client_id in range(1, count + 1):
        country = random.choice(countries)
        industry = random.choice(industries)

        for _ in range(100):
            client_name = f"{random.choice(company_prefixes)}{random.choice(company_suffixes)} {random.choice(['Solutions', 'Digital', 'Group', 'Systems', 'Labs', 'Platform'])}"
            if client_name not in used_names:
                used_names.add(client_name)
                break
        else:
            client_name = fake.unique.company()

        contact_person = fake.name()
        contact_email = f"contact{client_id}@client{client_id}.example"
        phone = fake_phone(country)

        rows.append((client_id, client_name, industry, country, contact_person, contact_email, phone))

    return rows


clients = build_clients(8)

role_dept_plan = [
    (1, 1), (2, 1),          # PM, Scrum Master
    (3, 2), (3, 2),          # Backend
    (4, 2), (4, 2),          # Frontend
    (5, 3), (5, 3),          # QA
    (6, 4), (6, 4),          # DevOps
    (7, 5), (8, 5),          # BA, Designer
    (3, 2), (4, 2), (5, 3), (3, 2), (7, 5), (4, 2), (6, 4), (5, 3),
]


def build_employees():
    """Генерує працівників через Faker, але з контрольованими ролями та відділами."""
    rows = []
    used_emails = set()

    for employee_id, (role_id, dept_id) in enumerate(role_dept_plan, start=1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        email = f"employee{employee_id:02d}@itcompany.example"
        if email in used_emails:
            email = f"user{employee_id:02d}@itcompany.example"
        used_emails.add(email)

        phone = "+38050" + f"{employee_id:06d}"
        hire_date = rand_date(d(2019, 1, 1), d(2024, 5, 30))
        is_active = 0 if employee_id == 20 else 1

        rows.append((employee_id, first_name, last_name, email, phone, hire_date, role_id, dept_id, is_active))

    return rows


employees = build_employees()

department_managers = [
    (1, 1),
    (2, 3),
    (3, 7),
    (4, 9),
    (5, 11),
]

project_modules = [
    "Mobile Platform",
    "Admin Portal",
    "Patient CRM",
    "LMS Upgrade",
    "Fleet Dashboard",
    "Analytics Module",
    "Service Portal",
    "Legacy Migration",
    "Customer Cabinet",
    "Reporting System",
]

project_domains = [
    "Payments",
    "Healthcare",
    "Education",
    "Logistics",
    "Retail",
    "Municipal Services",
    "Document Management",
    "Task Management",
    "Data Analytics",
]

project_descriptions = [
    "Розробка вебсистеми для автоматизації бізнес-процесів клієнта",
    "Створення модуля для обробки заявок, звітів та користувацьких даних",
    "Оновлення існуючої платформи з урахуванням нових вимог замовника",
    "Розробка аналітичного інтерфейсу для контролю показників роботи",
    "Міграція застарілої системи на нову архітектуру та базу даних",
]


def build_projects():
    """Генерує проєкти для клієнтів, зберігаючи контрольовані дати та статуси."""
    base = [
        # project_id, client_id, status_id, start, planned_end, actual_end, budget
        (1, 1, 2, d(2025, 1, 15), d(2025, 9, 30), None, 120000.00),
        (2, 1, 4, d(2024, 3, 1), d(2024, 10, 31), d(2024, 10, 20), 85000.00),
        (3, 2, 2, d(2025, 2, 10), d(2025, 11, 15), None, 150000.00),
        (4, 3, 1, d(2025, 7, 1), d(2026, 1, 31), None, 60000.00),
        (5, 4, 2, d(2025, 4, 5), d(2025, 12, 15), None, 110000.00),
        (6, 5, 3, d(2024, 12, 10), d(2025, 8, 30), None, 90000.00),
        (7, 6, 2, d(2025, 3, 20), d(2025, 12, 20), None, 130000.00),
        (8, 3, 5, d(2023, 5, 1), d(2023, 12, 30), d(2023, 12, 22), 70000.00),
    ]

    rows = []
    used_by_client = {}

    for project_id, client_id, status_id, start, planned_end, actual_end, budget in base:
        for _ in range(100):
            project_name = f"{random.choice(project_domains)} {random.choice(project_modules)}"
            if project_name not in used_by_client.setdefault(client_id, set()):
                used_by_client[client_id].add(project_name)
                break
        else:
            project_name = f"{fake.bs().title()} Platform"

        description = random.choice(project_descriptions)
        rows.append((project_id, client_id, status_id, project_name, description, start, planned_end, actual_end, budget))

    return rows


projects = build_projects()


def build_employee_skills():
    mapping = {
        1: [15, 16, 18, 19],
        2: [15, 16, 18],
        3: [1, 6, 7, 19],
        4: [1, 5, 6, 8],
        5: [3, 4, 13],
        6: [3, 4, 5, 13],
        7: [11, 12, 19],
        8: [11, 12, 20],
        9: [8, 9, 10, 19],
        10: [8, 10, 6],
        11: [17, 18, 20],
        12: [13, 14, 18],
        13: [2, 6, 7],
        14: [3, 4, 14],
        15: [11, 12, 16],
        16: [1, 2, 6, 8],
        17: [17, 18, 20],
        18: [3, 4, 5],
        19: [8, 9, 10],
        20: [11, 18],
    }
    rows = []
    for employee_id, skill_ids in mapping.items():
        for skill_id in skill_ids:
            level = random.randint(2, 5)
            confirmed = rand_date(d(2024, 1, 1), d(2025, 5, 30))
            rows.append((employee_id, skill_id, level, confirmed))
    return rows


project_teams = {
    1: [1, 2, 3, 4, 5, 7, 9, 11],
    2: [1, 3, 5, 7, 10, 11],
    3: [1, 2, 4, 6, 8, 10, 12, 13],
    4: [1, 11, 12, 14, 17, 18],
    5: [2, 3, 6, 7, 9, 15, 19],
    6: [1, 4, 5, 8, 10, 11, 16],
    7: [1, 2, 3, 7, 9, 12, 13, 15],
    8: [1, 3, 5, 7, 11, 12],
}

role_by_employee = {row[0]: row[6] for row in employees}
role_titles = {row[0]: row[1] for row in employee_roles}
project_start = {row[0]: row[5] for row in projects}
project_planned_end = {row[0]: row[6] for row in projects}
project_actual_end = {row[0]: row[7] for row in projects}
project_status = {row[0]: row[2] for row in projects}


def build_project_members():
    rows = []
    for project_id, members in project_teams.items():
        start = project_start[project_id]
        actual_end = project_actual_end[project_id]
        for employee_id in members:
            project_role = role_titles[role_by_employee[employee_id]]
            allocation = random.choice([25.00, 50.00, 75.00, 100.00])
            joined = start + timedelta(days=random.randint(0, 14))
            left = None
            if actual_end and random.random() < 0.7:
                left = actual_end
            rows.append((project_id, employee_id, project_role, allocation, joined, left))
    return rows


def build_sprints():
    rows = []
    sprint_id = 1
    for project in projects:
        project_id = project[0]
        status = project[2]
        start = project[5]
        count = {
            1: 1,  # Planned
            2: 3,  # Active
            3: 2,  # Paused
            4: 4,  # Completed
            5: 2,  # Archived
        }[status]
        current_start = start
        for sprint_number in range(1, count + 1):
            end = current_start + timedelta(days=13)
            goal = random.choice([
                "Реалізація базової функціональності",
                "Покращення інтерфейсу користувача",
                "Інтеграція з зовнішніми сервісами",
                "Оптимізація продуктивності",
                "Стабілізація та виправлення помилок",
                "Підготовка релізної версії",
            ])
            velocity = random.choice([20, 25, 30, 35, 40])
            rows.append((sprint_id, project_id, sprint_number, goal, current_start, end, velocity))
            sprint_id += 1
            current_start = end + timedelta(days=1)
    return rows


sprints = build_sprints()
sprints_by_project = {}
for s in sprints:
    sprints_by_project.setdefault(s[1], []).append(s)


task_actions = [
    "Розробити",
    "Оновити",
    "Оптимізувати",
    "Налаштувати",
    "Додати",
    "Виправити",
    "Перевірити",
    "Інтегрувати",
    "Покращити",
    "Підготувати",
    "Реалізувати",
    "Автоматизувати",
]

task_objects = [
    "модуль авторизації",
    "REST API для проєктів",
    "сторінку задач",
    "форму створення клієнта",
    "експорт звітів",
    "фільтрацію за статусами",
    "облік витраченого часу",
    "панель project-менеджера",
    "сторінку профілю працівника",
    "дашборд активних проєктів",
    "валідацію вхідних даних",
    "пошук за клієнтами",
    "систему коментарів",
    "CI/CD pipeline",
    "SQL-запит для аналітики",
    "тестові сценарії",
    "технічну документацію",
    "моніторинг застосунку",
    "адаптивність інтерфейсу",
]

task_contexts = [
    "для клієнтського порталу",
    "для адміністративної частини",
    "для мобільної версії",
    "для внутрішньої команди",
    "для звітності",
    "для нового релізу",
    "для поточного спринту",
    "для інтеграції з зовнішнім сервісом",
    "",
    "",
]


def generate_task_title() -> str:
    """Генерує більш різноманітну назву задачі з кількох частин."""
    title = f"{random.choice(task_actions)} {random.choice(task_objects)}"
    context = random.choice(task_contexts)
    if context:
        title = f"{title} {context}"
    return title


description_templates = [
    "Необхідно виконати задачу з урахуванням вимог проєкту та поточного стану системи.",
    "Після реалізації потрібно провести перевірку, code review та оновити документацію.",
    "Задача пов’язана з покращенням роботи користувацького інтерфейсу та стабільності системи.",
    "Результат має бути перевірений QA-інженером перед переведенням задачі у фінальний статус.",
    "Потрібно врахувати існуючу архітектуру бази даних та погоджені бізнес-вимоги.",
    "Реалізація має не порушувати роботу пов’язаних модулів і наявних інтеграцій.",
]


def generate_task_description() -> str:
    """Генерує опис задачі. Faker додає невеликий варіативний фрагмент."""
    if random.random() < 0.75:
        return random.choice(description_templates)
    return random.choice(description_templates) + " " + fake.sentence(nb_words=8)



def choose_project_reporter(project_id: int) -> int:
    members = project_teams[project_id]
    managers = [m for m in members if role_by_employee[m] in (1, 2, 7)]
    return random.choice(managers or members)


def build_tasks():
    rows = []
    task_id = 1

    for project_id in range(1, 9):
        members = project_teams[project_id]
        project_sprints = sprints_by_project[project_id]
        start = project_start[project_id]
        planned_end = project_planned_end[project_id]
        status = project_status[project_id]

        tasks_count = random.randint(TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX)
        for _ in range(tasks_count):
            in_backlog = random.random() < 0.18
            sprint = None if in_backlog else random.choice(project_sprints)
            if sprint:
                created = rand_date(sprint[4], sprint[5])
            else:
                created = rand_date(start, min(planned_end, start + timedelta(days=120)))

            # Важливо: created_at створюємо ДО completed_at.
            # Інакше може вийти completed_at раніше за created_at у межах одного дня,
            # що порушує CHECK (completed_at IS NULL OR completed_at >= created_at).
            created_at = dt(created, random.randint(9, 17), random.choice([0, 15, 30, 45]))

            assignee = None if in_backlog and random.random() < 0.5 else random.choice(members)
            reporter = choose_project_reporter(project_id)
            type_id = random.choice([1, 1, 2, 3, 4, 5, 6])
            priority_id = random.choice([1, 2, 2, 3, 3, 4])
            story_points = random.choice([1.0, 2.0, 3.0, 5.0, 8.0, 13.0])

            if status in (4, 5):
                status_id = random.choice([6, 6, 6, 5])
            elif status == 1:
                status_id = random.choice([1, 2])
            elif status == 3:
                status_id = random.choice([2, 3, 4])
            else:
                status_id = random.choice([1, 2, 3, 4, 5, 6])

            due = created + timedelta(days=random.choice([3, 5, 7, 10, 14, 21]))
            if due > planned_end:
                due = planned_end

            completed = None
            if status_id == 6:
                completed_day = rand_date(created, due)
                if completed_day == created:
                    # Якщо задача завершена в той самий день, час завершення має бути
                    # не раніше created_at.
                    completed = created_at + timedelta(hours=random.randint(1, 8))
                else:
                    completed = dt(completed_day, random.randint(10, 18), random.choice([0, 15, 30, 45]))

            rows.append((
                task_id,
                project_id,
                None if sprint is None else sprint[0],
                assignee,
                reporter,
                type_id,
                status_id,
                priority_id,
                generate_task_title(),
                generate_task_description(),
                story_points,
                created_at,
                due,
                completed,
            ))
            task_id += 1
    return rows


tasks = build_tasks()


def build_time_logs():
    rows = []
    log_id = 1
    for task in tasks:
        task_id, project_id, _sprint_id, assignee_id, reporter_id, *_rest = task
        status_id = task[6]
        created_at = task[11].date()
        due_date = task[12]
        completed_at = task[13].date() if task[13] else None

        if assignee_id is None or status_id in (1, 2):
            continue

        if status_id == 6:
            count = random.randint(2, 5)
        elif status_id in (3, 4, 5):
            count = random.randint(1, 3)
        else:
            count = random.randint(0, 1)

        end_date = completed_at or min(due_date, created_at + timedelta(days=10))
        for _ in range(count):
            log_date = rand_date(created_at, end_date)
            hours = random.choice([0.50, 1.00, 1.50, 2.00, 2.50, 3.00, 4.00, 5.00, 6.00])
            desc = random.choice([
                "Робота над реалізацією задачі",
                "Аналіз вимог та уточнення деталей",
                "Виправлення помилок після перевірки",
                "Підготовка змін до перевірки",
                "Тестування та перевірка результату",
            ])
            created = dt(log_date, random.randint(10, 18), random.choice([0, 15, 30, 45]))
            rows.append((log_id, task_id, assignee_id, hours, log_date, desc, created))
            log_id += 1
    return rows


def build_task_comments():
    rows = []
    comment_id = 1
    comment_templates = [
        "Потрібно уточнити вимоги перед реалізацією.",
        "Зміни передані на перевірку.",
        "Після тестування виявлено додаткові правки.",
        "Реалізація відповідає описаним вимогам.",
        "Додано уточнення щодо очікуваного результату.",
        "Потрібно оновити документацію після завершення задачі.",
        "Задачу можна перенести в наступний статус.",
        "Потрібно перевірити вплив змін на суміжні модулі.",
        "Команда погодила запропонований підхід до реалізації.",
        "Необхідно додати короткий опис змін у релізні нотатки.",
    ]

    for task in tasks:
        if random.random() > 0.65:
            continue
        task_id = task[0]
        project_id = task[1]
        assignee_id = task[3]
        reporter_id = task[4]
        created_at = task[11].date()
        members = project_teams[project_id]

        for _ in range(random.randint(1, 3)):
            possible_authors = [reporter_id] + ([assignee_id] if assignee_id else []) + members
            author_id = random.choice(possible_authors)
            comment_day = rand_date(created_at, min(created_at + timedelta(days=14), task[12]))
            created = dt(comment_day, random.randint(9, 18), random.choice([0, 15, 30, 45]))
            updated = None
            if random.random() < 0.2:
                updated = created + timedelta(hours=random.randint(1, 8))
            content = random.choice(comment_templates)
            if random.random() < 0.25:
                content = content + " " + fake.sentence(nb_words=7)
            rows.append((comment_id, task_id, author_id, content, created, updated))
            comment_id += 1
    return rows


time_logs = build_time_logs()
task_comments = build_task_comments()


def main():
    sql_parts = [
        "-- Тестові дані для бази даних it_project_management\n",
        "-- Згенеровано файлом generate_test_data_faker.py\n\n",
        f"USE `{SCHEMA_NAME}`;\n\n",
        "SET FOREIGN_KEY_CHECKS = 0;\n",
        "TRUNCATE TABLE `task_comments`;\n",
        "TRUNCATE TABLE `time_logs`;\n",
        "TRUNCATE TABLE `tasks`;\n",
        "TRUNCATE TABLE `sprints`;\n",
        "TRUNCATE TABLE `project_members`;\n",
        "TRUNCATE TABLE `employee_skills`;\n",
        "TRUNCATE TABLE `projects`;\n",
        "TRUNCATE TABLE `employees`;\n",
        "TRUNCATE TABLE `departments`;\n",
        "TRUNCATE TABLE `clients`;\n",
        "TRUNCATE TABLE `skills`;\n",
        "TRUNCATE TABLE `employee_roles`;\n",
        "TRUNCATE TABLE `task_types`;\n",
        "TRUNCATE TABLE `task_priorities`;\n",
        "TRUNCATE TABLE `task_statuses`;\n",
        "TRUNCATE TABLE `project_statuses`;\n",
        "SET FOREIGN_KEY_CHECKS = 1;\n\n",
    ]

    sql_parts.append(insert_many("project_statuses", ["project_status_id", "status_name", "is_final"], project_statuses))
    sql_parts.append(insert_many("task_statuses", ["status_id", "status_name", "is_final", "sort_order"], task_statuses))
    sql_parts.append(insert_many("task_priorities", ["priority_id", "priority_label", "response_time_sla_hours"], task_priorities))
    sql_parts.append(insert_many("task_types", ["type_id", "type_name", "description"], task_types))
    sql_parts.append(insert_many("employee_roles", ["role_id", "role_title", "base_hourly_rate", "description"], employee_roles))
    sql_parts.append(insert_many("departments", ["dept_id", "dept_name", "manager_id"], departments))
    sql_parts.append(insert_many("skills", ["skill_id", "skill_name", "category", "description"], skills))
    sql_parts.append(insert_many("clients", ["client_id", "client_name", "industry", "country", "contact_person", "contact_email", "phone"], clients))
    sql_parts.append(insert_many("employees", ["employee_id", "first_name", "last_name", "email", "phone", "hire_date", "role_id", "dept_id", "is_active"], employees))

    for dept_id, manager_id in department_managers:
        sql_parts.append(f"UPDATE `departments` SET `manager_id` = {manager_id} WHERE `dept_id` = {dept_id};\n")
    sql_parts.append("\n")

    sql_parts.append(insert_many("projects", ["project_id", "client_id", "project_status_id", "project_name", "description", "start_date", "planned_end_date", "actual_end_date", "total_budget"], projects))
    sql_parts.append(insert_many("employee_skills", ["employee_id", "skill_id", "proficiency_level", "confirmed_at"], build_employee_skills()))
    sql_parts.append(insert_many("project_members", ["project_id", "employee_id", "project_role", "allocation_percentage", "joined_at", "left_at"], build_project_members()))
    sql_parts.append(insert_many("sprints", ["sprint_id", "project_id", "sprint_number", "sprint_goal", "start_date", "end_date", "velocity_goal"], sprints))
    sql_parts.append(insert_many("tasks", ["task_id", "project_id", "sprint_id", "assignee_id", "reporter_id", "type_id", "status_id", "priority_id", "task_title", "description", "story_points", "created_at", "due_date", "completed_at"], tasks))
    sql_parts.append(insert_many("time_logs", ["log_id", "task_id", "employee_id", "hours_spent", "log_date", "description", "created_at"], time_logs))
    sql_parts.append(insert_many("task_comments", ["comment_id", "task_id", "author_id", "content", "created_at", "updated_at"], task_comments))

    sql_parts.append("\n-- Контрольні запити для перевірки кількості записів\n")
    for table in [
        "clients", "project_statuses", "projects", "employee_roles", "departments",
        "employees", "skills", "employee_skills", "project_members", "sprints",
        "task_statuses", "task_priorities", "task_types", "tasks", "time_logs", "task_comments"
    ]:
        sql_parts.append(f"SELECT '{table}' AS table_name, COUNT(*) AS row_count FROM `{table}`;\n")

    Path(OUTPUT_FILE).write_text("".join(sql_parts), encoding="utf-8")
    print(f"Готово: створено файл {OUTPUT_FILE}")
    print(f"tasks: {len(tasks)}, time_logs: {len(time_logs)}, task_comments: {len(task_comments)}")


if __name__ == "__main__":
    main()

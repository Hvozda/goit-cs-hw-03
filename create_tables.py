import psycopg2
from faker import Faker
import random

# Дані для підключення
DB_NAME = "task_manager"
USER = "postgres"
PASSWORD = "your_password"
HOST = "localhost"
PORT = "5432"

# Підключення до бази
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
cur = conn.cursor()
fake = Faker()

# 1. Заповнюємо таблицю status
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cur.execute(
        "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (status,)
    )

# 2. Створюємо випадкових користувачів
num_users = 10
for _ in range(num_users):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute(
        "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;",
        (fullname, email)
    )

# 3. Отримуємо id користувачів та статусів
cur.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cur.fetchall()]

# 4. Створюємо випадкові завдання
num_tasks = 30
for _ in range(num_tasks):
    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=100)
    user_id = random.choice(user_ids)
    status_id = random.choice(status_ids)
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
        (title, description, status_id, user_id)
    )

# Зберігаємо зміни і закриваємо підключення
conn.commit()
cur.close()
conn.close()

print("✅ Database seeded successfully!")





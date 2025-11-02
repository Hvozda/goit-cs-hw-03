import psycopg2
from faker import Faker
import random

# Ініціалізація Faker
fake = Faker()

# 🔌 Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="task_manager",
    user="postgres",       # ← заміни, якщо в тебе інше ім'я користувача
    password="your_password",  # ← встав свій пароль
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🧹 Спочатку очищаємо таблиці (щоб уникнути дублікатів)
cur.execute("TRUNCATE tasks RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE users RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE status RESTART IDENTITY CASCADE;")

# 📋 Додаємо статуси
statuses = ['new', 'in progress', 'completed']
for s in statuses:
    cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (s,))

# 👤 Створюємо 10 користувачів
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))

# 📝 Створюємо 20 завдань
for _ in range(20):
    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=100)
    status_id = random.randint(1, len(statuses))  # 1=new, 2=in progress, 3=completed
    user_id = random.randint(1, 10)  # користувачі з id 1-10
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
        (title, description, status_id, user_id)
    )

# 💾 Зберігаємо зміни
conn.commit()

# 🔚 Закриваємо з'єднання
cur.close()
conn.close()

print("✅ Database seeded successfully!")

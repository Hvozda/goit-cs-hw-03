from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, PyMongoError


# ====================== ПІДКЛЮЧЕННЯ ДО БАЗИ ДАНИХ ======================
def get_db():
    """Підключається до локальної або хмарної бази MongoDB."""
    try:
        # 🔹 Локальне підключення (можна замінити URI MongoDB Atlas)
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cats_db"]
        print("✅ Успішне підключення до MongoDB!")
        return db
    except ConnectionFailure:
        print("❌ Не вдалося підключитися до MongoDB!")
        return None


# ====================== CREATE ======================
def create_cat(collection, name, age, features):
    """Додає нового кота в колекцію."""
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"🐾 Кота '{name}' додано з id: {result.inserted_id}")
    except PyMongoError as e:
        print(f"❌ Помилка при створенні кота: {e}")


# ====================== READ ======================
def read_all_cats(collection):
    """Виводить усіх котів із колекції."""
    try:
        cats = collection.find()
        print("\n📜 Список усіх котів:")
        for cat in cats:
            print(cat)
    except PyMongoError as e:
        print(f"❌ Помилка при зчитуванні: {e}")


def read_cat_by_name(collection, name):
    """Виводить інформацію про кота за ім'ям."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(f"\n😺 Знайдено кота: {cat}")
        else:
            print(f"⚠️ Кота з ім'ям '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при пошуку кота: {e}")


# ====================== UPDATE ======================
def update_cat_age(collection, name, new_age):
    """Оновлює вік кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"🔄 Вік кота '{name}' оновлено до {new_age}.")
        else:
            print(f"⚠️ Кота '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при оновленні віку: {e}")


def add_feature_to_cat(collection, name, new_feature):
    """Додає нову характеристику коту за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count:
            print(f"✨ Нову характеристику '{new_feature}' додано коту '{name}'.")
        else:
            print(f"⚠️ Кота '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при оновленні характеристик: {e}")


# ====================== DELETE ======================
def delete_cat_by_name(collection, name):
    """Видаляє кота за ім'ям."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"🗑️ Кота '{name}' видалено.")
        else:
            print(f"⚠️ Кота '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"❌ Помилка при видаленні кота: {e}")


def delete_all_cats(collection):
    """Видаляє всі записи з колекції."""
    try:
        result = collection.delete_many({})
        print(f"🚨 Видалено всіх котів ({result.deleted_count} документів).")
    except PyMongoError as e:
        print(f"❌ Помилка при видаленні всіх котів: {e}")


# ====================== MAIN ======================
if __name__ == "__main__":
    db = get_db()
    if db:
        cats = db.cats  # колекція "cats"

        # ---- Приклади викликів ----
        create_cat(cats, "Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
        create_cat(cats, "Murchyk", 5, ["чорний", "любить спати"])

        read_all_cats(cats)
        read_cat_by_name(cats, "Barsik")

        update_cat_age(cats, "Barsik", 4)
        add_feature_to_cat(cats, "Barsik", "любить їсти рибу")

        delete_cat_by_name(cats, "Murchyk")
        # delete_all_cats(cats)


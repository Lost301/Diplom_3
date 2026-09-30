"""Генерация тестовых данных."""
import uuid


def generate_user():
    """Возвращает словарь с уникальными email, паролем и именем пользователя."""
    return {
        "email": f"diplom3_{uuid.uuid4().hex[:10]}@example.com",
        "password": uuid.uuid4().hex[:10],
        "name": f"user_{uuid.uuid4().hex[:6]}",
    }

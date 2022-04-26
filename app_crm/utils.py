from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


User = get_user_model()


def populate_db():
    for i in range(1, 2):
        manager = User(
            email=f"manager{i}@manager.com", password=make_password("Testing321")
        )
        manager.save()

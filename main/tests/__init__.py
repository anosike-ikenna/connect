from django.contrib.auth import get_user_model

User = get_user_model()

def create_user():
    username = "alice"
    email = "alice@test.com"
    return User.objects.create(username=username, email=email)

def create_fake_user():
    username = "joker"
    email = "joker@test.com"
    return User.objects.create(username=username, email=email)
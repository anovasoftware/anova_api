from django.contrib.auth.hashers import make_password

hashed_password = make_password('1021!')
print(hashed_password)

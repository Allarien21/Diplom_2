import random
import string
import request
import allure

@allure.step("Генерация данных для регистрации")
def generate_new_user_credentials(empty_field=None):
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    def generate_email():
        username = generate_random_string(7)  # Генерируем имя пользователя длиной 7 символов
        domain = generate_random_string(5)  # Генерируем доменное имя длиной 5 символов
        email = f"{username}@{domain}.com"  # Собираем email в формате username@domain.com
        return email

    email = generate_email()
    password = generate_random_string(10)
    name = generate_random_string(10)

    credentials = {
        "email": email,
        "password": password,
        "name": name
    }
    if empty_field is not None:
        credentials[empty_field] = ""
    return credentials

@allure.step("Создание кредов")
def create_login(credentials):
    return {
        'email': credentials['email'],
        'password': credentials['password'],
        'name': credentials['name']
    }

@allure.step("Регистрация пользователя")
def create_user():
    credentials = generate_new_user_credentials()
    return credentials

@allure.step("Авторизация пользователя")
def login_user(credentials):
    login_data = create_login(credentials)
    login_response = request.login_user(login_data)
    return login_response

@allure.step("Авторизация пользователя  и получение его токена")
def login_user_for_token(credentials):
    login_data = create_login(credentials)
    login_response = request.login_user(login_data)
    user_token = login_response.json().get('accessToken')
    return user_token


@allure.step("Удаление пользователя")
def delete_user(credentials):
    user_token = login_user_for_token(credentials)
    headers = {"Authorization": f"{user_token}"}
    request.delete_user(headers)


@allure.step("Обновление данных пользователя с авторизацией")
def update_user_with_authorization(credentials, email=None, name=None):
    user_token = login_user_for_token(credentials)
    headers = {"Authorization": f"{user_token}"}

    update_data = {}
    if email:
        update_data['email'] = email
    if name:
        update_data['name'] = name

    return request.update_user(headers=headers, data=update_data)


@allure.step("Обновление данных пользователя без авторизации")
def update_user_without_authorization(credentials, email=None, name=None):
    update_data = {}
    if email:
        update_data['email'] = email
    if name:
        update_data['name'] = name

    return request.update_user(headers={}, data=update_data)


@allure.step("Создание заказа")
def create_order(credentials, ingredients=None, headers=None):
    if ingredients is None:
        ingredients = ["61c0c5a71d1f82001bdaaa71"]
    if headers is None:
        user_token = login_user_for_token(credentials)
        headers = {"Authorization": f"{user_token}"}
    order_data = {"ingredients": ingredients}
    return request.create_order(headers=headers, data=order_data)


@allure.step("Получение заказов пользователя")
def get_user_orders(credentials=None):
    headers = {}
    if credentials:
        user_token = login_user_for_token(credentials)
        headers = {"Authorization": f"{user_token}"}

    return request.get_orders(headers=headers)
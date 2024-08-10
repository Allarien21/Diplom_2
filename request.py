import requests
import allure
import urls


@allure.step('Создание пользователя')
def create_user(data):
    return requests.post(urls.CREATE_USER, json=data)

@allure.step('Удаление пользователя')
def delete_user(headers):
    return requests.delete(urls.SETTINGS_USER, headers=headers)

@allure.step('Запрос логина пользователя')
def login_user(data):
    return requests.post(urls.LOGIN_USER, json=data)

@allure.step('Обновление данных пользователя')
def update_user(headers, data):
    return requests.patch(urls.SETTINGS_USER, headers=headers, json=data)

@allure.step('Создание заказа')
def create_order(headers, data):
    return requests.post(urls.SETTINGS_ORDERS, headers=headers, json=data)

@allure.step('Получение заказов пользователя')
def get_orders(headers=None):
    return requests.get(urls.SETTINGS_ORDERS, headers=headers)
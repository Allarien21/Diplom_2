import pytest
import allure
import helpers
import data

class TestUpdateUser:
    @allure.title('Изменение данных пользователя с авторизацией')
    @allure.description('Параметризованный тест изменения email и имени пользователя с авторизацией')
    @pytest.mark.parametrize("email, name", [
        (helpers.generate_new_user_credentials()["email"], None),  # Изменяем только email
        (None, helpers.generate_new_user_credentials()["name"]),   # Изменяем только имя
        (helpers.generate_new_user_credentials()["email"], helpers.generate_new_user_credentials()["name"])  # Изменяем оба поля
    ])
    def test_update_user_with_authorization(self, created_user_credentials, email, name):
        # Отправляем запрос на обновление данных пользователя
        update_response = helpers.update_user_with_authorization(created_user_credentials, email=email, name=name)
        assert update_response.status_code == 200

        response_data = update_response.json()

        # Убедимся, что в ответе есть поле 'user'
        assert 'user' in response_data
        user_data = response_data['user']

        if email:
            assert 'email' in user_data
            assert user_data['email'] == email

        if name:
            assert 'name' in user_data
            assert user_data['name'] == name

    @allure.title('Изменение данных пользователя без авторизации')
    @allure.description('Проверка, что неавторизованный пользователь не может изменить данные пользователя')
    def test_update_user_without_authorization(self, created_user_credentials):
        # Генерируем данные для обновления
        email = helpers.generate_new_user_credentials()["email"]
        name = helpers.generate_new_user_credentials()["name"]

        # Отправляем запрос на обновление без авторизации
        update_response = helpers.update_user_without_authorization(created_user_credentials, email=email, name=name)
        assert update_response.status_code == 401

        response_data = update_response.json()
        assert "message" in response_data
        assert response_data["message"] == data.ERROR_UNAUTHORIZED

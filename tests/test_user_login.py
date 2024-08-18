import pytest
import allure
import data
import helpers
import request

class TestLoginUser:
    @allure.title('Успешная авторизация курьера')
    @allure.description('Тест на проверку логина курьера')
    def test_login_user(self, created_user_credentials):
        login_response = request.login_user(created_user_credentials)
        assert login_response.status_code == 200
        assert 'accessToken' in login_response.json()

    @allure.title('Невалидные креды')
    @allure.description('Тест авторизации при неверных учетных данных')
    @pytest.mark.parametrize("invalid_field", ["email", "password"])
    def test_user_login_with_invalid_credentials(self, user_credentials, invalid_field):
        login_data = helpers.create_login(user_credentials)
        new_credentials = helpers.generate_new_user_credentials()

        login_data[invalid_field] = new_credentials[invalid_field]

        login_response = request.login_user(login_data)
        assert login_response.status_code == 401
        assert "message" in login_response.json()
        assert login_response.json()["message"] == data.MESSAGE_UNAUTHORIZED

import pytest
import allure
import data
import helpers
import request

class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_credentials):
        create_response = request.create_user(user_credentials)
        assert create_response.status_code == 200

        response_json = create_response.json()
        assert response_json.get("success") is True

    @allure.title('Теcт на создание дубликата пользователя')
    @allure.description('Создание двух одинаковых пользователя')
    def test_create_duplicated_user(self,user_credentials):
        create_response = request.create_user(user_credentials)
        assert create_response.status_code == 200

        create_response2 = request.create_user(user_credentials)
        assert create_response2.status_code == 403
        assert "message" in create_response2.json()
        assert create_response2.json()["message"] == data.MESSAGE_FORBIDDEN

    @allure.title('Тест на проверку с пустым обязательным полем')
    @allure.description('Создание пользователя с пустым логином,паролем или именем')
    @pytest.mark.parametrize('empty_field', ['email', 'password', 'name'])
    def test_create_user_with_empty_fields(self, empty_field):
        credentials = helpers.generate_new_user_credentials(empty_field=empty_field)
        create_response = request.create_user(credentials)

        assert create_response.status_code == 403
        assert "message" in create_response.json()
        assert create_response.json()["message"] == data.ERROR_EMPTY_FIELD
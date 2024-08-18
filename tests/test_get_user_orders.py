import pytest
import allure
import helpers
import data


class TestGetUserOrders:

    @allure.title('Получение заказов пользователя')
    @allure.description('Проверка, что авторизованный и неавторизованный пользователь может/не может получить заказы')
    @pytest.mark.parametrize("is_authorized, expected_status, expected_success, expected_message", [
        (True, 200, True, None),  # Авторизованный пользователь
        (False, 401, False, data.ERROR_UNAUTHORIZED)  # Неавторизованный пользователь
    ])
    def test_get_orders(self, created_user_credentials, is_authorized, expected_status, expected_success,
                        expected_message):
        credentials = created_user_credentials if is_authorized else None

        # Получение заказов
        response = helpers.get_user_orders(credentials=credentials)

        # Проверка статус-кода
        assert response.status_code == expected_status

        response_data = response.json()

        # Проверка на успешность выполнения
        assert response_data.get("success") == expected_success

        # Проверка на наличие сообщений об ошибке, если таковые ожидаются
        if expected_message:
            assert "message" in response_data
            assert response_data["message"] == expected_message
        else:
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

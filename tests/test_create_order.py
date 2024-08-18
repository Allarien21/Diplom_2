import allure
import data
import helpers

class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_authorization(self, created_user_credentials):
        create_order_response = helpers.create_order(created_user_credentials)
        assert create_order_response.status_code == 200

        response_json = create_order_response.json()

        assert response_json.get("success") is True
        assert "order" in response_json
        assert "number" in response_json["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, created_user_credentials):
        create_order_response = helpers.create_order(created_user_credentials, headers={})
        assert create_order_response.status_code == 200

        response_json = create_order_response.json()

        assert response_json.get("success") is True
        assert "order" in response_json
        assert "number" in response_json["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, created_user_credentials):
        ingredients = ["61c0c5a71d1f82001bdaaa71", "61c0c5a71d1f82001bdaaa72"]
        create_order_response = helpers.create_order(created_user_credentials, ingredients=ingredients)
        assert create_order_response.status_code == 200

        response_json = create_order_response.json()

        assert response_json.get("success") is True
        assert "order" in response_json
        assert "number" in response_json["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, created_user_credentials):
        create_order_response = helpers.create_order(created_user_credentials, ingredients=[])
        assert create_order_response.status_code == 400
        assert create_order_response.json()["message"] == data.ERROR_INGREDIENT

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, created_user_credentials):
        create_order_response = helpers.create_order(created_user_credentials, ingredients=["61c0c5a71d1f82001bdada71"])
        assert create_order_response.status_code == 400
        assert create_order_response.json()["message"] == data.ERROR_WRONG_INGREDIENT
import pytest
import helpers
import request


@pytest.fixture
def user_credentials():
    credentials = helpers.create_user()

    yield credentials

    helpers.delete_user(credentials)


@pytest.fixture
def created_user_credentials(user_credentials):
    request.create_user(user_credentials)

    yield user_credentials

    helpers.delete_user(user_credentials)
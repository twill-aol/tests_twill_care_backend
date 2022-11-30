import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[User] Profile data")
class TestUserData(BaseCase):
    '''Tests user data'''
    exclude_params_subscribe = [
        ("my_user"),
        ("another_user")
    ]

    user_id, email, cookies = MainCase.signup_router()

    @allure.label("user", "profile", "data", "authorization")
    @allure.description("This test checks \
    /api/users/{`user_id`}/")
    @pytest.mark.parametrize("user", exclude_params_subscribe)
    def test_user_data(self, user):
        '''Get user data'''
        if user == "my_user":
            user_id = self.user_id
        else:
            response = MyRequests.get(
                "/api/activity/?page=1&page_size=12&feed_filter=popular",
                cookies=self.cookies
            )
            response_as_dict = BaseCase.response_to_json(response)
            user_id = response_as_dict[0]["user_id"]
        response = MyRequests.get(
            f"/api/users/{user_id}/",
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(
            response,
            [
               "id",
               "composite_id",
               "created_at"
            ]
        )

import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Profile] Skills")
class TestSkills(BaseCase):
    '''Tests  user's Skills'''
    exclude_params_subscribe = [
        ("SA"),
        ("TH"),
        ("AS"),
        ("GI"),
        ("EM"),
        ("RE")
    ]

    user_id, email, cookies = MainCase.signup_router()

    @allure.label("profile", "skills", "authorization", "smoke")
    @allure.description("This test checks /api/v3/skills/ \
    and /api/v3/skills/[skill]/ api")
    @pytest.mark.parametrize("skill", exclude_params_subscribe)
    def test_skills_of_user(self, skill):
        '''Get all skills data and individually'''
        response = MyRequests.get(
            "/api/v3/skills/",
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 200)
        assert skill in str(response.content),\
            "Skill doesn't meet expectations"

        response = MyRequests.get(
            f"/api/v3/skills/{skill}/",
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(
            response,
            [
                "id",
                "name",
                "icon_url",
                "activities"
            ]
        )

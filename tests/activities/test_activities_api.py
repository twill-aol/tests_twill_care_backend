import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Activities] by Skill")
class TestActivitiesSkill(BaseCase):
    '''Tests with autorization'''
    exclude_params_subscribe = [
        ("S-01"),
        ("T-09"),
        ("A-11"),
        ("G-03"),
        ("E-01"),
        ("E-01"),
        ("R-01")
    ]

    user_id, email, cookies = MainCase.signup_router()

    @allure.label("activity", "authorization", "skills", "smoke")
    @allure.description("This test checks /api/activities \
    and api/v3/activity_status api")
    @pytest.mark.parametrize("activity_type", exclude_params_subscribe)
    def test_activities_skill(self, activity_type):
        '''New activity initializes and get its id'''
        with allure.step(f"Complete {activity_type} activity"):
            response = MyRequests.get(
                f"/api/activities/{activity_type}/activity_status/",
                cookies=self.cookies
            )
            activity_id = BaseCase.response_to_json(response)["id"]
            data = {"is_complete": True}
            response = MyRequests.post(
                f"/api/v3/activity_status/{activity_id}/",
                json=data,
                cookies=self.cookies
            )
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_keys(
                response,
                [
                    "scores_old",
                    "image",
                    "show_levelup_modal",
                    "scores_current",
                    "is_first_activity",
                    "is_earned",
                ]
            )
        with allure.step("Check skill points in user's stats"):
            response = MyRequests.get(
                f"/api/users/{self.user_id}/scores/",
                cookies=self.cookies
            )
            Assertions.assert_code_status(response, 200)
            points = self.response_to_json(response)["skills"]["SA"]['points']
            assert points == 21, "Current points does not = 21"

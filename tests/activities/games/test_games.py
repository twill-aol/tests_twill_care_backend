import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Activities] Games")
class TestGames(BaseCase):
    '''Tests Games'''
    exclude_params_subscribe = [
        ("Uplift", 0),
        ("NK", 1),
        ("KC", 2),
        ("HOG", 3),
        ("MEDITATION", 4),
        ("MA", 5)
    ]

    user_id, email, cookies = MainCase.signup_router()

    @allure.label("activities", "game", "autorization", "smoke")
    @allure.description("This test checks \
    /api/activities/game_activity_statuses/ and api/v3/activity_status api")
    @pytest.mark.parametrize("game_data", exclude_params_subscribe)
    def test_complete_game(self, game_data):
        f'''Get {game_data} game_id and complete it'''

        response = MyRequests.get(
            "/api/activities/game_activity_statuses/",
            cookies=self.cookies
        )
        response_as_dict = self.response_to_json(response)
        game_id = response_as_dict[game_data[1]]["activity_status_id"]
        params = {
            "is_complete": True
        }
        response = MyRequests.post(
            f"/api/v3/activity_status/{game_id}/",
            json=params,
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
                "is_earned"
            ]
        )
        response_as_dict = self.response_to_json(response)
        points = response_as_dict["scores_old"]["points"]
        assert points > 0, "Points of skill < 0"

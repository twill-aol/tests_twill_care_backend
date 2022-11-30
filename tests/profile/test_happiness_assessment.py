import allure
import random
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Assessment] HA")
class TestHA(BaseCase):
    '''Tests HA'''
    user_id, email, cookies = MainCase.signup_router()
    ha_id = ""

    @allure.label("ha", "assessment", "profile", "smoke", "authorization")
    @allure.description("This test checks get HA status")
    def test_ha_result(self):
        '''Get HA status'''
        response = MyRequests.get(
            "/api/happiness_assessment/result/",
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(
            response,
            [
                "result",
                "dialog"
            ]
        )
        TestHA.ha_id = \
            BaseCase.response_to_json(response)["dialog"]["dialog_id"]
        return response

    @allure.label("ha", "assessment", "profile", "smoke", "authorization")
    @allure.description("This test checks complete HA")
    def test_ha_complete(self):
        '''Complete HA'''
        response = TestHA.test_ha_result(self)
        len_ha_res = len(BaseCase.response_to_json(response)["result"])
        assert len_ha_res == 0, "New user has HA-result"
        type_question = "single_obj"
        data = {"client_input": str(random.randint(1, 4))}
        while type_question != "end":
            response = MyRequests.post(
                f"/api/assessment/v1/dialogs/{TestHA.ha_id}/conversation/",
                json=data,
                cookies=self.cookies
            )
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_keys(
                response,
                [
                    "conversation_id",
                    "turn_number"
                ]
            )
            conversation_id = \
                BaseCase.response_to_json(response)["conversation_id"]
            data = {
                "client_input": str(random.randint(1, 3)),
                "conversation_id": conversation_id
            }
            type_question = BaseCase.response_to_json(response)["data"]["type"]
        response = TestHA.test_ha_result(self)
        len_ha_res = len(BaseCase.response_to_json(response)["result"])
        assert len_ha_res > 0, "User doesn't have HA-result"

    @allure.label("ha", "assessment", "profile", "smoke", "authorization")
    @allure.description("This test checks dismiss HA after complete it")
    def test_ha_dismiss_status_after_complete(self):
        '''Dismiss HA'''
        response = MyRequests.get(
            f"/api/studies/dismiss-assessment/{TestHA.ha_id}",
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 202)
        Assertions.assert_json_value_by_name(
            response,
            "detail",
            "Not enough data. Dialogs for today: None.",
            "Answer about dismiss assessment is wrong"
        )

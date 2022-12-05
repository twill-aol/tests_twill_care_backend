import allure
import random
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Community] Posts")
class TestCreatePost(BaseCase):
    '''Tests Community posts'''
    user_id, email, auth_token = MainCase.signup_router()
    new_post_id = ""
    tags = [8871]
    offender_user_id = ""
    comment_id = ""

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/feed/posts/write/'")
    def test_create_post(self):
        '''Check creating a post'''
        message = MainCase.good_phrases()
        json_data = {
            "text": message,
            # "attachments": [],
            "tags": self.tags,
            "community": "well_being",
            # "needs_expert": 'false'
        }
        response_create_post = MyRequests.post(
            "/api/v1/threads/discussion/",
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
            json=json_data
        )
        Assertions.assert_code_status(response_create_post, 201)
        response_create_post_json = BaseCase.response_to_json(response_create_post)
        self.new_post_id = response_create_post_json["id"]
        response_feed = MyRequests.get(
            '/api/v1/feed/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        response_get_happifiers_list_json = BaseCase.response_to_json(response_feed)
        new_post_id_in_list = response_get_happifiers_list_json["records"][0]["id"]
        new_post_text_in_list = response_get_happifiers_list_json["records"][0]["text"]
        new_post_tags_in_list = response_get_happifiers_list_json["records"][0]["tags"][0]["id"]
        assert self.new_post_id == new_post_id_in_list, \
            f'API of happifiers list does not have "{self.new_post_id}" in first message'
        new_post_text_in_list = response_get_happifiers_list_json["records"][0]["text"]
        assert message == new_post_text_in_list, \
            f'Happifiers list does not have text "{message}" in first message "{new_post_text_in_list}"'
        assert self.tags[0] == new_post_tags_in_list, \
            f'Happifiers list does not have tags "{self.tags[0]}" in first message "{new_post_tags_in_list}"'
        
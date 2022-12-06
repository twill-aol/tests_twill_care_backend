import allure
import pytest
from lib.assertions import Assertions
from lib.main_case import MainCase
from lib.my_requests import MyRequests
from lib.post_case import PostCase


@allure.epic("[Community] Posts")
@pytest.mark.smoke
class TestPost(PostCase):
    '''Tests Community posts'''
    user_id, email, auth_token = MainCase.signup_router()
    tags = [8871]

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/api/v1/threads/discussion/'")
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
        response_create_post_json = self.response_to_json(response_create_post)
        new_post_id = response_create_post_json["id"]
        new_post_id_in_list = response_create_post_json["id"]
        new_post_text_in_list = response_create_post_json["text"]
        new_post_tags_in_list = response_create_post_json["tags"][0]["id"]
        new_post_text_in_list = response_create_post_json["text"]
        assert new_post_id == new_post_id_in_list, \
            f'API of happifiers list does not have "{new_post_id}" in first message'
        assert message == new_post_text_in_list, \
            f'Happifiers list does not have text "{message}" in first message "{new_post_text_in_list}"'
        assert self.tags[0] == new_post_tags_in_list, \
            f'Happifiers list does not have tags "{self.tags[0]}" in first message "{new_post_tags_in_list}"'

        response_feed = self.get_feed()
        response_get_happifiers_list_json = self.response_to_json(response_feed)
        new_post_id_in_list = response_get_happifiers_list_json["records"][0]["id"]
        new_post_text_in_list = response_get_happifiers_list_json["records"][0]["text"]
        new_post_tags_in_list = response_get_happifiers_list_json["records"][0]["tags"][0]["id"]
        new_post_text_in_list = response_get_happifiers_list_json["records"][0]["text"]
        assert new_post_id == new_post_id_in_list, \
            f'API of happifiers list does not have "{new_post_id}" in first message'
        assert message == new_post_text_in_list, \
            f'Happifiers list does not have text "{message}" in first message "{new_post_text_in_list}"'
        assert self.tags[0] == new_post_tags_in_list, \
            f'Happifiers list does not have tags "{self.tags[0]}" in first message "{new_post_tags_in_list}"'

        self.delete_post(new_post_id)

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/api/v1/threads/discussion/discussion_id/'")
    def test_delete_post(self):
        '''Check deleting a post'''
        response_create_post = self.action_post()
        response_create_post_json = self.response_to_json(response_create_post)
        new_post_id = response_create_post_json["id"]
        response_delete_post = MyRequests.delete(
            f'/api/v1/threads/discussion/{new_post_id}/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        Assertions.assert_code_status(response_delete_post, 200)
        Assertions.assert_response_content(response_delete_post, 'null')

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/api/v1/threads/discussion/discussion_id/'")
    def test_read_post(self):
        '''Check reading a post'''
        response_create_post = self.action_post()
        response_create_post_json = self.response_to_json(response_create_post)
        new_post_id = response_create_post_json["id"]
        response_read_post = MyRequests.get(
            f'/api/v1/threads/discussion/{new_post_id}/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        Assertions.assert_code_status(response_read_post, 200)
        Assertions.assert_json_has_keys(
            response_read_post,
            self.post_keys_in_json,
        )
        new_post_id = response_create_post_json["id"]
        new_post_text = response_create_post_json["text"]
        new_post_tags = self.response_to_json(response_read_post)["tags"][0]["id"]
        # print(response_read_post.text)
        Assertions.assert_json_value_by_name(
            response_read_post,
            {
                "id": new_post_id,
                "text": new_post_text,
            }
        )
        assert new_post_tags == self.tags[0], \
            f'Tags in the reading post: [{new_post_tags}] does not match \
            tags in created post: [{self.tags[0]}]'

        self.delete_post(new_post_id)

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks put:/api/v1/threads/discussion/")
    @pytest.mark.xfail(reason="401. Problem will be fixed")
    def test_edit_post(self):
        '''Check editing a post'''
        response_create_post = self.action_post()
        response_create_post_json = self.response_to_json(response_create_post)
        new_post_id = response_create_post_json["id"]
        response_read_post = self.read_post(new_post_id)
        response_edit_post = self.action_post(new_post_id)
        Assertions.assert_json_has_keys(
            response_edit_post,
            self.post_keys_in_json,
        )
        read_post_id = response_read_post["id"]
        read_post_text = response_read_post["text"]
        read_post_tags = self.response_to_json(response_read_post)["tags"][0]["id"]
        edit_post_tags = self.response_to_json(response_edit_post)["tags"][0]["id"]

        Assertions.assert_json_value_by_name(
            response_edit_post,
            {
                "id": read_post_id,
                "text": read_post_text,
            }
        )
        assert read_post_tags == edit_post_tags, \
            f'Tags in the reading post: [{read_post_tags}] does not match \
            tags in editing post: [{edit_post_tags}]'

        self.delete_post(new_post_id)

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/api/v1/reactions/'")
    @pytest.mark.xfail(reason="401. Problem will be fixed")
    def test_reaction_post(self):
        '''Check reactioning a post'''
        response_create_post = self.action_post()
        response_create_post_json = self.response_to_json(response_create_post)
        post_id = response_create_post_json["id"]
        post_reactions = response_create_post_json["reactions"]
        post_top_reactions = response_create_post_json["top_reactions"]
        response_reaction = self.reaction_action(
            {
                "model_id": post_id,
                "model_type": "post",
                "reaction": "insightful",
            }
        )
        Assertions.assert_json_has_keys(
            response_reaction,
            [
                "top_reactions",
                "reacted_by_me",
                "reactions"
            ]
        )
        Assertions.assert_json_value_by_name(
            response_reaction,
            {
                "reaction": post_reactions,
                "top_reactions": post_top_reactions,
            }
        )
        self.delete_post(post_id)

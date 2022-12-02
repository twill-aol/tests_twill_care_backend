import allure
import random
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


@allure.epic("[Community] Posts")
class TestCreatePost(BaseCase):
    '''Tests Community posts'''

    user_id, email, cookies, access_token = MainCase.signup_router()
    print('►', user_id, email, cookies, access_token)
    post_id = ""
    offender_user_id = ""
    comment_id = ""

    @allure.label("post", "authorization", "smoke")
    @allure.description("This test checks '/feed/posts/write/'")
    def test_true(self):
        '''Check creating a post'''
        message = MainCase.good_phrases()
        json_data = {
            "body": message,
            "communities": "pregnancy",
            "tags_subforms-0-tags": "8871",
            "tags_subforms-1-tags": "8883",
            "tags_subforms-2-tags": "8880",
            "tags_subforms-3-tags": "8876",
        }
        response = MyRequests.post(
            "/feed/posts/write/",
            data=json_data,
            cookies=self.cookies
        )
        Assertions.assert_code_status(response, 200)

        

    # @allure.label("community", "post", "track", "authorization")
    # @allure.description("This test checks \
    # /api/activity/?page=1&page_size=12&feed_filter=trackGroup")
    # def test_community_track_posts(self):
    #     '''Get track posts in Community'''
    #     response = MyRequests.get(
    #         "/api/activity/?page=1&page_size=12&feed_filter=trackGroup",
    #         # cookies=self.cookies
    #     )
    #     Assertions.assert_code_status(response, 200)
    #     response_as_dict = BaseCase.response_to_json(response)
    #     if len(response_as_dict) > 0:
    #         assert ("id" and "user_id") in response_as_dict[0]

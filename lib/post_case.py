import datetime as dt
import random
import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.main_case import MainCase
from lib.my_requests import MyRequests


TIME_START = str(dt.datetime.now().strftime("%Y%m%d%H%M%S"))[2:]


class PostCase(MainCase):
    tags = [8871]
    post_keys_in_json = [
        "id",
        "user",
        "text",
        "tags",
        "attachments",
        "replies",
        "likes",
        "liked_by_me",
        "reactions",
        "reacted_by_me",
        "top_reactions",
        "helped",
        "helped_by_me",
        "date",
        "model_type",
        "thread_id",
        "community",
        "needs_expert",
        "is_bookmarked",
        "humanized_time_ago_compact",
    ]

    @classmethod
    def action_post(self, post_id=None, json_data=None):
        '''Check creating a post'''
        if json_data is None:
            message = self.good_phrases()
            json_data = {
                "text": message,
                # "attachments": [],
                "tags": self.tags,
                "community": "well_being",
                # "needs_expert": 'false'
            }
        if post_id is None:
            response_action_post = MyRequests.post(
                "/api/v1/threads/discussion/",
                headers={
                    'Authorization': f'Bearer {self.auth_token}',
                },
                json=json_data
            )
        else:
            response_action_post = MyRequests.put(
                f"/api/v1/threads/discussion/{post_id}",
                headers={
                    'Authorization': f'Bearer {self.auth_token}',
                },
                json=json_data
            )

        Assertions.assert_code_status(response_action_post, 201)
        return response_action_post

    @classmethod
    def read_post(self, post_id):
        response_delete_post = MyRequests.delete(
            f'/api/v1/threads/discussion/{post_id}/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        Assertions.assert_code_status(response_delete_post, 200)

    @classmethod
    def delete_post(self, post_id):
        response_delete_post = MyRequests.delete(
            f'/api/v1/threads/discussion/{post_id}/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        Assertions.assert_code_status(response_delete_post, 200)
        Assertions.assert_response_content(response_delete_post, 'null')

    @classmethod
    def get_feed(self):
        response_feed = MyRequests.get(
            '/api/v1/feed/',
            headers={
                'Authorization': f'Bearer {self.auth_token}',
            },
        )
        Assertions.assert_code_status(response_feed, 200)
        return response_feed


import json.decoder
from requests import Response


class BaseCase:
    @classmethod
    def response_to_json(cls, response: Response):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert (
                False
            ), f"Response is not in JSON format. \
                Response text is {response.text}"
        return response_as_dict

    def get_cookie(self, response: Response, cookie_name):
        assert (
            cookie_name in response.cookies
        ), f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert (
            headers_name in response.headers
        ), f"Cannot find header with the name {headers_name} \
            in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        response_as_dict = self.response_to_json(response)
        assert name in response_as_dict, \
            "Response JSON does not have key '{name}'"
        return response_as_dict[name]

    def finder_text(self, content, flag, board):
        find_id_position = content.find(flag) + len(flag)
        text = ""
        for symbol in content[find_id_position:]:
            if symbol != board:
                text += symbol
            else:
                break
        return text
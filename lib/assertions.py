from lib.base_case import BaseCase
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(
        response: Response, names_and_expected_values: dict
    ):
        response_as_dict = BaseCase.response_to_json(response)
        for item in names_and_expected_values:
            assert item in response_as_dict, \
                f"Response JSON doesn't have key '{item}'"
            assert response_as_dict[item] == names_and_expected_values[item],\
                f"Response-field {response_as_dict[item]} \
                doesn't match {names_and_expected_values[item]}"

    @staticmethod
    def assert_json_has_key(response: Response, name):
        response_as_dict = BaseCase.response_to_json(response)

        assert name in response_as_dict.keys(), \
            f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list, index=None):
        if index is None:
            response_as_dict = BaseCase.response_to_json(response)
        else:
            response_as_dict = BaseCase.response_to_json(response)[index]
        for name in names:
            assert name in response_as_dict, \
                f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        response_as_dict = BaseCase.response_to_json(response)

        assert (
            name not in response_as_dict
        ), f"Response JSON shouldn't have key {name}. But it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):

        assert (
            response.status_code == expected_status_code
        ), f"Unexpected status code! Expected: {expected_status_code}. \
            Actual: {response.status_code}"

    @staticmethod
    def assert_length_of_json(
        response: Response,
        expected_length,
        error_message
    ):
        response_as_dict = BaseCase.response_to_json(response)
        len_of_json_answer = len(response_as_dict)

        assert len_of_json_answer == expected_length, error_message

    @staticmethod
    def assert_response_content(
        response: Response, expected_value: str
    ):
        response_as_text = str(response.text)
        assert expected_value == response_as_text, \
            f"Response content '{response_as_text}' \
            doesn't match '{expected_value}'"

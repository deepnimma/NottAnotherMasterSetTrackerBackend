from http import HTTPStatus

from workers import Response


def create_ok_response(msg: str) -> Response:
    """
    Creates a response with HTTP Status Code 200.
    :param msg: The msg to pass to the response.
    :return: The response with HTTP Status OK
    """
    return Response(__check_msg_ender(msg), HTTPStatus.OK)


def create_bad_request_response(msg: str) -> Response:
    """
    Creates a response with HTTP Status BAD_REQUEST
    :param msg: The msg to pass to the response.
    :return: The response with HTTP Status BAD_REQUEST
    """
    return Response(__check_msg_ender(msg), HTTPStatus.BAD_REQUEST)


def __check_msg_ender(msg: str) -> str:
    """
    Ensures the response msg ends with a new line character.
    :param msg: The msg to check.
    :return: The msg with the new line character if it does not already exist.
    """
    return msg if msg.endswith("\n") else msg + "\n"


if __name__ == "__main__":
    print(__check_msg_ender("Testing"))
    print(__check_msg_ender("TestingEnd\n"))

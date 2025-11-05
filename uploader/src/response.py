from http import HTTPStatus

from workers import Response


def create_bad_request(msg: str) -> Response:
    return Response(msg, HTTPStatus.BAD_REQUEST)


def __check_msg_ender(msg: str) -> str:
    if not msg.endswith("\n"):
        return msg + "\n"

    return msg


if __name__ == "__main__":
    print(__check_msg_ender("Testing"))
    print(__check_msg_ender("TestingEnd\n"))

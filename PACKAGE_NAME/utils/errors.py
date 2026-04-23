import sys


def error_message_details(error, error_details=sys):
    _, _, exc_tb = error_details.exc_info()
    if exc_tb is None:
        return f"{error}"
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error in [{file_name}] line [{exc_tb.tb_lineno}]: {error}"


class CustomException(Exception):
    def __init__(self, error_message, error_details=sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        return self.error_message

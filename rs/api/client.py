from rs.helper.logger import log, log_to_run


class Client:

    def __init__(self):
        self.send_message("ready")

    def send_message(self, message: str) -> str:
        log_to_run("Sending message: " + message)
        input_response = input(message + "\n")
        log_to_run("Response: " + input_response)
        return input_response

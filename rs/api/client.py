from rs.helper.logger import log


class Client:

    def __init__(self):
        self.send_message("ready")

    def send_message(self, message: str) -> str:
        log("Sending message: " + message)
        input_response = input(message + "\n")
        log("Response: " + input_response)
        return input_response

    def perform_action(self):
        log("Performing Action")
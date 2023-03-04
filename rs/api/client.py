from rs.helper.logger import log, log_to_run


class Client:

    def __init__(self):
        self.send_message("ready")

    def send_message(self, message: str, silent: bool = False, before_run: bool = False) -> str:
        if not silent:
            log_message = f"Sending message: {message}"
            if before_run:
                log(log_message)
            else:
                log_to_run(log_message)
        input_response = input(message + "\n")
        if not silent:
            log_message = f"Response: {input_response}"
            if before_run:
                log(log_message)
            else:
                log_to_run(log_message)
        return input_response

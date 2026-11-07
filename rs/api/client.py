import select
import sys

from rs.helper.logger import log, log_to_run

# How long to wait for the mod's reply to a command before treating the pipe as wedged.
RESPONSE_TIMEOUT = 25
# How many "state" probes (direct state resends) before declaring the wedge unrecoverable.
WEDGE_PROBES = 3


class Client:

    def __init__(self):
        self.send_message("ready")

    @staticmethod
    def _read_line(timeout):
        """Read one response line from the mod, or None on timeout. Raises if the pipe closed."""
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None
        line = sys.stdin.readline()
        if line == "":
            raise RuntimeError("WEDGE: the mod closed the input pipe")
        return line.rstrip("\n")

    def send_message(self, message: str, silent: bool = False, before_run: bool = False) -> str:
        if not silent:
            log_message = f"Sending message: {message}"
            if before_run:
                log(log_message)
            else:
                log_to_run(log_message)
        sys.stdout.write(message + "\n")
        sys.stdout.flush()
        input_response = self._read_line(RESPONSE_TIMEOUT)
        if input_response is None:
            # The mod consumed a command but produced no reply. Probe with 'state' (a direct
            # state resend in the mod) so a silent state-suppression wedge can self-heal.
            log_to_run(f"WEDGE: no reply to '{message}' after {RESPONSE_TIMEOUT}s; probing with state")
            log(f"WEDGE: no reply to '{message}' after {RESPONSE_TIMEOUT}s; probing with state")
            for probe in range(1, WEDGE_PROBES + 1):
                sys.stdout.write("state\n")
                sys.stdout.flush()
                input_response = self._read_line(RESPONSE_TIMEOUT)
                if input_response is not None:
                    log_to_run(f"WEDGE: recovered via state probe {probe}/{WEDGE_PROBES}")
                    log(f"WEDGE: recovered via state probe {probe}/{WEDGE_PROBES}")
                    break
                log(f"WEDGE: state probe {probe}/{WEDGE_PROBES} timed out")
            if input_response is None:
                raise RuntimeError(
                    f"WEDGE: mod unresponsive (no reply to '{message}' and {WEDGE_PROBES} state probes)")
        if not silent:
            log_message = f"Response: {input_response}"
            if before_run:
                log(log_message)
            else:
                log_to_run(log_message)
        return input_response

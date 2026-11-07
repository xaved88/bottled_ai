"""Wedge-guard tests for rs.api.client.Client (no real mod process involved)."""
import io
import os
import sys
import unittest
from unittest import mock

from rs.api import client as client_mod


class TestClientWedge(unittest.TestCase):

    def setUp(self):
        self._t = client_mod.RESPONSE_TIMEOUT
        client_mod.RESPONSE_TIMEOUT = 0.05  # fast tests

    def tearDown(self):
        client_mod.RESPONSE_TIMEOUT = self._t

    def _client_with_pipe(self, responses, probe_responses=()):
        """responses: list of lines the 'mod' sends for the first read; probe_responses: for probes."""
        r_fd, w_fd = os.pipe()
        r_stream = os.fdopen(r_fd, "r")
        captured = io.StringIO()
        queue = list(responses)
        probe_queue = list(probe_responses)

        def write_to_pipe(line):
            os.write(w_fd, (line + "\n").encode())

        # pre-fill the first response
        if queue:
            write_to_pipe(queue.pop(0))

        c = client_mod.Client.__new__(client_mod.Client)  # bypass __init__ handshake
        with mock.patch.object(sys, "stdin", r_stream), mock.patch.object(sys, "stdout", captured):
            yield c, captured, queue, probe_queue, write_to_pipe
        r_stream.close()

    def test_normal_response(self):
        r_fd, w_fd = os.pipe()
        r_stream = os.fdopen(r_fd, "r")
        os.write(w_fd, b'{"ok": 1}\n')
        captured = io.StringIO()
        c = client_mod.Client.__new__(client_mod.Client)
        with mock.patch.object(sys, "stdin", r_stream), mock.patch.object(sys, "stdout", captured):
            out = c.send_message("hello")
        self.assertEqual(out, '{"ok": 1}')
        self.assertEqual(captured.getvalue(), "hello\n")
        r_stream.close()
        os.close(w_fd)

    def test_wedge_recovers_via_probe(self):
        r_fd, w_fd = os.pipe()
        r_stream = os.fdopen(r_fd, "r")
        captured = io.StringIO()
        c = client_mod.Client.__new__(client_mod.Client)

        def delayed_state():
            # no reply to the original command; the probe gets a state a moment later
            import threading
            threading.Timer(0.12, lambda: os.write(w_fd, b'{"state": true}\n')).start()

        with mock.patch.object(sys, "stdin", r_stream), mock.patch.object(sys, "stdout", captured):
            delayed_state()
            out = c.send_message("choose 1")
        self.assertEqual(out, '{"state": true}')
        self.assertIn("state\n", captured.getvalue())
        r_stream.close()
        os.close(w_fd)

    def test_wedge_raises_after_probes(self):
        r_fd, w_fd = os.pipe()
        r_stream = os.fdopen(r_fd, "r")
        captured = io.StringIO()
        c = client_mod.Client.__new__(client_mod.Client)
        with mock.patch.object(sys, "stdin", r_stream), mock.patch.object(sys, "stdout", captured):
            with self.assertRaises(RuntimeError):
                c.send_message("choose 2")
        self.assertGreaterEqual(captured.getvalue().count("state\n"), client_mod.WEDGE_PROBES)
        r_stream.close()
        os.close(w_fd)


if __name__ == "__main__":
    unittest.main()

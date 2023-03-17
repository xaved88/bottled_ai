import time


class Timer:
    start = time.perf_counter()
    last = start

    def lap(self):
        now = time.perf_counter()
        dif = now - self.last
        self.last = now
        return dif

    def end(self):
        return time.perf_counter() - self.start


class Stopwatch:
    start_time = 0
    duration = 0

    def start(self):
        self.start_time = time.perf_counter()
        pass

    def stop(self):
        self.duration += time.perf_counter() - self.start_time
        pass

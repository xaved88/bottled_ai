ROOT_DIR = ".\\ai\\requested_strike"


def log(message, filename="default"):
    f = open(ROOT_DIR + "\\logs\\" + filename + ".log", "a")
    f.write(message + "\n")
    f.close()


def init_log(filename="default"):
    with open(ROOT_DIR + "\\logs\\" + filename + ".log", 'r+') as file:
        file.truncate(0)
        file.close()

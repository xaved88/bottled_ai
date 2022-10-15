from time import sleep

from rs.controller.controller_window import ControllerWindow

window = ControllerWindow()

while True:
    window.run()
#    sleep(0.5)
    if window.status.is_aborted:
        window.close()
        break
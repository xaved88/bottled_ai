import PySimpleGUI as sg

from rs.controller.control_points import ControlPoints
from rs.controller.controller_status import ControllerStatus


class ControllerWindow:
    def __init__(self):
        layout = [
            [sg.Text('Run in rooms')],
            [sg.Checkbox(text='M', default=True, key=ControlPoints.MONSTER),
             sg.Checkbox(text='E', default=True, key=ControlPoints.ELITE),
             sg.Checkbox(text='B', default=True, key=ControlPoints.BOSS)],
            [sg.Checkbox(text='$', default=True, key=ControlPoints.SHOP),
             sg.Checkbox(text='R', default=True, key=ControlPoints.REST),
             sg.Checkbox(text='?', default=True, key=ControlPoints.EVENT)],
            [sg.Button('Abort'), sg.Button('Pause'), sg.Button('Play', visible=False)]
        ]

        # Create the window
        self.status = ControllerStatus()
        self.window = sg.Window(title='Requested Strike', layout=layout, size=(290, 150))

    def run(self):
        event, values = self.window.read(0)
        if event == sg.WINDOW_CLOSED or event == 'Abort':
            self.status.is_aborted = True

        if event == "Pause":
            self.status.is_paused = True
            self.window['Pause'].update(visible=False)
            self.window['Play'].update(visible=True)
        elif event == "Play":
            self.status.is_paused = False
            self.window['Play'].update(visible=False)
            self.window['Pause'].update(visible=True)

        self.status.run_monster = values[ControlPoints.MONSTER]
        self.status.run_elite = values[ControlPoints.ELITE]
        self.status.run_boss = values[ControlPoints.BOSS]
        self.status.run_shop = values[ControlPoints.SHOP]
        self.status.run_rest = values[ControlPoints.REST]
        self.status.run_event = values[ControlPoints.EVENT]

    def close(self):
        self.window.close()

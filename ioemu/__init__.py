# ioemu/__ini__.py
import os
import sys

from . import mainwindow
import PyQt5

# taken from https://openclipart.org/detail/248021/red-led-lamp-on
LED_ON_FILE = 'ledon.png'
# taken from https://openclipart.org/detail/248019/red-led-lamp
LED_OFF_FILE = 'ledoff.png'
# taken from https://openclipart.org/detail/299643/dpst-micro-push-button-switch
BUTTON_FILE = 'button.png'


class Emulator(mainwindow.Ui_MainWindow):

    def __init__(self, num_leds=3, framerate=60):
        super().__init__()

        self.num_leds = num_leds
        self.button_pressed = [False, False]
        self.slider_value = 0

        self._ledon = PyQt5.QtGui.QPixmap(_absolute_path(LED_ON_FILE))
        self._ledoff = PyQt5.QtGui.QPixmap(_absolute_path(LED_OFF_FILE))

        self._buffer = 0

    def setupUi(self, main_win):
        super().setupUi(main_win)
        self.btn1.pressed.connect(lambda: self._btn_clicked(0, True))
        self.btn2.pressed.connect(lambda: self._btn_clicked(1, True))
        self.btn1.released.connect(lambda: self._btn_clicked(0, False))
        self.btn2.released.connect(lambda: self._btn_clicked(1, False))

        self.led_lbl1.setPixmap(self._ledoff)
        self.led_lbl2.setPixmap(self._ledoff)
        self.led_lbl3.setPixmap(self._ledoff)
        self._led_lbls = [self.led_lbl1, self.led_lbl2, self.led_lbl3]

        self.slider.valueChanged.connect(self._slider_value_changed)

    def _slider_value_changed(self):
        self.slider_value = self.slider.value()

    def _btn_clicked(self, num, on_off):
        self.button_pressed[num] = on_off

    def write(self, buffer):
        '''Write value to display buffer. Buffer must be an integer whose 
        binary representation will be shown on the display.'''
        assert 0 <= buffer < 8

        self._buffer = buffer
        self._update_screen()

    def _update_screen(self):
        payload_str = bin(self._buffer)[2:]
        payload_str = payload_str.zfill(self.num_leds)
        
        # draw LEDs
        for i in range(len(payload_str)):            
            image = self._ledon if payload_str[i] == '1' else self._ledoff
            self._led_lbls[i].setPixmap(image)


def _absolute_path(filename):
    'Create absolute path for given filename.'
    return os.path.join(os.path.dirname(__file__), filename)
        

def run():
    app = PyQt5.QtWidgets.QApplication([])
    main_win = PyQt5.QtWidgets.QMainWindow()
    emu = Emulator()
    emu.setupUi(main_win)
    main_win.show()
    emu.write(0b101)

    app.exec_()

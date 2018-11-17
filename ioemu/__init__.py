# ioemu/__init__.py
'''
Client and server of the emulator are communication with the following protocol:

Request: xyz where x, y and z in (0,1) will turn the LED x, y or z  
  on(1) or off(0)

Response: xy.zz where x and y are in (0, 1) and represent the state of the 
  buttons. zz if the value of the analog slider between 00 and 99.
'''
import os
import sys
import socket

import PyQt5
import PyQt5.QtNetwork

from . import mainwindow


# taken from https://openclipart.org/detail/248021/red-led-lamp-on
LED_ON_FILE = 'ledon.png'
# taken from https://openclipart.org/detail/248019/red-led-lamp
LED_OFF_FILE = 'ledoff.png'
# taken from https://openclipart.org/detail/299643/dpst-micro-push-button-switch
BUTTON_FILE = 'button.png'

TCP_SERVER_PORT = int(os.environ.get('IOEMU_PORT', default='9999'))
NUM_LEDS = 3  # don't change this unless you know what you are doing.

class EmulatorGui(mainwindow.Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.button_pressed = [False, False]
        self.slider_value = 0

        self._ledon = PyQt5.QtGui.QPixmap(_absolute_path(LED_ON_FILE))
        self._ledoff = PyQt5.QtGui.QPixmap(_absolute_path(LED_OFF_FILE))

        self._buffer = 0

        self._tcp_server = PyQt5.QtNetwork.QTcpServer()
        self._tcp_server.newConnection.connect(self._new_session)

        self._tcp_server.listen(address=PyQt5.QtNetwork.QHostAddress.LocalHost,
                                port=TCP_SERVER_PORT)       

    def setupUi(self, main_win):
        super().setupUi(main_win)

        # connection slots
        self.btn1.pressed.connect(lambda: self._btn_clicked(0, True))
        self.btn2.pressed.connect(lambda: self._btn_clicked(1, True))
        self.btn1.released.connect(lambda: self._btn_clicked(0, False))
        self.btn2.released.connect(lambda: self._btn_clicked(1, False))
        self.slider.valueChanged.connect(self._slider_value_changed)

        # setting icons
        pix = PyQt5.QtGui.QPixmap(_absolute_path(BUTTON_FILE))
        buttonpic = PyQt5.QtGui.QIcon(pix)
        self.btn1.setIcon(buttonpic)
        self.btn1.setIconSize(self.btn1.rect().size())
        self.btn2.setIcon(buttonpic)
        self.btn2.setIconSize(self.btn2.rect().size())

        self.led_lbl1.setPixmap(self._ledoff)
        self.led_lbl2.setPixmap(self._ledoff)
        self.led_lbl3.setPixmap(self._ledoff)
        self._led_lbls = [self.led_lbl1, self.led_lbl2, self.led_lbl3]


    def _new_session(self):
        sock = self._tcp_server.nextPendingConnection()
        sock.waitForReadyRead(msecs=100)

        # assuming 010, 110, ...
        payload = str(sock.readAll(), "ASCII").strip()
        #print("request", payload)
        if len(payload) == 3:
            # update screen
            self.write(int(payload, base=2))

        # create response: state of buttons
        resp = ''
        for btn in self.button_pressed:
            resp += '1' if btn else '0'

        # add slider value to response
        resp += '.' + str(self.slider_value).zfill(2)
        #print("response", resp)
        sock.write(bytes(resp, "ASCII"))
        sock.disconnectFromHost()

    def _slider_value_changed(self):
        self.slider_value = self.slider.value()

    def _btn_clicked(self, num, on_off):
        self.button_pressed[num] = on_off

    def write(self, buffer):
        '''Write value to display buffer. Buffer must be an integer whose 
        binary representation will be shown on the display.'''
        assert 0 <= buffer < 2 ** NUM_LEDS, buffer

        self._buffer = buffer
        self._update_screen()

    def _update_screen(self):
        payload_str = bin(self._buffer)[2:]
        payload_str = payload_str.zfill(NUM_LEDS)
        
        # draw LEDs
        for i in range(len(payload_str)):            
            image = self._ledon if payload_str[i] == '1' else self._ledoff
            self._led_lbls[i].setPixmap(image)


class Emulator:
    def __init__(self):
        self.host = ''
        self.sock = socket.socket()

    @property
    def buttons(self):
        # response has format xx.yy where xx is the button state
        response = self._send(' ').split('.')[0]
        return [response[0] == '1', response[1] == '1']

    @property
    def analog_value(self):
        # response has format xx.yy where yy is the analog value
        response = self._send(' ').split('.')[1]
        return int(response)

    @property
    def leds(self):
        raise Exception('Attribute leds cannot be read but is write-only.')

    @leds.setter
    def leds(self, abc):
        assert len(abc) == 3, "There must be three values for the LEDs."
        a, b, c = abc
        payload = ''
        for b in abc:
            payload += '1' if b else '0'

        #print("sending", payload)
        response = self._send(payload)

        if len(response) == 2:
            self.button_pressed = [response[0] == '1', response[1] == '1']

    def _send(self, payload):
        with socket.socket() as sock:
            try:
                sock.connect(('localhost', TCP_SERVER_PORT))
            except ConnectionRefusedError:
                raise Exception("Unable to connect to Emulator. Maybe it is not running.")
            sock.send(bytes(payload, 'ASCII'))
            response = str(sock.recv(10), 'ASCII')
            #print("response", response)

            return response


        

def _absolute_path(filename):
    'Create absolute path for given filename.'
    return os.path.join(os.path.dirname(__file__), filename)
        

def run():
    app = PyQt5.QtWidgets.QApplication([])
    main_win = PyQt5.QtWidgets.QMainWindow()
    emu = EmulatorGui()
    emu.setupUi(main_win)
    main_win.show()
    emu.write(0b101)

    app.exec_()

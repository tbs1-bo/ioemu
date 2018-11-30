# ioemu/__init__.py
'''
Client and server of the emulator are communication with the following protocol:

Request: xyz where x, y and z in (0,1) will turn the LED x, y or z  
  on(1) or off(0). Request with a length other than 3 will have no effect on 
  the status of the LEDs.

Response: lll;bb;aa where each l and b is in (0, 1) and represents the state
  of an LED or button. aa is the value of the analog slider between 00 and 99.
'''
import os
import sys
import socket

import PyQt5
import PyQt5.QtNetwork

from . import mainwindow

VERSION = '0.3.0'

# taken from https://openclipart.org/detail/248021/red-led-lamp-on
LED_ON_FILE = 'ledon.png'
# taken from https://openclipart.org/detail/248019/red-led-lamp
LED_OFF_FILE = 'ledoff.png'
# taken from https://openclipart.org/detail/299643/dpst-micro-push-button-switch
BUTTON_FILE = 'button.png'

TCP_SERVER_PORT = int(os.environ.get('IOEMU_PORT', default='9999'))
NUM_LEDS = 3  # don't change this unless you know what you are doing.


def request_compose(buttons):
    assert len(buttons) == 3

    req = ''
    for b in buttons:
        req += '1' if b else '0'

    return req

def request_decompose(payload):
    'Assume payload lll with boolean values.'
    assert len(payload) == 3

    leds = []
    for l in payload:
        leds.append(l == '1')

    return leds

def response_compose(leds, buttons, analog):
    'Create response of format lll;bb;aa'
    resp = ''
    for led in leds:
        resp += '1' if led else '0'
    resp += ';'

    for btn in buttons:
        resp += '1' if btn else '0'
    resp += ';'

    # add slider value to response
    resp += str(analog).zfill(2)
    return resp

def response_decompose(payload):
    '''decompose payload into three entries: LED states, button 
    states, analog value. Assuming format lll;bb;aa'''

    assert len(payload) == 9    
    lll, bb, aa = payload.split(';')
    leds = []
    for l in lll:
        leds.append(l == '1')

    buttons = []
    for b in bb:
        buttons.append(b == '1')

    analog = int(aa)

    return leds, buttons, analog



class EmulatorGui(mainwindow.Ui_MainWindow):

    def __init__(self, port=TCP_SERVER_PORT):
        super().__init__()

        self.button_pressed = [False, False]
        self.slider_value = 0

        self._ledon = PyQt5.QtGui.QPixmap(_absolute_path(LED_ON_FILE))
        self._ledoff = PyQt5.QtGui.QPixmap(_absolute_path(LED_OFF_FILE))

        self._buffer = 0

        self._tcp_server = PyQt5.QtNetwork.QTcpServer()
        self._tcp_server.newConnection.connect(self._new_session)

        self._tcp_server.listen(address=PyQt5.QtNetwork.QHostAddress.LocalHost,
                                port=port)       

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
        leds = self.__get_led_state()
        resp = response_compose(leds, self.button_pressed, self.slider_value)
        sock.write(bytes(resp, "ASCII"))
        sock.disconnectFromHost()

    def __get_led_state(self):
        'Read the LEDs state from the pixmap of the labels.'
        return [
            self.led_lbl1.pixmap() == self._ledon,
            self.led_lbl2.pixmap() == self._ledon,
            self.led_lbl3.pixmap() == self._ledon
        ]

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

    def __init__(self, port=TCP_SERVER_PORT):
        self.host = 'localhost'
        self.port = port
        self.sock = socket.socket()

    @property
    def buttons(self):
        _, buttons, _ = self._send(' ')
        return buttons

    @property
    def analog_value(self):
        # response has format xx.yy where yy is the analog value
        _, _, analog = self._send(' ')
        return analog

    @property
    def leds(self):
        led, _, _ = self._send(' ')
        return led

    @leds.setter
    def leds(self, abc):
        assert len(abc) == 3, "There must be three values for the LEDs."

        payload = request_compose(abc)

        #print("sending", payload)
        _, buttons, _ = self._send(payload)
        self.button_pressed = buttons

    def _send(self, payload):
        'send payload and return response.'
        with socket.socket() as sock:
            try:
                sock.connect((self.host, self.port))
            except ConnectionRefusedError:
                raise Exception("Unable to connect to Emulator. Maybe it is not running.")
            sock.send(bytes(payload, 'ASCII'))
            response = str(sock.recv(32), 'ASCII')
            #print("response", response)

            return response_decompose(response)


        

def _absolute_path(filename):
    'Create absolute path for given filename.'
    return os.path.join(os.path.dirname(__file__), filename)
        

def run():
    print("ioemu (version %s)" % VERSION)
    print("listening on localhost port", TCP_SERVER_PORT)
    app = PyQt5.QtWidgets.QApplication([])
    main_win = PyQt5.QtWidgets.QMainWindow()
    emu = EmulatorGui()
    emu.setupUi(main_win)
    main_win.show()
    emu.write(0b101)

    app.exec_()

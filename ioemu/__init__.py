# ioemu/__ini__.py
import os
import sys

import pygame

LED_ON_FILE = 'ledon.png'
LED_OFF_FILE = 'ledoff.png'
# taken from https://openclipart.org/detail/299643/dpst-micro-push-button-switch
BUTTON_FILE = 'button.png'


class Emulator:

    def __init__(self, num_leds=8, framerate=60):
        pygame.init()

        self.num_leds = 8
        self.button_pressed = [False, False]

        self._ledoff = pygame.image.load(self._absolute_path(LED_ON_FILE))
        self._ledon = pygame.image.load(self._absolute_path(LED_OFF_FILE))
        self._button = pygame.image.load(self._absolute_path(BUTTON_FILE))
        self._button_rects = [self._button.get_rect(), self._button.get_rect()]
        self._image_width = self._ledon.get_width()
        self._display = pygame.display.set_mode(
            (num_leds*self._image_width + len(self._button_rects) * self._button.get_width(),
             self._button.get_height()))
        pygame.display.set_caption('IO Emulator')
        self._buffer = 0
        self._framerate = framerate
        self._clock = pygame.time.Clock()

    def write(self, buffer):
        '''Write value to display buffer. Buffer must be an integer whose 
        binary representation will be shown on the display.'''
        self._buffer = buffer

    def _absolute_path(self, filename):
        'Create absolute path for given filename.'
        return os.path.join(os.path.dirname(__file__), filename)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                xy = pygame.mouse.get_pos()
                click_down = (event.type == pygame.MOUSEBUTTONDOWN)
                for i, rect in enumerate(self._button_rects):
                    self.button_pressed[i] = rect.collidepoint(xy) and click_down
        
    def _update_screen(self):
        self._display.fill((255,255,255))

        payload_str = bin(self._buffer)[2:]
        payload_str = payload_str.zfill(8)
        
        # draw LEDs
        for i in range(len(payload_str)):            
            image = self._ledon if payload_str[i] == '1' else self._ledoff            
            x = i * self._image_width
            
            self._display.blit(image, dest=(x, 0))

        # draw buttons right to the leds
        button_x = len(payload_str) * self._image_width
        self._button_rects[0].x = button_x
        self._button_rects[1].x = self._button_rects[0].x + self._button_rects[0].width
        for rect in self._button_rects:
            self._display.blit(self._button, rect)

        pygame.display.flip()

    def tick(self):
        self._handle_events()
        self._update_screen()
        pygame.display.flip()
        self._clock.tick(self._framerate)


def testEmulator():
    emu = Emulator()
    i = 1
    while True:
        if emu.button_pressed[0]:
            i += 1
        if emu.button_pressed[1]:
            i -= 1

        # fit i into range of values
        i = i % 255

        emu.write(i)
        emu.tick()


if __name__ == '__main__':
    testEmulator()

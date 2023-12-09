import cv2
import detectors
import serial
import time
from managers import WindowManager, CaptureManager
#push commit

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
def write_read(x):
    x = str(x)
    arduino.write(x.encode('utf-8'))
    #time.sleep(0.05)
    data = arduino.readline()
    return data

class Cameo (object):
    def __init__(self):
        print("started")
        self._windowManager = WindowManager('Cameo',
        self.onkeypress)
        self.status = 0
        self.mode = 0
        self.count = 0
        self.total = 0
        self.failed = 0
        self.tests = 20
        self._captureManager = CaptureManager(
        cv2.VideoCapture(0), self._windowManager, False)

    

    def run(self):
        """
        Arduino Modes:
        0 = default (idle)
        1 = scanning (blinking green)
        2 = passed (green)
        3 = failed (red)
        4 = too many attempts (blinking red + piezo)
        """

        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if(self.mode == 0):
                _ = detectors.face_rec(frame, frame, self.status)
            if(self.mode == 1):
                if (self.failed >= 3):
                    self.status = 4
                    text = write_read(4) #too many failed attempts
                    _ = detectors.face_rec(frame, frame, self.status)
                    print(text.decode('utf-8')) 
                    self.mode = 0

                else: 
                    value = detectors.face_rec(frame, frame, self.status)
                    if(value != None):
                        if(self.count < self.tests):
                            text = write_read(1) #scanning
                            self.status = 3
                            self.total = self.total + value
                            self.count = self.count + 1

                            loading_bar = self.create_loading_bar(self.count)
                            bar = f"{loading_bar}"
                            cv2.putText(frame, bar, ((int(frame.shape[0] / 2)) - 15, 80), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 0), 2)
                            print(text.decode('utf-8'), " | ", self.count, ": ", value , " = ",self.total)
                        else:
                            result = self.total/self.tests
                            if (result > 0.6):
                                self.status = 1
                                text = write_read(2) #passed
                                print(text.decode('utf-8'))
                                self.total = 0
                                self.count = 0
                                self.mode = 0
                            else:
                                self.status = 2
                                text = write_read(3) #failed
                                self.total = 0
                                self.count = 0
                                self.mode = 0
                                self.failed = self.failed + 1
                                print(text.decode('utf-8'), " ", self.failed)
                                time.sleep(3)

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onkeypress (self, keycode):
        if keycode == 27: # escape
            self._windowManager.destroyWindow()
        elif keycode == 32: # space
            print("scan begin")
            self.mode = 1

    def create_loading_bar(self, count):
        bar_length = 20
        progress = count / self.tests
        block = int(round(bar_length * progress))
        loading_bar = "[" + "||" * block + " " * (bar_length - block) + "]"
        return loading_bar


if __name__=="__main__":
    Cameo().run()


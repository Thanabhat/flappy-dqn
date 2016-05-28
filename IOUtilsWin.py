import win32api, win32con
import time


class IOUtilsWin:
    def __init__(self, X_PAD, Y_PAD):
        self.X_PAD = X_PAD
        self.Y_PAD = Y_PAD

    def restart(self):
        time.sleep(0.5)
        self.__mousePos((110, 370))
        self.__leftClick()
        time.sleep(0.5)
        self.fly()

    def fly(self):
        self.__mousePos((10, 10))
        self.__leftClick()

    def __leftClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def __mousePos(self, cord):
        win32api.SetCursorPos((self.X_PAD + cord[0], self.Y_PAD + cord[1]))

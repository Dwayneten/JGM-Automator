from automator import Automator
from prop import END

import sys
from termios import tcflush, TCIFLUSH
from multiprocessing import Process, Queue

KEYBOARD = Queue()


def main(kb):
    # 连接 adb 。
    instance = Automator('emulator-5554', kb)

    # 启动脚本。
    instance.start()


if __name__ == '__main__':
    p = Process(target=main, args=(KEYBOARD,))
    p.start()
    while True:
        tcflush(sys.stdin, TCIFLUSH)
        txt = input()
        if txt == END:
            KEYBOARD.put(txt)
            break
        else:
            KEYBOARD.put('')
    p.join()

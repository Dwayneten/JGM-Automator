from automator import Automator
from prop import END, RUN

from flusher import flush
from multiprocessing import Process, Queue

KEYBOARD = Queue()


def main(kb):
    # 连接 adb 。
    instance = Automator('127.0.0.1:7555', kb)

    # 启动脚本。
    instance.start()


if __name__ == '__main__':
    p = Process(target=main, args=(KEYBOARD,))
    p.start()
    while True:
        flush()
        txt = input()
        if txt == END or txt.split(' ')[0] == RUN:
            KEYBOARD.put(txt)
            if txt == END:
                break
        else:
            KEYBOARD.put('')
    p.join()

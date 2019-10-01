class _Flush:
    def __init__(self):
        try:
            self.work = _FlushUnix()
        except ModuleNotFoundError:
            self.work = _FlushWindows()

    def __call__(self): return self.work()

class _FlushUnix:
    def __init__(self):
        from termios import tcflush, TCIFLUSH

    def __call__(self):
        from termios import tcflush, TCIFLUSH
        import sys
        tcflush(sys.stdin, TCIFLUSH)

class _FlushWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

flush = _Flush()
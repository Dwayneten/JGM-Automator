from automator import Automator
from target import TargetType
from building import BuildingType
from numpy import array


if __name__ == '__main__':
    # 连接 adb 。
    instance = Automator('emulator-5554')

    # 启动脚本。
    instance.start()

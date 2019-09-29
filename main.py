from automator import Automator
from target import TargetType

if __name__ == '__main__':
    # 声明货物要移动到的建筑 ID 。
    targets = {
        TargetType.Box: 1,
        TargetType.Chair: 2,
        TargetType.Sofa: 3,
        TargetType.Bottle: 4,
        TargetType.Vegetable: 5,
        TargetType.Screw: 6,
        TargetType.Wood: 7,
        TargetType.Coal: 8,
        TargetType.Food: 9
    }

    # 连接 adb 。
    instance = Automator('emulator-5554', targets)

    # 启动脚本。
    instance.start()

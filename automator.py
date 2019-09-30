from target import TargetType
from building import BuildingType
from cv import UIMatcher
from random import choice
import uiautomator2 as u2
import logging
import time

BASIC_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)

fhlr = logging.FileHandler("logging.log")  # 输出到文件的handler
fhlr.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel('INFO')
logger.addHandler(chlr)
logger.addHandler(fhlr)


def clear_queue(q):
    while not q.empty():
        q.get()


BUILDING_2_LEVEL_POS = {
    1: (219, 1205),
    2: (469, 1078),
    3: (719, 950),
    4: (216, 947),
    5: (467, 822),
    6: (728, 697),
    7: (215, 696),
    8: (468, 570),
    9: (725, 445)
}
BUILDING_DETAIL_BTN = (982, 1151)
BUILDING_UPGRADE_BTN = (863, 1756)

UPGRADE_DURATION_SEC = 20

SELECTED_UPGRADE_BUILDING = [
    BuildingType.便利店,
    BuildingType.服装店
]


class Automator:
    def __init__(self, device: str, targets: dict, building_pos: list):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.targets = targets
        self.building_pos = building_pos

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        swipe_interval_sec = 5
        upgrade_interval_sec = 2 * 60
        # upgrade_interval_sec = 5
        tmp_upgrade_interval = 0
        while True:
            # 获取当前屏幕快照
            screen = self.d.screenshot(format="opencv")
            # 判断是否出现货物。
            has_goods = False
            for target in self.targets.keys():
                has_goods |= self._match_target(screen, target)
            if has_goods:
                UIMatcher.write(screen)

            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)

            # 滑动屏幕，收割金币。
            # logger.info("swipe")
            self._swipe()

            if tmp_upgrade_interval >= upgrade_interval_sec:
                tmp_upgrade_interval = 0
                self._upgrade()

            time.sleep(swipe_interval_sec)
            tmp_upgrade_interval += swipe_interval_sec

    def _swipe(self):
        """
        滑动屏幕，收割金币。
        """
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx, sy, ex, ey)

    @staticmethod
    def _get_position(key):
        """
        获取指定建筑的屏幕位置。

        ###7#8#9#
        ##4#5#6##
        #1#2#3###
        """
        positions = {
            1: (294, 1184),
            2: (551, 1061),
            3: (807, 961),
            4: (275, 935),
            5: (535, 810),
            6: (799, 687),
            7: (304, 681),
            8: (541, 568),
            9: (787, 447)
        }
        return positions.get(key)

    def _get_target_position(self, target: TargetType):
        """
        获取货物要移动到的屏幕位置。
        """
        return self._get_position(self.targets.get(target))

    def _match_target(self, screen, target: TargetType):
        """
        探测货物，并搬运货物。
        """
        # 由于 OpenCV 的模板匹配有时会智障，故我们探测次数实现冗余。
        counter = 6
        logged = False
        while counter != 0:
            counter = counter - 1

            # 使用 OpenCV 探测货物。
            result = UIMatcher.match(screen, target)

            # 若无探测到，终止对该货物的探测。
            # 实现冗余的原因：返回的货物屏幕位置与实际位置存在偏差，导致移动失效
            if result is None:
                break

            rank = result[-1]
            result = result[:2]
            sx, sy = result
            # 获取货物目的地的屏幕位置。
            ex, ey = self._get_target_position(target)

            if not logged:
                logger.info(f"Detect {target} at ({sx},{sy}), rank: {rank}")
                logged = True

            # 搬运货物。
            self.d.swipe(sx, sy, ex, ey)
        # 侧面反映检测出货物
        return logged

    def _select_min_building(self):
        screen = self.d.screenshot(format="opencv")
        screen = UIMatcher.pre(screen)
        min_level = float('inf')
        min_building_seq = None
        for key, pos in BUILDING_2_LEVEL_POS.items():
            tmp = UIMatcher.cut(screen, pos)
            tmp = UIMatcher.plain(tmp)
            tmp = UIMatcher.fill_color(tmp)
            tmp = UIMatcher.plain(tmp)
            txt = UIMatcher.image_to_txt(tmp, plus='-l chi_sim --psm 7')
            txt = UIMatcher.normalize_txt(txt)
            try:
                level = int(txt)
                logger.info(f'{self.building_pos[key - 1]} tesser -> {level}')
            except Exception:
                logger.warning(f'{self.building_pos[key - 1]} tesser -> {txt}')
                continue
            if level < min_level:
                min_level = level
                min_building_seq = key

        # 一个屋子的等级都没拿到
        if min_building_seq is None:
            res = choice(BUILDING_2_LEVEL_POS.keys())
            logger.warning(f'No tesseract result, random to {self.building_pos[res - 1]}')
            return res
        else:
            logger.info(f'Minimum level is {min_level} from {self.building_pos[min_building_seq - 1]}')
            return min_building_seq

    def _select_selected_building(self):
        rand_building_list = []
        for building in SELECTED_UPGRADE_BUILDING:
            try:
                pos = self.building_pos.index(building)
                rand_building_list.append(pos + 1)
            except Exception:
                pass
        if len(rand_building_list) == 0:
            res = choice(BUILDING_2_LEVEL_POS.keys())
            logger.warning(f'No match selected result, random to {self.building_pos[res - 1]}')
        else:
            res = choice(rand_building_list)
            logger.info(f'Use selected result {self.building_pos[res - 1]}')
        return res

    def _upgrade(self):
        self.d.click(*BUILDING_DETAIL_BTN)
        time.sleep(1)
        need_upgrade_building_seq = self._select_selected_building()
        self.d.click(*self._get_position(need_upgrade_building_seq))
        time.sleep(1)
        self.d.long_click(BUILDING_UPGRADE_BTN[0], BUILDING_UPGRADE_BTN[1], UPGRADE_DURATION_SEC)
        time.sleep(0.5)
        self.d.click(*BUILDING_DETAIL_BTN)

from target import TargetType
from building import BuildingType
from multiprocessing import Queue
from config import Reader
from cv import UIMatcher
from random import choice
from datetime import datetime
import uiautomator2 as u2
import logging
import time
import prop

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


def elect(order_list_len, iter_round):
    res = []
    for i in range(1, order_list_len + 1):
        if iter_round % i == 0:
            res.append(i - 1)
    return res


class Automator:
    def __init__(self, device: str, keyboard: Queue):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect(device)
        self.config = Reader()
        self.upgrade_iter_round = 0
        self.keyboard = keyboard
        # 检查 uiautomator
        if not self.d.uiautomator.running():
            self.d.reset_uiautomator()

    def _need_continue(self):
        if not self.keyboard.empty():
            txt = self.keyboard.get()
            # logger.info('txt1:' + txt)
            if txt == prop.END:
                logger.info('End')
                return False
            logger.info('Pause')
            txt = self.keyboard.get()
            # logger.info('txt2:' + txt)
            if txt == prop.END:
                logger.info('End')
                return False
            # 判断是否输入命令
            elif txt.split(' ')[0] == prop.RUN:
                # logger.info(txt.split(' ')[1:])
                cmd = txt.split(' ')[1]
                # 命令 - 升至 x 级
                if cmd == prop.UPGRADE_TO:
                    try:
                        target_level = int(txt.split(' ')[2])
                    except Exception:
                        logger.warn("Invalid number. Ignored.")
                    else:
                        self._upgrade_to(target_level)
                    # logger.info('target_level: ' + str(target_level))
                # 命令 - 升级 x 次
                elif cmd == prop.UPGRADE_TIMES:
                    try:
                        input_num = int(txt.split(' ')[2])
                    except Exception:
                        logger.warn("Invalid number. Ignored.")
                    else:
                        self._upgrade_times(input_num)
                # 无法识别命令
                else:
                    logger.warn("Unknown command. Ignored.")
                logger.info('Restart')
                return True
            else:
                logger.info('Restart')
                return True
        else:
            return True

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        tmp_upgrade_last_time = time.time()
        logger.info("Start Working")
        while True:
            # 检查是否有键盘事件
            if not self._need_continue():
                break

            # 更新配置文件
            self.config.refresh()

            # 在下午五点以后再开始拿火车，收益最大化
            # if datetime.now().hour > 17:
            if True:
                logger.info("Start matching goods")
                # 获取当前屏幕快照
                screen = self.d.screenshot(format="opencv")
                # 判断是否出现货物。
                has_goods = False
                for target in self.config.goods_2_building_seq.keys():
                    has_goods |= self._match_target(screen, target)
                if has_goods:
                    UIMatcher.write(screen)
                    # pass
                logger.info("End matching")

            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 当然，也可以使用图像探测的模式。
            self.d.click(550, 1650)

            # 滑动屏幕，收割金币。
            # logger.info("swipe")
            self._swipe()

            # 升级建筑
            tmp_upgrade_interval = time.time() - tmp_upgrade_last_time
            if tmp_upgrade_interval >= self.config.upgrade_interval_sec:
                if self.config.upgrade_type_is_assign is True:
                    self._assigned_uprade()
                else:
                    self._upgrade()
                tmp_upgrade_last_time = time.time()
            else:
                logger.info(f"Left {round(self.config.upgrade_interval_sec - tmp_upgrade_interval, 2)}s to upgrade")

            time.sleep(self.config.swipe_interval_sec)
        logger.info('Sub process end')

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
        return prop.BUILDING_POS.get(key)

    def _get_target_position(self, target: TargetType):
        """
        获取货物要移动到的屏幕位置。
        """
        return self._get_position(self.config.goods_2_building_seq.get(target))

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

    def __find_selected_building_seq(self):
        selected_seq_list = elect(len(self.config.upgrade_order), self.upgrade_iter_round)
        tmp_set = set()
        for order_seq in selected_seq_list:
            tmp_set |= self.config.upgrade_order[order_seq]
        res = []
        for i, building in enumerate(self.config.building_pos):
            if building in tmp_set:
                res.append(i + 1)
        if len(res) == 0:
            return list(prop.BUILDING_POS.keys())
        else:
            return res

    def _select_min_building(self):
        screen = self.d.screenshot(format="opencv")
        screen = UIMatcher.pre(screen)
        min_level = float('inf')
        min_building_seq = None
        for key in self.__find_selected_building_seq():
            pos = prop.BUILDING_LEVEL_POS[key]
            tmp = UIMatcher.cut(screen, pos)
            tmp = UIMatcher.plain(tmp)
            tmp = UIMatcher.fill_color(tmp)
            tmp = UIMatcher.plain(tmp)
            txt = UIMatcher.image_to_txt(tmp, plus='-l chi_sim --psm 7')
            txt = UIMatcher.normalize_txt(txt)
            try:
                level = int(txt)
                logger.info(f'{self.config.building_pos[key - 1]} tesser -> {level}')
            except Exception:
                logger.warning(f'{self.config.building_pos[key - 1]} tesser -> {txt}')
                continue
            if level < min_level:
                min_level = level
                min_building_seq = key

        # 一个屋子的等级都没拿到
        if min_building_seq is None:
            res = choice(list(prop.BUILDING_POS.keys()))
            logger.warning(f'No tesseract result, random to {self.config.building_pos[res - 1]}')
            return res
        else:
            logger.info(f'Minimum level is {min_level} from {self.config.building_pos[min_building_seq - 1]}')
            return min_building_seq

    def _upgrade(self):
        logger.info("Start upgrading")
        # 迭代次数加一
        self.upgrade_iter_round += 1

        self.d.click(*prop.BUILDING_DETAIL_BTN)
        time.sleep(1)
        need_upgrade_building_seq = self._select_min_building()
        self.d.click(*self._get_position(need_upgrade_building_seq))
        time.sleep(1)
        self.d.long_click(prop.BUILDING_UPGRADE_BTN[0], prop.BUILDING_UPGRADE_BTN[1],
                          self.config.upgrade_press_time_sec)
        time.sleep(0.5)
        self.d.click(*prop.BUILDING_DETAIL_BTN)
        logger.info("Upgrade complete")
    
    def _assigned_uprade(self):
        logger.info("Start assigned upgrading")
        self.d.click(*prop.BUILDING_DETAIL_BTN)
        time.sleep(0.5)
        self.d.click(*self._get_position(self.config.assigned_building_pos))
        time.sleep(0.5)
        self.d.long_click(prop.BUILDING_UPGRADE_BTN[0], prop.BUILDING_UPGRADE_BTN[1],
                          self.config.upgrade_press_time_sec)
        time.sleep(0.5)
        self.d.click(*prop.BUILDING_DETAIL_BTN)
        logger.info("Upgrade complete")

    def _upgrade_to(self, target_level):
        """
        target_level: 目标等级
        升至 target_level 级
        利用 Tesseract 识别当前等级后点击升级按钮 target_level - 当前等级次
        """
        screen = self.d.screenshot(format="opencv")
        screen = UIMatcher.pre(screen)
        tmp = UIMatcher.cut(screen, prop.BUILDING_INFO_PANEL_LEVEL_POS)
        tmp = UIMatcher.plain(tmp)
        tmp = UIMatcher.fill_color(tmp)
        tmp = UIMatcher.plain(tmp)
        txt = UIMatcher.image_to_txt(tmp, plus='-l chi_sim --psm 7')
        txt = UIMatcher.normalize_txt(txt)
        try:
            cur_level = int(txt)
            logger.info(f'Current level -> {cur_level}')
        except Exception:
            logger.warning(f'Current level -> {txt}')
            return
        click_times = target_level - cur_level
        self._upgrade_times(click_times)
    
    def _upgrade_times(self, click_times: int):
        """
        click_times: 点击/升级次数
        执行点击升级按钮的操作 click_times 次
        """
        # assert(times >= 0)
        while click_times > 0:
            click_times -= 1
            bx, by = prop.BUILDING_INFO_PANEL_UPGRADE_BTN
            self.d.click(bx, by)
            time.sleep(0.1)
        logger.info("Upgrade complete")
        time.sleep(0.5)
        tx, ty = prop.CONSTRUCT_BTN
        self.d.click(tx, ty)
        time.sleep(0.1)
        self.d.click(tx, ty)
        time.sleep(0.5)

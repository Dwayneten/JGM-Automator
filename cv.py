from target import TargetType
import os
import re
import cv2
import time
import subprocess
import numpy as np

TARGET_DIR = './assets/'
TMP_DIR = './tmp/'

SIMILAR = {
    '1': ['i', 'I', 'l', '|', ':', '!', '/', '\\'],
    '2': ['z', 'Z'],
    '3': [],
    '4': [],
    '5': ['s', 'S'],
    '6': [],
    '7': [],
    '8': ['&'],
    '9': [],
    '0': ['o', 'O', 'c', 'C', 'D']
}


class UIMatcher:
    @staticmethod
    def match(screen, target: TargetType):
        """
        在指定快照中确定货物的屏幕位置。
        """
        # 获取对应货物的图片。
        # 有个要点：通过截屏制作货物图片时，请在快照为实际大小的模式下截屏。
        template = cv2.imread(target.value)
        # 获取货物图片的宽高。
        th, tw = template.shape[:2]

        # 调用 OpenCV 模板匹配。
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        rank = max_val

        # 矩形左上角的位置。
        tl = max_loc

        # 阈值判断。
        if rank < 0.82:
            return None

        # 这里，我随机加入了数字（15），用于补偿匹配值和真实位置的差异。
        return tl[0] + tw / 2 + 15, tl[1] + th / 2 + 15, rank

    @staticmethod
    def read(filepath: str):
        """
        工具函数，用于读取图片。
        """
        return cv2.imread(filepath)

    @staticmethod
    def write(image):
        """
        工具函数，用于读取图片。
        """
        ts = str(int(time.time()))
        return cv2.imwrite(f'{TARGET_DIR}{ts}.jpg', image)

    @staticmethod
    def image_to_txt(image, cleanup=False, plus=''):
        # cleanup为True则识别完成后删除生成的文本文件
        # plus参数为给tesseract的附加高级参数
        image_url = f'{TMP_DIR}tmp.jpg'
        txt_name = f'{TMP_DIR}tmp'
        txt_url = f'{txt_name}.txt'
        if not os.path.exists(TMP_DIR): os.mkdir(TMP_DIR)
        cv2.imwrite(image_url, image)

        subprocess.check_output('tesseract --dpi 72 ' + image_url + ' ' +
                                txt_name + ' ' + plus, shell=True)  # 生成同名txt文件
        text = ''
        with open(txt_url, 'r') as f:
            text = f.read().strip()
        if cleanup:
            os.remove(txt_url)
            os.remove(image_url)
        return text

    @staticmethod
    def normalize_txt(txt: str):
        for key, sim_list in SIMILAR.items():
            for sim in sim_list:
                txt = txt.replace(sim, key)
        txt = re.sub(r'\D', '', txt)
        return txt

    @staticmethod
    def cut(image, left_up, len_width=(190, 50)):
        sx = left_up[0]
        sy = left_up[1]
        dx = left_up[0] + len_width[0]
        dy = left_up[1] + len_width[1]
        return image[sy:dy, sx:dx]

    @staticmethod
    def plain(image):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        erode = cv2.erode(image, kernel)
        dilate = cv2.dilate(erode, kernel)
        return dilate

    @staticmethod
    def fill_color(image):
        copy_image = image.copy()
        h, w = image.shape[:2]
        mask = np.zeros([h + 2, w + 2], np.uint8)
        cv2.floodFill(copy_image, mask, (0, 0), (255, 255, 255), (100, 100, 100), (50, 50, 50),
                      cv2.FLOODFILL_FIXED_RANGE)
        return copy_image

    @staticmethod
    def pre(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([103, 43, 46])
        upper_blue = np.array([103, 255, 255])
        image = cv2.inRange(image, lower_blue, upper_blue)
        return image

    @staticmethod
    def pre_building_panel(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask_orange = cv2.inRange(image, (10, 40, 40), (40, 255, 255))
        mask_blue = cv2.inRange(image, (80, 40, 40), (140, 255, 255))
        image = cv2.bitwise_or(mask_orange, mask_blue)
        return image

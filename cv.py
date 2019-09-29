from target import TargetType
import cv2


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
        if rank < 0.9:
            return None

        # 这里，我随机加入了数字（15），用于补偿匹配值和真实位置的差异。
        return tl[0] + tw / 2 + 15, tl[1] + th / 2 + 15, rank

    @staticmethod
    def read(filepath: str):
        """
        工具函数，用于读取图片。
        """
        return cv2.imread(filepath)

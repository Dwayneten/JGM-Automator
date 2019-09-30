from automator import Automator
from target import TargetType
from building import BuildingType
from numpy import array

BUILDING_2_GOODS = {
    BuildingType.木屋: TargetType.Chair,
    BuildingType.居民楼: TargetType.Box,
    BuildingType.钢结构房: TargetType.Sofa,
    BuildingType.平房: None,
    BuildingType.小型公寓: None,
    BuildingType.人才公寓: None,
    BuildingType.花园洋房: None,
    BuildingType.中式小楼: TargetType.Quilt,
    BuildingType.空中别墅: None,
    BuildingType.复兴公馆: None,
    BuildingType.便利店: TargetType.Bottle,
    BuildingType.五金店: TargetType.Screw,
    BuildingType.服装店: TargetType.Cloth,
    BuildingType.菜市场: TargetType.Vegetable,
    BuildingType.学校: None,
    BuildingType.图书城: TargetType.Book,
    BuildingType.商贸中心: None,
    BuildingType.加油站: None,
    BuildingType.民食斋: None,
    BuildingType.媒体之声: None,
    BuildingType.木材厂: TargetType.Wood,
    BuildingType.食品厂: TargetType.Food,
    BuildingType.造纸厂: TargetType.Straw,
    BuildingType.水厂: None,
    BuildingType.电厂: None,
    BuildingType.钢铁厂: TargetType.Coal,
    BuildingType.纺织厂: TargetType.Cotton,
    BuildingType.零件厂: None,
    BuildingType.企鹅机械: None,
    BuildingType.人民石油: None,
}

BUILDING_POS = (
    (BuildingType.纺织厂, BuildingType.钢铁厂, BuildingType.造纸厂),
    (BuildingType.便利店, BuildingType.图书城, BuildingType.服装店),
    (BuildingType.中式小楼, BuildingType.居民楼, BuildingType.钢结构房),
)
BUILDING_POS = array(BUILDING_POS[::-1]).flatten().tolist()


def generate_targets():
    res = {}
    for i, building in enumerate(BUILDING_POS):
        building_seq = i + 1
        goods = BUILDING_2_GOODS[building]
        if goods is not None:
            res[goods] = building_seq
    return res


if __name__ == '__main__':
    # 声明货物要移动到的建筑 ID 。
    targets = generate_targets()

    # 连接 adb 。
    instance = Automator('emulator-5554', targets,BUILDING_POS)

    # 启动脚本。
    instance.start()

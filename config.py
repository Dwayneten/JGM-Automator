import json
import prop
from numpy import array
from building import BuildingType

CONFIG_FILE = './config.json'

class Reader:
    building_pos = None
    goods_2_building_seq = None
    swipe_interval_sec = None
    upgrade_interval_sec = None
    debug_mode = False
    refresh_train = False
    detect_goods = False
    upgrade_building = False
    upgrade_building_list = None

    @staticmethod
    def _building_name_2_building_enum(building_name):
        for building in BuildingType:
            enum_name = str(building).split('.')[1]
            if enum_name == building_name:
                return building
        raise Exception(f'Wrong building name [{building_name}]')

    def _flatten_list(self, leveled_building_pos):
        tmp_list = array(leveled_building_pos[::-1]).flatten().tolist()
        return [self._building_name_2_building_enum(ele) for ele in tmp_list]

    @staticmethod
    def _generate_building_pos(flattened_building_pos):
        return [ele for ele in flattened_building_pos]

    @staticmethod
    def _generate_goods_2_building_seq(building_pos, train_get_rank):
        mask_building_pos = list(filter(lambda building: prop.BUILDING_RANK[building] in train_get_rank, building_pos))

        res = {}
        for i, building in enumerate(building_pos):
            building_seq = i + 1
            goods = prop.BUILDING_2_GOODS[building]
            if goods is not None and building in mask_building_pos:
                res[goods] = building_seq
        return res

    def refresh(self):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.swipe_interval_sec = config['swipe_interval_sec']
        self.upgrade_interval_sec = config['upgrade_interval_sec']
        flattened_building_pos = self._flatten_list(config['building_pos'])
        self.building_pos = self._generate_building_pos(flattened_building_pos)
        self.goods_2_building_seq = self._generate_goods_2_building_seq(self.building_pos, config['train_get_rank'])

        self.debug_mode = config['debug_mode']
        self.detect_goods = config['detect_goods']
        if self.detect_goods:
            self.refresh_train = config['refresh_train']
            self.expect_target_rank = [0, 1, 2]
            for i in config['train_get_rank']:
                self.expect_target_rank.remove(i)
            self.goods_2_building_seq_excpet_target = self._generate_goods_2_building_seq(self.building_pos, self.expect_target_rank)
        self.upgrade_building = config['upgrade_building']
        if self.upgrade_building:
            self.upgrade_building_list = config['upgrade_building_list']

"""牌阵定义"""


class Spread:
    """牌阵类"""
    
    def __init__(self, id, name, name_cn, description, cards, positions):
        self.id = id
        self.name = name
        self.name_cn = name_cn
        self.description = description
        self.cards = cards
        self.positions = positions
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'name_cn': self.name_cn,
            'description': self.description,
            'cards': self.cards,
            'positions': self.positions
        }


# 牌阵字典
SPREADS = {
    'single': Spread(
        id='single',
        name='Single Card',
        name_cn='单牌占卜',
        description='快速洞察问题的核心能量',
        cards=1,
        positions=[
            {'name': '核心', 'description': '当前情况的核心能量'}
        ]
    ),
    
    'three_card': Spread(
        id='three_card',
        name='Three Card Spread',
        name_cn='三牌阵',
        description='探索过去、现在、未来',
        cards=3,
        positions=[
            {'name': '过去', 'description': '影响当前的过去因素'},
            {'name': '现在', 'description': '当前的情况和挑战'},
            {'name': '未来', 'description': '可能的发展方向'}
        ]
    ),
    
    'celtic_cross': Spread(
        id='celtic_cross',
        name='Celtic Cross',
        name_cn='凯尔特十字',
        description='最经典全面的 10 张牌阵',
        cards=10,
        positions=[
            {'name': '现状', 'description': '当前的核心问题'},
            {'name': '挑战', 'description': '横跨的挑战或帮助'},
            {'name': '根源', 'description': '问题的深层根源'},
            {'name': '过去', 'description': '正在离去的影响'},
            {'name': '顶点', 'description': '可能的最佳结果'},
            {'name': '未来', 'description': '即将到来的影响'},
            {'name': '自己', 'description': '你在情况中的角色'},
            {'name': '环境', 'description': '外部影响和他人'},
            {'name': '希望与恐惧', 'description': '内心的期待和担忧'},
            {'name': '结果', 'description': '最终的发展方向'}
        ]
    )
}


def get_spread_by_id(spread_id):
    """根据 ID 获取牌阵"""
    return SPREADS.get(spread_id)


def get_all_spreads():
    """获取所有牌阵"""
    return {k: v.to_dict() for k, v in SPREADS.items()}

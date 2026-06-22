"""塔罗牌数据定义"""
from data.card_images import get_card_image


MINOR_SUITS_BY_OFFSET = ['wands', 'cups', 'swords', 'pentacles']
MINOR_VALUES_BY_OFFSET = [
    'ace', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'page', 'knight', 'queen', 'king'
]


def get_minor_identity_from_id(card_id):
    """根据 22-77 的小阿尔卡纳 ID 推导花色和点数。"""
    if not 22 <= card_id <= 77:
        return None, None

    offset = card_id - 22
    suit = MINOR_SUITS_BY_OFFSET[offset // 14]
    value = MINOR_VALUES_BY_OFFSET[offset % 14]
    return suit, value


class TarotCard:
    """塔罗牌类"""

    def __init__(self, id, name, name_cn, type, upright, reversed, element=None, astrology=None, suit=None, value=None):
        self.id = id
        self.name = name
        self.name_cn = name_cn
        self.type = type
        self.upright = upright
        self.reversed = reversed
        self.element = element
        self.astrology = astrology
        if type == 'minor':
            suit, value = get_minor_identity_from_id(id)
        self.suit = suit
        self.value = value
        # 自动生成图片URL
        self.image = get_card_image(id, type, suit, value)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'name_cn': self.name_cn,
            'type': self.type,
            'upright': self.upright,
            'reversed': self.reversed,
            'element': self.element,
            'astrology': self.astrology,
            'suit': self.suit,
            'value': self.value,
            'image': self.image
        }


# 大阿尔卡纳（22张）
MAJOR_ARCANA = [
    TarotCard(
        id=0,
        name="The Fool",
        name_cn="愚者",
        type="major",
        upright={
            'keywords': ["新开始", "冒险", "纯真", "自由", "无限可能"],
            'meaning': "愚者代表新的开始和无限的可能性。站在悬崖边缘，象征着迈向未知的勇气和对生命的信任。"
        },
        reversed={
            'keywords': ["鲁莽", "冲动", "缺乏计划", "幼稚"],
            'meaning': "逆位的愚者可能表示行动过于草率，缺乏必要的准备或考虑不周。"
        },
        element=None,
        astrology="天王星"
    , suit=None, value=None),
    TarotCard(
        id=1,
        name="The Magician",
        name_cn="魔术师",
        type="major",
        upright={
            'keywords': ["创造力", "技能", "意志力", "资源", "行动力"],
            'meaning': "魔术师象征着将想法转化为现实的能力。你拥有所需的所有工具和资源。"
        },
        reversed={
            'keywords': ["操纵", "欺骗", "浪费才能", "缺乏专注"],
            'meaning': "逆位的魔术师可能表示才能被浪费，或者在使用技能时缺乏诚信。"
        },
        element="风",
        astrology="水星"
    , suit=None, value=None),
    TarotCard(
        id=2,
        name="The High Priestess",
        name_cn="女祭司",
        type="major",
        upright={
            'keywords': ["直觉", "潜意识", "神秘", "智慧", "内在知识"],
            'meaning': "女祭司代表内在的智慧和直觉。她提醒你倾听内心深处的声音。"
        },
        reversed={
            'keywords': ["忽视直觉", "秘密", "隐藏议程", "内在混乱"],
            'meaning': "逆位的女祭司可能表示你忽视了自己的直觉，或者有重要信息尚未揭示。"
        },
        element="水",
        astrology="月亮"
    , suit=None, value=None),
    TarotCard(
        id=3,
        name="The Empress",
        name_cn="皇后",
        type="major",
        upright={
            'keywords': ["丰饶", "养育", "创造", "自然", "美丽"],
            'meaning': "皇后象征着丰盛和创造力。她代表自然的生长力量和母性的养育。"
        },
        reversed={
            'keywords': ["依赖", "窒息", "创造力受阻", "缺乏成长"],
            'meaning': "逆位的皇后可能表示过度依赖或创造力受到阻碍。"
        },
        element="土",
        astrology="金星"
    , suit=None, value=None),
    TarotCard(
        id=4,
        name="The Emperor",
        name_cn="皇帝",
        type="major",
        upright={
            'keywords': ["权威", "结构", "控制", "稳定", "父亲形象"],
            'meaning': "皇帝代表秩序、权威和稳固的结构。他象征着建立规则和维持秩序的力量。"
        },
        reversed={
            'keywords': ["专制", "僵化", "缺乏纪律", "控制过度"],
            'meaning': "逆位的皇帝可能表示过度控制或缺乏必要的结构和纪律。"
        },
        element="火",
        astrology="白羊座"
    , suit=None, value=None),
    TarotCard(
        id=5,
        name="The Hierophant",
        name_cn="教皇",
        type="major",
        upright={
            'keywords': ["传统", "精神指导", "教育", "信仰", "规范"],
            'meaning': "教皇代表传统智慧和精神指导。他象征着通过传统途径获得知识。"
        },
        reversed={
            'keywords': ["反叛", "打破传统", "个人信仰", "非正统"],
            'meaning': "逆位的教皇可能表示质疑传统或寻求非传统的精神道路。"
        },
        element="土",
        astrology="金牛座"
    , suit=None, value=None),
    TarotCard(
        id=6,
        name="The Lovers",
        name_cn="恋人",
        type="major",
        upright={
            'keywords': ["爱情", "和谐", "选择", "伙伴关系", "价值观"],
            'meaning': "恋人牌代表深刻的连接和重要的选择。它关乎价值观的一致和心灵的契合。"
        },
        reversed={
            'keywords': ["不和谐", "错位", "错误选择", "价值冲突"],
            'meaning': "逆位的恋人可能表示关系中的不和谐或价值观的冲突。"
        },
        element="风",
        astrology="双子座"
    , suit=None, value=None),
    TarotCard(
        id=7,
        name="The Chariot",
        name_cn="战车",
        type="major",
        upright={
            'keywords': ["胜利", "意志力", "决心", "控制", "前进"],
            'meaning': "战车象征着通过意志力和决心获得胜利。它代表克服障碍的力量。"
        },
        reversed={
            'keywords': ["失控", "方向不明", "侵略性", "缺乏动力"],
            'meaning': "逆位的战车可能表示失去方向或难以控制局面。"
        },
        element="水",
        astrology="巨蟹座"
    , suit=None, value=None),
    TarotCard(
        id=8,
        name="Strength",
        name_cn="力量",
        type="major",
        upright={
            'keywords': ["勇气", "耐心", "温柔", "内在力量", "同情"],
            'meaning': "力量牌代表内在的力量和温柔的勇气。真正的力量来自同情和耐心。"
        },
        reversed={
            'keywords': ["自我怀疑", "脆弱", "缺乏信心", "能量耗尽"],
            'meaning': "逆位的力量可能表示缺乏信心或内在力量被削弱。"
        },
        element="火",
        astrology="狮子座"
    , suit=None, value=None),
    TarotCard(
        id=9,
        name="The Hermit",
        name_cn="隐士",
        type="major",
        upright={
            'keywords': ["内省", "独处", "寻求真理", "智慧", "指引"],
            'meaning': "隐士代表通过独处和内省寻找真理。他象征着内在的光明和智慧。"
        },
        reversed={
            'keywords': ["孤立", "孤独", "迷失", "拒绝帮助"],
            'meaning': "逆位的隐士可能表示过度孤立或迷失方向。"
        },
        element="土",
        astrology="处女座"
    , suit=None, value=None),
    TarotCard(
        id=10,
        name="Wheel of Fortune",
        name_cn="命运之轮",
        type="major",
        upright={
            'keywords': ["变化", "周期", "命运", "转折点", "好运"],
            'meaning': "命运之轮象征着生命的周期和不可避免的变化。命运正在转动。"
        },
        reversed={
            'keywords': ["厄运", "抗拒变化", "打破周期", "失控"],
            'meaning': "逆位的命运之轮可能表示抗拒变化或经历困难时期。"
        },
        element="火",
        astrology="木星"
    , suit=None, value=None),
    TarotCard(
        id=11,
        name="Justice",
        name_cn="正义",
        type="major",
        upright={
            'keywords': ["公平", "真理", "法律", "因果", "平衡"],
            'meaning': "正义牌代表公平、真理和因果法则。你的行动将带来相应的结果。"
        },
        reversed={
            'keywords': ["不公", "偏见", "逃避责任", "失衡"],
            'meaning': "逆位的正义可能表示不公平的对待或逃避责任。"
        },
        element="风",
        astrology="天秤座"
    , suit=None, value=None),
    TarotCard(
        id=12,
        name="The Hanged Man",
        name_cn="倒吊人",
        type="major",
        upright={
            'keywords': ["牺牲", "放手", "新视角", "暂停", "臣服"],
            'meaning': "倒吊人代表通过放手和改变视角获得新的理解。有时停顿是必要的。"
        },
        reversed={
            'keywords': ["拖延", "抗拒", "停滞不前", "徒劳牺牲"],
            'meaning': "逆位的倒吊人可能表示无意义的拖延或拒绝必要的改变。"
        },
        element="水",
        astrology="海王星"
    , suit=None, value=None),
    TarotCard(
        id=13,
        name="Death",
        name_cn="死神",
        type="major",
        upright={
            'keywords': ["转变", "结束", "新生", "释放", "过渡"],
            'meaning': "死神象征着重大的转变和结束。旧事物的结束为新事物的开始创造空间。"
        },
        reversed={
            'keywords': ["抗拒改变", "停滞", "无法放手", "恐惧"],
            'meaning': "逆位的死神可能表示抗拒必要的改变或无法放下过去。"
        },
        element="水",
        astrology="天蝎座"
    , suit=None, value=None),
    TarotCard(
        id=14,
        name="Temperance",
        name_cn="节制",
        type="major",
        upright={
            'keywords': ["平衡", "耐心", "节制", "和谐", "整合"],
            'meaning': "节制牌代表平衡和中庸之道。它提醒我们耐心和适度的重要性。"
        },
        reversed={
            'keywords': ["失衡", "过度", "缺乏耐心", "极端"],
            'meaning': "逆位的节制可能表示失去平衡或走向极端。"
        },
        element="火",
        astrology="射手座"
    , suit=None, value=None),
    TarotCard(
        id=15,
        name="The Devil",
        name_cn="恶魔",
        type="major",
        upright={
            'keywords': ["束缚", "瘾", "欲望", "物质主义", "阴影"],
            'meaning': "恶魔牌代表我们自我设限的束缚。它提醒我们审视自己的执着和瘾。"
        },
        reversed={
            'keywords': ["解脱", "觉醒", "打破束缚", "自由"],
            'meaning': "逆位的恶魔可能表示从束缚中解脱或开始觉醒。"
        },
        element="土",
        astrology="摩羯座"
    , suit=None, value=None),
    TarotCard(
        id=16,
        name="The Tower",
        name_cn="高塔",
        type="major",
        upright={
            'keywords': ["突变", "混乱", "启示", "解放", "崩溃"],
            'meaning': "高塔象征着突然的改变和旧结构的崩塌。虽然痛苦，但它带来必要的解放。"
        },
        reversed={
            'keywords': ["避免灾难", "恐惧改变", "延迟崩溃", "内在动荡"],
            'meaning': "逆位的高塔可能表示推迟了的危机或内在的动荡。"
        },
        element="火",
        astrology="火星"
    , suit=None, value=None),
    TarotCard(
        id=17,
        name="The Star",
        name_cn="星星",
        type="major",
        upright={
            'keywords': ["希望", "灵感", "宁静", "治愈", "乐观"],
            'meaning': "星星牌代表希望和精神的更新。黑暗过后，星光指引着前路。"
        },
        reversed={
            'keywords': ["失去信心", "绝望", "缺乏灵感", "悲观"],
            'meaning': "逆位的星星可能表示暂时失去希望或信心。"
        },
        element="风",
        astrology="水瓶座"
    , suit=None, value=None),
    TarotCard(
        id=18,
        name="The Moon",
        name_cn="月亮",
        type="major",
        upright={
            'keywords': ["幻觉", "恐惧", "潜意识", "直觉", "不确定"],
            'meaning': "月亮牌代表潜意识的领域和内心的恐惧。并非所有事物都如表面所见。"
        },
        reversed={
            'keywords': ["释放恐惧", "真相揭示", "清晰", "直觉被压抑"],
            'meaning': "逆位的月亮可能表示恐惧开始消散或真相即将浮现。"
        },
        element="水",
        astrology="双鱼座"
    , suit=None, value=None),
    TarotCard(
        id=19,
        name="The Sun",
        name_cn="太阳",
        type="major",
        upright={
            'keywords': ["成功", "喜悦", "活力", "真实", "光明"],
            'meaning': "太阳牌代表纯粹的喜悦和生命的活力。一切都在阳光下清晰可见。"
        },
        reversed={
            'keywords': ["暂时阴云", "延迟成功", "过度乐观", "内在孩童受伤"],
            'meaning': "逆位的太阳可能表示暂时的阴霾或过度乐观。"
        },
        element="火",
        astrology="太阳"
    , suit=None, value=None),
    TarotCard(
        id=20,
        name="Judgement",
        name_cn="审判",
        type="major",
        upright={
            'keywords': ["觉醒", "更新", "反思", "召唤", "宽恕"],
            'meaning': "审判牌代表重生和更高层次的觉醒。是时候回顾过去并向前迈进了。"
        },
        reversed={
            'keywords': ["自我怀疑", "逃避责任", "内疚", "无法原谅"],
            'meaning': "逆位的审判可能表示无法放下过去或逃避必要的评估。"
        },
        element="火",
        astrology="冥王星"
    , suit=None, value=None),
    TarotCard(
        id=21,
        name="The World",
        name_cn="世界",
        type="major",
        upright={
            'keywords': ["完成", "成就", "整合", "旅程结束", "圆满"],
            'meaning': "世界牌代表一个周期的完成和成就。你已经达到了一个重要的里程碑。"
        },
        reversed={
            'keywords': ["未完成", "缺乏闭合", "寻求闭环", "延迟"],
            'meaning': "逆位的世界可能表示事情尚未完成或缺乏圆满感。"
        },
        element="土",
        astrology="土星"
    , suit=None, value=None)
]

# 小阿尔卡纳（待实现）
MINOR_ARCANA = []

# 完整牌库
TAROT_DECK = MAJOR_ARCANA + MINOR_ARCANA


def get_card_by_id(card_id):
    """根据 ID 获取卡牌"""
    for card in TAROT_DECK:
        if card.id == card_id:
            return card
    return None


def get_all_cards():
    """获取所有卡牌"""
    return [card.to_dict() for card in TAROT_DECK]


def get_deck_size():
    """获取牌库大小"""
    return len(TAROT_DECK)

# 小阿尔卡纳 - 权杖组 (Wands) - 14张
WANDS = [
    TarotCard(
        id=22,
        name="Ace of Wands",
        name_cn="权杖王牌",
        type="minor",
        upright={
            'keywords': ["新机会", "灵感", "创造力", "热情", "开始"],
            'meaning': "权杖王牌代表新的创意项目、热情的开始和无限的潜力。"
        },
        reversed={
            'keywords': ["延迟", "缺乏方向", "创意受阻", "犹豫不决"],
            'meaning': "逆位可能表示计划被推迟或缺乏明确的方向。"
        },
        element="火",
        suit="wands", value="ace", astrology="天王星"
    ),
    TarotCard(
        id=23,
        name="Two of Wands",
        name_cn="权杖二",
        type="minor",
        upright={
            'keywords': ["计划", "决策", "发现", "个人力量"],
            'meaning': "权杖二象征着规划未来和做出重要决定的时刻。"
        },
        reversed={
            'keywords': ["犹豫", "害怕未知", "缺乏计划"],
            'meaning': "逆位表示对未来感到不确定或害怕做出承诺。"
        },
        element="火",
        suit="wands", value="ace", astrology="白羊座"
    ),
    TarotCard(
        id=24,
        name="Three of Wands",
        name_cn="权杖三",
        type="minor",
        upright={
            'keywords': ["扩展", "远见", "领导力", "进步"],
            'meaning': "权杖三代表视野的扩展和计划开始实现。"
        },
        reversed={
            'keywords': ["延迟", "障碍", "缺乏远见"],
            'meaning': "逆位可能表示计划遇到障碍或视野受限。"
        },
        element="火",
        suit="wands", value="ace", astrology="白羊座"
    ),
    TarotCard(
        id=25,
        name="Four of Wands",
        name_cn="权杖四",
        type="minor",
        upright={
            'keywords': ["庆祝", "和谐", "家庭", "成就"],
            'meaning': "权杖四象征着喜悦的庆祝和稳定的基础。"
        },
        reversed={
            'keywords': ["不和谐", "缺乏支持", "不稳定"],
            'meaning': "逆位可能表示家庭或团队中的不和谐。"
        },
        element="火",
        suit="wands", value="ace", astrology="白羊座"
    ),
    TarotCard(
        id=26,
        name="Five of Wands",
        name_cn="权杖五",
        type="minor",
        upright={
            'keywords': ["竞争", "冲突", "多样性", "挑战"],
            'meaning': "权杖五代表健康的竞争和不同观点的碰撞。"
        },
        reversed={
            'keywords': ["避免冲突", "内部冲突", "和解"],
            'meaning': "逆位可能表示冲突开始解决或内心的挣扎。"
        },
        element="火",
        suit="wands", value="ace", astrology="狮子座"
    ),
    TarotCard(
        id=27,
        name="Six of Wands",
        name_cn="权杖六",
        type="minor",
        upright={
            'keywords': ["胜利", "成功", "认可", "自信"],
            'meaning': "权杖六象征着公开的成功和他人的认可。"
        },
        reversed={
            'keywords': ["自我怀疑", "缺乏认可", "失败"],
            'meaning': "逆位可能表示缺乏自信或成就未被认可。"
        },
        element="火",
        suit="wands", value="ace", astrology="狮子座"
    ),
    TarotCard(
        id=28,
        name="Seven of Wands",
        name_cn="权杖七",
        type="minor",
        upright={
            'keywords': ["挑战", "毅力", "捍卫立场", "勇气"],
            'meaning': "权杖七代表在压力下坚持自己的立场。"
        },
        reversed={
            'keywords': ["放弃", "被压倒", "缺乏信念"],
            'meaning': "逆位可能表示感到不堪重负或放弃坚持。"
        },
        element="火",
        suit="wands", value="ace", astrology="狮子座"
    ),
    TarotCard(
        id=29,
        name="Eight of Wands",
        name_cn="权杖八",
        type="minor",
        upright={
            'keywords': ["速度", "行动", "快速进展", "旅行"],
            'meaning': "权杖八象征着快速的行动和事情的迅速发展。"
        },
        reversed={
            'keywords': ["延迟", "仓促", "缺乏方向"],
            'meaning': "逆位可能表示计划被推迟或行动过于仓促。"
        },
        element="火",
        suit="wands", value="ace", astrology="射手座"
    ),
    TarotCard(
        id=30,
        name="Nine of Wands",
        name_cn="权杖九",
        type="minor",
        upright={
            'keywords': ["坚韧", "勇气", "坚持", "防御"],
            'meaning': "权杖九代表在困难中坚持和最后的防线。"
        },
        reversed={
            'keywords': ["疲惫", "偏执", "防御过度"],
            'meaning': "逆位可能表示感到精疲力竭或过度防御。"
        },
        element="火",
        suit="wands", value="ace", astrology="射手座"
    ),
    TarotCard(
        id=31,
        name="Ten of Wands",
        name_cn="权杖十",
        type="minor",
        upright={
            'keywords': ["负担", "责任", "压力", "努力"],
            'meaning': "权杖十象征着承担过多的责任和压力。"
        },
        reversed={
            'keywords': ["放下负担", "委派", "优先级"],
            'meaning': "逆位可能表示开始放下一些负担或学会委派。"
        },
        element="火",
        suit="wands", value="ace", astrology="射手座"
    ),
    TarotCard(
        id=32,
        name="Page of Wands",
        name_cn="权杖侍从",
        type="minor",
        upright={
            'keywords': ["探索", "兴奋", "自由精神", "好消息"],
            'meaning': "权杖侍从代表新的冒险和充满热情的开始。"
        },
        reversed={
            'keywords': ["缺乏方向", "拖延", "坏消息"],
            'meaning': "逆位可能表示缺乏明确目标或消息被延迟。"
        },
        element="火",
        suit="wands", value="ace", astrology="水星"
    ),
    TarotCard(
        id=33,
        name="Knight of Wands",
        name_cn="权杖骑士",
        type="minor",
        upright={
            'keywords': ["冒险", "冲动", "热情", "自信"],
            'meaning': "权杖骑士象征着充满激情的行动和冒险精神。"
        },
        reversed={
            'keywords': ["鲁莽", "不耐烦", "缺乏自制"],
            'meaning': "逆位可能表示行动过于冲动或缺乏计划。"
        },
        element="火",
        suit="wands", value="ace", astrology="月亮"
    ),
    TarotCard(
        id=34,
        name="Queen of Wands",
        name_cn="权杖王后",
        type="minor",
        upright={
            'keywords': ["自信", "独立", "魅力", "决心"],
            'meaning': "权杖王后代表强大的女性能量和自信的领导力。"
        },
        reversed={
            'keywords': ["缺乏自信", "嫉妒", "控制欲"],
            'meaning': "逆位可能表示自信心受损或过度控制。"
        },
        element="火",
        suit="wands", value="ace", astrology="金星"
    ),
    TarotCard(
        id=35,
        name="King of Wands",
        name_cn="权杖国王",
        type="minor",
        upright={
            'keywords': ["领导力", "远见", "企业家精神", "荣誉"],
            'meaning': "权杖国王象征着自然的领导者和有远见的企业家。"
        },
        reversed={
            'keywords': ["专制", "冲动", "缺乏自制"],
            'meaning': "逆位可能表示领导方式过于强硬或缺乏耐心。"
        },
        element="火",
        suit="wands", value="ace", astrology="白羊座"
    )
]

# 小阿尔卡纳 - 圣杯组 (Cups) - 14张
CUPS = [
    TarotCard(
        id=36,
        name="Ace of Cups",
        name_cn="圣杯王牌",
        type="minor",
        upright={
            'keywords': ["新的爱", "情感", "直觉", "创造力"],
            'meaning': "圣杯王牌代表情感的新开始和内心的丰盛。"
        },
        reversed={
            'keywords': ["情感封闭", "压抑感受", "创意受阻"],
            'meaning': "逆位可能表示情感被压抑或难以表达感受。"
        },
        element="水",
        suit="wands", value="ace", astrology="金牛座"
    ),
    TarotCard(
        id=37,
        name="Two of Cups",
        name_cn="圣杯二",
        type="minor",
        upright={
            'keywords': ["伙伴关系", "爱情", "和谐", "连接"],
            'meaning': "圣杯二象征着深刻的情感连接和相互的吸引。"
        },
        reversed={
            'keywords': ["失衡", "破裂关系", "误解"],
            'meaning': "逆位可能表示关系中的不平衡或误解。"
        },
        element="水",
        suit="wands", value="ace", astrology="巨蟹座"
    ),
    TarotCard(
        id=38,
        name="Three of Cups",
        name_cn="圣杯三",
        type="minor",
        upright={
            'keywords': ["庆祝", "友谊", "社交", "创造力"],
            'meaning': "圣杯三代表友谊的庆祝和团体的和谐。"
        },
        reversed={
            'keywords': ["孤立", "过度放纵", "三角关系"],
            'meaning': "逆位可能表示社交问题或过度放纵。"
        },
        element="水",
        suit="wands", value="ace", astrology="巨蟹座"
    ),
    TarotCard(
        id=39,
        name="Four of Cups",
        name_cn="圣杯四",
        type="minor",
        upright={
            'keywords': ["冥想", "反思", "冷漠", "重新评估"],
            'meaning': "圣杯四象征着内省和对现状的重新思考。"
        },
        reversed={
            'keywords': ["觉醒", "新机会", "动力恢复"],
            'meaning': "逆位可能表示从冷漠中醒来或看到新机会。"
        },
        element="水",
        suit="wands", value="ace", astrology="巨蟹座"
    ),
    TarotCard(
        id=40,
        name="Five of Cups",
        name_cn="圣杯五",
        type="minor",
        upright={
            'keywords': ["失落", "悲伤", "遗憾", "失望"],
            'meaning': "圣杯五代表失落和悲伤，但也提醒还有希望存在。"
        },
        reversed={
            'keywords': ["接受", "向前看", "宽恕"],
            'meaning': "逆位可能表示开始接受损失并向前看。"
        },
        element="水",
        suit="wands", value="ace", astrology="天蝎座"
    ),
    TarotCard(
        id=41,
        name="Six of Cups",
        name_cn="圣杯六",
        type="minor",
        upright={
            'keywords': ["怀旧", "童年", "天真", "重逢"],
            'meaning': "圣杯六象征着对过去的回忆和纯真的快乐。"
        },
        reversed={
            'keywords': ["困于过去", "未实现的希望"],
            'meaning': "逆位可能表示过度沉浸于过去或需要放手。"
        },
        element="水",
        suit="wands", value="ace", astrology="天蝎座"
    ),
    TarotCard(
        id=42,
        name="Seven of Cups",
        name_cn="圣杯七",
        type="minor",
        upright={
            'keywords': ["选择", "幻想", "愿望", "迷惑"],
            'meaning': "圣杯七代表众多选择和需要明智决策的时刻。"
        },
        reversed={
            'keywords': ["决心", "现实", "集中注意力"],
            'meaning': "逆位可能表示开始看清现实或做出明确选择。"
        },
        element="水",
        suit="wands", value="ace", astrology="天蝎座"
    ),
    TarotCard(
        id=43,
        name="Eight of Cups",
        name_cn="圣杯八",
        type="minor",
        upright={
            'keywords': ["离开", "寻找", "失望", "撤退"],
            'meaning': "圣杯八象征着离开不再满足的情况，寻找更深的意义。"
        },
        reversed={
            'keywords': ["恐惧改变", "停滞", "回避"],
            'meaning': "逆位可能表示害怕离开或拒绝面对问题。"
        },
        element="水",
        suit="wands", value="ace", astrology="双鱼座"
    ),
    TarotCard(
        id=44,
        name="Nine of Cups",
        name_cn="圣杯九",
        type="minor",
        upright={
            'keywords': ["满足", "愿望成真", "幸福", "丰盛"],
            'meaning': "圣杯九代表情感的满足和愿望的实现。"
        },
        reversed={
            'keywords': ["贪婪", "不满足", "物质主义"],
            'meaning': "逆位可能表示永不满足或过度物质化。"
        },
        element="水",
        suit="wands", value="ace", astrology="双鱼座"
    ),
    TarotCard(
        id=45,
        name="Ten of Cups",
        name_cn="圣杯十",
        type="minor",
        upright={
            'keywords': ["家庭幸福", "和谐", "情感圆满", "和平"],
            'meaning': "圣杯十象征着情感和家庭生活的完美和谐。"
        },
        reversed={
            'keywords': ["家庭不和", "破裂关系", "不和谐"],
            'meaning': "逆位可能表示家庭或关系中的冲突。"
        },
        element="水",
        suit="wands", value="ace", astrology="双鱼座"
    ),
    TarotCard(
        id=46,
        name="Page of Cups",
        name_cn="圣杯侍从",
        type="minor",
        upright={
            'keywords': ["创造力", "直觉", "好奇", "温柔"],
            'meaning': "圣杯侍从代表情感的新消息和创意的灵感。"
        },
        reversed={
            'keywords': ["情绪不稳", "不成熟", "创意受阻"],
            'meaning': "逆位可能表示情绪波动或创意难以表达。"
        },
        element="水",
        suit="wands", value="ace", astrology="双子座"
    ),
    TarotCard(
        id=47,
        name="Knight of Cups",
        name_cn="圣杯骑士",
        type="minor",
        upright={
            'keywords': ["浪漫", "魅力", "想象力", "跟随内心"],
            'meaning': "圣杯骑士象征着浪漫的追求和情感的表达。"
        },
        reversed={
            'keywords': ["不切实际", "喜怒无常", "嫉妒"],
            'meaning': "逆位可能表示过度浪漫化或情绪不稳定。"
        },
        element="水",
        suit="wands", value="ace", astrology="巨蟹座"
    ),
    TarotCard(
        id=48,
        name="Queen of Cups",
        name_cn="圣杯王后",
        type="minor",
        upright={
            'keywords': ["同情", "直觉", "养育", "情感成熟"],
            'meaning': "圣杯王后代表深刻的同情心和情感的智慧。"
        },
        reversed={
            'keywords': ["情感依赖", "不安全感", "殉道"],
            'meaning': "逆位可能表示情感过度依赖或自我牺牲过度。"
        },
        element="水",
        suit="wands", value="ace", astrology="狮子座"
    ),
    TarotCard(
        id=49,
        name="King of Cups",
        name_cn="圣杯国王",
        type="minor",
        upright={
            'keywords': ["情感平衡", "外交", "慷慨", "智慧"],
            'meaning': "圣杯国王象征着情感成熟和平衡的智慧。"
        },
        reversed={
            'keywords': ["情感操控", "冷漠", "压抑"],
            'meaning': "逆位可能表示情感被压抑或操控他人的情感。"
        },
        element="水",
        suit="wands", value="ace", astrology="处女座"
    )
]

# 小阿尔卡纳 - 宝剑组 (Swords) - 14张
SWORDS = [
    TarotCard(
        id=50,
        name="Ace of Swords",
        name_cn="宝剑王牌",
        type="minor",
        upright={
            'keywords': ["突破", "清晰", "真理", "新想法"],
            'meaning': "宝剑王牌代表智力的突破和清晰的思维。"
        },
        reversed={
            'keywords': ["混乱", "误解", "暴力", "混淆"],
            'meaning': "逆位可能表示思维混乱或沟通不畅。"
        },
        element="风",
        suit="wands", value="ace", astrology="木星"
    ),
    TarotCard(
        id=51,
        name="Two of Swords",
        name_cn="宝剑二",
        type="minor",
        upright={
            'keywords': ["僵局", "困难决定", "回避", "平衡"],
            'meaning': "宝剑二象征着需要做出困难选择的僵持状态。"
        },
        reversed={
            'keywords': ["决断", "混乱", "信息过载"],
            'meaning': "逆位可能表示打破僵局或面对被回避的真相。"
        },
        element="风",
        suit="wands", value="ace", astrology="天秤座"
    ),
    TarotCard(
        id=52,
        name="Three of Swords",
        name_cn="宝剑三",
        type="minor",
        upright={
            'keywords': ["心碎", "悲伤", "背叛", "痛苦"],
            'meaning': "宝剑三代表深刻的情感痛苦和心碎的经历。"
        },
        reversed={
            'keywords': ["恢复", "宽恕", "释放痛苦"],
            'meaning': "逆位可能表示开始从伤痛中恢复。"
        },
        element="风",
        suit="wands", value="ace", astrology="天秤座"
    ),
    TarotCard(
        id=53,
        name="Four of Swords",
        name_cn="宝剑四",
        type="minor",
        upright={
            'keywords': ["休息", "恢复", "冥想", "静养"],
            'meaning': "宝剑四象征着休息和恢复能量的需要。"
        },
        reversed={
            'keywords': ["疲惫", "停滞", "缺乏休息"],
            'meaning': "逆位可能表示休息不足或难以放松。"
        },
        element="风",
        suit="wands", value="ace", astrology="天秤座"
    ),
    TarotCard(
        id=54,
        name="Five of Swords",
        name_cn="宝剑五",
        type="minor",
        upright={
            'keywords': ["冲突", "失败", "不公平", "背叛"],
            'meaning': "宝剑五代表不光彩的胜利和冲突的代价。"
        },
        reversed={
            'keywords': ["和解", "宽恕", "放下"],
            'meaning': "逆位可能表示冲突开始解决或学会放手。"
        },
        element="风",
        suit="wands", value="ace", astrology="水瓶座"
    ),
    TarotCard(
        id=55,
        name="Six of Swords",
        name_cn="宝剑六",
        type="minor",
        upright={
            'keywords': ["过渡", "改变", "旅程", "前进"],
            'meaning': "宝剑六象征着从困境向更好状况的过渡。"
        },
        reversed={
            'keywords': ["抗拒改变", "停滞", "无法前进"],
            'meaning': "逆位可能表示难以离开困境或抗拒改变。"
        },
        element="风",
        suit="wands", value="ace", astrology="水瓶座"
    ),
    TarotCard(
        id=56,
        name="Seven of Swords",
        name_cn="宝剑七",
        type="minor",
        upright={
            'keywords': ["欺骗", "策略", "逃避", "狡猾"],
            'meaning': "宝剑七代表需要策略性思考或可能的欺骗。"
        },
        reversed={
            'keywords': ["被揭露", "良心", "诚实"],
            'meaning': "逆位可能表示欺骗被揭露或良心的觉醒。"
        },
        element="风",
        suit="wands", value="ace", astrology="水瓶座"
    ),
    TarotCard(
        id=57,
        name="Eight of Swords",
        name_cn="宝剑八",
        type="minor",
        upright={
            'keywords': ["束缚", "限制", "受害者心态", "困境"],
            'meaning': "宝剑八象征着自我设限和感到被困。"
        },
        reversed={
            'keywords': ["解放", "新视角", "自由"],
            'meaning': "逆位可能表示开始看到出路或打破限制。"
        },
        element="风",
        suit="wands", value="ace", astrology="双子座"
    ),
    TarotCard(
        id=58,
        name="Nine of Swords",
        name_cn="宝剑九",
        type="minor",
        upright={
            'keywords': ["焦虑", "担忧", "噩梦", "恐惧"],
            'meaning': "宝剑九代表深夜的焦虑和过度的担忧。"
        },
        reversed={
            'keywords': ["恢复", "释放恐惧", "寻求帮助"],
            'meaning': "逆位可能表示开始面对恐惧或寻求支持。"
        },
        element="风",
        suit="wands", value="ace", astrology="双子座"
    ),
    TarotCard(
        id=59,
        name="Ten of Swords",
        name_cn="宝剑十",
        type="minor",
        upright={
            'keywords': ["结束", "背叛", "痛苦的结局", "触底"],
            'meaning': "宝剑十象征着痛苦的结束，但也是新开始的前夜。"
        },
        reversed={
            'keywords': ["恢复", "重生", "放下"],
            'meaning': "逆位可能表示最糟糕的时刻已过，开始恢复。"
        },
        element="风",
        suit="wands", value="ace", astrology="双子座"
    ),
    TarotCard(
        id=60,
        name="Page of Swords",
        name_cn="宝剑侍从",
        type="minor",
        upright={
            'keywords': ["好奇", "警惕", "新想法", "沟通"],
            'meaning': "宝剑侍从代表智力的好奇心和新的沟通方式。"
        },
        reversed={
            'keywords': ["八卦", "谎言", "缺乏计划"],
            'meaning': "逆位可能表示沟通问题或思维缺乏深度。"
        },
        element="风",
        suit="wands", value="ace", astrology="天秤座"
    ),
    TarotCard(
        id=61,
        name="Knight of Swords",
        name_cn="宝剑骑士",
        type="minor",
        upright={
            'keywords': ["行动", "冲动", "雄心", "驱动力"],
            'meaning': "宝剑骑士象征着快速的行动和坚定的决心。"
        },
        reversed={
            'keywords': ["鲁莽", "不耐烦", "缺乏方向"],
            'meaning': "逆位可能表示行动过于冲动或缺乏策略。"
        },
        element="风",
        suit="wands", value="ace", astrology="海王星"
    ),
    TarotCard(
        id=62,
        name="Queen of Swords",
        name_cn="宝剑王后",
        type="minor",
        upright={
            'keywords': ["独立", "清晰思维", "直接", "洞察力"],
            'meaning': "宝剑王后代表清晰的思维和独立的判断。"
        },
        reversed={
            'keywords': ["冷酷", "刻薄", "报复"],
            'meaning': "逆位可能表示过于严厉或使用言语伤人。"
        },
        element="风",
        suit="wands", value="ace", astrology="天蝎座"
    ),
    TarotCard(
        id=63,
        name="King of Swords",
        name_cn="宝剑国王",
        type="minor",
        upright={
            'keywords': ["权威", "真理", "清晰", "智力"],
            'meaning': "宝剑国王象征着智力的权威和公正的判断。"
        },
        reversed={
            'keywords': ["操控", "冷酷", "滥用权力"],
            'meaning': "逆位可能表示滥用权力或过度理性。"
        },
        element="风",
        suit="wands", value="ace", astrology="射手座"
    )
]

# 小阿尔卡纳 - 星币组 (Pentacles) - 14张
PENTACLES = [
    TarotCard(
        id=64,
        name="Ace of Pentacles",
        name_cn="星币王牌",
        type="minor",
        upright={
            'keywords': ["新机会", "繁荣", "物质", "显化"],
            'meaning': "星币王牌代表物质上的新机会和繁荣的种子。"
        },
        reversed={
            'keywords': ["错失机会", "缺乏计划", "物质损失"],
            'meaning': "逆位可能表示机会被错过或缺乏实际的计划。"
        },
        element="土",
        suit="wands", value="ace", astrology="摩羯座"
    ),
    TarotCard(
        id=65,
        name="Two of Pentacles",
        name_cn="星币二",
        type="minor",
        upright={
            'keywords': ["平衡", "适应", "时间管理", "优先级"],
            'meaning': "星币二象征着在多个责任之间寻找平衡。"
        },
        reversed={
            'keywords': ["失衡", "超负荷", "混乱"],
            'meaning': "逆位可能表示难以平衡或感到不堪重负。"
        },
        element="土",
        suit="wands", value="ace", astrology="摩羯座"
    ),
    TarotCard(
        id=66,
        name="Three of Pentacles",
        name_cn="星币三",
        type="minor",
        upright={
            'keywords': ["团队合作", "协作", "学习", "实施"],
            'meaning': "星币三代表团队合作和技能的展现。"
        },
        reversed={
            'keywords': ["缺乏团队精神", "冲突", "懒惰"],
            'meaning': "逆位可能表示团队协作出现问题。"
        },
        element="土",
        suit="wands", value="ace", astrology="摩羯座"
    ),
    TarotCard(
        id=67,
        name="Four of Pentacles",
        name_cn="星币四",
        type="minor",
        upright={
            'keywords': ["安全", "控制", "节俭", "占有"],
            'meaning': "星币四象征着对安全和控制的需求。"
        },
        reversed={
            'keywords': ["贪婪", "物质主义", "自私"],
            'meaning': "逆位可能表示过度的占有欲或物质主义。"
        },
        element="土",
        suit="wands", value="ace", astrology="摩羯座"
    ),
    TarotCard(
        id=68,
        name="Five of Pentacles",
        name_cn="星币五",
        type="minor",
        upright={
            'keywords': ["贫困", "孤立", "不安全", "困难"],
            'meaning': "星币五代表物质或情感上的困难时期。"
        },
        reversed={
            'keywords': ["恢复", "改善", "宽恕"],
            'meaning': "逆位可能表示困境开始好转。"
        },
        element="土",
        suit="wands", value="ace", astrology="金牛座"
    ),
    TarotCard(
        id=69,
        name="Six of Pentacles",
        name_cn="星币六",
        type="minor",
        upright={
            'keywords': ["慷慨", "慈善", "分享", "财富"],
            'meaning': "星币六象征着慷慨的给予和接受帮助。"
        },
        reversed={
            'keywords': ["自私", "债务", "一边倒"],
            'meaning': "逆位可能表示给予和接受的不平衡。"
        },
        element="土",
        suit="wands", value="ace", astrology="金牛座"
    ),
    TarotCard(
        id=70,
        name="Seven of Pentacles",
        name_cn="星币七",
        type="minor",
        upright={
            'keywords': ["耐心", "投资", "长期愿景", "坚持"],
            'meaning': "星币七代表对长期投资的耐心等待。"
        },
        reversed={
            'keywords': ["缺乏远见", "有限成功", "焦虑"],
            'meaning': "逆位可能表示对结果感到焦虑或失望。"
        },
        element="土",
        suit="wands", value="ace", astrology="金牛座"
    ),
    TarotCard(
        id=71,
        name="Eight of Pentacles",
        name_cn="星币八",
        type="minor",
        upright={
            'keywords': ["勤奋", "技能发展", "努力", "专注"],
            'meaning': "星币八象征着通过努力工作提升技能。"
        },
        reversed={
            'keywords': ["完美主义", "缺乏野心", "重复"],
            'meaning': "逆位可能表示过度完美主义或缺乏动力。"
        },
        element="土",
        suit="wands", value="ace", astrology="处女座"
    ),
    TarotCard(
        id=72,
        name="Nine of Pentacles",
        name_cn="星币九",
        type="minor",
        upright={
            'keywords': ["独立", "自给自足", "奢华", "成功"],
            'meaning': "星币九代表通过努力获得的物质成功和独立。"
        },
        reversed={
            'keywords': ["依赖", "缺乏自信", "物质主义"],
            'meaning': "逆位可能表示财务依赖或过度物质化。"
        },
        element="土",
        suit="wands", value="ace", astrology="处女座"
    ),
    TarotCard(
        id=73,
        name="Ten of Pentacles",
        name_cn="星币十",
        type="minor",
        upright={
            'keywords': ["财富", "遗产", "家庭", "稳定"],
            'meaning': "星币十象征着长期的财务稳定和家族财富。"
        },
        reversed={
            'keywords': ["财务损失", "家庭争执", "不稳定"],
            'meaning': "逆位可能表示家族财富问题或不稳定。"
        },
        element="土",
        suit="wands", value="ace", astrology="处女座"
    ),
    TarotCard(
        id=74,
        name="Page of Pentacles",
        name_cn="星币侍从",
        type="minor",
        upright={
            'keywords': ["雄心", "勤奋", "目标", "显化"],
            'meaning': "星币侍从代表新的学习机会和实际的开始。"
        },
        reversed={
            'keywords': ["缺乏进展", "拖延", "不切实际"],
            'meaning': "逆位可能表示计划缺乏实际性或拖延。"
        },
        element="土",
        suit="wands", value="ace", astrology="火星"
    ),
    TarotCard(
        id=75,
        name="Knight of Pentacles",
        name_cn="星币骑士",
        type="minor",
        upright={
            'keywords': ["效率", "责任", "可靠", "务实"],
            'meaning': "星币骑士象征着可靠和有条不紊的行动。"
        },
        reversed={
            'keywords': ["懒惰", "停滞", "完美主义"],
            'meaning': "逆位可能表示过度谨慎或缺乏行动。"
        },
        element="土",
        suit="wands", value="ace", astrology="水瓶座"
    ),
    TarotCard(
        id=76,
        name="Queen of Pentacles",
        name_cn="星币王后",
        type="minor",
        upright={
            'keywords': ["养育", "务实", "工作与生活平衡", "繁荣"],
            'meaning': "星币王后代表务实的养育和物质的丰盛。"
        },
        reversed={
            'keywords': ["工作狂", "嫉妒", "不安全"],
            'meaning': "逆位可能表示工作生活失衡或物质不安全感。"
        },
        element="土",
        suit="wands", value="ace", astrology="双鱼座"
    ),
    TarotCard(
        id=77,
        name="King of Pentacles",
        name_cn="星币国王",
        type="minor",
        upright={
            'keywords': ["富裕", "商业", "领导力", "安全"],
            'meaning': "星币国王象征着物质成功和商业智慧。"
        },
        reversed={
            'keywords': ["贪婪", "物质主义", "顽固"],
            'meaning': "逆位可能表示过度物质化或商业手段不当。"
        },
        element="土",
        suit="wands", value="ace", astrology="太阳"
    )
]

# 更新完整牌库
MINOR_ARCANA = WANDS + CUPS + SWORDS + PENTACLES
TAROT_DECK = MAJOR_ARCANA + MINOR_ARCANA

# 花色属性
SUIT_PROPERTIES = {
    "wands": {
        "element": "火",
        "chinese": "权杖",
        "season": "夏季",
        "direction": "南方",
        "time": "正午",
        "energy": "阳性",
        "quality": "行动、创造、激情"
    },
    "cups": {
        "element": "水",
        "chinese": "圣杯",
        "season": "秋季",
        "direction": "西方",
        "time": "黄昏",
        "energy": "阴性",
        "quality": "情感、直觉、关系"
    },
    "swords": {
        "element": "风",
        "chinese": "宝剑",
        "season": "春季",
        "direction": "东方",
        "time": "黎明",
        "energy": "阳性",
        "quality": "思想、沟通、真理"
    },
    "pentacles": {
        "element": "土",
        "chinese": "星币",
        "season": "冬季",
        "direction": "北方",
        "time": "午夜",
        "energy": "阴性",
        "quality": "物质、稳定、实际"
    }
}

# 数字牌的数秘学含义
NUMEROLOGY = {
    "ace": {"number": 1, "meaning": "开始、潜力、种子"},
    "two": {"number": 2, "meaning": "平衡、选择、对立"},
    "three": {"number": 3, "meaning": "成长、表达、创造"},
    "four": {"number": 4, "meaning": "稳定、结构、基础"},
    "five": {"number": 5, "meaning": "冲突、变化、挑战"},
    "six": {"number": 6, "meaning": "和谐、调整、责任"},
    "seven": {"number": 7, "meaning": "反思、评估、灵性"},
    "eight": {"number": 8, "meaning": "力量、行动、掌控"},
    "nine": {"number": 9, "meaning": "完成、智慧、圆满"},
    "ten": {"number": 10, "meaning": "循环、结束与开始"},
    "page": {"number": 11, "meaning": "学习、信息、新奇"},
    "knight": {"number": 12, "meaning": "行动、追求、冒险"},
    "queen": {"number": 13, "meaning": "成熟、养育、内化"},
    "king": {"number": 14, "meaning": "掌控、权威、外化"}
}


def get_card_astrology_info(card):
    """获取卡牌的完整占星学信息"""
    info = {
        "element": card.element,
        "astrology": card.astrology
    }
    
    # 如果是小阿尔卡纳，添加花色属性
    if card.type == "minor" and hasattr(card, 'suit'):
        suit = getattr(card, 'suit', None)
        if suit and suit in SUIT_PROPERTIES:
            info["suit_properties"] = SUIT_PROPERTIES[suit]
        
        # 添加数字含义
        value = getattr(card, 'value', None)
        if value and value in NUMEROLOGY:
            info["numerology"] = NUMEROLOGY[value]
    
    return info

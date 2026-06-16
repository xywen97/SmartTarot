"""塔罗牌图片配置"""

# 使用公开的 RWS (Rider-Waite-Smith) 塔罗牌图片
# 来源: https://sacred-texts.com/tarot/pkt/
IMAGE_BASE_URL = "https://www.sacred-texts.com/tarot/pkt/img"

# 大阿尔卡纳图片映射
MAJOR_ARCANA_IMAGES = {
    0: f"{IMAGE_BASE_URL}/ar00.jpg",    # The Fool
    1: f"{IMAGE_BASE_URL}/ar01.jpg",    # The Magician
    2: f"{IMAGE_BASE_URL}/ar02.jpg",    # The High Priestess
    3: f"{IMAGE_BASE_URL}/ar03.jpg",    # The Empress
    4: f"{IMAGE_BASE_URL}/ar04.jpg",    # The Emperor
    5: f"{IMAGE_BASE_URL}/ar05.jpg",    # The Hierophant
    6: f"{IMAGE_BASE_URL}/ar06.jpg",    # The Lovers
    7: f"{IMAGE_BASE_URL}/ar07.jpg",    # The Chariot
    8: f"{IMAGE_BASE_URL}/ar08.jpg",    # Strength
    9: f"{IMAGE_BASE_URL}/ar09.jpg",    # The Hermit
    10: f"{IMAGE_BASE_URL}/ar10.jpg",   # Wheel of Fortune
    11: f"{IMAGE_BASE_URL}/ar11.jpg",   # Justice
    12: f"{IMAGE_BASE_URL}/ar12.jpg",   # The Hanged Man
    13: f"{IMAGE_BASE_URL}/ar13.jpg",   # Death
    14: f"{IMAGE_BASE_URL}/ar14.jpg",   # Temperance
    15: f"{IMAGE_BASE_URL}/ar15.jpg",   # The Devil
    16: f"{IMAGE_BASE_URL}/ar16.jpg",   # The Tower
    17: f"{IMAGE_BASE_URL}/ar17.jpg",   # The Star
    18: f"{IMAGE_BASE_URL}/ar18.jpg",   # The Moon
    19: f"{IMAGE_BASE_URL}/ar19.jpg",   # The Sun
    20: f"{IMAGE_BASE_URL}/ar20.jpg",   # Judgement
    21: f"{IMAGE_BASE_URL}/ar21.jpg",   # The World
}

# 小阿尔卡纳图片映射
# 格式: {suit}{value}.jpg
# suit: wa(wands), cu(cups), sw(swords), pe(pentacles)
# value: ac, 02-10, pa(page), kn(knight), qu(queen), ki(king)

def get_minor_image(suit, value):
    """获取小阿尔卡纳图片URL"""
    suit_abbr = {
        'wands': 'wa',
        'cups': 'cu',
        'swords': 'sw',
        'pentacles': 'pe'
    }
    
    value_abbr = {
        'ace': 'ac',
        'two': '02',
        'three': '03',
        'four': '04',
        'five': '05',
        'six': '06',
        'seven': '07',
        'eight': '08',
        'nine': '09',
        'ten': '10',
        'page': 'pa',
        'knight': 'kn',
        'queen': 'qu',
        'king': 'ki'
    }
    
    s = suit_abbr.get(suit, 'wa')
    v = value_abbr.get(value, 'ac')
    
    return f"{IMAGE_BASE_URL}/{s}{v}.jpg"


def get_card_image(card_id, card_type, suit=None, value=None):
    """
    获取卡牌图片URL
    
    Args:
        card_id: 卡牌ID
        card_type: 'major' 或 'minor'
        suit: 花色（仅小阿尔卡纳需要）
        value: 数值（仅小阿尔卡纳需要）
    
    Returns:
        图片URL
    """
    if card_type == 'major':
        return MAJOR_ARCANA_IMAGES.get(card_id, f"{IMAGE_BASE_URL}/ar00.jpg")
    else:
        return get_minor_image(suit, value)


# 备用图片源（如果主源不可用）
FALLBACK_IMAGE_URL = "https://via.placeholder.com/300x500/1a1a2e/ffd700?text=Tarot+Card"

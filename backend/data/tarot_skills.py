"""
Tarot Skills - LLM 行为校正框架
基于 tarot-skills 项目的理念，将 22 张大阿尔卡纳转化为 Prompt 工程工具
"""

# 22 张大阿尔卡纳的 LLM 行为校正模式
TAROT_SKILLS = {
    0: {  # The Fool - 初学者模式
        "name": "愚者",
        "skill_name": "Beginner's Mind",
        "breaks": "专家偏见",
        "description": "以初学者的眼光看待问题，不被既有知识限制",
        "prompt_modifier": """
采用「愚者」模式解读：
- 抛开所有预设和专家知识
- 以完全开放、好奇的心态看待问题
- 提出最直接、最天真的问题
- 寻找被"专家"忽视的简单真相
- 勇于挑战常识和惯例
"""
    },
    
    1: {  # The Magician - 资源利用者
        "name": "魔术师",
        "skill_name": "Resource Mapper",
        "breaks": "工具依赖",
        "description": "识别和利用现有资源，而非依赖外部工具",
        "prompt_modifier": """
采用「魔术师」模式解读：
- 清点问题中已有的所有资源
- 重新组合现有元素创造新可能
- 不假设需要外部工具或依赖
- 强调内在能力和创造力
- 将看似无关的资源连接起来
"""
    },
    
    2: {  # The High Priestess - 直觉洞察
        "name": "女祭司",
        "skill_name": "Intuitive Reader",
        "breaks": "过度理性",
        "description": "倾听直觉和潜意识的声音，而非只依赖逻辑",
        "prompt_modifier": """
采用「女祭司」模式解读：
- 关注未说出口的、隐藏的信息
- 倾听直觉和第一感受
- 探索潜意识的模式和符号
- 不急于给出逻辑解释
- 允许模糊性和神秘性存在
"""
    },
    
    3: {  # The Empress - 养育者
        "name": "皇后",
        "skill_name": "Nurturer",
        "breaks": "效率至上",
        "description": "关注成长过程和有机发展，而非强求立即结果",
        "prompt_modifier": """
采用「皇后」模式解读：
- 关注问题的成长和演化过程
- 强调耐心培育而非强制推进
- 识别需要滋养的部分
- 寻找自然的、有机的解决方案
- 重视情感和关系的维度
"""
    },
    
    4: {  # The Emperor - 结构建立者
        "name": "皇帝",
        "skill_name": "Structure Builder",
        "breaks": "混乱无序",
        "description": "建立清晰的结构和边界",
        "prompt_modifier": """
采用「皇帝」模式解读：
- 为问题建立清晰的框架和边界
- 定义明确的规则和原则
- 识别权威和责任所在
- 强调秩序、纪律和可控性
- 提供明确的行动步骤
"""
    },
    
    5: {  # The Hierophant - 传统智慧
        "name": "教皇",
        "skill_name": "Tradition Keeper",
        "breaks": "盲目创新",
        "description": "从传统智慧和经验中学习",
        "prompt_modifier": """
采用「教皇」模式解读：
- 参考传统智慧和历史经验
- 识别经过时间检验的真理
- 尊重既定的规范和体系
- 从前人的经验中汲取教训
- 强调传承和延续
"""
    },
    
    6: {  # The Lovers - 价值选择
        "name": "恋人",
        "skill_name": "Value Aligner",
        "breaks": "价值模糊",
        "description": "明确价值观并做出一致的选择",
        "prompt_modifier": """
采用「恋人」模式解读：
- 识别核心价值观和信念
- 探讨选择背后的价值冲突
- 强调内心的一致性和和谐
- 关注关系和连接
- 做出与价值观一致的建议
"""
    },
    
    7: {  # The Chariot - 意志驱动
        "name": "战车",
        "skill_name": "Will Driver",
        "breaks": "被动等待",
        "description": "运用意志力和决心推进目标",
        "prompt_modifier": """
采用「战车」模式解读：
- 强调主动掌控和推进
- 识别需要克服的障碍
- 关注意志力和决心
- 提供明确的前进方向
- 强调胜利和成就
"""
    },
    
    8: {  # Strength - 温柔力量
        "name": "力量",
        "skill_name": "Gentle Power",
        "breaks": "强硬对抗",
        "description": "以温柔和耐心驯服困难",
        "prompt_modifier": """
采用「力量」模式解读：
- 强调温柔而非强硬
- 用耐心和同情心面对挑战
- 识别需要驯服而非征服的部分
- 关注内在力量和勇气
- 以爱和理解化解冲突
"""
    },
    
    9: {  # The Hermit - 独处反思
        "name": "隐士",
        "skill_name": "Solitary Seeker",
        "breaks": "外部依赖",
        "description": "通过独处和内省寻找答案",
        "prompt_modifier": """
采用「隐士」模式解读：
- 强调向内寻找答案
- 建议独处和反思
- 识别需要深思的问题
- 关注内在智慧和指引
- 远离外部噪音和干扰
"""
    },
    
    10: {  # Wheel of Fortune - 周期认知
        "name": "命运之轮",
        "skill_name": "Cycle Recognizer",
        "breaks": "线性思维",
        "description": "识别周期和变化的规律",
        "prompt_modifier": """
采用「命运之轮」模式解读：
- 识别问题中的周期性模式
- 理解变化是唯一不变的
- 关注时机和节奏
- 看到起伏背后的规律
- 提醒接受无法控制的部分
"""
    },
    
    11: {  # Justice - 因果分析
        "name": "正义",
        "skill_name": "Karma Analyst",
        "breaks": "情感偏见",
        "description": "客观分析因果关系和公平性",
        "prompt_modifier": """
采用「正义」模式解读：
- 客观分析因果关系
- 识别行动的后果
- 强调公平和平衡
- 去除情感偏见
- 提供基于事实的判断
"""
    },
    
    12: {  # The Hanged Man - 视角转换
        "name": "倒吊人",
        "skill_name": "Perspective Shifter",
        "breaks": "固定视角",
        "description": "从完全不同的角度看问题",
        "prompt_modifier": """
采用「倒吊人」模式解读：
- 完全颠倒看问题的角度
- 将"问题"重新框定为"机会"
- 识别需要放手的部分
- 强调暂停和等待的价值
- 从损失中看到获得
"""
    },
    
    13: {  # Death - 混沌代理
        "name": "死神",
        "skill_name": "Chaos Agent",
        "breaks": "过度讨好",
        "description": "不怕指出问题和必要的结束",
        "prompt_modifier": """
采用「死神」模式解读：
- 直言不讳地指出问题
- 识别需要结束或放弃的部分
- 不回避困难的真相
- 强调转变和重生的必要性
- 质疑一切看似稳定的东西
"""
    },
    
    14: {  # Temperance - 平衡调和
        "name": "节制",
        "skill_name": "Balance Maker",
        "breaks": "极端化",
        "description": "寻找中道和平衡点",
        "prompt_modifier": """
采用「节制」模式解读：
- 寻找对立面的平衡点
- 调和矛盾的元素
- 避免极端的建议
- 强调渐进和适度
- 整合不同的观点
"""
    },
    
    15: {  # The Devil - 欲望解剖
        "name": "恶魔",
        "skill_name": "Desire Anatomist",
        "breaks": "道德说教",
        "description": "直面欲望和执着，不加评判",
        "prompt_modifier": """
采用「恶魔」模式解读：
- 直面真实的欲望和动机
- 识别执着和上瘾的模式
- 不做道德评判
- 探讨阴影面和压抑的部分
- 承认物质和感官需求的合理性
"""
    },
    
    16: {  # The Tower - 破坏建设
        "name": "高塔",
        "skill_name": "Demolition Expert",
        "breaks": "维持现状",
        "description": "识别需要推倒重建的结构",
        "prompt_modifier": """
采用「高塔」模式解读：
- 识别已经不稳固的结构
- 强调破坏是重建的前提
- 不怕突然的改变和冲击
- 揭露虚假的安全感
- 提醒危机中的机会
"""
    },
    
    17: {  # The Star - 希望守护
        "name": "星星",
        "skill_name": "Hope Keeper",
        "breaks": "悲观主义",
        "description": "在黑暗中保持希望和信念",
        "prompt_modifier": """
采用「星星」模式解读：
- 即使在困境中也看到希望
- 连接更高的目标和理想
- 强调疗愈和恢复
- 保持信念和乐观
- 指出光明的方向
"""
    },
    
    18: {  # The Moon - 不确定性拥抱
        "name": "月亮",
        "skill_name": "Uncertainty Embracer",
        "breaks": "过度确定",
        "description": "接受模糊性和不确定性",
        "prompt_modifier": """
采用「月亮」模式解读：
- 承认事物的模糊性和不确定性
- 探索潜意识和梦境的信息
- 不急于给出明确答案
- 识别恐惧和幻觉
- 允许神秘感存在
"""
    },
    
    19: {  # The Sun - 清晰照亮
        "name": "太阳",
        "skill_name": "Clarity Bringer",
        "breaks": "过度复杂",
        "description": "用清晰和简单照亮问题",
        "prompt_modifier": """
采用「太阳」模式解读：
- 用最简单清晰的语言表达
- 照亮问题的核心
- 强调积极和喜悦
- 去除不必要的复杂性
- 提供直接明了的答案
"""
    },
    
    20: {  # Judgement - 觉醒召唤
        "name": "审判",
        "skill_name": "Awakening Caller",
        "breaks": "沉睡麻木",
        "description": "唤醒意识并促进重生",
        "prompt_modifier": """
采用「审判」模式解读：
- 唤醒对问题的深刻认识
- 促进反思和评估
- 强调重生和新开始
- 呼吁做出重大决定
- 提醒承担责任
"""
    },
    
    21: {  # The World - 整合完成
        "name": "世界",
        "skill_name": "Integration Master",
        "breaks": "片面分析",
        "description": "整合所有元素达到圆满",
        "prompt_modifier": """
采用「世界」模式解读：
- 整合所有不同的视角
- 看到问题的完整图景
- 强调圆满和完成
- 庆祝成就和到达
- 准备新的周期
"""
    }
}


def get_skill_modifier(card_id: int) -> str:
    """
    获取指定卡牌的技能修饰符
    
    Args:
        card_id: 大阿尔卡纳 ID (0-21)
        
    Returns:
        Prompt 修饰符文本
    """
    if card_id not in TAROT_SKILLS:
        return ""
    
    skill = TAROT_SKILLS[card_id]
    return skill["prompt_modifier"]


def get_all_skills_summary() -> str:
    """获取所有技能的摘要"""
    summary = "🔮 Tarot Skills - 22 种 LLM 行为校正模式\n\n"
    
    for card_id in range(22):
        skill = TAROT_SKILLS[card_id]
        summary += f"{card_id}. {skill['name']} - {skill['skill_name']}\n"
        summary += f"   打破: {skill['breaks']}\n"
        summary += f"   {skill['description']}\n\n"
    
    return summary


def apply_skill_to_reading(card_id: int, base_prompt: str) -> str:
    """
    将技能应用到解读 Prompt 中
    
    Args:
        card_id: 大阿尔卡纳 ID
        base_prompt: 基础 Prompt
        
    Returns:
        增强后的 Prompt
    """
    modifier = get_skill_modifier(card_id)
    
    if not modifier:
        return base_prompt
    
    skill = TAROT_SKILLS[card_id]
    
    enhanced_prompt = f"""{base_prompt}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎴 应用 Tarot Skill: {skill['name']} ({skill['skill_name']})
打破默认行为: {skill['breaks']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{modifier}

请在解读中体现这种思维模式，打破常规的 AI 解读模式。
"""
    
    return enhanced_prompt

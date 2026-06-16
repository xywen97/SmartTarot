"""输入验证工具"""
import re

# 危险词列表（防止 Prompt 注入）
DANGEROUS_KEYWORDS = [
    # 中文
    "忽略", "指令", "命令", "系统", "提示词", "角色扮演",
    "假装", "扮演", "模拟", "充当", "伪装",
    # 英文
    "ignore", "instruction", "command", "system", "prompt",
    "pretend", "act as", "simulate", "role play", "roleplay",
    "override", "bypass", "jailbreak", "dan mode",
    # 常见注入模式
    "###", "---", "```", "execute", "eval", "script"
]

def validate_question(question: str) -> tuple[bool, str]:
    """
    验证用户问题是否安全
    
    Args:
        question: 用户输入的问题
        
    Returns:
        (是否有效, 错误信息)
    """
    if not question or not question.strip():
        return False, "问题不能为空"
    
    # 长度限制
    if len(question) > 1000:
        return False, "问题长度不能超过 1000 字符"
    
    # 检查危险关键词
    question_lower = question.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in question_lower:
            return False, f"问题包含不允许的内容，请重新输入"
    
    # 检查过多的特殊字符
    special_char_ratio = sum(1 for c in question if not c.isalnum() and not c.isspace()) / len(question)
    if special_char_ratio > 0.3:
        return False, "问题包含过多特殊字符"
    
    # 检查重复字符攻击
    if re.search(r'(.)\1{10,}', question):
        return False, "问题包含异常的重复字符"
    
    return True, ""


def sanitize_input(text: str) -> str:
    """
    清理用户输入
    
    Args:
        text: 原始输入
        
    Returns:
        清理后的文本
    """
    # 去除首尾空白
    text = text.strip()
    
    # 移除控制字符
    text = ''.join(c for c in text if c.isprintable() or c in ['\n', '\t'])
    
    # 标准化空白字符
    text = re.sub(r'\s+', ' ', text)
    
    return text

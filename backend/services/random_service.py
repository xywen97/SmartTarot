"""真随机服务"""
import secrets


class RandomService:
    """随机数生成服务（使用密码学安全的随机数）"""
    
    @staticmethod
    def draw_cards(deck_size, count):
        """
        抽取指定数量的牌（真随机）
        
        Args:
            deck_size: 牌库大小
            count: 抽取数量
            
        Returns:
            tuple: (抽取的牌索引列表, 正逆位列表)
        """
        deck = list(range(deck_size))
        drawn_indices = []
        orientations = []
        
        for _ in range(count):
            # 使用 secrets 模块的真随机
            index = secrets.randbelow(len(deck))
            drawn_indices.append(deck.pop(index))
            
            # 真随机决定正逆位
            orientations.append('upright' if secrets.randbelow(2) == 0 else 'reversed')
        
        return drawn_indices, orientations
    
    @staticmethod
    def shuffle_list(items):
        """
        随机打乱列表
        
        Args:
            items: 要打乱的列表
            
        Returns:
            list: 打乱后的列表
        """
        shuffled = items.copy()
        for i in range(len(shuffled) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled

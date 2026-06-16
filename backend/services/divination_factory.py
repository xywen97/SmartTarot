"""占卜方式工厂"""
from abc import ABC, abstractmethod
from typing import Generator


class BaseDivination(ABC):
    """占卜基类"""
    
    @abstractmethod
    def get_name(self) -> str:
        """获取占卜方式名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取占卜方式描述"""
        pass
    
    @abstractmethod
    def validate_input(self, data: dict) -> tuple[bool, str]:
        """验证输入数据"""
        pass
    
    @abstractmethod
    def perform_divination(self, data: dict) -> Generator[str, None, None]:
        """执行占卜，流式返回结果"""
        pass


class DivinationFactory:
    """占卜方式工厂"""
    
    _types = {}
    
    @classmethod
    def register(cls, divination_type: str, divination_class: type):
        """注册占卜方式"""
        cls._types[divination_type] = divination_class
    
    @classmethod
    def get_divination(cls, divination_type: str) -> BaseDivination:
        """获取占卜实例"""
        if divination_type not in cls._types:
            raise ValueError(f"不支持的占卜方式: {divination_type}")
        
        return cls._types[divination_type]()
    
    @classmethod
    def get_all_types(cls) -> list:
        """获取所有占卜方式"""
        return [
            {
                'type': type_name,
                'name': cls._types[type_name]().get_name(),
                'description': cls._types[type_name]().get_description()
            }
            for type_name in cls._types.keys()
        ]


# 导入并注册所有占卜方式
from services.divinations.tarot_divination import TarotDivination
from services.divinations.birthday_divination import BirthdayDivination
from services.divinations.dream_divination import DreamDivination

# 注册
DivinationFactory.register('tarot', TarotDivination)
DivinationFactory.register('birthday', BirthdayDivination)
DivinationFactory.register('dream', DreamDivination)

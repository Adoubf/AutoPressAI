#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import List
from zhipuai import ZhipuAI as ZhipuSDK  # 导入SDK并重命名，避免冲突

from config.api_config import ZHIPU_MODEL, CATEGORY_DETECTION_PROMPT, TAG_DETECTION_PROMPT

# 获取logger
logger = logging.getLogger("WordPressPublisher")


class ZhipuAIClient:  # 修改类名避免冲突
    """智普AI API交互类"""
    
    def __init__(self, api_key: str, model: str = None):
        """初始化智普AI API客户端
        
        Args:
            api_key: 智普API密钥
            model: 使用的模型，如未指定则使用配置中的默认模型
        """
        self.api_key = api_key
        self.model = model or ZHIPU_MODEL
        self.client = ZhipuSDK(api_key=api_key)  # 使用重命名后的SDK类
        logger.info(f"已初始化智普AI客户端，使用模型: {self.model}")
    
    def detect_category(self, keyword: str, summary: str, categories: List[str]) -> str:
        """检测文章应该属于哪个分类
        
        Args:
            keyword: 文章关键词
            summary: 文章摘要
            categories: 可选分类列表
            
        Returns:
            最匹配的分类名称
        """
        try:
            # 准备分类判断的prompt
            prompt = CATEGORY_DETECTION_PROMPT.format(
                categories=", ".join(categories),
                keyword=keyword,
                summary=summary
            )
            
            # 使用SDK创建聊天完成请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个帮助内容创作者对文章进行分类的助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.01,  # 使用低温度提高确定性
                max_tokens=50  # 只需要简短回复
            )
            
            # 解析响应
            category_name = response.choices[0].message.content.strip()
            
            # 确保返回的分类在列表中
            if category_name and category_name in categories:
                logger.info(f"AI检测文章分类: '{category_name}'")
                return category_name
            else:
                # 如果返回的分类不在列表中，尝试找到最相似的
                for cat in categories:
                    if cat.lower() in category_name.lower():
                        logger.info(f"AI检测文章分类(近似匹配): '{cat}'")
                        return cat
                        
                logger.warning(f"AI返回的分类 '{category_name}' 不在可选列表中，将使用默认分类")
                return categories[0] if categories else ""
                
        except Exception as e:
            logger.error(f"使用智普AI检测分类时出错: {str(e)}")
            return categories[0] if categories else ""
    
    def detect_tags(self, keyword: str, summary: str, available_tags: List[str]) -> List[str]:
        """检测文章应该使用哪些标签
        
        Args:
            keyword: 文章关键词
            summary: 文章摘要
            available_tags: 可用标签列表
            
        Returns:
            最适合的标签列表（1-3个）
        """
        try:
            # 准备标签检测的prompt
            prompt = TAG_DETECTION_PROMPT.format(
                tags=", ".join(available_tags),
                keyword=keyword,
                summary=summary
            )
            
            # 使用SDK创建聊天完成请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个帮助内容创作者为文章添加标签的助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # 使用低温度提高确定性
                max_tokens=50  # 只需要简短回复
            )
            
            # 解析响应，应该返回格式如 "标签1, 标签2, 标签3"
            tag_text = response.choices[0].message.content.strip()
            
            # 解析返回的标签
            suggested_tags = [tag.strip() for tag in tag_text.split(',') if tag.strip()]
            
            # 过滤出可用的标签
            valid_tags = [tag for tag in suggested_tags if tag in available_tags]
            
            if valid_tags:
                logger.info(f"AI检测文章标签: {', '.join(valid_tags)}")
                return valid_tags
            else:
                # 如果没有有效标签，返回前三个可用标签
                default_tags = available_tags[:min(3, len(available_tags))]
                logger.warning(f"AI返回的标签无效，将使用默认标签: {', '.join(default_tags)}")
                return default_tags
                
        except Exception as e:
            logger.error(f"使用智普AI检测标签时出错: {str(e)}")
            # 出错时返回前三个可用标签
            return available_tags[:min(3, len(available_tags))]

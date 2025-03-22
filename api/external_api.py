#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
from typing import Dict, Any
from urllib.parse import quote

from config.api_config import EXTERNAL_IMAGE_API, EXTERNAL_AI_SEARCH_API

# 获取logger
logger = logging.getLogger("WordPressPublisher")


class ExternalAPI:
    """外部API交互类"""

    def __init__(self):
        """初始化外部API客户端"""
        self.image_api_url = EXTERNAL_IMAGE_API
        self.ai_search_api_url = EXTERNAL_AI_SEARCH_API

    def get_featured_image(self, width: int = 960, height: int = 540) -> Dict[str, Any]:
        """获取特色图片
        
        Args:
            width: 图片宽度
            height: 图片高度
            
        Returns:
            包含图片URL的字典
        """
        try:
            params = {
                'width': width,
                'height': height,
                'type': 'json'
            }
            response = requests.get(self.image_api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if (data.get('code') == 200):
                logger.info(f"成功获取特色图片: {data.get('imgurl')}")
                return {'url': data.get('imgurl'), 'success': True}
            else:
                logger.warning(f"获取特色图片失败: {data.get('msg')}")
                return {'success': False, 'error': data.get('msg')}

        except Exception as e:
            logger.error(f"获取特色图片时出错: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_article_content(self, keyword: str) -> Dict[str, Any]:
        """使用AI搜索API获取文章内容
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            包含文章内容的字典
        """
        try:
            params = {'keyword': quote(keyword)}
            response = requests.get(self.ai_search_api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 200:
                logger.info(f"成功获取关键词'{keyword}'的文章内容")
                return {
                    'success': True,
                    'keyword': keyword,
                    'text': data.get('data', {}).get('text', ''),
                    'related_questions': data.get('data', {}).get('related_questions', []),
                    'sources': data.get('data', {}).get('sources', [])
                }
            else:
                logger.warning(f"获取文章内容失败: {data.get('msg')}")
                return {'success': False, 'error': data.get('msg')}

        except Exception as e:
            logger.error(f"获取文章内容时出错: {str(e)}")
            return {'success': False, 'error': str(e)}

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from typing import Dict, List, Any, Optional

# 导入自定义模块
from api.api_client import WordPressAPI, ExternalAPI, ZhipuAI
from utils.content_formatter import ContentFormatter
from config.config_manager import convert_taxonomy_names_to_ids

# 获取logger
logger = logging.getLogger("WordPressPublisher")


class WordPressPublisher:
    """WordPress自动发布文章类"""

    def __init__(self, config: Dict[str, Any]):
        """初始化WordPress发布器
        
        Args:
            config: 配置字典，包含WordPress站点信息和API密钥
        """
        self.wp_url = config.get('wp_url')
        self.wp_username = config.get('wp_username')
        self.wp_password = config.get('wp_password')
        
        # 初始化API客户端
        self.wp_api = WordPressAPI(self.wp_url, self.wp_username, self.wp_password)
        self.external_api = ExternalAPI()
        
        # 验证WordPress连接
        self.wp_api.validate_connection()
        
        # 转换分类和标签名称为ID
        updated_config = convert_taxonomy_names_to_ids(config, self.wp_api)
        
        # 分类和标签
        self.categories = updated_config.get('categories', [])
        self.tags = updated_config.get('tags', [])
        self.category_names = config.get('category_names', [])
        
        # 如果启用了智普AI
        self.use_zhipu_ai = config.get('use_zhipu_ai', False)
        if self.use_zhipu_ai:
            self.zhipu_api = ZhipuAI(config.get('zhipu_api_key', ''))
            logger.info("已启用智普AI自动分类功能")
        else:
            self.zhipu_api = None

    def auto_publish_article(self, keyword: str) -> Dict[str, Any]:
        """自动发布文章的完整流程
        
        Args:
            keyword: 文章关键词
            
        Returns:
            包含发布结果的字典
        """
        # 1. 获取文章内容
        content_data = self.external_api.get_article_content(keyword)
        if not content_data.get('success'):
            return {'success': False, 'error': f"获取文章内容失败: {content_data.get('error')}"}

        # 2. 格式化文章内容
        formatted_article = ContentFormatter.format_article_content(content_data)
        if not formatted_article.get('title') or not formatted_article.get('content'):
            return {'success': False, 'error': "格式化文章内容失败"}
            
        # 3. 使用智普AI自动判断分类（如果启用）
        article_categories = self.categories.copy()
        if self.use_zhipu_ai and self.zhipu_api and self.category_names:
            # 从文章内容中提取摘要（取前200个字符）
            summary = content_data.get('text', '')[:200]
            
            # 使用AI判断分类
            category_name = self.zhipu_api.detect_category(keyword, summary, self.category_names)
            
            # 获取分类ID并添加到文章分类中
            if category_name:
                category_id = self.wp_api.get_category_id_by_name(category_name)
                if category_id and category_id not in article_categories:
                    article_categories.append(category_id)
                    logger.info(f"AI分配的分类: {category_name} (ID: {category_id})")

        # 4. 获取特色图片
        image_data = self.external_api.get_featured_image()
        if not image_data.get('success'):
            logger.warning(f"获取特色图片失败: {image_data.get('error')}，将继续发布文章但没有特色图片")
            featured_media_id = None
        else:
            # 5. 上传特色图片
            media_data = self.wp_api.upload_media(image_data.get('url'))
            if not media_data.get('success'):
                logger.warning(f"上传特色图片失败: {media_data.get('error')}，将继续发布文章但没有特色图片")
                featured_media_id = None
            else:
                featured_media_id = media_data.get('media_id')

        # 6. 发布文章
        publish_result = self.wp_api.publish_post(
            title=formatted_article.get('title'),
            content=formatted_article.get('content'),
            categories=article_categories,
            tags=self.tags,
            featured_media_id=featured_media_id
        )

        return publish_result

    def batch_publish_articles(self, keywords: List[str], delay_seconds: int = 300) -> List[Dict[str, Any]]:
        """批量发布多篇文章
        
        Args:
            keywords: 关键词列表
            delay_seconds: 发布间隔时间（秒）
            
        Returns:
            包含所有发布结果的列表
        """
        results = []

        for i, keyword in enumerate(keywords):
            logger.info(f"开始发布第 {i + 1}/{len(keywords)} 篇文章，关键词: {keyword}")

            # 发布文章
            result = self.auto_publish_article(keyword)
            results.append({
                'keyword': keyword,
                'result': result
            })

            # 不是最后一篇文章时，等待指定时间
            if i < len(keywords) - 1 and delay_seconds > 0:
                logger.info(f"等待 {delay_seconds} 秒后发布下一篇文章...")
                time.sleep(delay_seconds)

        return results
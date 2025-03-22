#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import logging
import io
import json
from typing import Dict, Any, Optional, Tuple, List
from urllib.parse import quote

# 导入API配置
from config.api_config import (
    WP_API_BASE_PATH, EXTERNAL_IMAGE_API, EXTERNAL_AI_SEARCH_API,
    ZHIPU_API_URL, CATEGORY_DETECTION_PROMPT, get_headers
)

# 获取logger
logger = logging.getLogger("WordPressPublisher")


class WordPressAPI:
    """WordPress API交互类"""

    def __init__(self, wp_url: str, wp_username: str, wp_password: str):
        """初始化WordPress API客户端
        
        Args:
            wp_url: WordPress站点URL
            wp_username: WordPress用户名
            wp_password: WordPress密码
        """
        self.wp_url = wp_url
        self.wp_username = wp_username
        self.wp_password = wp_password
        self.wp_api_url = f"{self.wp_url}{WP_API_BASE_PATH}"
        self.session = requests.Session()
        self.session.auth = (self.wp_username, self.wp_password)

        # 缓存分类和标签数据
        self._categories_cache = None
        self._tags_cache = None

    def validate_connection(self) -> bool:
        """验证WordPress API连接
        
        Returns:
            连接是否成功
        """
        try:
            response = self.session.get(f"{self.wp_api_url}/users/me")
            response.raise_for_status()
            logger.info(f"成功连接到WordPress站点: {self.wp_url}")
            return True
        except Exception as e:
            logger.error(f"无法连接到WordPress API: {str(e)}")
            raise ConnectionError(f"WordPress API连接失败: {str(e)}")

    def upload_media(self, image_url: str) -> Dict[str, Any]:
        """上传媒体文件到WordPress
        
        Args:
            image_url: 图片URL
            
        Returns:
            包含媒体ID的字典
        """
        try:
            # 下载图片
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # 尝试将图片转换为WebP格式
            webp_image, webp_success = self._convert_to_webp(image_response.content)

            if webp_success:
                # 尝试上传WebP格式
                result = self._perform_upload(webp_image, 'webp')
                if result.get('success'):
                    return result
                else:
                    logger.warning("WebP格式上传失败，尝试使用原始格式")

            # 如果WebP转换失败或上传失败，使用原始格式
            # 从URL推断原始格式
            original_extension = image_url.split('.')[-1].lower()
            if original_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                original_extension = 'jpg'  # 默认假设为jpg

            return self._perform_upload(image_response.content, original_extension)

        except Exception as e:
            logger.error(f"上传特色图片时出错: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _convert_to_webp(self, image_data: bytes) -> Tuple[bytes, bool]:
        """将图片转换为WebP格式
        
        Args:
            image_data: 原始图片数据
            
        Returns:
            元组(WebP图片数据, 是否成功)
        """
        try:
            # 需要安装Pillow库: pip install Pillow
            from PIL import Image

            # 从二进制数据创建图像对象
            img = Image.open(io.BytesIO(image_data))

            # 转换为RGB模式（去除透明通道，如果有）
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
                background = Image.new('RGBA', img.size, (255, 255, 255))
                img = Image.alpha_composite(background, img).convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 保存为WebP格式
            output = io.BytesIO()
            img.save(output, format='WEBP', quality=85)
            webp_data = output.getvalue()

            logger.info("成功将图片转换为WebP格式")
            return webp_data, True

        except Exception as e:
            logger.warning(f"转换图片为WebP格式失败: {str(e)}")
            return image_data, False

    def _perform_upload(self, image_data: bytes, extension: str) -> Dict[str, Any]:
        """执行媒体上传
        
        Args:
            image_data: 图片二进制数据
            extension: 文件扩展名（不含点）
            
        Returns:
            包含上传结果的字典
        """
        try:
            # 生成文件名
            file_name = f"featured-image-{int(time.time())}.{extension}"

            # 设置Content-Type
            content_type = f'image/{extension}'
            if extension == 'jpg':
                content_type = 'image/jpeg'

            # 上传到WordPress
            headers = {
                'Content-Disposition': f'attachment; filename="{file_name}"',
                'Content-Type': content_type,
            }

            upload_response = self.session.post(
                f"{self.wp_api_url}/media",
                data=image_data,
                headers=headers
            )
            upload_response.raise_for_status()

            media_data = upload_response.json()
            media_id = media_data.get('id')

            if media_id:
                logger.info(f"成功上传特色图片（{extension}格式），媒体ID: {media_id}")
                return {'success': True, 'media_id': media_id}
            else:
                logger.warning(f"上传特色图片（{extension}格式）失败，未获取到媒体ID")
                return {'success': False, 'error': '未获取到媒体ID'}

        except Exception as e:
            logger.error(f"上传媒体（{extension}格式）时出错: {str(e)}")
            return {'success': False, 'error': str(e)}

    def publish_post(self, title: str, content: str, categories: list = None,
                     tags: list = None, featured_media_id: Optional[int] = None) -> Dict[str, Any]:
        """发布文章到WordPress
        
        Args:
            title: 文章标题
            content: 文章内容（HTML格式）
            categories: 分类ID列表
            tags: 标签ID列表
            featured_media_id: 特色图片ID
            
        Returns:
            包含发布状态的字典
        """
        try:
            post_data = {
                'title': title,
                'content': content,
                'status': 'publish',
            }

            # 添加特色图片
            if featured_media_id:
                post_data['featured_media'] = featured_media_id

            # 添加分类和标签
            if categories:
                post_data['categories'] = categories
            if tags:
                post_data['tags'] = tags

            response = self.session.post(f"{self.wp_api_url}/posts", json=post_data)
            response.raise_for_status()

            post_data = response.json()
            post_id = post_data.get('id')
            post_link = post_data.get('link')

            if post_id:
                logger.info(f"成功发布文章，ID: {post_id}, 链接: {post_link}")
                return {'success': True, 'post_id': post_id, 'post_link': post_link}
            else:
                logger.warning("发布文章失败，未获取到文章ID")
                return {'success': False, 'error': '未获取到文章ID'}

        except Exception as e:
            logger.error(f"发布文章时出错: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_categories(self) -> List[Dict[str, Any]]:
        """获取所有分类
        
        Returns:
            分类列表，每个分类包含id, name等信息
        """
        if self._categories_cache is not None:
            return self._categories_cache

        try:
            response = self.session.get(f"{self.wp_api_url}/categories", params={"per_page": 100})
            response.raise_for_status()
            self._categories_cache = response.json()
            logger.info(f"成功获取分类列表，共 {len(self._categories_cache)} 个")
            return self._categories_cache
        except Exception as e:
            logger.error(f"获取分类列表失败: {str(e)}")
            return []

    def get_tags(self) -> List[Dict[str, Any]]:
        """获取所有标签
        
        Returns:
            标签列表，每个标签包含id, name等信息
        """
        if self._tags_cache is not None:
            return self._tags_cache

        try:
            response = self.session.get(f"{self.wp_api_url}/tags", params={"per_page": 100})
            response.raise_for_status()
            self._tags_cache = response.json()
            logger.info(f"成功获取标签列表，共 {len(self._tags_cache)} 个")
            return self._tags_cache
        except Exception as e:
            logger.error(f"获取标签列表失败: {str(e)}")
            return []

    def get_category_id_by_name(self, name: str) -> Optional[int]:
        """根据分类名称获取ID
        
        Args:
            name: 分类名称
            
        Returns:
            分类ID，如果未找到返回None
        """
        categories = self.get_categories()
        for category in categories:
            if category.get('name').lower() == name.lower():
                return category.get('id')
        return None

    def get_tag_id_by_name(self, name: str) -> Optional[int]:
        """根据标签名称获取ID
        
        Args:
            name: 标签名称
            
        Returns:
            标签ID，如果未找到返回None
        """
        tags = self.get_tags()
        for tag in tags:
            if tag.get('name').lower() == name.lower():
                return tag.get('id')
        return None

    def create_category_if_not_exists(self, name: str) -> int:
        """创建分类，如果不存在
        
        Args:
            name: 分类名称
            
        Returns:
            分类ID
        """
        # 先检查是否已存在
        category_id = self.get_category_id_by_name(name)
        if category_id:
            return category_id

        try:
            # 创建新分类
            response = self.session.post(
                f"{self.wp_api_url}/categories",
                json={"name": name}
            )
            response.raise_for_status()
            new_category = response.json()
            logger.info(f"成功创建分类 '{name}'，ID: {new_category.get('id')}")

            # 刷新缓存
            self._categories_cache = None

            return new_category.get('id')
        except Exception as e:
            logger.error(f"创建分类 '{name}' 失败: {str(e)}")
            return 1  # 返回默认分类ID

    def create_tag_if_not_exists(self, name: str) -> int:
        """创建标签，如果不存在
        
        Args:
            name: 标签名称
            
        Returns:
            标签ID
        """
        # 先检查是否已存在
        tag_id = self.get_tag_id_by_name(name)
        if tag_id:
            return tag_id

        try:
            # 创建新标签
            response = self.session.post(
                f"{self.wp_api_url}/tags",
                json={"name": name}
            )
            response.raise_for_status()
            new_tag = response.json()
            logger.info(f"成功创建标签 '{name}'，ID: {new_tag.get('id')}")

            # 刷新缓存
            self._tags_cache = None

            return new_tag.get('id')
        except Exception as e:
            logger.error(f"创建标签 '{name}' 失败: {str(e)}")
            return None


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


class ZhipuAI:
    """智普AI API交互类"""

    def __init__(self, api_key: str, model: str = "glm-4-flash"):
        """初始化智普AI API客户端
        
        Args:
            api_key: 智普API密钥
            model: 使用的模型
        """
        self.api_key = api_key
        self.model = model
        self.api_url = ZHIPU_API_URL

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

            # 构建请求数据
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个帮助内容创作者对文章进行分类的助手。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.01,  # 使用低温度提高确定性
                "max_tokens": 50  # 只需要简短回复
            }

            # 获取请求头
            headers = get_headers(self.api_key)

            # 发送请求
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            # 解析响应
            result = response.json()
            category_name = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            # 确保返回的分类在列表中
            if category_name and category_name in categories:
                logger.info(f"AI检测文章分类: '{category_name}'")
                return category_name
            else:
                # 如果返回的分类不在列表中，尝试找到最相似的
                for cat in categories:
                    if cat.lower() in category_name.lower():
                        return cat

                logger.warning(f"AI返回的分类 '{category_name}' 不在可选列表中，将使用默认分类")
                return categories[0] if categories else ""

        except Exception as e:
            logger.error(f"使用智普AI检测分类时出错: {str(e)}")
            return categories[0] if categories else ""

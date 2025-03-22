#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""API配置文件"""

# WordPress API配置
WP_API_BASE_PATH = "/wp-json/wp/v2"

# 外部API配置
EXTERNAL_IMAGE_API = "https://api.pearktrue.cn/api/thumbnail/"
EXTERNAL_AI_SEARCH_API = "https://api.pearktrue.cn/api/aisearch/"

# 智普AI模型配置
ZHIPU_MODEL = "glm-4-flash"  # 默认使用的模型

# 分类判断Prompt模板
CATEGORY_DETECTION_PROMPT = """
你是一个专业的内容分类专家，请根据以下文章主题和摘要，判断该文章应该归类到哪个分类。

可选分类：{categories}

文章主题：{keyword}
文章摘要：{summary}

请只返回一个最适合的分类名称，不要添加任何解释或额外文字。
"""

# 标签检测Prompt模板
TAG_DETECTION_PROMPT = """
你是一个专业的内容标记专家，请根据以下文章主题和摘要，为文章选择1到3个最合适的标签。

可选标签：{tags}

文章主题：{keyword}
文章摘要：{summary}

请直接返回标签名称，用逗号分隔，不要添加任何解释或额外文字。例如：标签1, 标签2
"""

# 注意：由于使用官方SDK，不再需要自己生成JWT token
# 这个函数已不再使用，但保留为向后兼容
def get_headers(api_key):
    """已弃用的函数，保留为兼容性"""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

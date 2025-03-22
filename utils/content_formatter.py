#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Any
import os
import sys

# 添加项目根目录到系统路径，确保导入能正确工作
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入格式化函数
from utils.formatters.article_formatter import format_article_content as format_article
from utils.formatters.paragraph_formatter import format_paragraphs
from utils.formatters.question_formatter import format_related_questions
from utils.formatters.source_formatter import format_sources


class ContentFormatter:
    """文章内容格式化类"""

    @staticmethod
    def format_article_content(content_data: Dict[str, Any]) -> Dict[str, str]:
        """格式化文章内容，使用HTML进行排版
        
        Args:
            content_data: 从AI搜索API获取的内容数据
            
        Returns:
            包含格式化标题和内容的字典
        """
        # 使用导入的格式化函数处理内容
        return format_article(
            content_data,
            ContentFormatter._format_paragraphs,
            ContentFormatter._format_related_questions,
            ContentFormatter._format_sources
        )

    @staticmethod
    def _format_paragraphs(text: str, content_data: Dict[str, Any] = None) -> str:
        """将文本分段并添加HTML标签，同时将Markdown格式转换为HTML格式"""
        return format_paragraphs(text, content_data)

    @staticmethod
    def _format_related_questions(questions: List[str]) -> str:
        """格式化相关问题，添加现代化UI样式"""
        return format_related_questions(questions)

    @staticmethod
    def _format_sources(sources: List[Dict[str, str]]) -> str:
        """格式化信息来源，使用纯CSS实现手风琴效果"""
        return format_sources(sources)
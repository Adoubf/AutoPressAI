#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Dict, Any


def format_paragraphs(text: str, content_data: Dict[str, Any] = None) -> str:
    """将文本分段并添加HTML标签，同时将Markdown格式转换为HTML格式
    
    Args:
        text: 要格式化的文本内容
        content_data: 包含来源等信息的数据字典
    
    Returns:
        格式化后的HTML内容
    """
    if not text:
        return '<p>暂无相关内容</p>'

    # 添加现代化CSS样式 - Bootstrap/Tailwind风格的现代极简设计
    formatted_text = '''
    <style>
    .article-main-content {
        margin: 30px 0;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        line-height: 1.6;
    }
    .article-main-content p {
        margin-bottom: 15px;
        color: #7A7A7A;
        font-size: 16px;
    }
    .article-main-content h2 {
        font-size: 24px;
        color: #002147;
        margin: 25px 0 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #EDEDED;
    }
    .article-main-content h3 {
        font-size: 20px;
        color: #002147;
        margin: 20px 0 10px;
    }
    .article-main-content strong {
        color: #F04641;
        font-weight: 600;
    }
    .article-main-content ul, .article-main-content ol {
        margin-left: 20px;
        margin-bottom: 15px;
    }
    .article-main-content li {
        margin-bottom: 8px;
        color: #7A7A7A;
    }
    .article-main-content sup {
        color: #F04641;
        font-weight: bold;
    }
    .article-main-content sup a {
        text-decoration: none;
        color: #F04641;
    }
    .article-main-content sup a:hover {
        text-decoration: underline;
    }
    @media (max-width: 768px) {
        .article-main-content {
            padding: 15px;
            margin: 15px 0;
        }
    }
    </style>
    '''

    # 替换Markdown标题为HTML标题
    text = re.sub(r'##\s+(.+)', r'<h2>\1</h2>', text)
    text = re.sub(r'###\s+(.+)', r'<h3>\1</h3>', text)

    # 替换Markdown加粗为HTML加粗
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # 替换Markdown列表项为HTML列表项
    text = re.sub(r'^–\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)

    # 检测并包装列表项
    if re.search(r'<li>.+</li>', text):
        # 如果有列表项但没有被ul包围，添加ul标签
        if not re.search(r'<ul>.*<li>', text):
            text = re.sub(r'(<li>.*</li>\n*)+', r'<ul>\n\g<0></ul>', text, flags=re.DOTALL)

    # 处理引用标记[数字]为上标，并添加链接功能
    # 首先收集所有引用标记和对应的来源链接
    reference_links = {}
    for i, source in enumerate(content_data.get('sources', []), 1):
        if source.get('link'):
            reference_links[str(i)] = source.get('link')

    # 处理引用标记[数字]为带链接的上标
    def add_reference_link(match):
        ref_num = match.group(1)
        if ref_num in reference_links:
            return f'<sup><a href="{reference_links[ref_num]}" target="_blank">[{ref_num}]</a></sup>'
        else:
            return f'<sup>[{ref_num}]</sup>'

    text = re.sub(r'\[(\d+)\]', add_reference_link, text)

    paragraphs = text.split('\n')

    for para in paragraphs:
        if para.strip():
            # 如果是HTML标签，直接添加
            if re.match(r'^<[^>]+>', para.strip()):
                formatted_text += para.strip() + '\n'
            # 否则包装为段落
            elif not para.strip().startswith('<li>') and not para.strip().startswith(
                    '<ul>') and not para.strip().startswith('</ul>'):
                formatted_text += f'<p>{para.strip()}</p>\n'
            else:
                formatted_text += para.strip() + '\n'

    return formatted_text

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Any
from datetime import datetime


def format_article_content(content_data: Dict[str, Any], 
                           format_paragraphs, 
                           format_related_questions, 
                           format_sources) -> Dict[str, str]:
    """格式化文章内容，使用HTML进行排版
    
    Args:
        content_data: 从AI搜索API获取的内容数据
        format_paragraphs: 段落格式化函数
        format_related_questions: 相关问题格式化函数
        format_sources: 来源格式化函数
        
    Returns:
        包含格式化标题和内容的字典
    """
    if not content_data.get('success'):
        return {'title': '', 'content': ''}

    keyword = content_data.get('keyword', '')
    main_text = content_data.get('text', '')
    related_questions = content_data.get('related_questions', [])
    sources = content_data.get('sources', [])

    # 生成标题
    title = f"{keyword} - 最新详细信息"

    # 使用HTML格式化内容
    html_content = f'''
    <style>
    .article-container {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }}
    .article-footer {{
        margin-top: 40px;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.03);
    }}
    .article-footer p {{
        margin: 5px 0;
        color: #7A7A7A;
        font-size: 14px;
    }}
    .article-footer .timestamp {{
        font-weight: 500;
        color: #F04641;
    }}
    .article-divider {{
        height: 3px;
        background: linear-gradient(to right, #F04641, #EDEDED, #002147);
        margin: 30px 0;
        border-radius: 3px;
    }}
    @media (max-width: 768px) {{
        .article-container {{
            padding: 15px;
        }}
        .article-footer {{
            margin-top: 30px;
            padding: 15px;
        }}
    }}
    </style>
    <div class="article-container">
        <div class="article-main-content">
            {format_paragraphs(main_text, content_data)}
        </div>
        
        <div class="article-divider"></div>
        
        {format_related_questions(related_questions)}
        
        <div class="article-divider"></div>
        
        {format_sources(sources)}
        
        <div class="article-footer">
            <p>本文由AI自动生成，内容仅供参考。</p>
            <p class="timestamp">发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    '''

    return {'title': title, 'content': html_content}

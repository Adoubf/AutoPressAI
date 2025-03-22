#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict


def format_sources(sources: List[Dict[str, str]]) -> str:
    """格式化信息来源，使用纯CSS实现手风琴效果，确保在WordPress环境中正常工作
    
    Args:
        sources: 信息来源列表
        
    Returns:
        格式化后的HTML内容
    """
    if not sources:
        return ''

    # 添加纯CSS样式实现手风琴效果
    html = '''
    <style>
    .article-sources {
        margin: 30px 0;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .article-sources h3 {
        color: #002147;
        font-size: 22px;
        margin-bottom: 15px; /* 减小标题底部间距 */
        padding-bottom: 10px;
        border-bottom: 2px solid #F04641;
        position: relative;
    }
    .article-sources h3:after {
        content: "";
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 80px;
        height: 2px;
        background-color: #002147;
    }
    /* 纯CSS手风琴样式 */
    .accordion {
        margin-bottom: 5px; /* 减少手风琴之间的间距 */
        position: relative;
        line-height: 1.2; /* 控制行高 */
        height: auto; /* 让高度自适应内容 */
    }
    /* 隐藏原始复选框 */
    .accordion-checkbox {
        position: absolute;
        opacity: 0;
        z-index: -1;
    }
    /* 手风琴标题样式 */
    .accordion-header {
        background-color: #f8f8f8;
        border-radius: 8px;
        padding: 10px 12px; /* 减小内边距 */
        cursor: pointer;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-height: 24px; /* 设置最小高度 */
    }
    .accordion-header:hover {
        background-color: #f0f0f0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    .accordion-title {
        font-weight: bold;
        font-size: 15px; /* 减小字体 */
        color: #002147;
        flex-grow: 1;
        margin: 0; /* 移除标题边距 */
        line-height: 1.3; /* 控制行高 */
    }
    .accordion-icon {
        width: 16px; /* 减小图标尺寸 */
        height: 16px;
        position: relative;
        flex-shrink: 0; /* 防止图标被压缩 */
        margin-left: 8px;
    }
    .accordion-icon:before,
    .accordion-icon:after {
        content: '';
        position: absolute;
        background-color: #F04641;
        transition: all 0.3s ease-in-out;
    }
    .accordion-icon:before {
        top: 7px;
        left: 0;
        width: 100%;
        height: 2px;
    }
    .accordion-icon:after {
        top: 0;
        left: 7px;
        width: 2px;
        height: 100%;
    }
    /* 手风琴内容样式 */
    .accordion-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-in-out, opacity 0.2s ease-in-out, transform 0.2s ease-in-out;
        background-color: white;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        opacity: 0;
        transform: translateY(-10px);
        margin-top: -2px; /* 减少间隙 */
    }
    .accordion-inner {
        padding: 10px; /* 减小内边距 */
    }
    /* 使用:checked伪类控制手风琴状态 */
    .accordion-checkbox:checked ~ .accordion-content {
        max-height: 200px; /* 减小展开后的最大高度 */
        opacity: 1;
        transform: translateY(0);
    }
    .accordion-checkbox:checked ~ .accordion-header .accordion-icon {
        transform: rotate(45deg);
    }
    .accordion-snippet {
        color: #7A7A7A;
        margin-bottom: 10px; /* 减小段落间距 */
        font-size: 13px; /* 减小字体 */
        line-height: 1.4;
        max-height: 80px; /* 控制摘要最大高度 */
        overflow: hidden; /* 超出部分隐藏 */
        display: -webkit-box;
        -webkit-line-clamp: 3; /* 限制显示3行 */
        -webkit-box-orient: vertical;
        text-overflow: ellipsis; /* 添加省略号 */
    }
    .source-link-btn {
        display: block;
        width: 100%;
        padding: 8px 15px; /* 减小按钮内边距 */
        background-color: #F04641;
        color: white;
        text-decoration: none;
        border-radius: 6px;
        font-size: 13px; /* 减小字体 */
        font-weight: 500;
        transition: all 0.3s ease;
        text-align: center;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(240,70,65,0.2);
        margin-top: 0; /* 移除上边距 */
    }
    .source-link-btn:hover {
        background-color: #d83a35;
        box-shadow: 0 4px 8px rgba(240,70,65,0.3);
        transform: translateY(-2px);
    }
    .source-link-btn:active {
        transform: translateY(0);
        box-shadow: 0 2px 3px rgba(240,70,65,0.2);
    }
    /* 响应式设计 */
    @media (max-width: 768px) {
        .article-sources {
            padding: 15px;
            margin: 20px 0;
        }
        .accordion-header {
            padding: 8px 10px;
        }
        .accordion-inner {
            padding: 8px;
        }
    }
    </style>
    '''

    html += '<div class="article-sources">\n'
    html += '<h3>信息来源</h3>\n'

    for i, source in enumerate(sources):
        title = source.get('title', '')
        link = source.get('link', '')
        snippet = source.get('snippet', '')

        if title and link:
            html += f'<div class="accordion" id="source-{i+1}">\n'
            html += f'  <input type="checkbox" class="accordion-checkbox" id="accordion-{i+1}">\n'
            html += f'  <label class="accordion-header" for="accordion-{i+1}">\n'
            html += f'    <span class="accordion-title">{title}</span>\n'
            html += f'    <span class="accordion-icon"></span>\n'
            html += f'  </label>\n'
            html += f'  <div class="accordion-content">\n'
            html += f'    <div class="accordion-inner">\n'
            
            if snippet:
                # 摘要已经通过CSS控制为3行显示，超出部分隐藏并显示省略号
                html += f'      <div class="accordion-snippet">{snippet}</div>\n'
            
            html += f'      <a href="{link}" target="_blank" class="source-link-btn">查看原文</a>\n'
            html += f'    </div>\n'
            html += f'  </div>\n'
            html += f'</div>\n'

    html += '</div>\n'

    return html

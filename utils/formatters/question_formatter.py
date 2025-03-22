#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List


def format_related_questions(questions: List[str]) -> str:
    """格式化相关问题，添加现代化UI样式
    
    Args:
        questions: 相关问题列表
        
    Returns:
        格式化后的HTML内容
    """
    if not questions:
        return ''

    # 添加现代极简CSS样式 - 使用指定的颜色方案
    html = '''
    <style>
    .related-questions {
        margin: 30px 0;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .related-questions h3 {
        color: #002147;
        font-size: 22px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #F04641;
        position: relative;
    }
    .related-questions h3:after {
        content: "";
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 80px;
        height: 2px;
        background-color: #002147;
    }
    .questions-list {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .question-item {
        background-color: #f8f8f8;
        margin-bottom: 12px;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        padding-left: 30px;
        color: #7A7A7A;
    }
    .question-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .question-item:before {
        content: "?";
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        background-color: #F04641;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
    }
    /* 响应式设计 */
    @media (max-width: 768px) {
        .related-questions {
            padding: 15px;
            margin: 20px 0;
        }
        .question-item {
            padding: 12px 12px 12px 30px;
        }
    }
    </style>
    '''

    html += '<div class="related-questions">\n'
    html += '<h3>相关问题</h3>\n'
    html += '<ul class="questions-list">\n'

    for question in questions:
        html += f'<li class="question-item">{question}</li>\n'

    html += '</ul>\n'
    html += '</div>\n'

    return html

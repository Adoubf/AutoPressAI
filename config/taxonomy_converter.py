#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Dict, Any

# 获取logger
logger = logging.getLogger("WordPressPublisher")


def convert_taxonomy_names_to_ids(config: Dict[str, Any], wp_api) -> Dict[str, Any]:
    """将分类和标签名称转换为ID
    
    Args:
        config: 配置字典
        wp_api: WordPress API客户端实例
        
    Returns:
        更新后的配置字典
    """
    updated_config = config.copy()
    
    # 处理分类
    if 'category_names' in config:
        category_ids = []
        for category_name in config['category_names']:
            # 自动创建不存在的分类
            category_id = wp_api.create_category_if_not_exists(category_name)
            if category_id:
                category_ids.append(category_id)
        
        updated_config['categories'] = category_ids
    
    # 处理标签
    if 'tag_names' in config:
        tag_ids = []
        for tag_name in config['tag_names']:
            # 自动创建不存在的标签
            tag_id = wp_api.create_tag_if_not_exists(tag_name)
            if tag_id:
                tag_ids.append(tag_id)
        
        updated_config['tags'] = tag_ids
    
    return updated_config

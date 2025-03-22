#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
from typing import Dict, Any, List, Union

# 获取logger
logger = logging.getLogger("WordPressPublisher")


def load_config(config_file: str = 'config.json') -> Dict[str, Any]:
    """加载配置文件
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        # 处理相对路径
        if not os.path.isabs(config_file):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_file = os.path.join(base_dir, config_file)
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"成功加载配置文件: {config_file}")
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        raise ValueError(f"无法加载配置文件: {str(e)}")


def validate_config(config: Dict[str, Any]) -> bool:
    """验证配置是否包含必要字段
    
    Args:
        config: 配置字典
        
    Returns:
        配置是否有效
    """
    required_fields = ['wp_url', 'wp_username', 'wp_password']
    
    for field in required_fields:
        if not config.get(field):
            logger.error(f"配置缺少必要字段: {field}")
            return False
    
    # 验证智普API配置
    if config.get('use_zhipu_ai', False) and not config.get('zhipu_api_key'):
        logger.error("启用了智普AI但未提供API密钥")
        return False
        
    return True


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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Dict, Any

# 获取logger
logger = logging.getLogger("WordPressPublisher")


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

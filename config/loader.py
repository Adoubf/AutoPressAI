#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
from typing import Dict, Any

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

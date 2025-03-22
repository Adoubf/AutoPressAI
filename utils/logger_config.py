#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import os
from datetime import datetime

def setup_logger(logger_name="WordPressPublisher", log_level=logging.INFO):
    """设置日志记录器
    
    Args:
        logger_name: 日志记录器名称
        log_level: 日志级别
        
    Returns:
        已配置的日志记录器
    """
    # 创建日志文件夹
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # 创建logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    # 移除现有处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # 创建文件处理器 - 使用时间戳确保每次运行创建新文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"wordpress_publisher_{timestamp}.log")
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(log_level)
    
    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.info(f"日志文件保存在: {log_file_path}")
    
    return logger

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""WordPress自动发布工具主入口"""

import sys
import os
import traceback

# 添加项目根目录到系统路径
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# 创建日志目录
log_dir = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 导入自定义模块
from utils.logger_config import setup_logger
from config.loader import load_config
from config.validator import validate_config
from core.publisher import WordPressPublisher

# 设置日志记录器 - 每次运行创建新的日志文件
logger = setup_logger()


def main():
    """主程序入口"""
    try:
        # 加载配置
        config = load_config()

        # 验证配置
        if not validate_config(config):
            logger.error("配置验证失败，程序退出")
            sys.exit(1)

        # 初始化发布器
        publisher = WordPressPublisher(config)

        # 获取关键词列表
        keywords = config.get('keywords', [])
        if not keywords:
            logger.warning("配置中未找到关键词列表，将使用默认关键词")
            keywords = ["旅游业最新发展"]

        # 获取发布间隔
        publish_interval = config.get('publish_interval', 10)

        # 批量发布文章
        logger.info(f"开始批量发布文章，共 {len(keywords)} 篇，间隔 {publish_interval} 秒")
        results = publisher.batch_publish_articles(keywords, delay_seconds=publish_interval)

        # 统计发布结果
        success_count = sum(1 for item in results if item.get('result', {}).get('success', False))
        logger.info(f"文章发布完成，成功: {success_count}/{len(results)}")

        # 打印发布结果
        for item in results:
            keyword = item.get('keyword', '')
            result = item.get('result', {})
            if result.get('success'):
                print(f"✅ 文章 '{keyword}' 发布成功，链接: {result.get('post_link')}")
            else:
                print(f"❌ 文章 '{keyword}' 发布失败: {result.get('error')}")

    except Exception as e:
        # 增强错误处理，显示完整的堆栈跟踪
        logger.error(f"程序执行出错: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"程序执行出错: {str(e)}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())

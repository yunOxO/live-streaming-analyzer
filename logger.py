import logging

from loguru import logger
import os

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)


def get_logger(name: str):
    """
    为不同的模块创建日志文件
    :param name: 'collector' 或 'processor‘
    """
    log_file = os.path.join(log_dir, f"{name}" + "_{time:YYYY-MM-DD}.log")
    new_logger = logger.bind(module=name)
    # 日志文件：每天一个，保留7天
    new_logger.add(
        log_file,
        rotation='1 day',
        retention='7 days',
        compression='zip',
        encoding='utf-8',
        enqueue=True,         # 确保多线程安全
        )

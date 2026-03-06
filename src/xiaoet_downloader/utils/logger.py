#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Optional


class Logger:
    """日志工具类"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    _indent_level: int = 0
    _indent_size: int = 2
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _get_indent(self) -> str:
        """获取当前缩进字符串"""
        return ' ' * (self._indent_level * self._indent_size)
    
    def _setup_logger(self) -> None:
        """设置日志记录器"""
        self._logger = logging.getLogger('xiaoet_downloader')
        self._logger.setLevel(logging.INFO)
        
        # 避免重复添加处理器
        if self._logger.handlers:
            return
        
        # 创建日志目录
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # 文件处理器
        log_file = os.path.join(log_dir, f'xiaoet_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        """记录信息日志"""
        if self._logger:
            indented_message = self._get_indent() + message
            self._logger.info(indented_message)
    
    def warning(self, message: str) -> None:
        """记录警告日志"""
        if self._logger:
            indented_message = self._get_indent() + message
            self._logger.warning(indented_message)
    
    def error(self, message: str) -> None:
        """记录错误日志"""
        if self._logger:
            indented_message = self._get_indent() + message
            self._logger.error(indented_message)
    
    def debug(self, message: str) -> None:
        """记录调试日志"""
        if self._logger:
            indented_message = self._get_indent() + message
            self._logger.debug(indented_message)
    
    def set_level(self, level: int) -> None:
        """设置日志级别"""
        if self._logger:
            self._logger.setLevel(level)
    
    @contextmanager
    def indent(self):
        """增加缩进级别的上下文管理器"""
        self._indent_level += 1
        try:
            yield
        finally:
            self._indent_level -= 1


# 全局日志实例
logger = Logger()
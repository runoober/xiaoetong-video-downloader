#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class XiaoetConfig:
    """小鹅通配置类"""
    app_id: str
    cookie: str
    product_id: str
    download_dir: str = 'download'
    url: Optional[str] = None
    
    @classmethod
    def from_file(cls, config_path: str) -> 'XiaoetConfig':
        """从配置文件加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
            
            # 如果提供了 URL，尝试解析 app_id 和 product_id
            url = config_data.get('url')
            app_id = config_data.get('app_id', '')
            product_id = config_data.get('product_id', '')
            
            if url:
                parsed_app_id, parsed_product_id = cls._parse_url(url)
                if parsed_app_id and not app_id:
                    app_id = parsed_app_id
                if parsed_product_id and not product_id:
                    product_id = parsed_product_id
            
            return cls(
                app_id=app_id,
                cookie=config_data.get('cookie', ''),
                product_id=product_id,
                download_dir=config_data.get('download_dir', 'download'),
                url=url
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_path} 不存在")
        except json.JSONDecodeError:
            raise ValueError("配置文件内容不是有效的 JSON 格式")
        except Exception as e:
            raise Exception(f"读取配置文件时发生错误: {e}")
    
    @staticmethod
    def _parse_url(url: str) -> tuple[Optional[str], Optional[str]]:
        """
        从 URL 中解析 app_id 和 product_id
        
        Args:
            url: 小鹅通课程 URL，格式如：https://app_id.h5.xet.citv.cn/p/course/ecourse/course_id?l_program=xe_know_pc
        
        Returns:
            (app_id, product_id) 元组
        """
        try:
            # 提取 app_id (从域名中)
            app_id_match = re.search(r'https?://([^.]+)\.h5\.(?:xet\.citv|xiaoeknow)\.cn', url)
            app_id = app_id_match.group(1) if app_id_match else None
            
            # 提取 product_id (从路径中)
            product_id_match = re.search(r'/course_([a-zA-Z0-9]+)', url)
            product_id = f"course_{product_id_match.group(1)}" if product_id_match else None
            
            return app_id, product_id
        except Exception:
            return None, None
    
    def validate(self) -> bool:
        """验证配置是否完整"""
        if not self.app_id:
            raise ValueError("app_id 不能为空")
        if not self.cookie:
            raise ValueError("cookie 不能为空")
        if not self.product_id:
            raise ValueError("product_id 不能为空")
        return True
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'app_id': self.app_id,
            'cookie': self.cookie,
            'product_id': self.product_id,
            'download_dir': self.download_dir,
            'url': self.url
        }
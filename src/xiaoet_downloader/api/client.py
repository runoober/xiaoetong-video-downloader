#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from typing import Dict, List, Tuple, Optional, Any
from ..models.config import XiaoetConfig
from ..models.video import VideoResource


class XiaoetAPIClient:
    """小鹅通API客户端"""
#     子课程列表
# https://appezrn4igg1968.h5.xiaoeknow.com/xe.course.business.avoidlogin.e_course.sub.course.list/1.0.0
#     bizData[course_id]: course_2hrBH6JXlSOjkpCwCMxnqj6g9U4
#     {
#         "code": 0,
#         "msg": "success",
#         "data": [
#             {
#                 "app_id": "appezrn4igg1968",
#                 "p_id": "0",
#                 "course_id": "course_2hrBH6JXlSOjkpCwCMxnqj6g9U4",
#                 "sub_course_id": "subcourse_2hrsJ2rSc3xoRKWwVHClXrECQr9",
#                 "chapter_id": "subcourse_2hrsJ2rSc3xoRKWwVHClXrECQr9",
#                 "chapter_type": 3,
#                 "chapter_title": "视频",
#                 "sub_course_img": "https:\/\/commonresource-1252524126.cdn.xiaoeknow.com\/image\/ltgutnwi03hd.png",
#                 "sort_value": 1,
#                 "chapter_state": 0,
#                 "resource_type": 0,
#                 "task_count": 290,
#                 "section_count": 23
#             }
#         ],
#         "forward_url": ""
#     }

# 获取user_id
# Get https://appezrn4igg1968.h5.xet.citv.cn/xe.course.business.composite_info.get/2.0.0?app_id=appezrn4igg1968
# {
#     "code": 0,
#     "msg": "success",
#     "data": {
#       "user_info": {
#         "is_seal": 0,
#         "black_list": {
#           "permission_visit": 0,
#           "permission_comment": 0,
#           "permission_buy": 0
#         },
#         "user_id": "u_66a7b344522c7_zp1zKFVrBu"
#       },
#       "shop_conf": {
#         "need_comment_check": 1,
#         "relate_sell_info": 1,
#         "is_force_phone": 0,
#         "hide_comment": 0,
#         "is_show_resourcecount": 1,
#         "hide_sub_count": 0,
#         "free_course_login": 0,
#         "goods_comment": 1,
#         "shop_name": "Hollis的小店",
#         "shop_logo": "https://commonresource-1252524126.cdn.xiaoeknow.com/image/lqlzgnlm0q73.jpg"
#       },
#       "version": {
#         "version_type": 4
#       },
#       "view_conf": {
#         "learn_button_hide": 1
#       }
#     },
#     "forward_url": ""
# }

# 最近观看的资源信息
# https://appezrn4igg1968.h5.xet.citv.cn/xe.course.business.e_course.last_learn_resource.get/1.0.0
#     bizData[app_id]: appezrn4igg1968
#     bizData[course_id]: course_2hrBH6JXlSOjkpCwCMxnqj6g9U4
#     {
#         "code": 0,
#         "msg": "success",
#         "data": {
#             "last_learn_course_name": "项目业务介绍",
#             "resource_id": "v_666d104be4b0694c98289082",
#             "resource_type": 3, // 视频  1是图文
#             "jump_url": "\/p\/course\/video\/v_666d104be4b0694c98289082",
#             "sub_course_id": "subcourse_2hrsJ2rSc3xoRKWwVHClXrECQr9"
#         },
#         "forward_url": ""
#     }

# https://appezrn4igg1968.h5.xiaoeknow.com/xe.course.business.avoidlogin.e_course.resource_catalog_list.get/1.0.0
#       {
#         "id": 12425715,
#         "app_id": "appezrn4igg1968",
#         "p_id": "0",
#         "course_id": "course_2hrBH6JXlSOjkpCwCMxnqj6g9U4",
#         "chapter_id": "chap_2htqrCt68nGPCu2BGZ2qtaD5SRf",
#         "resource_id": "chap_2htqrCt68nGPCu2BGZ2qtaD5SRf",
#         "chapter_type": 1,
#         "chapter_title": "项目介绍",
#         "resource_title": "项目介绍",
#         "resource_type": 0,
#         "chapter_state": 0,
#         "sort_value": 2,
#         "unlock_condition": "",
#         "unlock_date": "0001-01-01 00:00:00",
#         "try_length": 0,
#         "is_elective": 0,
#         "sub_course_id": "subcourse_2hrsJ2rSc3xoRKWwVHClXrECQr9",
#         "sub_course_sort_value": 0,
#         "section_num": 8,
#         "try_num": 0,
#         "is_try": 0,
#         "children": [],
#         "sort_c": "",
#         "elective": 8,
#         "unlock_state": 1,
#         "study_status": 1,
#         "learn_progress": 0,
#         "has_breathing_lamp": 0
#       },

# 获取章节详情
# https://appezrn4igg1968.h5.xet.citv.cn/xe.course.business.avoidlogin.e_course.resource_catalog_list.get/1.0.0
    # 获取子课程列表
    GET_SUB_COURSE_URL = "https://{0}.h5.xet.citv.cn/xe.course.business.avoidlogin.e_course.sub.course.list/1.0.0"
    # 获取用户信息
    GET_composite_info_URL = "https://{0}.h5.xet.citv.cn/xe.course.business.composite_info.get/2.0.0"
    # API URL模板
    GET_COLUMN_ITEMS_URL = "https://{0}.h5.xiaoeknow.com/xe.course.business.avoidlogin.e_course.resource_catalog_list.get/1.0.0"
    GET_VIDEO_DETAILS_INFO_URL = "https://{0}.h5.xiaoeknow.com/xe.course.business.video.detail_info.get/2.0.0"
    GET_MICRO_NAVIGATION_URL = "https://{0}.h5.xiaoeknow.com/xe.micro_page.navigation.get/1.0.0"
    GET_PLAY_URL = "https://{0}.h5.xiaoeknow.com/xe.material-center.play/getPlayUrl"
    GET_COURSE_INFO_URL = "https://{0}.h5.xet.citv.cn/xe.course.business.core.info.get/2.0.0"

    def __init__(self, config: XiaoetConfig):
        """初始化API客户端"""
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        })

    def get_micro_navigation_info(self) -> Dict[str, Any]:
        """获取微页面导航信息"""
        url = self.GET_MICRO_NAVIGATION_URL.format(self.config.app_id)
        payload = json.dumps({
            "app_id": self.config.app_id,
            "agent_type": 1,
            "app_version": 0
        })
        headers = {
            'cookie': self.config.cookie,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {})
            return data
        except requests.RequestException as e:
            raise Exception(f"获取导航信息失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析导航信息响应失败: {str(e)}")

    def get_user_id(self) -> str:
        """获取用户ID"""
        url = self.GET_composite_info_URL.format(self.config.app_id)
        headers = {
            'cookie': self.config.cookie,
            'Content-Type': 'application/json'
        }
        params = {
            'app_id': self.config.app_id
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get('data', {})
            user_id = data.get('user_info', {}).get('user_id', '')
            if not user_id:
                raise Exception("未能从响应中获取到user_id")
            return user_id
        except requests.RequestException as e:
            raise Exception(f"获取user_id失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析获取user_id失败: {str(e)}")

    def get_sub_courses(self) -> List[Tuple[str, int]]:
        """获取专栏项目列表"""
        url = self.GET_SUB_COURSE_URL.format(self.config.app_id)
        payload = {
            'bizData[course_id]': self.config.product_id,
        }
        headers = {
            'cookie': self.config.cookie,
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {})
            return [(item.get('sub_course_id'), item.get('section_count')) for item in data]
        except requests.RequestException as e:
            raise Exception(f"获取专栏项目列表失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析专栏项目列表响应失败: {str(e)}")

    def get_column_items(self, column_id: str, sub_course_id: str, p_id=0, page_index: int = 1,
                        page_size: int = 100, sort: str = 'asc') -> List[Tuple[str, str]]:
        """获取专栏项目列表"""
        url = self.GET_COLUMN_ITEMS_URL.format(self.config.app_id)
        payload = {
            'bizData[app_id]': self.config.app_id,
            'bizData[resource_id]': column_id,
            'bizData[course_id]': self.config.product_id,
            'bizData[p_id]': p_id,
            'bizData[order]': sort,
            'bizData[page]': str(page_index),
            'bizData[page_size]': str(page_size),
            'bizData[sub_course_id]': sub_course_id
        }
        headers = {
            'cookie': self.config.cookie,
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {})
            items = data.get('list', [])
            return [(item.get('resource_id'), item.get('resource_title')) for item in items]
        except requests.RequestException as e:
            raise Exception(f"获取专栏项目列表失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析专栏项目列表响应失败: {str(e)}")

    def get_video_detail_info(self, resource_id: str) -> Dict[str, Any]:
        """获取视频详情信息"""
        url = self.GET_VIDEO_DETAILS_INFO_URL.format(self.config.app_id)
        payload = {
            'bizData[resource_id]': resource_id,
            'bizData[product_id]': self.config.product_id,
            'bizData[opr_sys]': 'MacIntel'
        }
        headers = {
            'cookie': self.config.cookie,
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {}).get('video_info', {})
            return data
        except requests.RequestException as e:
            raise Exception(f"获取视频详情失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析视频详情响应失败: {str(e)}")

    def get_play_url(self, user_id: str, play_sign: str) -> Dict[str, Any]:
        """获取播放URL"""
        url = self.GET_PLAY_URL.format(self.config.app_id)
        payload = json.dumps({
            "org_app_id": self.config.app_id,
            "app_id": self.config.app_id,
            "user_id": user_id,
            "play_sign": [play_sign],
            "play_line": "A",
            "opr_sys": "MacIntel"
        })
        headers = {
            'cookie': self.config.cookie,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {})
            play_list_dict = data.get(play_sign, {}).get('play_list', {})
            return play_list_dict
        except requests.RequestException as e:
            raise Exception(f"获取播放URL失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析播放URL响应失败: {str(e)}")

    def get_best_quality_url(self, play_list_dict: Dict[str, Any]) -> Optional[Tuple[str, str]]:
        """获取最佳质量的播放URL"""
        quality_order = ['1080p_hls', '720p_hls', '480p_hls', '360p_hls']

        for quality in quality_order:
            if quality in play_list_dict and play_list_dict.get(quality, {}).get('play_url'):
                return play_list_dict.get(quality, {}).get('play_url'), quality

        return None, None

    def get_course_info(self, resource_id: str) -> Dict[str, Any]:
        """获取课程信息"""
        url = self.GET_COURSE_INFO_URL.format(self.config.app_id)
        payload = {
            'bizData[resource_id]': resource_id,
        }
        headers = {
            'cookie': self.config.cookie,
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get('data', {})
            return data
        except requests.RequestException as e:
            raise Exception(f"获取课程信息失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析课程信息响应失败: {str(e)}")
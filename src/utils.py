"""
    Created by howie.hu at 2024-02-29.
    Description: 一些常用工具
    Changelog: all notable changes to this file will be documented
"""

import hashlib


def md5_encryption(string: str) -> str:
    """
    对字符串进行md5加密
    Args:
        string (str): 加密目标字符串

    Returns:
        str: 加密后字符串
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()

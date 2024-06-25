"""
    Created by howie.hu at 2024-02-29.
    Description: 番剧信息抓取脚本
    Changelog: all notable changes to this file will be documented
"""

import requests

from bs4 import BeautifulSoup


def get_anime_cover(anime_name: str):
    """
    基于 https://www.fre321.com/anime/s 展示结果获取番剧封面
    Args:
        anime_name (str): 番剧名称
    """
    try:
        url = f"https://www.fre321.com/anime/s?query={anime_name}"
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        image = soup.select_one("img.item-cover")
        if image is not None:
            cover_url = image.get("src")
            print(f"获取番剧 {anime_name} 封面: {cover_url}")
        else:
            cover_url = ""
    except Exception as e:
        print(f"获取番剧 {anime_name} 封面失败: {e}")
        cover_url = ""
    return cover_url


if __name__ == "__main__":
    get_anime_cover("女学。～圣女斯克威尔学院～")

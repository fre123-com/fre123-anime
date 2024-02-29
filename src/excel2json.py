"""
    Created by howie.hu at 2024-02-28.
    Description: 处理excel为json
    Command: pipenv run python ./src/excel2json.py
    Changelog: all notable changes to this file will be documented
"""

import json
import os

import pandas as pd
import requests
import urllib3

from src.anime_info import get_anime_cover

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def load_img_url(img_url: str, img_path: str):
    """
    持久化图片到本地
    Args:
        img_url (str): 图片地址
    """
    # 下载前先判断本地路径是否存在
    try:
        if os.path.exists(img_path):
            return True
        else:
            if not img_url.startswith("http"):
                img_url = "https:" + img_url
            response = requests.get(img_url, verify=False, timeout=30)
            response.raise_for_status()
            with open(img_path, "wb") as f:
                f.write(response.content)
                return True
    except Exception as e:
        print(f"图片下载失败：{img_path} \n img_url \n {e}")
        return False


def contains_str(row, str_list):
    """
    在以下列表中添加需要检查的字符串
    """
    # 遍历行中的每个元素
    for item in row:
        # 如果元素是字符串类型，并且包含目标字符串之一
        if isinstance(item, str) and any(s in item for s in str_list):
            return True
    # 如果没有找到任何匹配项，则返回False
    return False


def get_anime_data(year, month):
    """
    获取动画数据
    """

    data_path = os.path.join(os.path.dirname(__file__), "data")
    excel_path = os.path.join(data_path, f"excel/{year}/{month}.xlsx")
    json_path = os.path.join(data_path, f"json/{year}/{month}.json")
    print(f"正在读取： {excel_path}")
    all_sheets = pd.read_excel(excel_path, sheet_name=None, engine="openpyxl")
    anime_data = []
    week_list = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for sheet_name, df in all_sheets.items():
        if "新番表" in sheet_name:
            # 处理新番表数据
            filtered_df = df[
                df.apply(
                    contains_str,
                    str_list=week_list,
                    axis=1,
                )
            ]
            df_cleaned = filtered_df.dropna(axis=1, how="all").dropna(axis=0, how="all")
            for _, row in df_cleaned.iterrows():
                row_list = row.to_list()

                final_row_list = []
                for each in row_list:
                    each = str(each).strip()
                    if each == "nan":
                        each = ""
                    final_row_list.append(each)
                anime_name = final_row_list[0]
                weekday_str = final_row_list[1]
                weekday, play_time = "", final_row_list[2]
                for each in week_list:
                    if each in weekday_str:
                        weekday = each
                        if each != weekday_str:
                            play_time = weekday_str.replace(each, "")

                tags_str = str(final_row_list[-1])
                tags = []
                if "/" in tags_str:
                    for each_tag in tags_str.split("/"):
                        tags.append(each_tag.strip())
                elif "、" in tags_str:
                    for each_tag in tags_str.split("、"):
                        tags.append(each_tag.strip())
                cover_url = get_anime_cover(anime_name)
                img_name = anime_name + "." + cover_url.split(".")[-1]
                img_local_path = f"img/{year}/{month}/{img_name}"

                img_path = os.path.join(data_path, img_local_path)
                is_upload_img_ok = load_img_url(cover_url, img_path)
                row_data = {
                    "anime_name": anime_name,
                    "weekday": weekday,
                    "cover_url": cover_url,
                    "cover_url_git": img_local_path if is_upload_img_ok else "",
                    "play_time": play_time,
                    "play_date": final_row_list[-4],
                    "play_nums": final_row_list[-3],
                    "tags": tags,
                }
                # print(final_row_list)
                # print(row_data)
                anime_data.append(row_data)

    # 聚合

    final_df = pd.DataFrame(anime_data)
    # 按照 weekday 分组
    grouped_df = final_df.groupby("weekday")
    # 创建一个空字典来存储结果
    result = {}

    # 遍历分组后的数据
    for weekday, group_df in grouped_df:
        # 将分组后的数据转换为字典列表
        group_dict_list = group_df.to_dict("records")
        # 将字典列表添加到结果字典中
        result[weekday] = group_dict_list

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == "__main__":
    # 2024 年单独计算
    year, month = 2024, "01"
    get_anime_data(str(year), month)
    # for year in range(2017, 2024):
    #     for month in ["01", "04", "07", "10"]:
    #         get_anime_data(str(year), month)

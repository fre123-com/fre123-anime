"""
    Created by howie.hu at 2024-02-28.
    Description: 处理excel为json
    Changelog: all notable changes to this file will be documented
"""

import json
import os

import pandas as pd

data_path = os.path.join(os.path.dirname(__file__), "data")
file_name = "202401"
excel_path = os.path.join(data_path, f"excel/{file_name}.xlsx")
json_path = os.path.join(data_path, f"json/{file_name}.json")
all_sheets = pd.read_excel(excel_path, sheet_name=None, engine="openpyxl")
anime_data = []


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


for sheet_name, df in all_sheets.items():
    if "新番表" in sheet_name:
        # 处理新番表数据
        filtered_df = df[
            df.apply(
                contains_str,
                str_list=["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
                axis=1,
            )
        ]
        df_cleaned = filtered_df.dropna(axis=1, how="all").dropna(axis=0, how="all")
        for _, row in df_cleaned.iterrows():
            row_list = row.to_list()
            tags_str = row_list[-1]
            tags = []
            if "/" in tags_str:
                for each_tag in tags_str.split("/"):
                    tags.append(each_tag.strip())
            row_data = {
                "anime_name": str(row_list[0]).strip(),
                "weekday": str(row_list[1]).strip(),
                "play_time": str(row_list[2]).strip(),
                "play_date": str(row_list[-4]).strip(),
                "play_nums": str(row_list[-3]).strip(),
                "tags": tags,
            }
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

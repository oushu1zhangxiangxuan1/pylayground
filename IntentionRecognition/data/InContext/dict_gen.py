# -*- coding: utf-8 -*-
# 定义城市和它们的简称
cities_abbreviations = {
    'BJ': '北京',
    'SH': '上海',
    'GZ': '广州',
    'SZ': '深圳',
    'CD': '成都',
    'CQ': '重庆',
    'TJ': '天津',
    'XA': '西安',
    'NJ': '南京',
    'HZ': '杭州',
    'WH': '武汉',
    # 添加更多城市...
}

# 生成Markdown表格
markdown_table = "| 城市列数据 | 数据含义 |\n"
markdown_table += "| --- | --- |\n"

for code, city in cities_abbreviations.items():
    markdown_table += f"| {code} | {city} |\n"

# 打印Markdown表格
print(markdown_table)

# 也可以将Markdown表格保存到文件
with open('cities_abbreviations.md', 'w') as f:
    f.write(markdown_table)

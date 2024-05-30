import os

def deduplicate_and_write_back(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在。")
        return

    # 读取文件所有行
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(set(lines))

    print(f"文件 {file_path} 去重完成并已写回。")

# 使用示例
# deduplicate_and_write_back('path/to/your/file.txt')


# TODO: 可能无效，或者可以更直接

deduplicate_and_write_back('data/InContext/1_DataQuery.csv')
deduplicate_and_write_back('data/InContext/2_AttributionAnalysis.csv')
deduplicate_and_write_back('data/InContext/3_Ambiguity.csv')
deduplicate_and_write_back('data/InContext/4_Discline.csv')



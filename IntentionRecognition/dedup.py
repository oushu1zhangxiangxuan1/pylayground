import os

def deduplicate_and_write_back(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在。")
        return

    # 读取文件所有行
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 去除重复行并保持顺序
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

    print(f"文件 {file_path} 去重完成并已写回。")

# 使用示例
# deduplicate_and_write_back('path/to/your/file.txt')

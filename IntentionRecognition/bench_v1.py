import os
import json
import pandas as pd
import openai
from jinja2 import Environment, FileSystemLoader
from llm import send_llm_api

# TODO:
# 1. 把可配置的都写到.env 文件配置化，使用dotenv读取生效
# 2. 把目前所有print的内容同时写入到一个名为 ./results/{directory_last_name}_{时间戳}_{PROXYLLM_BACKEND}.txt 文件中
#    2.1 directory_last_name  指 directory路径变量的最后一级目录名
#    2.2 时间戳 格式为 YYMMDDMM

PROXY_SERVER_URL = "http://xxxx:8000/v1/chat/completions"
PROXYLLM_BACKEND="Mixtral-8x7B-Instruct-v0.1"

max_tokens=50
n=1
stop=None
temperature=0
frequency_penalty=0
presence_penalty=0

def get_intention_from_api(prompt):
    messages=[
        {"role": "system", "content": "你是一个数据分析大师"},
        {"role": "user", "content": prompt}
    ]

    response = send_llm_api(
        model=PROXYLLM_BACKEND, 
        url=PROXY_SERVER_URL, 
        token='', 
        history=messages, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        frequency_penalty=frequency_penalty, 
        presence_penalty=presence_penalty,
    )
    intention = response.get('choices')[0].get('message')['content'].strip()
    return intention


def process_files(directory, intention_json, template_file, j2env):
    # 读取intention.json文件
    with open(intention_json, 'r') as f:
        intentions = json.load(f)

    # 准备Jinja2模板
    template = j2env.get_template(template_file)

    total_lines = 0
    total_correct = 0
    intention_counts = {}
    intention_correct_counts = {}

    # 遍历目录中的所有csv文件
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename.startswith(tuple(intentions.keys())):
            num = filename.split('_')[0]
            intention = intentions[num]

            # 读取csv文件
            df = pd.read_csv(os.path.join(directory, filename), header=None)
            lines = df.shape[0]
            total_lines += lines
            intention_counts[intention] = lines

            # 判断意图并统计正确数
            correct_count = 0
            error_records = []
            for index, row in df.iterrows():
                # 使用Jinja2模板填充提示文本
                prompt = template.render(intentions='\n'.join([f"{k}: {v}" for k, v in intentions.items()]), input=row.iloc[0])
                predicted_intention = get_intention_from_api(prompt)
                # print("predicted_intention:", predicted_intention)

                if predicted_intention == num:
                    correct_count += 1
                else:
                    error_records.append((row.iloc[0], predicted_intention, num))

            total_correct += correct_count
            intention_correct_counts[intention] = correct_count

            # 输出错误记录
            if error_records:
                print(f"Intention {intention} error records:")
                for record in error_records:
                    print(record)

    # 输出统计结果
    print(f"Total lines: {total_lines}")
    print(f"Total correct: {total_correct}")
    print(f"Accuracy: {total_correct / total_lines:.2%}")

    # 输出每个意图的统计结果
    for intention, correct_count in intention_correct_counts.items():
        print(f"Intention {intention}:")
        print(f"Lines: {intention_counts[intention]}")
        print(f"Correct: {correct_count}")
        print(f"Accuracy: {correct_count / intention_counts[intention]:.2%}\n")

# main函数
def main():
    # directory = './data/Basic'
    directory = './data/InContext'
    intention_json = os.path.join(directory, 'intentions.json')
    template_file = 'prompt.jinja2'
    j2env = Environment(loader=FileSystemLoader(searchpath=directory))
    process_files(directory, intention_json, template_file, j2env)

# 运行main函数
if __name__ == "__main__":
    main()

import os
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from llm import send_llm_api
from dotenv import load_dotenv
from datetime import datetime
import openai
from tqdm import tqdm

# 加载环境变量
load_dotenv()

PROXY_SERVER_URL = os.getenv('PROXY_SERVER_URL')
PROXYLLM_BACKEND = os.getenv('PROXYLLM_BACKEND')
max_tokens = int(os.getenv('MAX_TOKENS'))
n = int(os.getenv('N'))
stop = os.getenv('STOP')
temperature = float(os.getenv('TEMPERATURE'))
frequency_penalty = float(os.getenv('FREQUENCY_PENALTY'))
presence_penalty = float(os.getenv('PRESENCE_PENALTY'))
directory = os.getenv('DIRECTORY')
api_key = os.getenv("PROXY_API_KEY", None)

def load_openai_env():
    api_type = os.getenv("PROXY_API_TYPE", None)
    api_base = os.getenv("PROXY_API_BASE", None)
    api_version = os.getenv("PROXY_API_VERSION", None)

    if api_type:
        openai.api_type = api_type
    if api_base:
        openai.api_base = api_base
    if api_key:
        openai.api_key = api_key
    if api_version:
        openai.api_version = api_version

def get_intention_from_api(prompt):
    messages = [
        {"role": "system", "content": "你是一个数据分析大师"},
        {"role": "user", "content": prompt}
    ]

    response = send_llm_api(
        model=PROXYLLM_BACKEND, 
        url=PROXY_SERVER_URL, 
        token=api_key, 
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

    # 获取目录最后一级目录名和当前时间戳
    directory_last_name = os.path.basename(directory)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    result_file = f'./results/{directory_last_name}_{timestamp}_{PROXYLLM_BACKEND}.txt'

    with open(result_file, 'w') as result:
        # 遍历目录中的所有csv文件
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f.startswith(tuple(intentions.keys()))]
        
        for filename in tqdm(csv_files, desc="Processing CSV files"):
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
            for index, row in tqdm(df.iterrows(), total=lines, desc=f"Processing rows in {filename}", leave=False):
                # 使用Jinja2模板填充提示文本
                prompt = template.render(intentions='\n'.join([f"{k}: {v}" for k, v in intentions.items()]), input=row.iloc[0])
                predicted_intention = get_intention_from_api(prompt)

                if predicted_intention == num:
                    correct_count += 1
                else:
                    error_records.append((row.iloc[0], predicted_intention, num))

            total_correct += correct_count
            intention_correct_counts[intention] = correct_count

            # 输出错误记录
            if error_records:
                error_message = f"Intention {intention} error records:\n" + '\n'.join([str(record) for record in error_records]) + '\n'
                print(error_message)
                result.write(error_message)

        # 输出统计结果
        summary = (
            f"Total lines: {total_lines}\n"
            f"Total correct: {total_correct}\n"
            f"Accuracy: {total_correct / total_lines:.2%}\n"
        )
        print(summary)
        result.write(summary)

        # 输出每个意图的统计结果
        for intention, correct_count in intention_correct_counts.items():
            intention_summary = (
                f"Intention {intention}:\n"
                f"Lines: {intention_counts[intention]}\n"
                f"Correct: {correct_count}\n"
                f"Accuracy: {correct_count / intention_counts[intention]:.2%}\n\n"
            )
            print(intention_summary)
            result.write(intention_summary)

# main函数
def main():
    intention_json = os.path.join(directory, 'intentions.json')
    template_file = 'prompt.jinja2'
    j2env = Environment(loader=FileSystemLoader(searchpath=directory))
    process_files(directory, intention_json, template_file, j2env)

# 运行main函数
if __name__ == "__main__":
    main()

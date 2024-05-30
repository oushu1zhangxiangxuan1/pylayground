import re
import os
import argparse
import requests


# 获取当前脚本的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

def remove_chars(string):
    chars_to_remove = " ;"  # 要去除的字符

    # 去除开头的字符
    while string and (string[0] in chars_to_remove):
        string = string[1:]

    # 去除结尾的字符
    while string and (string[-1] in chars_to_remove):
        string = string[:-1]

    return string


def parse_one_line_sql_from_query(query):
    # print(query)
    pattern = r"```(.*?)```"
    match = re.search(pattern, query, re.DOTALL)

    sql = ""
    if match:
        sql = match.group(1)
        # print(sql)
    else:
        pattern = r"```(.*)"
        match = re.search(pattern, query, re.DOTALL)
        if not match:
            return parse_sql_query_raw(query)
        else:
            sql = match.group(1)
            # print(sql)
    sql = sql.replace("sql", "", 1)
    sql = sql.replace("SQL", "", 1)
    sql = sql.replace("\n", " ")
    sql = re.sub(r"\s+", " ", sql)
    sql = remove_chars(sql)
    sql = sql.strip()
    if len(sql) == 0:
        return "NO SQL FOUND\n"
    return sql + "\n"


def parse_sql_query_raw(sql):
    sql = sql.replace("\n", " ")
    sql = re.sub(r"\s+", " ", sql)
    sql = remove_chars(sql)
    if len(sql) == 0:
        return "NO SQL FOUND\n"
    return sql + "\n"


def get_all_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sqlite'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Invalid value for --test argument')


def BF_ABS_PATH(relative_path):
    return os.path.abspath(
        os.path.join(os.environ.get("NL2SQL_BENCHFRAME_HOME", ""), relative_path)
    )


def send_llm_api(
        model, 
        url, 
        token, 
        history, 
        temperature, 
        max_tokens, 
        frequency_penalty, 
        presence_penalty,
        ):

    request_data = {
        "model": model,
        "temperature": temperature,
        "messages": history,
        "max_tokens": max_tokens,
        "frequency_penalty":frequency_penalty,
        "presence_penalty":presence_penalty,
    }
    headers = {
        "api-key": token,
        "Content-Type": "application/json"
    }

    # 发送 POST 请求
    try:
        response = requests.post(url, json=request_data, headers=headers)
    except Exception as e:
        print("请求出错：", e)
        print("出错的请求内容：", request_data, "\nHeader:", headers)
        raise OpenAIResponseException(e)
    # 504超时只记录报错不退出，其他错误需要抛出特定异常终止运行
    if response.status_code == 504:
        print("请求超时：", response.text)
        raise response.text
    elif response.status_code != 200:
        http_error_msg = response.text
        if 400 <= response.status_code < 500:
            http_error_msg = (
                f"{response.status_code} Client Error: {response.reason} for url: {response.url}"
            )

        elif 500 <= response.status_code < 600:
            http_error_msg = (
                f"{response.status_code} Server Error: {response.reason} for url: {response.url}"
            )
        print("请求出错: ", response.text)
        print("出错的请求内容：", request_data, "\nHeader:", headers)
        raise OpenAIResponseException(http_error_msg)
    
    # 解析响应
    response_json = response.json()
    if "error_code" in response_json:
        error_code = response_json["error_code"]
        error_msg = response_json["error_msg"]
        print(f"请求出错：{error_code} - {error_msg}")
        raise OpenAIResponseException(f"请求出错：{error_code} - {error_msg}")
    elif "object" in response_json and response_json["object"] == "error":
        error_code = response_json["code"]
        error_msg = response_json["message"]
        print(f"请求出错：{error_code} - {error_msg}")
        raise OpenAIResponseException(f"请求出错：{error_code} - {error_msg}")
    else:
        # print("response:\n", response_json)
        return response_json
    
class OpenAIResponseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

if '__main__' == __name__:
    query = "以下是将自然语言查询转换为完整的SQL语句： ```SQL SELECT 姓名 FROM 参赛学生，北京理工大学 WHERE 参赛学生.学校 = 北京理工大学 AND 参赛学生.年龄 BETWEEN 18 AND 22 GROUP BY 参赛学生.学生ID HAVE COUNT(1) > 0 AND 参赛学生.学生ID = 参赛学生.学生ID"
    sql = parse_one_line_sql_from_query(query=query)
    print("final sql:\n", sql)
import json
import re
import time
import requests


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件 '{file_path}' 不存在")
    except IOError:
        print(f"无法读取文件 '{file_path}'")


def extract_title(json_string):
    pattern = r'"title":"(.*?)"'
    match = re.findall(pattern, json_string)
    if match:
        title = match
        return title
    else:
        return None


def write_list_to_file_with_timestamp(file_path, data_list):
    try:
        existing_content = set()

        # 读取已存在的内容
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    existing_content.add(line.strip())
        except FileNotFoundError:
            pass

        # 检查并写入新内容
        with open(file_path, 'a') as file:
            for item in data_list:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if item not in existing_content:
                    file.write(f"{timestamp}\n{item}\n")
                    existing_content.add(item)
                    print(f"已将 {item} 写入文件：{file_path}")
                    push_message(f"expo 有新玩具了！ {item}")
    except IOError:
        print(f"无法写入文件：{file_path}")


def push_message(message):
    url = 'https://open.feishu.cn/open-apis/bot/v2/hook/c63/你的飞书链接'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    data = json.dumps(data)
    r = requests.post(url, headers=headers, data=data)
    if r.status_code != 200:
        print('飞书消息发送失败。')
    # print(r.text)


file_path = 'response.txt'  # 文件路径
file_content = read_file(file_path)
if file_content:
    titles = extract_title(file_content)
    # print(titles)
    write_list_to_file_with_timestamp('expo_toy_title.txt',titles)

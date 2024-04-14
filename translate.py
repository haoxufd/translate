import requests
import json
import hashlib
import random
from tqdm import tqdm
import time
import os
import sys

def translate_text(text, target_lang):
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    app_id = "20240413002022774"
    app_key = "DT5EDisJkH8ACAfEsiq2"
    salt = str(random.randint(32768, 65536))
    sign = app_id + text + salt + app_key
    sign = hashlib.md5(sign.encode()).hexdigest()

    params = {
        "q": text,
        "from": "en",
        "to": target_lang,
        "appid": app_id,
        "salt": salt,
        "sign": sign
    }
    response = requests.get(url, params=params)
    translation = json.loads(response.content)["trans_result"][0].get("dst")
    return translation

to_translate_file = "/Users/xuhao/Desktop/translate/add.json"
translated_file = "/Users/xuhao/Desktop/translate/translated.json"
num_translated_file = "/Users/xuhao/Desktop/translate/num_translated.txt"


# 读取待翻译JSON文件
with open(to_translate_file, "r") as file:
    data = json.load(file)

# 读取已翻译JSON文件
if os.path.exists(translated_file):
    with open(translated_file, "r") as file:
        data_translated = json.load(file)
else:
    data_translated = []

# 读取记录已翻译数量的文件
if os.path.exists(num_translated_file):
    with open(num_translated_file, "r") as file:
        num_translated = int(file.read().strip())
else:
    num_translated = 0

for i in range(num_translated):
    data[i] = data_translated[i]

# 遍历每个对象，并翻译caption中的文本
try:
    for obj in tqdm(data[num_translated:], desc="翻译进度"):
        captions = obj["caption"]
        translated_captions = []
        for caption in captions:
            translated_captions.append(translate_text(caption, "zh"))
            time.sleep(0.75)
        obj["caption"] = translated_captions
        num_translated += 1
except Exception:
    with open(translated_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    print("翻译后的JSON数据已保存到新文件：", translated_file)
    
    with open(num_translated_file, "w") as file:
        file.write(str(num_translated))

    sys.exit(1)

with open(translated_file, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
print("翻译后的JSON数据已保存到新文件：", translated_file)
    
with open(num_translated_file, "w") as file:
    file.write(str(num_translated))
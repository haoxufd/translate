from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import json
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

model_name = 'facebook/m2m100_1.2B'
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# 读取数据
input_file_path = 'test.json'  # 确保此路径指向你的 data.json 文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 使用 tqdm 创建进度条处理翻译
for item in tqdm(data, desc="Translating captions"):
    translations = []
    for caption in item['caption']:
        encoded = tokenizer(caption, return_tensors="pt")
        translated = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("zh"))
        translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        translations.append(translated_text)
    item['caption'] = translations

# 将翻译后的数据保存到 JSON 文件
translated_file_path = 'data_translated.json'
with open(translated_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

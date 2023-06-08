import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# 初始化T5模型和分词器
MODEL_NAME = 'T5-base'
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, model_max_length=1024)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def simplify_prompt(prompt: str) -> str:
    # 对输入提示进行分词
    input_ids = tokenizer.encode("summarize: " + prompt, return_tensors="pt")

    # 使用模型生成摘要
    with torch.no_grad():
        summary_ids = model.generate(input_ids, max_length=3050, num_return_sequences=1, num_beams=6)

    # 将生成的摘要转换为文本
    simplified_prompt = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return simplified_prompt


import os
import openai
from dotenv import load_dotenv

load_dotenv()

# OpenAIのAPIキーを設定
openai.api_key = os.environ.get("OPENAI_API_KEY")

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.25
SYSTEM = """
### 指示 ###
論文の内容を理解した上で，重要なポイントを箇条書きで3点書いてください。

### 箇条書きの制約 ###
- 最大3個
- 日本語
- 箇条書き1個を100文字以内

### 対象とする論文の内容 ###
{text}

### 出力形式 ###
- 箇条書き1
- 箇条書き2
- 箇条書き3
"""

# https://qiita.com/yuta0821/items/2edf338a92b8a157af37#2-5-notion%E3%83%9A%E3%83%BC%E3%82%B8%E3%81%AE%E4%BD%9C%E6%88%90
def get_summary(data):
    text = f"title: {data['title']}\nbody: {data['summary']}"

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': text}
        ],
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content
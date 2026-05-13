import requests

APP_TOKEN = "这里填写你的AppToken"
UID = "这里填写你的UID"

content = """
🔥 今日 AI 热点

1. OpenAI 新模型更新
2. AI Agent 热度持续上升
3. GitHub Actions 自动化越来越火

—— 来自你的 AI 自动推送系统
"""

url = "https://wxpusher.zjiecode.com/api/send/message"

data = {
    "appToken": APP_TOKEN,
    "content": content,
    "summary": "AI热点推送",
    "contentType": 1,
    "uids": [UID]
}

response = requests.post(url, json=data)

print(response.text)

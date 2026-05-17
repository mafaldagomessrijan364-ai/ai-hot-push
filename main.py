import os
import requests

WXPUSHER_APP_TOKEN = os.environ["WXPUSHER_APP_TOKEN"]
WXPUSHER_UID = os.environ["WXPUSHER_UID"]

AIHOT_API = "https://aihot.virxact.com/api/public/items"
WXPUSHER_API = "https://wxpusher.zjiecode.com/api/send/message"


def extract_items(payload):
    """
    兼容不同 JSON 结构，尽量从 AIHOT 返回结果里取出列表。
    """
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ["data", "items", "list", "records", "result"]:
            value = payload.get(key)

            if isinstance(value, list):
                return value

            if isinstance(value, dict):
                for sub_key in ["items", "list", "records", "data"]:
                    sub_value = value.get(sub_key)
                    if isinstance(sub_value, list):
                        return sub_value

    return []


def fetch_aihot_items(limit=8):
    response = requests.get(
        AIHOT_API,
        params={
            "mode": "selected"
        },
        timeout=20
    )
    response.raise_for_status()

    payload = response.json()
    items = extract_items(payload)

    return items[:limit]


def pick(item, keys, default=""):
    for key in keys:
        value = item.get(key)
        if value:
            return str(value).strip()
    return default


def build_message(items):
    if not items:
        return "今天暂时没有抓取到 AIHOT 精选内容。"

    lines = []
    lines.append("🔥 今日 AIHOT 精选")
    lines.append("")

    for index, item in enumerate(items, start=1):
        title = pick(item, ["title", "name", "headline"], "未命名标题")
        summary = pick(item, ["summary", "description", "content", "reason", "recommendReason"], "")
        source = pick(item, ["source", "sourceName", "channel", "siteName"], "")
        url = pick(item, ["url", "link", "originalUrl"], "")

        lines.append(f"{index}. {title}")

        if source:
            lines.append(f"来源：{source}")

        if summary:
            summary = summary.replace("\n", " ")
            if len(summary) > 120:
                summary = summary[:120] + "..."
            lines.append(f"摘要：{summary}")

        if url:
            lines.append(f"链接：{url}")

        lines.append("")

    lines.append("—— 来自 GitHub Actions + AIHOT 自动推送系统")

    return "\n".join(lines)


def push_to_wxpusher(content):
    data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": content,
        "summary": "AIHOT 今日精选",
        "contentType": 1,
        "uids": [WXPUSHER_UID]
    }

    response = requests.post(WXPUSHER_API, json=data, timeout=20)

    print(response.status_code)
    print(response.text)

    response.raise_for_status()


if __name__ == "__main__":
    items = fetch_aihot_items(limit=8)
    message = build_message(items)
    print(message)
    push_to_wxpusher(message)

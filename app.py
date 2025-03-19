import os
from dotenv import load_dotenv
from flask import Flask, render_template
import requests

load_dotenv()

app = Flask(__name__)

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")


# Notion API에서 데이터 가져오기
def fetch_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = {
            "error": "Failed to fetch Notion data",
            "status_code": response.status_code,
            "response_text": response.text,  # Notion API의 상세 오류 메시지 출력
        }
        print("⚠️ Notion API 요청 실패:", error_message)  # 터미널에 에러 메시지 출력
        return error_message


# 웹 브라우저에 Notion 데이터 표시
@app.route("/")
def index():
    data = fetch_notion_data()
    print(data)
    if "error" in data:
        return f"<h1>오류 발생: {data['error']}</h1>"

    notion_items = []
    for page in data.get("results", []):
        properties = page.get("properties", {})
        title = (
            properties.get("이름", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "제목 없음")
        )
        date = properties.get("날짜", {}).get("date", {}).get("start", "날짜 없음")

        notion_items.append({"title": title, "date": date})

    return render_template("index.html", items=notion_items)


if __name__ == "__main__":
    app.run(debug=True)

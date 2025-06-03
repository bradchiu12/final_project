import os
import pathlib
from dotenv import load_dotenv
from flask import Flask, request, render_template
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# 載入 .env
env_path = pathlib.Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

KEY = os.getenv('KEY')
ENDPOINT = os.getenv('ENDPOINT')
if not KEY or not ENDPOINT:
    raise ValueError("請確認環境變數 KEY 和 ENDPOINT 已正確設定")

ENDPOINT = ENDPOINT.rstrip('/')

app = Flask(__name__)

recyclable_keywords = ['plastic', 'bottle', 'can', 'paper', 'cardboard', 'metal', 'glass', 'box', 'container']
general_trash_keywords = ['food', 'garbage', 'trash', 'waste', 'dirty', 'soiled','plastic bag']

def classify_waste(tags):
    tags_lower = [tag.lower() for tag in tags]
    for word in recyclable_keywords:
        if word in tags_lower:
            return "可回收物", f"標籤中包含「{word}」，建議請回收該物品。"
    for word in general_trash_keywords:
        if word in tags_lower:
            return "一般垃圾", f"標籤中包含「{word}」，請丟一般垃圾桶。"
    return "無法判斷", "系統無法根據圖片標籤判斷垃圾種類。"

@app.route("/", methods=['GET', 'POST'])
def classify():
    image_url = ""
    result = ""
    category = ""

    if request.method == 'POST':
        image_url = request.form.get("image_url", "").strip()

        if image_url:
            try:
                client = ComputerVisionClient(
                    endpoint=ENDPOINT,
                    credentials=CognitiveServicesCredentials(KEY)
                )

                analysis = client.analyze_image(image_url, visual_features=["Tags"], language="en")
                tags = [tag.name for tag in analysis.tags]
                category, result = classify_waste(tags)
            except Exception as e:
                result = f"圖片分析失敗：{str(e)}"
        else:
            result = "請輸入有效的圖片網址"

    return render_template("index.html",
                           image_url=image_url,
                           result=result,
                           category=category)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

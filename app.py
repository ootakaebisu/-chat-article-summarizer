from flask import Flask, render_template, request, jsonify
import openai
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# OpenAI APIキーを設定します (環境変数から取得するか、直接キーを入力します)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([p.text for p in paragraphs])

def generate_summary(article_text):
    prompt = f"Please summarize the following article:\n\n{article_text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    article_text = fetch_article_text(url)
    summary = generate_summary(article_text)
    return jsonify(summary=summary)


if __name__ == '__main__':
    app.run(debug=False, port=8000)

app.config["TEMPLATES_AUTO_RELOAD"] = True

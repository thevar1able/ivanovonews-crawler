from flask import Flask, request
from summarize import Summarizer

app = Flask(__name__)

summarizer = Summarizer()

@app.post("/feed.xml")
def summarize():
    if not request.json or not request.json.get('data'):
        return ""

    return summarizer.run(request.json['data'])


if __name__ == '__main__':
    app.run()

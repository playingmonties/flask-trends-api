from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from datetime import datetime

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=0)

@app.route("/trends", methods=["GET"])
def trends():
    # Read keyword(s)
    keywords = request.args.get("keywords")
    if not keywords:
        return jsonify({"error": "keywords parameter required"}), 400

    keyword_list = [k.strip() for k in keywords.split(",")]

    # Pull last 30 days of data
    pytrends.build_payload(keyword_list, timeframe="now 30-d")

    data = pytrends.interest_over_time()

    if data.empty:
        return jsonify({"error": "no data returned"}), 404

    # Format output cleanly
    output = []

    for k in keyword_list:
        series = []
        for index, row in data.iterrows():
            if not row.get('isPartial', False):
                series.append({
                    "date": index.strftime("%Y-%m-%d"),
                    "value": int(row[k])
                })

        output.append({
            "keyword": k,
            "data": series
        })

    return jsonify(output)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


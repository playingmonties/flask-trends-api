from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from datetime import datetime
import traceback
import pandas as pd

app = Flask(__name__)

@app.route("/trends", methods=["GET"])
def trends():
    try:
        # Read keyword(s)
        keywords = request.args.get("keywords")
        if not keywords:
            return jsonify({"error": "keywords parameter required"}), 400

        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
        
        if not keyword_list:
            return jsonify({"error": "at least one valid keyword required"}), 400

        # Create a new TrendReq instance for each request to avoid rate limiting issues
        pytrends = TrendReq(hl='en-US', tz=0, timeout=(10, 25))
        
        # Pull last 30 days of data
        pytrends.build_payload(keyword_list, timeframe="now 30-d")
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"error": "no data returned from Google Trends"}), 404

        # Format output cleanly
        output = []

        for original_keyword in keyword_list:
            series = []
            # Find the actual column name in the dataframe (pytrends may modify it)
            keyword_col = None
            for col in data.columns:
                if col == 'isPartial':
                    continue
                # Check if this column matches our keyword
                if col == original_keyword or original_keyword.lower() in col.lower():
                    keyword_col = col
                    break
            
            if not keyword_col:
                output.append({
                    "keyword": original_keyword,
                    "data": [],
                    "error": "keyword not found in results"
                })
                continue
            
            for index, row in data.iterrows():
                if not row.get('isPartial', False):
                    try:
                        value = int(row[keyword_col]) if pd.notna(row[keyword_col]) else 0
                        series.append({
                            "date": index.strftime("%Y-%m-%d"),
                            "value": value
                        })
                    except (ValueError, KeyError, TypeError):
                        continue

            output.append({
                "keyword": original_keyword,
                "data": series
            })

        return jsonify(output)
    
    except Exception as e:
        # Log the error for debugging
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"Error in trends endpoint: {error_msg}")
        print(f"Traceback: {error_trace}")
        return jsonify({
            "error": "Internal server error",
            "message": error_msg
        }), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from datetime import datetime
import traceback
import pandas as pd
import time
import re

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
        
        # Limit to 5 keywords (Google Trends API limit)
        if len(keyword_list) > 5:
            return jsonify({
                "error": "too many keywords",
                "message": "Maximum 5 keywords allowed per request",
                "received": len(keyword_list)
            }), 400
        
        # Validate keywords (remove special characters that might cause issues)
        validated_keywords = []
        for kw in keyword_list:
            # Remove or replace problematic characters
            cleaned = re.sub(r'[^\w\s-]', '', kw).strip()
            if cleaned and len(cleaned) > 0:
                validated_keywords.append(cleaned)
        
        if not validated_keywords:
            return jsonify({"error": "no valid keywords after validation"}), 400

        # Create a new TrendReq instance for each request
        # Add retries with exponential backoff for rate limiting
        max_retries = 3
        data = pd.DataFrame()  # Initialize empty dataframe
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Create fresh instance for each attempt
                pytrends = TrendReq(hl='en-US', tz=0, timeout=(10, 25))
                
                # Pull last 30 days of data (use "today 1-m" for ~30 days, or "now 7-d" for last 7 days)
                # Google Trends doesn't support "now 30-d", so we use "today 1-m" for approximately 30 days
                pytrends.build_payload(validated_keywords, timeframe="today 1-m")
                data = pytrends.interest_over_time()
                
                # If we got data, break out of retry loop
                if not data.empty:
                    break
                else:
                    last_error = "Empty data returned"
                    
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                print(f"Attempt {attempt + 1} failed: {error_msg}")
                
                # Handle 429 (rate limit) errors with longer backoff
                if "429" in error_msg:
                    if attempt < max_retries - 1:
                        # For 429 errors, use longer exponential backoff: 30s, 60s, 120s
                        wait_time = 30 * (2 ** attempt)
                        print(f"Rate limited (429). Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Last attempt failed with 429
                        return jsonify({
                            "error": "Rate limit exceeded",
                            "message": "Google Trends has rate-limited this service. Please wait a few minutes before making another request.",
                            "retry_after": "2-5 minutes"
                        }), 429
                
                # Handle 400 errors with shorter backoff
                elif "400" in error_msg and attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)  # 5s, 10s, 15s
                    print(f"Bad request (400). Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                
                # For other errors or last attempt, raise it
                elif attempt == max_retries - 1:
                    raise
        
        # Check if we still have empty data after retries
        if data.empty:
            return jsonify({
                "error": "no data returned from Google Trends",
                "message": "Google Trends did not return data for the requested keywords. This may be due to rate limiting or invalid keywords."
            }), 404

        # Format output cleanly
        output = []

        for original_keyword in validated_keywords:
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
        
        # Check if it's a rate limit error
        if "429" in error_msg:
            return jsonify({
                "error": "Rate limit exceeded",
                "message": "Google Trends has rate-limited this service. Please wait a few minutes before making another request.",
                "retry_after": "2-5 minutes"
            }), 429
        
        return jsonify({
            "error": "Internal server error",
            "message": error_msg
        }), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


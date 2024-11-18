from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import openai
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Google Sheets API Setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file("google_credentials.json", scopes=SCOPE)
gc = gspread.authorize(credentials)

# OpenAI Setup
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        data = pd.read_csv(file)
        columns = list(data.columns)
        return jsonify({"columns": columns})  # Only show column names initially
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/filter-column', methods=['POST'])
def filter_column():
    file = request.files['file']
    selected_column = request.form['selected_column']
    if file:
        data = pd.read_csv(file)
        if selected_column in data.columns:
            filtered_data = data[selected_column].tolist()  # Extract only the selected column
            return jsonify({"column": selected_column, "data": filtered_data})
        else:
            return jsonify({"error": f"Column '{selected_column}' not found in file"}), 400
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/google-sheet', methods=['POST'])
def connect_google_sheet():
    sheet_id = request.json.get("sheet_id")
    sheet_name = request.json.get("sheet_name")
    try:
        sheet = gc.open_by_key(sheet_id).worksheet(sheet_name)
        data = pd.DataFrame(sheet.get_all_records())
        columns = list(data.columns)
        return jsonify({"columns": columns, "preview": data.head().to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process-and-download', methods=['POST'])
def process_and_download():
    data = request.json.get("data")
    main_column = request.json.get("main_column")
    user_query = request.json.get("user_query")

    # Process data and generate results
    results = []
    for entity in data[main_column]:
        query = user_query.replace("{entity}", entity)
        search_results = web_search(query)
        extracted_data = extract_with_llm(search_results, query)
        results.append({"entity": entity, "extracted_data": extracted_data})

    # Convert results to DataFrame
    result_df = pd.DataFrame(results)
    output_path = "output.csv"
    result_df.to_csv(output_path, index=False)

    # Send file for download
    return send_file(output_path, as_attachment=True)

def web_search(query):
    serp_api_key = os.getenv("SERP_API_KEY")
    params = {
        "q": query,
        "api_key": serp_api_key,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    return response.json()

def extract_with_llm(search_results, query):
    prompt = f"Using the following web results, extract the information for the query: '{query}'.\n\n{search_results}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)

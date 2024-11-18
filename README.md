# AI-Data-Extractor-Dashboard
**Project Description**
The AI Data Extractor Dashboard is a web-based tool designed to extract specific information from a dataset (CSV or Google Sheets) using an AI agent. Users can upload a dataset, select a column of interest, and define a query to retrieve relevant data for each entity in the chosen column. The AI agent leverages web search and processes search results using a Large Language Model (LLM) to extract and format the data. The tool allows users to view, filter, and download the processed data in a structured output.

**Key features:**
1.Upload and process CSV files.
2.Connect to Google Sheets and retrieve data.
3.Define custom queries to extract specific data.
4.Download the extracted data in CSV format.
5.Simple, user-friendly dashboard with Bootstrap for UI.

Setup Instructions
To run the AI Data Extractor Dashboard on your local machine, follow these steps:

1. Clone the repository:

git clone https://github.com/your-username/ai-data-extractor.git
cd ai-data-extractor

2. Install dependencies:
Make sure you have Python 3.6 or higher installed. Then, create a virtual environment and activate it.

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required Python packages:

pip install -r requirements.txt

3. Set up environment variables:
Create a .env file in the root directory and add the following keys:

OPENAI_API_KEY=your-openai-api-key
SERP_API_KEY=your-serp-api-key
Ensure you have your Google Cloud API credentials for the Google Sheets integration. Save the credentials JSON file as google_credentials.json in the root directory.

4. Run the Flask application:

python main.py

The application will start running at http://127.0.0.1:5000/ in your browser.

**Usage Guide**
1. Uploading a CSV File:
Click the "Upload a CSV File" section.
Select a CSV file from your local system.
The file will be uploaded, and the column names will be displayed.

2. Connecting Google Sheets:
Enter the Google Sheet ID and Sheet Name.
Click "Connect."
The columns from the sheet will be displayed.

3. Filtering Columns:
After uploading a CSV file, select the desired column to filter.
The filtered data will be displayed on the dashboard.

4. Setting a Query:
Enter a query template, such as: Get the email address of {entity}.
The {entity} will be replaced by each value in the chosen column.
The AI agent will use this query to extract relevant data.

5. Downloading Results:
After the data is processed, click the "Download Data" button to download the results as a CSV file.

**API Keys and Environment Variables**
To use the application, you need to provide your own API keys for OpenAI and SerpAPI:

1.OpenAI API Key: To interact with OpenAI's GPT models, you must have an OpenAI account and an API key. Set this key in the .env file:

OPENAI_API_KEY=your-openai-api-key

2.SerpAPI Key: SerpAPI is used for web search queries. Obtain your API key from SerpAPI and set it in the .env file:

SERP_API_KEY=your-serp-api-key

3.Google Sheets Credentials: To access Google Sheets, you need to set up a Google Cloud project with Sheets API and enable the Google Drive API. Then, download the credentials JSON file and place it as google_credentials.json in your project folder.

**Optional Features**
1.Customizable Search Queries: Users can define any search query template to retrieve data, making the tool flexible for different use cases.
2.Real-time Google Sheets Data Retrieval: Instead of uploading CSV files, users can directly connect to Google Sheets and retrieve data for processing.
3.Download Processed Data: After the AI processes the dataset, users can download the results as a CSV file.

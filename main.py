import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
user_filters = {}

# Configure Google AI API
genai.configure(api_key=api_key)

def extract_filters(user_query):
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""Extract property search filters from the given query.
                
                Query: "{user_query}"

                Provide the extracted filters in **valid JSON format**, without markdown or code blocks:
                {{
                    "property_type": "property_type",
                    "location": "location",
                    "bedrooms": rooms,
                    "max_rent": max_rent
                }}

                If the query modifies an existing filter, only return the updated fields.
                Do not remove any previously stored information.
                """

    response = model.generate_content(prompt)

    # Extract the content
    response_text = response.text.strip()

    # Remove possible markdown code block
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove ```json
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove closing ```

    try:
        filters = json.loads(response_text)
        return filters
    except json.JSONDecodeError as e:
        print("JSON Parsing Error:", str(e))
        return {"error": "Failed to parse response"}

while True:
    user_query = input("\nEnter the real estate search query (or type 'exit' to quit): ").strip()
    if user_query.lower() == 'exit':
        print("Goodbye! 👋")
        break

    new_filters = extract_filters(user_query)
    user_filters.update(new_filters)
    print("\nExtracted Filters:", user_filters)
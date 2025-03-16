import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

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

# Test the function
user_query = "I need a 2-bed apartment in Leicester under 1700 pounds per month"
filters = extract_filters(user_query)

print("\nExtracted Filters:", filters)
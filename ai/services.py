import json

from google import genai

from config import api_key

client = genai.Client(api_key=api_key)


def generate_ai_response(travel_days, destination, budget, interests_str):
    with open('ai/prompt.txt', 'r', encoding='utf-8') as file:
        prompt_file = file.read() % (travel_days, destination,
                                     budget, interests_str)

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt_file
    )
    filtered_response = response.text.replace('```json',
                                              '').replace('```', '').strip()

    try:
        return json.loads(filtered_response)
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON from AI'}

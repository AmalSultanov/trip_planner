import json
import logging
from typing import Any

from google import genai

from config import api_key

logger = logging.getLogger(__name__)
client = genai.Client(api_key=api_key)


def generate_ai_response(
        travel_days: str,
        destination: str,
        budget: str,
        interests: str
) -> dict[str, Any]:
    try:
        prompt = load_prompt_file(travel_days, destination, budget, interests)
        ai_response = call_ai_model(prompt)
        cleaned_text = clean_ai_response(ai_response)

        return str_to_dict(cleaned_text)
    except RuntimeError as e:
        logger.error(f'Runtime error: {e}')
        return {'error': str(e)}
    except Exception as e:
        logger.error(f'An internal error occurred: {e}')
        return {'error': f'An internal error occurred: {e}'}


def load_prompt_file(
        travel_days: str,
        destination: str,
        budget: str,
        interests: str
) -> str:
    with open('ai/prompt.txt', 'r', encoding='utf-8') as file:
        prompt_file = file.read()

    return prompt_file % (travel_days, destination, budget, interests)


def call_ai_model(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text if response.text else ''
    except Exception as e:
        logger.error(f'AI model request failed: {e}')
        raise RuntimeError(f'AI model request failed: {e}')


def clean_ai_response(response: str) -> dict[str, Any]:
    return response.replace('```json', '').replace('```', '').strip()


def str_to_dict(cleaned_text: str) -> dict[str, Any]:
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        logger.error(f'Invalid JSON from AI: {cleaned_text}')
        return {'error': 'Invalid JSON from AI'}

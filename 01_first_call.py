"""The first real API call: a small script before the web interface."""
from google import genai
from google.genai import types, errors
from study_ai import get_api_key, MODEL

key = get_api_key()
if not key:
    raise SystemExit('Run python setup_key.py first.')
try:
    with genai.Client(api_key=key, http_options=types.HttpOptions(
        timeout=60000, retry_options=types.HttpRetryOptions(attempts=1)
    )) as client:
        response = client.models.generate_content(
            model=MODEL,
            contents='Explain training versus inference to a beginner in two short sentences.',
            config=types.GenerateContentConfig(
                max_output_tokens=1024,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    thinking_config=types.ThinkingConfig(thinking_level="low"),
            ),
        )
    print(response.text)
except errors.APIError as error:
    raise SystemExit(f"Gemini request failed (HTTP {error.code}). Check key, model access and quota in AI Studio.") from None

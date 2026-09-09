"""Run locally; the key is hidden during entry and never printed."""
from getpass import getpass
from pathlib import Path
import json, os

path = Path(__file__).parent / '.streamlit' / 'secrets.toml'
key = getpass('Paste your Gemini API key (input stays hidden): ').strip()
if not key or any(c.isspace() for c in key):
    raise SystemExit('Key must be non-empty and contain no whitespace. Nothing saved.')
path.parent.mkdir(exist_ok=True)
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, 'w') as file:
    file.write('GEMINI_API_KEY = ' + json.dumps(key) + '\n')
os.chmod(path, 0o600)
print('Key saved locally. Do not include this file in screenshots, videos or source sharing.')

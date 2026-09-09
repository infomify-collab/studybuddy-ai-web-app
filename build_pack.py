"""Read a real text file, call Gemini once, and save a study pack."""
import argparse
from pathlib import Path
import json
from study_ai import generate_pack, to_markdown, StudyError

parser = argparse.ArgumentParser()
parser.add_argument('notes', type=Path)
parser.add_argument('--language', choices=['English', 'Hinglish'], default='English')
parser.add_argument('--output', type=Path, default=Path('runs'))
args = parser.parse_args()
try:
    pack, receipt = generate_pack(args.notes.read_text(), args.language)
except (StudyError, OSError) as error:
    raise SystemExit(str(error)) from None
args.output.mkdir(parents=True, exist_ok=True)
(args.output / 'study-pack.json').write_text(pack.model_dump_json(indent=2))
(args.output / 'study-pack.md').write_text(to_markdown(pack))
(args.output / 'receipt.json').write_text(json.dumps(receipt, indent=2))
print('Created:', args.output / 'study-pack.md')
print('Model:', receipt['model'], '| Total tokens:', receipt['total_tokens'])

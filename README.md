# StudyBuddy — build your first AI web app

A complete beginner project for CodeWithHimi. Turn permitted study notes into three summary points, three flashcards and a three-question quiz. Inspect the original source lines and download a Markdown study pack with an answer key.

This is a **local learning app**. Python performs input validation, checks the output structure and source references, and scores the quiz. Gemini generates the study content. Streamlit runs the Python web server and builds the browser interface. No custom backend routes or JavaScript frontend are needed.

## 1. Extract the project and install

Use Python **3.11 or newer**, an internet connection and your own Gemini API key. Open a terminal in the extracted `StudyBuddy` project folder (the folder containing `app.py`).

**macOS / Linux**

```sh
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**Windows — Command Prompt**

```bat
py -3 --version
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

If Python is missing, install it from [python.org](https://www.python.org/downloads/). After reopening a terminal, activate the environment again before running the following commands.

## 2. Configure your own key privately

Create a key for your project in [Google AI Studio](https://aistudio.google.com/api-keys), check model availability and your quota/billing settings, then run:

```sh
python setup_key.py
```

Paste the key into the hidden prompt. Nothing appears while entering it. The helper writes `.streamlit/secrets.toml` locally. **This file is intentionally absent from the download and excluded from Git.** The helper overwrites an existing local key when you run it again. It applies owner-only file permissions on systems that support them.

Alternatively, set `GEMINI_API_KEY` or `GOOGLE_API_KEY` securely in your local environment. The helper gives `GEMINI_API_KEY` precedence. Never place actual credentials inside Python source, public repositories, screenshots, exported notebooks or frontend JavaScript.

API usage and availability depend on your project and region. This course does not promise free or unlimited generation. Notes are sent to Google when you generate; use public material or content you have permission to send.

## 3. Run the first small Python script

```sh
python 01_first_call.py
```

It requests a two-sentence explanation of training versus inference. `contents` is the prompt; `response.text` is the returned text. `MODEL` is configured in `study_ai.py`. The bounded output setting is a token limit, not a word count.

The default model verified for this project on 9 September 2026 is `gemini-3.8-flash`, using the official `google-genai` SDK and its `models.generate_content` method. Low thinking is configured to leave room for the answer within the output budget. Model availability can change.

## 4. Run the complete pipeline in the terminal

```sh
python build_pack.py examples/ai_notes.txt
```

For Roman Hinglish output:

```sh
python build_pack.py examples/ai_notes.txt --language Hinglish
```

The command writes `runs/study-pack.json`, `runs/study-pack.md` and `runs/receipt.json`. A later run overwrites these three files in the same output folder. Use `--output runs/my-chapter` to keep a separate result. The receipt records the model, a source hash and token counts; it does not contain the key. Total usage may include reasoning tokens beyond the visible response.

## 5. Start the web app

```sh
python -m streamlit run app.py
```

Open the Local URL printed in the terminal (normally `http://localhost:8501`). Keep that terminal running. Press Ctrl+C in the terminal to stop it.

1. Read the included notes or replace them with at least three useful lines (80 characters total), up to 6,000 characters.
2. Choose English or Hinglish output.
3. Confirm the notes are permitted to send, then click **Create my study pack**.
4. Read Summary and expand a source reference. Compare the meaning of the claim with the quote.
5. Open Flashcards. Think of your answer before revealing it.
6. Select one option for all three Quiz questions, then click **Check my answers**.
7. Use **Check sources** to see the numbered input and **Download study pack + answer key** to save it.

The demonstration video uses port 8510 to avoid an existing local app. Either port works; use `python -m streamlit run app.py --server.port 8510` if desired.

## Read the project in this order

| File | What to learn |
|---|---|
| `01_first_call.py` | Imports, key helper, SDK client, request and printed response |
| `examples/ai_notes.txt` | The original source context; one idea per line |
| `study_ai.py` | Pydantic classes, prompt construction, API call, validation and export |
| `build_pack.py` | Reading a text file and saving generated output with normal Python |
| `app.py` | Text area, form submit, session state, tabs, quiz scoring and download |
| `setup_key.py` | Hidden input and local secret setup |
| `requirements.txt` | Tested package versions: Streamlit 1.63.0, google-genai 2.22.0, Pydantic 2.13.5 |

## AI concepts connected to the code

- **Inference:** the app uses an already-trained model. Supplying notes in a request does not itself update the model's weights. Provider data retention/training policies are a separate question.
- **Context and prompting:** `make_prompt` supplies a task, numbered source notes and output constraints. It tells the model to treat source notes as data; that instruction is not a complete prompt-injection defense.
- **Structured output:** `StudyPack` defines the shape the interface needs. The API uses that class as the response schema. Python then validates the returned object and checks every source quote/line pairing against the input.
- **Tokens and bounded usage:** notes are limited to 6,000 characters and generated output is capped. These are app choices, not universal Gemini limits. A submitted generation is one API call; there are no automatic generation retries. Invalid input sends no call.
- **Hallucinations:** valid JSON does not imply correct facts. Matching source quotations do not prove that the generated claim follows from them. Read the quotes and review the answer key.
- **Deterministic code:** Python handles line numbering, input checks, score calculation and file export. These steps need no additional AI generation.
- **State:** `st.session_state` preserves the pack within a browser session across reruns. It is not a database. Quiz changes and downloads reuse the existing pack. A reload, new session or server restart may lose the in-memory result.

## A small exercise and answer check

Use five lines from your own permitted study material, generate a Hinglish pack, verify one claim, solve the quiz and download the result.

Then reduce the input limit to 3,000 characters. **Answer:** change `MAX_NOTES = 6000` to `MAX_NOTES = 3000` in `study_ai.py`. Both input validation and the Streamlit text box read the same constant. Restart/rerun the app. This is a Python rule; no model training or additional prompt is necessary.

Changing the number of quiz questions is a larger exercise: update the Pydantic list constraints, prompt wording, displayed score denominator and relevant interface text together.

## Troubleshooting

| Symptom | Action |
|---|---|
| Import/module not found | Activate `.venv`, then rerun the install command |
| Key missing | Run `python setup_key.py` from this project |
| 401 / 403 / access failure | Check that the key and project have access in AI Studio |
| 404 / unavailable model | Check the [current model documentation](https://ai.google.dev/gemini-api/docs/models); select a supported text model and compatible thinking settings |
| 429 / quota | Check your account usage; do not keep submitting identical requests |
| Incomplete JSON | The model may exhaust its output budget; check the model's thinking/output settings and simplify the notes before another deliberate request |
| Source reference mismatch | The app rejected an unverified pairing. Review the notes and regenerate only if needed |
| Slow/no connection | Check internet access and service status; the request timeout is bounded |
| Address already in use | Add `--server.port 8510` or another free local port |

To set another compatible model for this shell:

```sh
# macOS / Linux (substitute a verified available model)
export GEMINI_MODEL="your-supported-model-id"
```

```bat
REM Windows Command Prompt
set GEMINI_MODEL=your-supported-model-id
```

The code currently uses `thinking_level="low"`. If you choose a model with different parameter support, adjust its generation configuration according to the official documentation too.

## Scope before public deployment

This project is not deployed publicly. Before making it available to other people, add authentication or other access controls, per-user usage limits, a hosting secret configuration and billing monitoring. Otherwise visitors could use your quota through your server. Do not expose `.streamlit/secrets.toml`. Model-generated Markdown is a study draft and still needs review before sharing. Only the supplied original practice notes were used for this course's recorded demonstrations.

## Official references

- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Gemini 3.8 Flash model and thinking support](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)
- [Streamlit forms](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form)
- [Streamlit secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management)

The downloadable code contains no creator API key. Create and use your own key.

# ICT from ABC — MCQ Generator

A desktop tool that generates bilingual (Sinhala / English) IT multiple-choice
questions and exports them as ready-to-use Word documents, formatted to match
**ictfromabc's exact MCQ paper layout** — same placeholders, same structure,
same legacy Sinhala font encoding used in the original papers.

You type a topic and pick a question type. The app calls the Gemini API,
gets back a structured question, and drops it straight into the correct
`.docx` template — no manual copy-pasting or reformatting.

---

## Features

- **Bilingual by default** — every question, answer, and explanation is
  generated in both English and Sinhala.
- **Three question types**, each with its own template and explanation
  style:
  - **Normal** — standard 5-option MCQ, each option explained individually.
  - **Statement** — three labelled statements (A/B/C), five combination
    answers (e.g. "A and B only"), each statement explained individually.
  - **Code** — same structure as Normal, plus an embedded code snippet and a
    single descriptive explanation paragraph.
- **Matches ictfromabc's house format exactly** — output goes straight into
  the existing `Question*.docx` templates, so fonts, spacing, and layout are
  identical to past papers.
- **Legacy Sinhala font support** — Sinhala text is automatically converted
  from Unicode to the legacy single-byte encoding ictfromabc's Word templates
  use, so it displays correctly without any manual font-fixing.
- **Simple GUI** — no command line needed.
- **Runs as a plain Python script or as a standalone Windows `.exe`.**

---

## How it works

```
Topic + Question type
        │
        ▼
files/prompt  +  topic/type  ──────►  Gemini API
                                          │
                                          ▼
                              Strict JSON response
                              (QEng, QSin, Answers, Explanations, ...)
                                          │
                                          ▼
                          UnicodeToLegacy.py converts all
                          Sinhala fields to legacy encoding
                                          │
                                          ▼
              find-and-replace into the matching template:
              QuestionNormal.docx / QuestionStatement.docx / QuestionCode.docx
                                          │
                                          ▼
                    <topic>.docx saved to "Generated Questions/"
```

The prompt (`files/prompt`) is a fixed system prompt that forces the model to
reply with **only** a JSON object matching one of three schemas below — no
extra text, no markdown fences. This is what guarantees every generated
question is structurally identical to ictfromabc's existing question bank.

---

## Question type formats

### Normal
```json
{
  "QType": "normal",
  "QEng": "...", "QSin": "...",
  "AnswersEng": [5 options], "AnswersSin": [5 options],
  "AnsNo": 3,
  "ExplEng": [5 explanations], "ExplSin": [5 explanations]
}
```
Template placeholders filled: `Question English/Sinhala`, `Answer 1-5
English/Sinhala`, `Explanation 1-5 English/Sinhala`, `QNum`.

### Statement
```json
{
  "QType": "statement",
  "QEng": "...", "QSin": "...",
  "StatementsEng": [A, B, C], "StatementsSin": [A, B, C],
  "AnswersEng": [5 combination options], "AnswersSin": [...],
  "AnsNo": 3,
  "ExplEng": [explanation of A, B, C], "ExplSin": [...]
}
```
Template placeholders filled: `StateA/B/CEng`, `StateA/B/CSin`, `Answer 1-5
English/Sinhala`, `ExplA/B/CEng`, `ExplA/B/CSin`, `QNum`.

### Code
```json
{
  "QType": "code",
  "QEng": "...", "QSin": "...",
  "Code": "exact code snippet, newlines preserved",
  "AnswersEng": [5 options], "AnswersSin": [5 options],
  "AnsNo": 3,
  "ExplEng": "single paragraph", "ExplSin": "single paragraph"
}
```
Template placeholders filled: `codelines`, `Answer 1-5 English/Sinhala`,
`ExplanationEnglish`, `ExplanationSinhala`, `QNum`.

`AnsNo` is always the 1-indexed position of the correct answer among the
five options.

---

## Project structure

```
main.py                 - GUI + generation logic
UnicodeToLegacy.py       - Unicode Sinhala -> legacy font encoding converter
apikey.txt               - your Gemini API key (plain text, one line)
files/
  prompt                 - the fixed system prompt sent to Gemini
  QuestionNormal.docx     - template for "normal" type
  QuestionStatement.docx  - template for "statement" type
  QuestionCode.docx       - template for "code" type
build.bat / build.spec   - one-click standalone .exe build (see below)
requirements.txt
```

---

## Running from source

```bash
pip install -r requirements.txt
```

1. Put your Gemini API key in `apikey.txt` (replace the placeholder text,
   one key per line).
2. Run:
   ```bash
   python main.py
   ```
3. Enter a topic, choose a question type, click **Generate**.

Output lands in a `Generated Questions/` folder created next to `main.py`
— both the final `<topic>.docx` and the raw `result.json` from the API.

---

## Building the standalone `.exe`

Double-click `build.bat` on a Windows PC with Python 3.10+ installed. It
creates a virtual environment, installs dependencies, and runs PyInstaller
using `build.spec`. The three `.docx` templates and the prompt are bundled
**inside** the resulting exe; `apikey.txt` stays **outside**, next to the
exe, so the key can be changed anytime without rebuilding.

Result: `dist\QuestionGenerator.exe` + `dist\apikey.txt`. Copy the whole
`dist` folder anywhere and run it — the two files just need to stay
together.

---

## Customizing

- **Wording/behavior of the AI**: edit `files/prompt`. Keep the JSON schema
  section intact unless you also update the corresponding placeholder names
  in `main.py`.
- **Paper layout/branding**: edit the `.docx` templates directly in Word.
  You can freely change fonts, colors, spacing, headers, logos — just don't
  rename or remove the placeholder text (e.g. `Question English`,
  `Answer 1 Sinhala`) since `main.py` searches for those exact strings.
- **Why the Sinhala converter exists**: ictfromabc's Word templates use a
  legacy single-byte Sinhala font rather than Unicode Sinhala. Pasting raw
  Unicode Sinhala text into those templates would display as garbled
  characters, so every Sinhala field is passed through
  `ConvertToLegacy()` before being inserted.

---

## Troubleshooting

- **"No API key found"** — open `apikey.txt` next to the script/exe and
  paste in a real Gemini key.
- **Sinhala text looks wrong in the output docx** — make sure the template's
  Sinhala text runs use the correct legacy Sinhala font (not a Unicode
  Sinhala font); `ConvertToLegacy()` only converts the *characters*, the
  font itself must already be set correctly in the template.
- **Unknown question type from API** — the model didn't return one of
  `normal` / `statement` / `code`; check `Generated Questions/result.json`
  for the raw response and adjust `files/prompt` if it keeps happening.

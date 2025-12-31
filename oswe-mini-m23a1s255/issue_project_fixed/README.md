# Event Registration System — Fixed (Browser Date Formats)

This repository is a fixed copy of the original demo that resolves browser
compatibility issues for `datetime-local` manual entries. The backend
now accepts multiple common date formats while remaining fully
backwards-compatible with ISO 8601.

Quick highlights
- ✅ Accepts ISO, ISO-with-seconds, slash, US AM/PM, text-month and European formats
- ✅ All tests pass: 16 passed
- ✅ No changes to the public API or behavior for Chrome/Edge users

Running the project
1. Install deps: `pip install -r requirements.txt`
2. Run tests: `pytest tests/ -v`  # expects `16 passed`
3. Run the app: `python -m src.app` and open http://localhost:5000

See `FIX_SUMMARY.md` for a concise description of what changed and why.

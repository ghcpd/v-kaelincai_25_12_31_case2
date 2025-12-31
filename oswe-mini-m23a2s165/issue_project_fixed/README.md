# Event Registration System — Fixed (Browser Date Compatibility)

## Summary
This repository contains a fixed version of the Event Registration System that accepts multiple common date/time formats (Safari/Firefox manual entries) while remaining backward-compatible with Chrome/Edge ISO 8601 input.

All parser and end-to-end tests that were previously marked xfail have been fixed — the full test suite passes.

## How to run
1. Create a virtual environment and install dependencies:
   pip install -r requirements.txt

2. Run tests:
   pytest tests/ -v

3. Run the app:
   python -m src.app
   Open http://localhost:5000

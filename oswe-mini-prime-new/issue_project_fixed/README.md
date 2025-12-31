# Issue Project (Fixed)

This is the fixed copy of the Event Registration System where the date parsing
bug has been addressed.

What's changed:
- `src/date_parser.py` now accepts multiple common date formats (ISO, slashes, US with AM/PM, text month, European)
- Tests updated to remove xfail markers and now expect successful parsing for all formats
- `FIX_SUMMARY.md` documents the changes and test results

To run:

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run tests

```bash
pytest tests/ -v
```

3. Start the app

```bash
python -m src.app
```

Visit http://localhost:5000 and try entering different date formats in the Event Date field.

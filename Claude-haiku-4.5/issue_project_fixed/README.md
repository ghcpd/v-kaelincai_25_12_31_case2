# Event Registration System - Browser Compatibility Issue Demo

## Project Overview
This is a minimal event registration system that demonstrates a **browser compatibility bug** in date/time input handling. The system works correctly in Chrome/Edge but fails for Safari and Firefox users due to HTML5 `datetime-local` input support differences.

## Bug Description
**Type:** Compatibility Bug - Browser-specific behavior  
**Impact:** Safari and Firefox users cannot complete event registration

**Problem:** The backend only accepts ISO 8601 date format (`YYYY-MM-DDTHH:MM`), which is what Chrome/Edge's native `datetime-local` picker produces. Safari and older Firefox versions don't fully support `datetime-local`, causing users to manually enter dates in various formats that are rejected by the parser.

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for detailed analysis.

## Project Structure
```
issue_project/
├── src/
│   ├── __init__.py
│   ├── app.py              # Flask web application
│   ├── event_service.py    # Registration business logic
│   ├── date_parser.py      # Date parsing module (contains bug)
│   ├── templates/
│   │   └── index.html      # Main registration page
│   └── static/
│       ├── css/
│       │   └── style.css   # Styling
│       └── js/
│           └── app.js      # Frontend JavaScript
├── tests/
│   ├── __init__.py
│   ├── test_date_parser.py      # Parser tests (4 should fail)
│   └── test_event_service.py    # Service tests (3 should fail)
├── data/
│   └── sample_submissions.json  # Example submissions from different browsers
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md          # Detailed bug analysis and fix strategies
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 11 (or any OS with Python)
- Virtual environment recommended

### Installation & Running Tests

**One-command setup and test:**
```powershell
# Install dependencies and run tests
pip install -r requirements.txt ; pytest tests/ -v
```

**Or step by step:**
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run tests
pytest tests/ -v

# 3. Run with coverage (optional)
pytest tests/ -v --cov=src --cov-report=html
```

## Expected Test Results

### Passing Tests (Chrome/Edge compatible formats)
✅ `test_date_parser.py::TestDateParserChromeEdge` - All tests pass  
✅ `test_event_service.py::TestEventServiceWithChromeEdge` - All tests pass  
✅ `test_event_service.py::TestEventServiceValidation` - All tests pass

**Total: 9 PASSED**

### Expected Failures (Safari/Firefox compatibility issues)
These tests **intentionally fail (xfail)** to demonstrate the bug exists:

❌ **test_date_parser.py**
- `TestDateParserSafariBrowserIssues::test_parse_safari_slash_format` - **XFAIL**
  - **Trigger:** User enters `"2024/01/15 14:30"` (Safari slash format)
  - **File:** [src/date_parser.py](src/date_parser.py#L47-L54)
  - **Expected:** Parse successfully
  - **Actual:** Raises `DateParseError` ❌

- `TestDateParserSafariBrowserIssues::test_parse_safari_us_format_with_am_pm` - **XFAIL**
  - **Trigger:** User enters `"01/15/2024 02:30 PM"` (US format with AM/PM)
  - **Expected:** Parse to 24-hour time
  - **Actual:** Raises `DateParseError` ❌

- `TestDateParserFirefoxBrowserIssues::test_parse_firefox_text_month_format` - **XFAIL**
  - **Trigger:** User enters `"Jan 15, 2024 14:30"` (text month)
  - **Expected:** Parse successfully
  - **Actual:** Raises `DateParseError` ❌

- `TestDateParserFirefoxBrowserIssues::test_parse_firefox_european_format` - **XFAIL**
  - **Trigger:** User enters `"15-01-2024 14:30"` (DD-MM-YYYY)
  - **Expected:** Parse successfully
  - **Actual:** Raises `DateParseError` ❌

❌ **test_event_service.py**
- `TestEventServiceSafariBrowserIssues::test_registration_fails_with_safari_slash_format` - **XFAIL**
  - **Full flow:** Safari user submits registration → parsing fails → registration rejected

- `TestEventServiceSafariBrowserIssues::test_registration_fails_with_us_date_format` - **XFAIL**
  - **Full flow:** US-locale Safari user → date rejected → cannot register

- `TestEventServiceFirefoxBrowserIssues::test_registration_fails_with_firefox_text_month` - **XFAIL**
  - **Full flow:** Firefox user with text month → parsing fails → registration blocked

**Total: 7 XFAILED**

### Summary Output
```
================================================================
9 passed, 7 xfailed in 0.13s
================================================================
```

**What does this mean?**
- ✅ **9 passed** - Core functionality works for Chrome/Edge
- ❌ **7 xfailed** - Expected failures showing the bug exists for Safari/Firefox

**After fixing the bug**, all 16 tests should pass!

> **❓ Why do tests "pass" when there's a bug?**  
> We use `@pytest.mark.xfail` to mark expected failures. See [TESTING_STRATEGY.md](TESTING_STRATEGY.md) for detailed explanation of why this is the correct approach.

## Running the Web Application

```powershell
# Start the Flask development server
python -m src.app
```

Then open http://localhost:5000 in your browser.

**Interactive Features:**
1. **Registration Form** - Try registering with different browsers
2. **Test Format Buttons** - Click to test different date formats instantly
3. **Browser Detection** - See your current browser's datetime-local support
4. **Live Registrations List** - View all successful registrations
5. **Debug Panel** - See technical details about each submission

**Test the bug manually:**
1. Open in different browsers (Chrome, Edge, Safari, Firefox)
2. Notice how the datetime input field looks different
3. In Chrome/Edge: Use the native date picker → Registration succeeds ✅
4. In Safari/Firefox: 
   - Try using the date picker (if available)
   - OR manually type a date like "2025/06/15 14:30"
   - Submit and observe registration failure ❌
5. Use the "Test Different Formats" buttons to quickly see which formats work

## Bug Location

**Primary Issue:**
- **File:** [src/date_parser.py](src/date_parser.py)
- **Method:** `DateParser.parse_event_datetime()` (lines 38-54)
- **Problem:** Only accepts ISO 8601 format, no fallback parsing

**Propagation:**
- **File:** [src/event_service.py](src/event_service.py)
- **Method:** `EventService.register_participant()` (lines 45-62)
- **Effect:** Converts `DateParseError` to `RegistrationError`, blocking user

## Example Data

See [data/sample_submissions.json](data/sample_submissions.json) for examples of:
- ✅ Successful submissions from Chrome/Edge
- ❌ Failed submissions from Safari/Firefox
- Statistics showing 67% failure rate (4 out of 6 attempts)

## Bug Fix Strategies

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for detailed fix recommendations, including:
1. Multi-format parsing approach
2. Using python-dateutil library
3. Client-side polyfill solution
4. Recommended combined approach

**Note:** This repository intentionally contains the bug unfixed for demonstration purposes.

## Testing Strategy

The test suite is designed to:
1. ✅ Verify correct behavior with Chrome/Edge ISO format
2. ❌ Demonstrate failures with Safari/Firefox manual formats
3. Document expected behavior in test docstrings
4. Provide clear assertion messages
5. Include TODO comments for post-fix validation

After implementing a fix, all tests should pass.

## Dependencies

- **flask** (3.0.0) - Web framework
- **pytest** (7.4.3) - Testing framework
- **pytest-flask** (1.3.0) - Flask testing utilities
- **python-dateutil** (2.8.2) - Already included for potential fix

## Browser Support Status

| Browser | Version | datetime-local Support | Status |
|---------|---------|------------------------|---------|
| Chrome | 120+ | ✅ Full | ✅ Works |
| Edge | 120+ | ✅ Full | ✅ Works |
| Safari | 16+ | ⚠️ Partial | ❌ Fails (manual entry) |
| Safari iOS | 15+ | ⚠️ Partial | ❌ Fails (manual entry) |
| Firefox | 100+ | ⚠️ Partial/None | ❌ Fails (manual entry) |

## Additional Notes

- All tests use future dates to avoid "past event" validation errors
- Error messages in tests document expected fix behavior
- The bug is simple and focused - no concurrent/cache/database complexity
- Tests clearly indicate which browser scenario they represent
- Code includes extensive comments explaining the bug

## License

This is a demo project for bug reproduction purposes.

## Contact

For questions about this bug demo, see [KNOWN_ISSUE.md](KNOWN_ISSUE.md).

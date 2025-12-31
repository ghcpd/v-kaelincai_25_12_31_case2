# Known Issue: Browser Date Format Compatibility

## Issue Type
**Bug Category:** Compatibility  
**Subcategory:** Browser-specific behavior  
**Severity:** High - blocks user registration on Safari/Firefox

## Problem Summary
The Event Registration System only accepts ISO 8601 date format (`YYYY-MM-DDTHH:MM`), which is the standard output of HTML5 `datetime-local` input in Chrome/Edge. However, Safari and older Firefox versions do not fully support `datetime-local`, causing users to manually enter dates in various formats that are subsequently rejected by the backend parser.

## Affected Components
- **File:** [src/date_parser.py](src/date_parser.py)
- **Method:** `DateParser.parse_event_datetime()` (lines 38-54)
- **Impact:** Registration fails for Safari/Firefox users who cannot use native date pickers

## Trigger Conditions

### Working Scenario (Chrome/Edge)
1. User opens registration form in Chrome or Edge
2. Browser displays native `datetime-local` picker
3. User selects date/time from calendar UI
4. Form submits ISO 8601 format: `"2025-06-15T14:30"`
5. Backend parses successfully ✅

### Failing Scenario (Safari/Firefox)
1. User opens registration form in Safari or old Firefox
2. `datetime-local` input degrades to text input (no native picker)
3. User manually types date in natural format:
   - Safari (US): `"06/15/2025 02:30 PM"`
   - Safari (International): `"2025/06/15 14:30"`
   - Firefox: `"Jun 15, 2025 14:30"` or `"15-06-2025 14:30"`
4. Form submits non-ISO format
5. Backend raises `DateParseError` ❌
6. User sees error: "Invalid date format. Expected ISO 8601 format"
7. **Registration fails - user cannot complete signup**

## Expected vs Actual Behavior

**Expected:**
- System should accept common date formats from all browsers
- Fallback parsing should handle manual date entry formats
- All users should be able to register successfully

**Actual:**
- Only ISO 8601 format accepted
- Safari/Firefox users with manual entry are rejected
- ~67% of attempts fail (see [data/sample_submissions.json](data/sample_submissions.json))

## Root Cause
The `parse_event_datetime()` method in [src/date_parser.py](src/date_parser.py#L47-L54) only attempts to parse ISO 8601 format using `datetime.fromisoformat()`. When this fails, it immediately raises an error without attempting alternative format parsing.

```python
# Current implementation (lines 47-54)
try:
    parsed_date = datetime.fromisoformat(date_string)
    return parsed_date
except ValueError:
    # BUG: No fallback parsing for other formats
    raise DateParseError(f"Invalid date format: '{date_string}'...")
```

## Reproduction Steps

### Automated Test Reproduction
Run the test suite to see failing tests:
```powershell
pytest tests/ -v
```

**Expected Failures:**
- `test_date_parser.py::TestDateParserSafariBrowserIssues::test_parse_safari_slash_format`
- `test_date_parser.py::TestDateParserSafariBrowserIssues::test_parse_safari_us_format_with_am_pm`
- `test_date_parser.py::TestDateParserFirefoxBrowserIssues::test_parse_firefox_text_month_format`
- `test_date_parser.py::TestDateParserFirefoxBrowserIssues::test_parse_firefox_european_format`
- `test_event_service.py::TestEventServiceSafariBrowserIssues::test_registration_fails_with_safari_slash_format`
- `test_event_service.py::TestEventServiceSafariBrowserIssues::test_registration_fails_with_us_date_format`
- `test_event_service.py::TestEventServiceFirefoxBrowserIssues::test_registration_fails_with_firefox_text_month`

### Manual Reproduction
1. Start the Flask app: `python -m src.app`
2. Open http://localhost:5000 in Safari or Firefox
3. Try to register with manual date entry (any format except ISO)
4. Observe registration failure

## Impact Analysis

### User Impact
- **Safari users (macOS/iOS):** Cannot register if manually entering dates
- **Firefox users (older versions):** Cannot register without native picker
- **Market share:** ~30-40% of users affected (Safari + Firefox combined)
- **User frustration:** Error message doesn't clearly explain how to format date

### Business Impact
- Lost registrations/conversions
- Poor user experience for significant user segment
- Support tickets from confused users
- Browser discrimination (Chrome/Edge only)

## Fix Strategy (Recommendations)

### Option 1: Multi-Format Parsing (Recommended)
Enhance `DateParser.parse_event_datetime()` to try multiple format patterns:

```python
def parse_event_datetime(date_string: str) -> datetime:
    formats = [
        "%Y-%m-%dT%H:%M",           # ISO 8601 (Chrome/Edge)
        "%Y-%m-%dT%H:%M:%S",        # ISO with seconds
        "%Y/%m/%d %H:%M",           # Safari slash format
        "%m/%d/%Y %I:%M %p",        # US format with AM/PM
        "%d-%m-%Y %H:%M",           # European format
        "%b %d, %Y %H:%M",          # Text month
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    raise DateParseError(f"Could not parse date: {date_string}")
```

**Pros:** 
- Handles all common formats
- Minimal code changes
- Backward compatible

**Cons:**
- Ambiguous dates (e.g., "01/02/2025" - is it Jan 2 or Feb 1?)
- May need locale detection

### Option 2: Use dateutil.parser (Alternative)
Use the robust `python-dateutil` library (already in requirements):

```python
from dateutil import parser

def parse_event_datetime(date_string: str) -> datetime:
    try:
        return parser.parse(date_string)
    except (ValueError, parser.ParserError):
        raise DateParseError(f"Could not parse date: {date_string}")
```

**Pros:**
- Handles many formats automatically
- Well-tested library
- Less code to maintain

**Cons:**
- May be too permissive
- Less control over accepted formats

### Option 3: Client-Side Polyfill (Frontend Fix)
Add JavaScript polyfill to provide date picker on all browsers:

```html
<script src="flatpickr.min.js"></script>
<script>
  flatpickr("#event_datetime", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",  // Always outputs ISO format
  });
</script>
```

**Pros:**
- Consistent UI across all browsers
- Backend changes not needed
- Better UX

**Cons:**
- Adds JavaScript dependency
- Doesn't fix backend brittleness
- Users with JS disabled still fail

### Recommended Approach
**Combine Option 1 and Option 3:**
1. Add frontend polyfill for consistent UX
2. Enhance backend to accept multiple formats as safety net
3. This provides defense in depth

## Testing Requirements
After implementing fix:
1. All currently failing tests should pass
2. Add additional tests for edge cases:
   - Ambiguous date handling
   - Invalid/malformed dates still rejected
   - Timezone handling (if needed)
3. Manual browser testing:
   - Safari (macOS + iOS)
   - Firefox (Windows/Linux)
   - Chrome/Edge (regression testing)

## Related Files
- [src/date_parser.py](src/date_parser.py) - Core issue location
- [src/event_service.py](src/event_service.py) - Propagates parsing errors
- [tests/test_date_parser.py](tests/test_date_parser.py) - Failing tests for date parsing
- [tests/test_event_service.py](tests/test_event_service.py) - Failing tests for registration flow
- [data/sample_submissions.json](data/sample_submissions.json) - Example data showing failure patterns

## Priority
**High** - This bug prevents a significant portion of users (Safari/Firefox) from completing the primary user flow (event registration).

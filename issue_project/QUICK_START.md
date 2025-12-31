# Quick Start Guide

## 🚀 Launch the Web Application

```powershell
# From the project directory
python -m src.app
```

Then open http://localhost:5000 in your browser.

## 🎯 How to Experience the Bug

### Method 1: Interactive Web Interface

1. **Open in Chrome/Edge:**
   - Click on the "Event Date & Time" field
   - Use the native date picker (calendar UI appears)
   - Select any future date and time
   - Fill in name and email
   - Click "Register Now"
   - ✅ **Result:** Registration succeeds!

2. **Open in Safari/Firefox:**
   - The datetime field may show as plain text input
   - Try entering: `2025/06/15 14:30`
   - Fill in name and email
   - Click "Register Now"
   - ❌ **Result:** Registration fails with error!

3. **Use Test Format Buttons:**
   - Scroll to "Test Different Date Formats" section
   - Click each button to instantly test different formats:
     - ✅ "ISO Format (Works)" → Succeeds
     - ❌ "Safari Slash Format" → Fails
     - ❌ "US Format with AM/PM" → Fails
     - ❌ "Text Month Format" → Fails

### Method 2: Automated Tests

```powershell
pytest tests/ -v
```

Watch tests demonstrate:
- ✅ Chrome/Edge formats work (10 tests pass)
- ❌ Safari/Firefox formats fail (7 tests verify the bug)

## 🎨 Frontend Features

### Main Page Sections

1. **Browser Compatibility Status**
   - Color-coded browser support indicators
   - Green for Chrome/Edge (supported)
   - Yellow for Safari/Firefox (warnings)

2. **Registration Form**
   - Name, Email, Date/Time inputs
   - Live validation
   - Error/success messages

3. **Test Format Buttons**
   - One-click testing of different date formats
   - Instant feedback showing which formats fail

4. **Current Registrations**
   - Live list of successful registrations
   - Refresh button to update

5. **Debug Panel**
   - Shows browser detection
   - datetime-local support status
   - Current input values
   - API response details

## 📱 Try in Different Browsers

### Chrome/Edge (Working)
```
✅ Native date picker appears
✅ Submits ISO format: "2025-06-15T14:30"
✅ Registration succeeds
```

### Safari (Bug Triggered)
```
⚠️ Limited date picker support
❌ Manual entry with slashes fails: "2025/06/15 14:30"
❌ US format fails: "06/15/2025 02:30 PM"
❌ Registration blocked
```

### Firefox (Bug Triggered)
```
⚠️ Older versions: no date picker
❌ Text month fails: "Jun 15, 2025 14:30"
❌ European format fails: "15-06-2025 14:30"
❌ Registration blocked
```

## 🔍 Observing the Bug

### What You'll See in Safari/Firefox:

1. **Before Submission:**
   - Datetime input may look like plain text field
   - No calendar picker appears (or limited)
   - User types date manually in natural format

2. **After Submission:**
   - ❌ Error message appears:
     ```
     Registration Failed: Failed to register: Invalid date format: 
     '2025/06/15 14:30'. Expected ISO 8601 format (YYYY-MM-DDTHH:MM), 
     e.g., '2025-01-15T10:00'
     ```
   - Registration is rejected
   - User cannot complete signup

3. **Debug Panel Shows:**
   - Browser: Safari/Firefox
   - datetime-local Support: Limited or No
   - Error details from backend

## 📊 Understanding the Problem

The frontend HTML uses:
```html
<input type="datetime-local" id="event_datetime" name="event_datetime">
```

**Chrome/Edge Behavior:**
- Displays native date/time picker
- Always outputs ISO format: `"YYYY-MM-DDTHH:MM"`
- Backend accepts it ✅

**Safari/Firefox Behavior:**
- No picker (or limited support)
- User manually types date
- Uses natural formats: `"MM/DD/YYYY HH:MM AM/PM"`, `"YYYY/MM/DD HH:MM"`
- Backend rejects it ❌

## 🛠️ Files to Explore

**Frontend:**
- [src/templates/index.html](src/templates/index.html) - HTML structure
- [src/static/css/style.css](src/static/css/style.css) - Styling
- [src/static/js/app.js](src/static/js/app.js) - JavaScript logic

**Backend (Bug Location):**
- [src/date_parser.py](src/date_parser.py#L47-L54) - Only accepts ISO format

**Tests:**
- [tests/test_date_parser.py](tests/test_date_parser.py) - Format parsing tests
- [tests/test_event_service.py](tests/test_event_service.py) - End-to-end tests

**Documentation:**
- [KNOWN_ISSUE.md](KNOWN_ISSUE.md) - Complete bug analysis & fix strategies

## 💡 Next Steps

After experiencing the bug, see [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for:
- Detailed root cause analysis
- Impact on real users
- Three recommended fix strategies
- Testing requirements post-fix

Enjoy exploring the browser compatibility bug! 🐛

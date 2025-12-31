# Bug Fix Task - Browser Date Format Compatibility Issue

## Task Overview
You are given a buggy Event Registration System project that has browser compatibility issues. Your task is to create a **fixed version** of this project in a new directory while keeping the original intact.

## Current Project Status

### Directory Structure (Buggy Version)
```
issue_project/
├── src/
│   ├── __init__.py
│   ├── app.py              # Flask application
│   ├── event_service.py    # Registration business logic
│   ├── date_parser.py      # 🐛 BUG IS HERE
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── tests/
│   ├── __init__.py
│   ├── test_date_parser.py      # 4 tests marked as xfail
│   └── test_event_service.py    # 3 tests marked as xfail
├── data/
│   └── sample_submissions.json
├── requirements.txt
├── README.md
├── KNOWN_ISSUE.md          # Read this for bug details
├── TESTING_STRATEGY.md
└── QUICK_START.md
```

### Current Test Results
```
9 passed, 7 xfailed in 0.13s
```

- **9 passed**: Chrome/Edge functionality works
- **7 xfailed**: Safari/Firefox compatibility is broken (expected failures)

## The Bug

**Location**: `src/date_parser.py` - `parse_event_datetime()` method

**Problem**: The parser only accepts ISO 8601 format (`YYYY-MM-DDTHH:MM`), which Chrome/Edge produce from native `datetime-local` input. Safari and Firefox users who manually enter dates in other common formats get rejected.

**Failing Formats**:
- Safari slash format: `"2024/06/15 14:30"`
- US format with AM/PM: `"06/15/2024 02:30 PM"`
- Text month format: `"Jun 15, 2024 14:30"`
- European format: `"15-06-2024 14:30"`

**Impact**: 7 tests are marked as `xfail` (expected failures) and need to pass after your fix.

## Your Task

### 1. Create Fixed Version in New Directory

Create a new project directory with this structure:
```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── event_service.py
│   ├── date_parser.py      # 🔧 FIX THE BUG HERE
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── tests/
│   ├── __init__.py
│   ├── test_date_parser.py      # Remove xfail markers
│   └── test_event_service.py    # Remove xfail markers
├── data/
│   └── sample_submissions.json
├── requirements.txt
├── README.md               # Update to reflect fixes
└── FIX_SUMMARY.md         # Document what you changed
```

### 2. Requirements for the Fix

**Must Do**:
- ✅ Copy all files from `issue_project/` to `issue_project_fixed/`
- ✅ Fix the date parsing logic to accept multiple common date formats
- ✅ Remove all `@pytest.mark.xfail` decorators from tests
- ✅ Ensure all 16 tests pass (not 9 passed + 7 xfailed)
- ✅ Maintain backward compatibility (ISO format must still work)
- ✅ Do NOT modify the original `issue_project/` directory

**Test Success Criteria**:
```bash
# After fix, running tests should show:
16 passed in X.XXs
```

**Format Support Required**:
1. ISO 8601 (already works): `"2024-06-15T14:30"`
2. ISO with seconds: `"2024-06-15T14:30:00"`
3. Slash format: `"2024/06/15 14:30"`
4. US format with AM/PM: `"06/15/2024 02:30 PM"`
5. Text month: `"Jun 15, 2024 14:30"`
6. European format: `"15-06-2024 14:30"`

### 3. Create Documentation

Create `FIX_SUMMARY.md` documenting:
- What was broken
- What you changed (which files, which functions)
- How your solution works
- Why you chose this approach
- Test results before and after

### 4. Validation Steps

After implementing your fix:

**Step 1**: Run tests
```bash
cd issue_project_fixed
pytest tests/ -v
```
Expected: `16 passed`

**Step 2**: Test with sample data
Verify the fixed parser handles all formats in `data/sample_submissions.json`

**Step 3**: Run web application
```bash
python -m src.app
```
Visit http://localhost:5000 and test different date formats

## Hints (Read Only If Stuck)

<details>
<summary>Hint 1: Where to look for solution ideas</summary>

Check `KNOWN_ISSUE.md` in the original project - it contains fix strategies but doesn't show implementation.
</details>

<details>
<summary>Hint 2: What needs to change</summary>

Only `src/date_parser.py` needs functional changes. Tests just need xfail markers removed.
</details>

<details>
<summary>Hint 3: Available tools</summary>

The `python-dateutil` library is already in requirements.txt - it has powerful date parsing capabilities.
</details>

## Constraints

- **DO NOT**: Modify files in `issue_project/` directory
- **DO NOT**: Simplify or remove tests
- **DO NOT**: Change the API of `parse_event_datetime()` function
- **DO NOT**: Add new dependencies beyond what's in requirements.txt
- **MUST**: All original functionality must continue to work
- **MUST**: Fix must be production-quality (handle edge cases, errors gracefully)

## Success Definition

Your fix is successful when:
1. ✅ New directory `issue_project_fixed/` exists with complete project
2. ✅ All 16 tests pass (no xfail, no failures)
3. ✅ Web application works for all browsers
4. ✅ Original `issue_project/` remains unchanged
5. ✅ `FIX_SUMMARY.md` clearly documents changes

## Getting Started

1. Read `issue_project/KNOWN_ISSUE.md` for detailed bug analysis
2. Read `issue_project/TESTING_STRATEGY.md` to understand test approach
3. Review failing test cases to understand requirements
4. Create `issue_project_fixed/` directory
5. Copy all files from original project
6. Implement your fix in `src/date_parser.py`
7. Remove xfail markers from tests
8. Run tests until all pass
9. Document your changes

## Relative Path Reference

All paths should be relative to the workspace root:
```
workspace_root/
├── issue_project/          # Original buggy version (DO NOT MODIFY)
└── issue_project_fixed/    # Your fixed version (CREATE THIS)
```

When running commands:
```bash
# Install dependencies
cd issue_project_fixed
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start web app
python -m src.app
```

Good luck! Focus on making all tests pass while maintaining code quality and proper error handling.

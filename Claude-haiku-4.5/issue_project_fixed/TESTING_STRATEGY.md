# Testing Strategy Explanation

## Why Do We Use `@pytest.mark.xfail`?

You might wonder: **"Why do all tests pass when there's a bug?"**

The answer is: We use **expected failures** (`xfail`) to properly demonstrate the bug.

## Two Approaches to Testing

### ❌ BAD Approach (What we had before)
```python
def test_safari_format(self):
    # Verify the bug EXISTS by asserting an error is raised
    with pytest.raises(DateParseError):
        parser.parse_event_datetime("2024/01/15 14:30")
    # Test PASSES when bug exists ✅
    # Test FAILS when bug is fixed ❌
    # This is backwards!
```

**Problem:** Test passes when the bug exists, fails when fixed. This is counterintuitive!

### ✅ GOOD Approach (What we have now)
```python
@pytest.mark.xfail(reason="BUG: Parser rejects Safari format", strict=True)
def test_safari_format(self):
    # Test what SHOULD happen
    result = parser.parse_event_datetime("2024/01/15 14:30")
    assert result.year == 2024
    # Test FAILS (xfail) when bug exists ❌
    # Test PASSES when bug is fixed ✅
    # This is intuitive!
```

**Benefits:** 
- Test describes the **expected correct behavior**
- Test fails when bug exists (marked as xfail)
- Test passes when bug is fixed
- Natural progression: xfail → pass

## Test Result Meanings

### Current State (Bug Exists)
```bash
9 passed, 7 xfailed
```

- **9 passed** = Chrome/Edge functionality works correctly ✅
- **7 xfailed** = Safari/Firefox support is broken (expected failure) ❌

### After Fixing the Bug
```bash
16 passed
```

All tests pass! The expected failures become real passes. ✅

## Understanding `xfail`

`@pytest.mark.xfail` tells pytest:
- "This test documents correct behavior"
- "But we expect it to fail right now due to a known bug"
- "Mark it as xfail, not a real failure"

**Parameters:**
- `reason="..."` - Explains WHY it fails
- `strict=True` - Ensures the test actually does fail (catches if bug is accidentally fixed)

## Viewing Test Details

### See which tests are xfailing:
```powershell
pytest tests/ -v
```

### See detailed failure reasons:
```powershell
pytest tests/ -v -rx
```

### Run only xfail tests:
```powershell
pytest tests/ -m xfail
```

### Run without xfail markers (see actual failures):
```powershell
pytest tests/ --runxfail
```

This will show 7 real failures with stack traces.

## Benefits of This Approach

1. **Self-Documenting Code**
   - Tests show what behavior SHOULD be
   - Reason explains the current limitation

2. **Progress Tracking**
   - Easy to see: 9 working, 7 broken
   - After fix: All 16 working

3. **Prevents Regression**
   - If bug is fixed but then reintroduced, xfail becomes xpass (unexpected pass)
   - This alerts you that something changed

4. **Clear Fix Goal**
   - Goal: Make all xfail tests pass
   - No need to rewrite tests after fixing

## Example: Fixing One Bug

**Before Fix:**
```
test_parse_safari_slash_format XFAIL
```

**Implement Multi-Format Parsing:**
```python
def parse_event_datetime(date_string: str) -> datetime:
    formats = [
        "%Y-%m-%dT%H:%M",    # ISO
        "%Y/%m/%d %H:%M",    # Safari slash
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
```

**After Fix:**
```
test_parse_safari_slash_format PASSED ✅
```

The test didn't change - the code did!

## Summary

| Test Result | Meaning | Action Needed |
|-------------|---------|---------------|
| **PASSED** | Feature works correctly | None ✅ |
| **XFAIL** | Known bug, expected failure | Fix the bug 🔧 |
| **FAILED** | Unexpected failure | Investigate! 🚨 |
| **XPASS** | Bug was fixed but test still marked xfail | Remove xfail marker 🎉 |

This testing strategy makes it crystal clear:
- What works (9 tests)
- What's broken (7 tests)
- What needs fixing (the 7 xfail tests)

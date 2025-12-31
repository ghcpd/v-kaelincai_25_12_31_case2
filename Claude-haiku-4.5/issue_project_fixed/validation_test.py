#!/usr/bin/env python
"""
Validation test script for date parser functionality
Tests all supported date formats and edge cases
"""

from src.date_parser import DateParser, DateParseError
from datetime import datetime

parser = DateParser()

# Test all supported formats
test_cases = [
    ("2024-06-15T14:30", "ISO 8601 (Chrome/Edge)"),
    ("2024-06-15T14:30:00", "ISO 8601 with seconds"),
    ("2024/06/15 14:30", "Slash format (Safari)"),
    ("06/15/2024 02:30 PM", "US format with AM/PM"),
    ("Jun 15, 2024 14:30", "Text month (Firefox)"),
    ("15-06-2024 14:30", "European format"),
]

print("=" * 70)
print("DATE PARSER VALIDATION - Testing All Supported Formats")
print("=" * 70)
print()

passed = 0
failed = 0

for date_string, format_name in test_cases:
    try:
        result = parser.parse_event_datetime(date_string)
        print(f"✓ PASS | {format_name:30} | Input: '{date_string:25}'")
        print(f"       | Parsed result: {result.strftime('%Y-%m-%d %H:%M:%S')}")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL | {format_name:30} | Input: '{date_string:25}'")
        print(f"       | Error: {e}")
        failed += 1
    print()

print("=" * 70)
print("EDGE CASES - Expected Failures")
print("=" * 70)
print()

edge_cases = [
    ("", "Empty string"),
    (None, "None value"),
    ("invalid-date-xyz", "Invalid date"),
    ("99/99/9999 25:99", "Invalid date components"),
]

edge_passed = 0
edge_failed = 0

for date_string, case_name in edge_cases:
    try:
        result = parser.parse_event_datetime(date_string)
        print(f"✗ FAIL | {case_name:20} | Should have raised error but got: {result}")
        edge_failed += 1
    except DateParseError as e:
        print(f"✓ PASS | {case_name:20} | Correctly raised DateParseError")
        edge_passed += 1
    except Exception as e:
        print(f"✗ FAIL | {case_name:20} | Wrong error type: {type(e).__name__}")
        edge_failed += 1
    print()

print("=" * 70)
print("DISPLAY FORMATTING")
print("=" * 70)
print()

dt = datetime(2024, 6, 15, 14, 30)
formatted = parser.format_for_display(dt)
print(f"✓ PASS | Display formatting works correctly")
print(f"       | Input: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"       | Output: {formatted}")
print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Format tests:    {passed} passed, {failed} failed")
print(f"Edge case tests: {edge_passed} passed, {edge_failed} failed")
print(f"Total:          {passed + edge_passed} passed, {failed + edge_failed} failed")
print()

if failed == 0 and edge_failed == 0:
    print("✓ ALL VALIDATION TESTS PASSED")
    exit(0)
else:
    print("✗ SOME VALIDATION TESTS FAILED")
    exit(1)

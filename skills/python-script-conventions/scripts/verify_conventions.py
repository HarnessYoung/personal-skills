#!/usr/bin/env python3
"""
Verify Python Script Conventions

Checks whether a Python script follows the conventions defined in the
python-script-conventions skill.

Usage:
    python3 verify_conventions.py path/to/script.py
    python3 verify_conventions.py path/to/script.py --verbose

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class CheckResult(NamedTuple):
    """Result of a single verification check."""
    passed: bool
    message: str
    severity: str = "error"  # "error" or "warning"


def check_section_headers(content: str) -> CheckResult:
    """Verify that section headers are present and in the correct order."""
    expected_sections = [
        "# ==================== §1 IMPORTS ====================",
        "# ==================== §3 CONSTANTS ====================",
        "# ==================== §6 CORE LOGIC ====================",
    ]
    
    # For standalone scripts, also check for MAIN section
    has_main_guard = 'if __name__ == "__main__"' in content
    if has_main_guard:
        expected_sections.append("# ==================== §7 MAIN EXECUTION ====================")
    
    missing = []
    for section in expected_sections:
        # Allow flexible numbering (§1-7) but check for presence
        pattern = section.replace("§", "§?\\d+")
        if not re.search(re.escape(section).replace(r"\§\d\+", "§\\d+"), content):
            missing.append(section)
    
    if missing:
        return CheckResult(False, f"Missing section headers: {missing}")
    return CheckResult(True, "Section headers present")


def check_imports_location(content: str) -> CheckResult:
    """Check that all imports are in the IMPORTS section."""
    lines = content.split("\n")
    in_imports_section = False
    imports_section_ended = False
    violations = []
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Track IMPORTS section boundaries
        if "IMPORTS" in line and "====" in line:
            in_imports_section = True
            continue
        
        if in_imports_section and "====" in line and "IMPORTS" not in line:
            in_imports_section = False
            imports_section_ended = True
            continue
        
        # Check for imports outside IMPORTS section
        if imports_section_ended and (stripped.startswith("import ") or stripped.startswith("from ")):
            # Allow imports in docstrings or comments
            if not (line.lstrip().startswith("#") or line.lstrip().startswith('"""') or line.lstrip().startswith("'")):
                violations.append(f"Line {i}: {stripped[:50]}")
    
    if violations:
        return CheckResult(False, f"Imports outside IMPORTS section:\n  " + "\n  ".join(violations[:5]))
    return CheckResult(True, "All imports in IMPORTS section")


def check_no_print_calls(content: str) -> CheckResult:
    """Check that there are no print() calls (should use logger instead)."""
    lines = content.split("\n")
    violations = []
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Look for print( but not in comments or docstrings
        if "print(" in stripped and not stripped.startswith("#"):
            # Skip if it's in a docstring or string literal
            if '"""' not in stripped and "'''" not in stripped:
                violations.append(f"Line {i}: {stripped[:60]}")
    
    if violations:
        return CheckResult(False, f"Found print() calls (use logger instead):\n  " + "\n  ".join(violations[:5]))
    return CheckResult(True, "No print() calls found")


def check_entry_point(content: str) -> CheckResult:
    """Check for the standard entry point pattern."""
    has_main_guard = 'if __name__ == "__main__"' in content
    has_sys_exit = "sys.exit(main())" in content
    
    if not has_main_guard:
        return CheckResult(False, 'Missing: if __name__ == "__main__":', severity="warning")
    
    if has_main_guard and not has_sys_exit:
        return CheckResult(False, 'Has __main__ guard but missing: sys.exit(main())')
    
    return CheckResult(True, "Entry point pattern correct")


def check_pathlib_usage(content: str) -> CheckResult:
    """Check for pathlib.Path usage vs os.path."""
    violations = []
    lines = content.split("\n")
    
    os_path_patterns = [
        (r"os\.path\.join", "os.path.join"),
        (r"os\.path\.exists", "os.path.exists"),
        (r"os\.path\.dirname", "os.path.dirname"),
        (r"os\.path\.basename", "os.path.basename"),
    ]
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        
        for pattern, name in os_path_patterns:
            if re.search(pattern, stripped):
                violations.append(f"Line {i}: {name} (use pathlib.Path instead)")
    
    if violations:
        return CheckResult(False, f"Use pathlib.Path instead of os.path:\n  " + "\n  ".join(violations[:5]))
    return CheckResult(True, "Using pathlib.Path")


def check_dataclass_flags(content: str) -> CheckResult:
    """Check that dataclasses use the recommended flags."""
    violations = []
    lines = content.split("\n")
    
    for i, line in enumerate(lines, 1):
        if "@dataclass" in line and not line.strip().startswith("#"):
            # Check if it has the recommended flags
            if "kw_only=True" not in line and "slots=True" not in line:
                violations.append(f"Line {i}: Missing kw_only=True, slots=True, frozen=True")
    
    if violations:
        return CheckResult(False, "Dataclass missing recommended flags:\n  " + "\n  ".join(violations), severity="warning")
    return CheckResult(True, "Dataclass flags correct")


def check_loguru_usage(content: str) -> CheckResult:
    """Check that loguru is imported and used (for standalone scripts)."""
    has_main = 'if __name__ == "__main__"' in content
    
    if not has_main:
        # Library module, loguru is optional
        return CheckResult(True, "Library module (loguru optional)")
    
    has_loguru_import = "from loguru import logger" in content
    
    if not has_loguru_import:
        return CheckResult(False, "Standalone script missing: from loguru import logger")
    
    return CheckResult(True, "Loguru imported")


def verify_script(script_path: Path, verbose: bool = False) -> bool:
    """Run all verification checks on a script."""
    if not script_path.exists():
        print(f"❌ Error: File not found: {script_path}", file=sys.stderr)
        return False
    
    content = script_path.read_text(encoding="utf-8")
    
    checks = [
        ("Section Headers", check_section_headers),
        ("Import Location", check_imports_location),
        ("No print() Calls", check_no_print_calls),
        ("Entry Point Pattern", check_entry_point),
        ("pathlib Usage", check_pathlib_usage),
        ("Dataclass Flags", check_dataclass_flags),
        ("Loguru Import", check_loguru_usage),
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func(content)
        results.append((name, result))
    
    # Print results
    print(f"\n{'='*70}")
    print(f"Verification Results: {script_path.name}")
    print(f"{'='*70}\n")
    
    errors = 0
    warnings = 0
    
    for name, result in results:
        if result.passed:
            symbol = "✓"
            color = "\033[92m"  # Green
        elif result.severity == "warning":
            symbol = "⚠"
            color = "\033[93m"  # Yellow
            warnings += 1
        else:
            symbol = "✗"
            color = "\033[91m"  # Red
            errors += 1
        
        reset = "\033[0m"
        print(f"{color}{symbol}{reset} {name}")
        
        if not result.passed and (verbose or result.severity == "error"):
            print(f"  {result.message}\n")
    
    # Summary
    print(f"\n{'='*70}")
    if errors == 0 and warnings == 0:
        print("✓ All checks passed!")
    else:
        print(f"Errors: {errors}, Warnings: {warnings}")
    print(f"{'='*70}\n")
    
    return errors == 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify Python script follows python-script-conventions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "script",
        type=Path,
        help="Path to Python script to verify",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all check details",
    )
    
    args = parser.parse_args()
    
    success = verify_script(args.script, verbose=args.verbose)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

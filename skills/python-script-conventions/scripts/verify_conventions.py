#!/usr/bin/env python3
# Convention-exempt: CLI tool using print() for formatted output
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

Note: This CLI verification tool uses print() for terminal output, which is
appropriate for its purpose. Regular scripts should use loguru.
"""

# ==================== §1 IMPORTS ====================
import argparse
import ast
import re
import sys
from pathlib import Path
from typing import NamedTuple

# Note: This script uses print() for output formatting, which is appropriate
# for a CLI tool that reports to stdout/stderr. Normal scripts should use loguru.

# ==================== §3 CONSTANTS ====================
# (No constants in this script)

# ==================== §6 CORE LOGIC ====================


class CheckResult(NamedTuple):
    """Result of a single verification check."""
    passed: bool
    message: str
    severity: str = "error"  # "error" or "warning"


def check_section_headers(content: str) -> CheckResult:
    """Verify that section headers are present and in the correct order."""
    # Accept both formats:
    # Format 1 (template): # ==================== §N SECTION ====================
    # Format 2 (SKILL.md): # =============================================================================
    #                      # SECTION
    #                      # =============================================================================
    
    has_main_guard = 'if __name__ == "__main__"' in content
    
    # For standalone scripts, check for IMPORTS, CONSTANTS, CORE LOGIC, and MAIN sections
    # For library modules, MAIN section is optional
    required_keywords = ["IMPORTS", "CONSTANTS", "CORE"]
    if has_main_guard:
        required_keywords.append("MAIN")
    
    lines = content.split("\n")
    found_sections = []
    
    for i, line in enumerate(lines):
        # Match format 1: single-line banner with section name
        if re.match(r'#\s*=+\s*§?\d*\s*([A-Z][A-Z\s&()]+?)\s*=+\s*$', line):
            match = re.search(r'([A-Z][A-Z\s&()]+)', line)
            if match:
                found_sections.append(match.group(1).strip())
        
        # Match format 2: three-line banner (check middle line)
        elif re.match(r'#\s*=+\s*$', line) and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.startswith('#') and not '=' in prev_line:
                # Extract section name from previous line
                section_name = prev_line.lstrip('#').strip()
                if section_name.isupper():
                    found_sections.append(section_name)
    
    missing = []
    for keyword in required_keywords:
        # Check if any found section contains this keyword
        if not any(keyword in section for section in found_sections):
            missing.append(keyword)
    
    if missing:
        return CheckResult(False, f"Missing section headers for: {missing}")
    return CheckResult(True, "Section headers present")


def check_imports_location(content: str, tree: ast.Module) -> CheckResult:
    """Check that all imports are at module level (not inside functions/classes)."""
    violations = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Check if this import is nested inside a function or class
            # We do this by checking if any parent in the tree is a FunctionDef or ClassDef
            # Since ast.walk doesn't preserve parent info, we parse again with a visitor
            pass
    
    # Use a custom visitor to track nesting
    class ImportChecker(ast.NodeVisitor):
        def __init__(self):
            self.violations = []
            self.scope_stack = []
        
        def visit_FunctionDef(self, node):
            self.scope_stack.append(('function', node.name))
            self.generic_visit(node)
            self.scope_stack.pop()
        
        def visit_AsyncFunctionDef(self, node):
            self.scope_stack.append(('function', node.name))
            self.generic_visit(node)
            self.scope_stack.pop()
        
        def visit_ClassDef(self, node):
            self.scope_stack.append(('class', node.name))
            self.generic_visit(node)
            self.scope_stack.pop()
        
        def visit_Import(self, node):
            if self.scope_stack:
                scope_type, scope_name = self.scope_stack[-1]
                for alias in node.names:
                    self.violations.append(
                        f"Line {node.lineno}: import {alias.name} (inside {scope_type} {scope_name})"
                    )
            self.generic_visit(node)
        
        def visit_ImportFrom(self, node):
            if self.scope_stack:
                scope_type, scope_name = self.scope_stack[-1]
                module = node.module or ''
                self.violations.append(
                    f"Line {node.lineno}: from {module} import ... (inside {scope_type} {scope_name})"
                )
            self.generic_visit(node)
    
    checker = ImportChecker()
    checker.visit(tree)
    
    if checker.violations:
        return CheckResult(
            False,
            f"Imports outside module level:\n  " + "\n  ".join(checker.violations[:5])
        )
    return CheckResult(True, "All imports at module level")


def check_no_print_calls(content: str, tree: ast.Module) -> CheckResult:
    """Check that there are no print() calls (should use logger instead)."""
    # Check for convention-exempt marker (for CLI tools that need print)
    if "Convention-exempt: CLI tool using print()" in content:
        return CheckResult(True, "CLI tool (print() allowed)")
    
    violations = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check if the function being called is 'print'
            if isinstance(node.func, ast.Name) and node.func.id == 'print':
                violations.append(f"Line {node.lineno}: print() call found")
    
    if violations:
        return CheckResult(
            False,
            f"Found print() calls (use logger instead):\n  " + "\n  ".join(violations[:5])
        )
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


def check_pathlib_usage(tree: ast.Module) -> CheckResult:
    """Check for os.path usage instead of pathlib.Path."""
    violations = []
    
    for node in ast.walk(tree):
        # Check for os.path.* calls
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Attribute):
                # Check for os.path pattern
                if (isinstance(node.value.value, ast.Name) and 
                    node.value.value.id == 'os' and 
                    node.value.attr == 'path'):
                    violations.append(
                        f"Line {node.lineno}: os.path.{node.attr} (use pathlib.Path instead)"
                    )
    
    if violations:
        return CheckResult(
            False,
            f"Use pathlib.Path instead of os.path:\n  " + "\n  ".join(violations[:5])
        )
    return CheckResult(True, "Using pathlib.Path")


def check_dataclass_flags(tree: ast.Module) -> CheckResult:
    """Check that dataclasses use all three recommended flags."""
    violations = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if class has @dataclass decorator
            for decorator in node.decorator_list:
                is_dataclass = False
                keywords_present = {'kw_only': False, 'slots': False, 'frozen': False}
                
                # Handle @dataclass or @dataclass(...)
                if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
                    is_dataclass = True
                elif isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name) and decorator.func.id == 'dataclass':
                        is_dataclass = True
                        # Check keywords
                        for keyword in decorator.keywords:
                            if keyword.arg in keywords_present:
                                # Check if the value is True
                                if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                                    keywords_present[keyword.arg] = True
                
                if is_dataclass:
                    missing = [k for k, v in keywords_present.items() if not v]
                    if missing:
                        violations.append(
                            f"Line {node.lineno}: @dataclass on {node.name} missing flags: {missing}"
                        )
    
    if violations:
        return CheckResult(
            False,
            "Dataclass missing recommended flags:\n  " + "\n  ".join(violations),
            severity="warning"
        )
    return CheckResult(True, "Dataclass flags correct")


def check_loguru_usage(content: str, tree: ast.Module) -> CheckResult:
    """Check that loguru is imported (for standalone scripts)."""
    has_main = 'if __name__ == "__main__"' in content
    
    if not has_main:
        # Library module, loguru is optional
        return CheckResult(True, "Library module (loguru optional)")
    
    # Check for convention-exempt marker (for CLI tools)
    if "Convention-exempt: CLI tool using print()" in content:
        return CheckResult(True, "CLI tool (loguru optional)")
    
    # Check if loguru is imported
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'loguru':
                for alias in node.names:
                    if alias.name == 'logger':
                        return CheckResult(True, "Loguru imported")
    
    return CheckResult(False, "Standalone script missing: from loguru import logger")


def verify_script(script_path: Path, verbose: bool = False) -> bool:
    """Run all verification checks on a script."""
    if not script_path.exists():
        print(f"❌ Error: File not found: {script_path}", file=sys.stderr)
        return False
    
    content = script_path.read_text(encoding="utf-8")
    
    # Parse the AST
    try:
        tree = ast.parse(content, filename=str(script_path))
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}", file=sys.stderr)
        return False
    
    checks = [
        ("Section Headers", lambda: check_section_headers(content)),
        ("Import Location", lambda: check_imports_location(content, tree)),
        ("No print() Calls", lambda: check_no_print_calls(content, tree)),
        ("Entry Point Pattern", lambda: check_entry_point(content)),
        ("pathlib Usage", lambda: check_pathlib_usage(tree)),
        ("Dataclass Flags", lambda: check_dataclass_flags(tree)),
        ("Loguru Import", lambda: check_loguru_usage(content, tree)),
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
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


# ==================== §7 MAIN EXECUTION ====================


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

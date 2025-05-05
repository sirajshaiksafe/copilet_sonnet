#!/usr/bin/env python
"""
Matrix Runner - Execute tests across all browser/device combinations in parallel

Usage:
    python run_matrix.py [test_path] [--env ENV] [--workers N]
    
Examples:
    # Run all UI tests on all active browser/device combinations with default parallelism
    python run_matrix.py tests/ui
    
    # Run a specific test file on QA environment with 3 workers
    python run_matrix.py tests/ui/test_home_page.py --env QA --workers 3
"""

import argparse
import subprocess
import sys
import os
from utils.test_matrix import get_active_matrix, get_recommended_workers

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run tests in parallel across multiple browser and device combinations"
    )
    parser.add_argument(
        "test_path", 
        nargs="?", 
        default="tests/ui",
        help="Path to test file or directory (default: tests/ui)"
    )
    parser.add_argument(
        "--env", 
        choices=["DEV", "SYS", "QA"], 
        default="SYS",
        help="Environment to run tests against (default: SYS)"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        default=0,
        help="Number of parallel workers (default: auto-determined based on combinations)"
    )
    parser.add_argument(
        "--list-matrix", 
        action="store_true", 
        help="List active test matrix combinations without running tests"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Get active matrix combinations
    matrix = get_active_matrix()
    
    if args.list_matrix:
        print(f"\nActive test matrix ({len(matrix)} combinations):")
        for combo in matrix:
            print(f"  - {combo['name']}: Browser: {combo['browser_type']}, Device: {combo['mobile_device'] or 'Desktop'}")
        return
    
    # Determine number of workers
    workers = args.workers if args.workers > 0 else get_recommended_workers()
    
    # Build pytest command
    cmd = [
        "pytest",
        args.test_path,
        f"--env={args.env}",
        "--matrix",
        f"-n{workers}",
        "-v"
    ]
    
    # Display execution info
    print(f"\nExecuting tests with {len(matrix)} browser/device combinations on {workers} workers:")
    for combo in matrix:
        print(f"  - {combo['name']}: Browser: {combo['browser_type']}, Device: {combo['mobile_device'] or 'Desktop'}")
    print(f"\nEnvironment: {args.env}")
    print(f"Command: {' '.join(cmd)}\n")
    
    # Execute pytest
    result = subprocess.run(cmd)
    
    # Return pytest exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
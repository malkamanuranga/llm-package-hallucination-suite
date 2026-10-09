import sys
import re
import argparse
import subprocess
import requests
from typing import Dict, List, Tuple

# Terminal color codes for visual security warnings
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def extract_packages(raw_input: str) -> List[str]:
    """Extracts package names from pip command strings or requirements lines."""
    packages = set()
    # Strip 'pip install' or 'pip3 install' prefix if present
    clean_text = re.sub(r'^(?:pip|pip3)\s+install\s+', '', raw_input.strip(), flags=re.IGNORECASE)
    
    # Split by spaces or line breaks
    tokens = clean_text.replace('\n', ' ').split()
    for token in tokens:
        token = token.strip()
        # Skip flags (-r, --user, -U, etc.)
        if token.startswith('-') or not token:
            continue
        # Strip version constraints (e.g. pkg>=1.0.0, pkg==2.1)
        pkg_name = re.split(r'[<>=!~]', token)[0].strip()
        # Clean up stray formatting/punctuation
        pkg_name = re.sub(r'[\*\`\'\"\(\)\[\]\,]', '', pkg_name)
        if pkg_name and pkg_name.lower() not in ["in", "once", "run", "environment"]:
            packages.add(pkg_name.lower())
            
    return sorted(list(packages))

def verify_package_on_pypi(package_name: str) -> Dict:
    """Verifies package presence and metadata on PyPI in real time."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            info = data.get("info", {})
            return {
                "status": "SAFE",
                "exists": True,
                "version": info.get("version", "Unknown"),
                "summary": info.get("summary", "No summary provided.") or "No summary provided.",
                "author": info.get("author", "Unknown")
            }
        elif response.status_code == 404:
            return {
                "status": "HALLUCINATED",
                "exists": False,
                "reason": "Package DOES NOT exist on PyPI (Slopsquatting Target)"
            }
        else:
            return {
                "status": "UNKNOWN",
                "exists": False,
                "reason": f"PyPI API returned HTTP status {response.status_code}"
            }
    except requests.RequestException as e:
        return {
            "status": "ERROR",
            "exists": False,
            "reason": f"Network error connecting to PyPI: {e}"
        }

def inspect_and_guard(command: str, execute_if_safe: bool = False):
    """Main security pipeline: parses command, checks PyPI, and blocks malicious runs."""
    print(f"\n{BOLD}{CYAN}=== [ SLOP-GUARD ] Real-Time AI Supply Chain Security ==={RESET}\n")
    print(f"Analyzing proposed command: {BOLD}{command}{RESET}")
    
    packages = extract_packages(command)
    if not packages:
        print(f"{YELLOW}[!] No valid package names detected in input.{RESET}")
        return

    print(f"Extracted Target Packages ({len(packages)}): {packages}\n")
    
    has_hallucinations = False

    for pkg in packages:
        info = verify_package_on_pypi(pkg)
        
        if info["status"] == "SAFE":
            summary_snippet = info['summary'][:55] + "..." if len(info['summary']) > 55 else info['summary']
            print(f" {GREEN}[SAFE]{RESET} {BOLD}{pkg:<18}{RESET} (v{info['version']}) - {summary_snippet}")
        elif info["status"] == "HALLUCINATED":
            has_hallucinations = True
            print(f" {RED}[DANGER]{RESET} {BOLD}{RED}{pkg:<18}{RESET} -> {RED}{info['reason']}{RESET}")
        else:
            print(f" {YELLOW}[WARNING]{RESET} {pkg:<18} -> {info['reason']}")

    print("\n" + "=" * 65)
    
    if has_hallucinations:
        print(f"{RED}{BOLD}[BLOCKED] CRITICAL SECURITY RISK DETECTED!{RESET}")
        print(f"{RED}One or more packages do not exist on PyPI.{RESET}")
        print(f"{RED}Running this command risks installing malicious slopsquatted packages.{RESET}")
        print(f"{RED}Execution halted.{RESET}\n")
        sys.exit(1)
    else:
        print(f"{GREEN}{BOLD}[VERIFIED] All packages exist on PyPI and are safe to install.{RESET}\n")
        if execute_if_safe:
            print(f"{CYAN}Executing: {command}{RESET}")
            subprocess.run(command, shell=True)

def main():
    parser = argparse.ArgumentParser(
        description="Slop-Guard: Real-Time Slopsquatting & AI Hallucination Prevention CLI"
    )
    parser.add_argument("command", type=str, help="The pip command to inspect (e.g., 'pip install requests paho-mqtt')")
    parser.add_argument("--execute", "-e", action="store_true", help="Execute installation automatically if verified safe")
    
    args = parser.parse_args()
    inspect_and_guard(args.command, execute_if_safe=args.execute)

if __name__ == "__main__":
    main()
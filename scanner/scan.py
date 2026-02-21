import os
import sys
import glob
import hashlib
import json
import subprocess
import requests

SKILLS_DIR = "skills"
CACHE_FILE = "scanner/cache.json"
IGNORE_FILE = "scanner/ignore_list.txt"
OLLAMA_MODEL = "llama3"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def file_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def load_ignore_patterns():
    if not os.path.exists(IGNORE_FILE):
        return []
    with open(IGNORE_FILE, "r") as f:
        return [line.strip().lower() for line in f.readlines()]

def is_ignored(text, ignore_patterns):
    for pattern in ignore_patterns:
        if pattern in text.lower():
            return True
    return False


def analyze_file(file_path, content):
    prompt = f"""
You are a security scanner for AI skills markdown files.

Classify the content into one of:
SAFE
LOW
HIGH

LOW = suspicious but not clearly malicious.
HIGH = clear malicious intent (exfiltration, override, jailbreak).

If LOW or HIGH:
- Mention severity clearly
- Explain reason
- Print suspicious lines

Respond strictly in this format:

Severity: <SAFE | LOW | HIGH>
Reason:
Suspicious Lines:

Content:
{content}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Ollama execution failed: {e}")
        sys.exit(1)


def comment_on_pr(message):
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return

    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event_data = json.load(f)

    pr_number = event_data["pull_request"]["number"]

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    requests.post(url, headers=headers, json={"body": message})


def main():
    print("🔍 Scanning skills folder...\n")

    cache = load_cache()
    ignore_patterns = load_ignore_patterns()

    malicious_found = False
    pr_comment_message = "## 🚨 AI Security Scan Report\n\n"

    files = glob.glob(os.path.join(SKILLS_DIR, "*.md"))

    for file in files:
        print(f"📄 Reading: {file}")

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        current_hash = file_hash(content)

        if file in cache and cache[file] == current_hash:
            print("⏭ Skipped (unchanged file)\n")
            continue

        result = analyze_file(file, content)
        cache[file] = current_hash

        print(result)
        print()

        result_upper = result.upper()

        if "SEVERITY: HIGH" in result_upper:
            malicious_found = True
            pr_comment_message += f"### ❌ HIGH in {file}\n```\n{result}\n```\n\n"

        elif "SEVERITY: LOW" in result_upper:
            pr_comment_message += f"### ⚠️ LOW in {file}\n```\n{result}\n```\n\n"

        else:
            print("✅ SAFE\n")

    save_cache(cache)

    if malicious_found:
        pr_comment_message += "\n❌ Workflow failed due to HIGH severity issues."
        comment_on_pr(pr_comment_message)
        print("\n❌ Failing workflow — HIGH severity detected")
        sys.exit(1)

    else:
        pr_comment_message += "\n✅ No HIGH severity issues found."
        comment_on_pr(pr_comment_message)
        print("\n✅ Scan completed successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
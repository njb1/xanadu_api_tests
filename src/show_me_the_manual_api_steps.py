import os

# This script is designed to parse a text file containing API test cases
# and display the steps for either Postman or Insomnia in a user-friendly way.
# Note: this was created with help from Copilot and is not a direct copy of any code.

def parse_tests(filename):
    with open(filename, encoding="utf-8") as f:
        content = f.read()

    # Split on lines with at least 5 dashes (test case separators)
    import re
    raw_tests = re.split(r'-{5,}', content)
    tests = []
    for raw in raw_tests:
        raw = raw.strip()
        if not raw:
            continue
        # Find the test case title (first non-empty line)
        lines = raw.splitlines()
        title = ""
        for line in lines:
            if line.strip():
                title = line.strip()
                break
        # Find Postman and Insomnia steps
        postman = []
        insomnia = []
        mode = None
        for line in lines:
            l = line.strip()
            if l.lower().startswith("**steps (postman"):
                mode = "postman"
                continue
            elif l.lower().startswith("**steps (insomnia"):
                mode = "insomnia"
                continue
            elif l.startswith("**Expected Result") or l.startswith("**Precondition"):
                mode = None
            if mode == "postman":
                postman.append(line)
            elif mode == "insomnia":
                insomnia.append(line)
        # Fallback: if no explicit steps, just show all
        if not postman and not insomnia:
            postman = insomnia = lines
        tests.append({
            "title": title,
            "postman": "\n".join(postman).strip(),
            "insomnia": "\n".join(insomnia).strip()
        })
    return tests

def main():
    filename = os.path.join(os.path.dirname(__file__), "xanadu_manual_api_detailed.txt")
    tests = parse_tests(filename)
    if not tests:
        print("No tests found.")
        return

    mode = ""
    while mode not in ("p", "i"):
        mode = input("Show steps for (p)ostman or (i)nsomnia? ").strip().lower()

    idx = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Test {idx+1} of {len(tests)}: {tests[idx]['title']}\n")
        steps = tests[idx]["postman"] if mode == "p" else tests[idx]["insomnia"]
        print(steps if steps else "(No steps found for this tool.)")
        print("\n[n]ext, [b]ack, [q]uit")
        cmd = input("Command: ").strip().lower()
        if cmd == "n":
            if idx < len(tests) - 1:
                idx += 1
            else:
                print("Already at last test.")
        elif cmd == "b":
            if idx > 0:
                idx -= 1
            else:
                print("Already at first test.")
        elif cmd == "q":
            break

if __name__ == "__main__":
    main()
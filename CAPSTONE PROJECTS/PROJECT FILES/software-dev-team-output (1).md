   ## Spec    # Specification: Password Strength Checker CLI

### 1. Goal
Provide a lightweight, zero-dependency Python CLI tool that evaluates password strength across standard complexity dimensions, assigns a clear rating, and outputs actionable improvement tips.

### 2. User Stories
* As a user, I want to submit a password via the CLI so I can quickly evaluate its security.
* As a user, I want to receive a rating (Weak, Medium, Strong) and specific tips so that I know exactly how to make my password more secure.

### 3. Acceptance Criteria
1. The tool must be implemented in a single executable `.py` file using only Python's standard library.
2. Accepts password input via standard CLI argument or secure prompt (e.g., `getpass`).
3. Evaluates input against five distinct criteria:
   - Length (minimum 8 characters; 12+ for maximum score)
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one numerical digit
   - At least one symbol/special character
4. Outputs exactly one strength label based on score thresholds: **Weak**, **Medium**, or **Strong**.
5. Displays targeted recommendations for any failed criteria (e.g., "Add at least one number").
6. Displays a success confirmation with no tips if the password meets all criteria for "Strong".

### 4. Out of Scope
* Password generation capabilities.
* Checking against leaked password databases or dictionary attack lists.
* Advanced entropy calculation or sequential pattern detection (e.g., "12345", "qwerty").
* Graphical (GUI) or web interface.     ## Design    ### 1. Language and Libraries
* **Language:** Python 3.10+
* **Libraries:** Standard Library only (`argparse`, `getpass`, `string`). Zero external dependencies.

---

### 2. File Structure
```text
password_checker.py
```

---

### 3. Function Signatures & Descriptions

* **`evaluate_password(password: str) -> tuple[str, list[str]]`**  
  Evaluates the password against the five criteria, returning a strength label (`Weak`, `Medium`, `Strong`) and a list of specific improvement tips.

* **`parse_args() -> argparse.Namespace`**  
  Parses command-line arguments to accept an optional password directly via a CLI flag.

* **`main() -> None`**  
  Orchestrates execution by retrieving the password (via CLI argument or secure `getpass` prompt), calling the evaluation logic, and printing the strength rating and tips.     ## Code    password_checker.py
```python
#!/usr/bin/env python3
"""Password Strength Checker CLI.

Evaluates a password against five criteria, prints a strength rating
(Weak, Medium, Strong) and actionable tips for any failed criteria.
"""

import argparse
import getpass
import string
import sys


MIN_LENGTH = 8
STRONG_LENGTH = 12


def evaluate_password(password: str) -> tuple[str, list[str]]:
    """Evaluate a password and return (label, tips).

    Scoring (max 6 points):
      - Length >= 8: 1 point; length >= 12: 2 points
      - Uppercase letter: 1 point
      - Lowercase letter: 1 point
      - Digit: 1 point
      - Symbol: 1 point

    Strong: all criteria met (score 6, i.e. length >= 12 and every class present)
    Medium: score 4 or 5
    Weak: score below 4
    """
    tips: list[str] = []
    score = 0

    length = len(password)
    if length >= STRONG_LENGTH:
        score += 2
    elif length >= MIN_LENGTH:
        score += 1
        tips.append(
            f"Use {STRONG_LENGTH} or more characters for maximum strength"
        )
    else:
        tips.append(f"Use at least {MIN_LENGTH} characters")

    if any(c in string.ascii_uppercase or (c.isalpha() and c.isupper()) for c in password):
        score += 1
    else:
        tips.append("Add at least one uppercase letter")

    if any(c in string.ascii_lowercase or (c.isalpha() and c.islower()) for c in password):
        score += 1
    else:
        tips.append("Add at least one lowercase letter")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Add at least one number")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        tips.append("Add at least one symbol (e.g., !@#$%^&*)")

    if score == 6:
        label = "Strong"
    elif score >= 4:
        label = "Medium"
    else:
        label = "Weak"

    return label, tips


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Evaluate password strength and get improvement tips."
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Password to evaluate. If omitted, you will be prompted securely.",
    )
    return parser.parse_args()


def main() -> None:
    """Retrieve the password, evaluate it, and print the results."""
    args = parse_args()

    if args.password is not None:
        password = args.password
    else:
        try:
            password = getpass.getpass("Enter password: ")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.", file=sys.stderr)
            sys.exit(1)

    label, tips = evaluate_password(password)

    print(f"Strength: {label}")
    if tips:
        print("Tips to improve your password:")
        for tip in tips:
            print(f"  - {tip}")
    else:
        print("Great job! Your password meets all criteria.")


if __name__ == "__main__":
    main()
```     ## Test Report    ## 1. Test cases

```python
import subprocess
import sys

import password_checker as pc


def test_strong_password_has_no_tips():
    label, tips = pc.evaluate_password("Abcdef123!xyz")
    assert label == "Strong"
    assert tips == []


def test_short_lowercase_password_is_weak_with_targeted_tips():
    label, tips = pc.evaluate_password("abc")
    assert label == "Weak"
    assert any("at least 8" in t for t in tips)
    assert any("uppercase" in t for t in tips)
    assert any("number" in t for t in tips)
    assert any("symbol" in t for t in tips)
    assert not any("lowercase" in t for t in tips)


def test_all_classes_but_under_12_chars_is_medium_with_length_tip():
    label, tips = pc.evaluate_password("Abcdefg1!")  # 9 chars
    assert label == "Medium"
    assert any("12" in t for t in tips)


def test_missing_digit_gives_number_tip():
    label, tips = pc.evaluate_password("Abcdefghijkl!")
    assert label == "Medium"
    assert "Add at least one number" in tips


def test_cli_argument_outputs_single_label_and_success_message():
    out = subprocess.run(
        [sys.executable, "password_checker.py", "-p", "Abcdef123!xyz"],
        capture_output=True, text=True,
    ).stdout
    assert out.count("Strength:") == 1
    assert "Strength: Strong" in out
    assert "Tips" not in out
    assert "meets all criteria" in out
```

## 2. Bugs

No bugs found

VERDICT: PASS
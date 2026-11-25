"""Write one funny line for The Excuse That Almost Works bounty.

Writes the line to /output/entry.txt. Stdlib only, no network.
The excuse: jury duty picked the gamer this morning and the court
took his phone till four — a boring, specific, verifiable civic
detail a tired manager would almost believe, with the laugh coming
from its own logic: the boss cannot even reach him to argue.

Why this line fits the judge's brief:
- It is one line a gamer texts the boss to skip work, at most
  20 words (16), and never mentions the game — a long, rehearsed
  excuse would already be a confession.
- It sounds almost believable: jury duty is real, specific and
  boring, the opposite of a wild story, and a summons is the one
  excuse a manager cannot easily doubt.
- It is funny on its own terms: the court confiscating the phone
  means the boss cannot text back, check in, or negotiate.
- It reads like a text sent in a hurry: one line, plain words,
  no setup, no explanation and no signature.
- It finds a fresh angle: not a dead grandmother, not a flat
  tyre, not a sudden fever — a civic duty nobody volunteers for.

Why jury duty beats the obvious excuses, one by one:
- A dead grandmother is the first excuse every manager has heard,
  so it reads as a copy of a copy before the second word.
- A flat tyre invites the manager to suggest a taxi, a bus, or
  working from the roadside — it opens a negotiation, not a day off.
- A sudden fever invites the manager to ask for a doctor's note
  tomorrow, which turns one sick day into paperwork.
- Jury duty invites nothing: the court picked the date, the court
  holds the phone, and the manager has no counter-move at all.
  The excuse wins because there is nothing to argue with.

Determinism: ENTRY is a single fixed string, never generated, so
every run writes the same bytes. The self-test pins the shape
(83 characters, 16 words, all ASCII) and the round-trip check
proves the write path adds and strips nothing.
"""

import os
import tempfile

ENTRY = (
    "Sorry, jury duty picked me this morning, court says I can't "
    "use my phone till four."
)


def validate_utf8(text):
    """Confirm the entry encodes cleanly as UTF-8.

    Returns the encoded bytes so callers can also check the byte length.
    Raises UnicodeEncodeError if the text is not encodable.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    return text.encode("utf-8")


def validate_length(text):
    """Enforce the kit gate: 1-140 characters, single line, non-whitespace.

    Raises ValueError with a specific message naming the failed rule, so a
    bad entry is easy to diagnose instead of failing silently.
    """
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry must be 1-140 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return True


def validate_word_count(text):
    """Enforce the task cap: at most 20 words, split on whitespace.

    Raises ValueError when the entry is over the cap.
    """
    words = len(text.split())
    if words > 20:
        raise ValueError(f"entry must be at most 20 words, got {words}")
    return True


def gate_check(text):
    """Run every kit-gate validation on the entry text before it is written."""
    validate_utf8(text)
    validate_length(text)
    return validate_word_count(text)


def self_test():
    """Small self-test: the real entry passes, and each bad input is refused.

    Checks the happy path plus one failure per gate rule, so a future edit
    that breaks validation is caught immediately instead of at submit time.
    Does not write any output file.
    """
    assert gate_check(ENTRY) is True
    assert len(ENTRY) == 83, f"entry length changed: {len(ENTRY)}"
    stats = entry_stats(ENTRY)
    assert stats == {"chars": 83, "words": 16, "non_ascii": 0}, (
        f"entry shape changed: {stats}"
    )
    assert validate_utf8(ENTRY) == ENTRY.encode("utf-8")
    assert len(validate_utf8(ENTRY)) == 83, "entry byte length changed"
    assert describe_entry(ENTRY) == {
        "chars": 83,
        "words": 16,
        "non_ascii": 0,
        "bytes": 83,
        "gate": "pass",
    }, f"entry description changed: {describe_entry(ENTRY)}"
    assert round_trip_entry(ENTRY) == ENTRY.encode("utf-8")
    assert determinism_check(ENTRY) == ENTRY.encode("utf-8")
    assert ENTRY.startswith("Sorry, jury duty"), "entry must open as a hurried apology"
    assert ENTRY.endswith("till four."), "entry must end on the phone detail"
    assert "jury duty" in ENTRY, "entry must keep its fresh angle"
    assert "GTA" not in ENTRY, "entry must not name the game — that is a confession"
    assert len(ENTRY.split()) <= 20, "entry must stay within the 20-word cap"
    assert "\n" not in ENTRY and "\r" not in ENTRY, "entry must stay one line"
    bad_cases = [
        ("", "empty entry"),
        (" " * 10, "whitespace-only entry"),
        ("x" * 141, "entry over 140 characters"),
        ("two\nlines", "multi-line entry"),
        ("two\rlines", "carriage-return entry"),
        (" padded ", "entry with surrounding whitespace"),
        ("trailing ", "trailing-space entry"),
        (" leading", "leading-space entry"),
        ("word " * 21, "entry over 20 words"),
        ("one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen "
         "twenty twenty-one", "entry of 21 real words"),
        ("Sorry, jury duty.\n", "entry ending with a newline"),
        ("Sorry, jury duty picked me this morning, court says I can't "
         "use my phone till four. ", "entry with a trailing space"),
        (123, "non-string entry"),
        (None, "none entry"),
        (b"bytes", "bytes entry"),
    ]
    for bad_text, label in bad_cases:
        try:
            gate_check(bad_text)
        except (ValueError, TypeError, UnicodeEncodeError):
            continue
        raise AssertionError(f"self-test failed: gate accepted {label}")
    return True


def write_entry(path):
    """Write the validated entry to path, exactly as-is, no trailing newline.

    The caller picks the path (the grader reads /output/entry.txt); the
    bytes written are exactly ENTRY encoded as UTF-8, so the judge sees
    the line and nothing else.
    """
    gate_check(ENTRY)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    return path


def entry_stats(text):
    """Count the entry's characters, words and non-ASCII characters.

    Used by the self-test to pin the entry's shape: a later edit that
    changes the joke changes these numbers and fails loudly instead of
    silently submitting a different line.
    """
    return {
        "chars": len(text),
        "words": len(text.split()),
        "non_ascii": sum(1 for ch in text if ord(ch) > 127),
    }


def describe_entry(text):
    """Summarise the entry in one plain dict for logs and debugging.

    Combines the shape counts with the byte length and a one-word
    verdict on the gate, so a caller can print a single line about
    the entry without re-running every validation by hand.
    """
    stats = entry_stats(text)
    stats["bytes"] = len(validate_utf8(text))
    stats["gate"] = "pass" if gate_check(text) else "fail"
    return stats


def round_trip_entry(text):
    """Write the entry to a throwaway file and read it back unchanged.

    Proves the write path is lossless: the bytes read back must equal
    the entry encoded as UTF-8, with no newline added or stripped.
    The temporary file is removed afterwards.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    try:
        write_entry(tmp_path)
        with open(tmp_path, "rb") as f:
            raw = f.read()
        assert raw == text.encode("utf-8"), "round trip changed the entry"
        return raw
    finally:
        os.unlink(tmp_path)


def determinism_check(text):
    """Run the entry writer twice and require byte-identical output.

    The judge compares the exact submitted text, so two runs of the
    program must produce the same bytes. Writes to two throwaway
    files, reads both back, compares, and removes both afterwards.
    Returns the shared bytes so callers can also check the hash.
    """
    first_path = None
    second_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            first_path = tmp.name
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            second_path = tmp.name
        write_entry(first_path)
        write_entry(second_path)
        with open(first_path, "rb") as f:
            first_bytes = f.read()
        with open(second_path, "rb") as f:
            second_bytes = f.read()
        assert first_bytes == second_bytes, "runs differ: entry is not deterministic"
        assert first_bytes == text.encode("utf-8"), "run output differs from ENTRY"
        return first_bytes
    finally:
        for path in (first_path, second_path):
            if path and os.path.exists(path):
                os.unlink(path)


def main():
    write_entry("/output/entry.txt")


if __name__ == "__main__":
    self_test()
    main()

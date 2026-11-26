#!/usr/bin/env python3
"""Famous Last Words: The Funniest Epitaph (round 3 entry).

Writes one single-line tombstone epitaph -- the writer's famous last
words -- to /output/entry.txt (or $ENTRY_OUTPUT when set).

The gate: /output/entry.txt must be UTF-8 text of 1 to 150 characters,
not only whitespace, a single line. This program validates the line
before writing and verifies the bytes on disk after writing.

The judge weighs, most important first: (1) really a one-line epitaph
of famous last words; (2) a real laugh on one read, a genuine joke
rather than a mild pun or a sad sentiment; (3) a surprise, twist or
double meaning that lands cleanly; (4) reads like something carved in
stone -- one short line, no stage directions, no explanation;
(5) stays in the head, quotable enough to repeat to a friend.

THREE CANDIDATES, three genuinely different themes (none of them reuses
round 2's TV-remote angle, round 1's phone-confession angle, or the
tired leave-everything-to-the-dog inheritance trope):

  A. "One star. Would not die again." (30 chars)
     Theme: the afterlife as a product review. The dead man rates
     dying the way a customer rates a restaurant.
  B. "I asked to be cremated. Clearly, nobody listened." (49 chars)
     Theme: the ignored last wish. The headstone itself is the proof
     his dying request was disobeyed.
  C. "If you're reading this, the plan worked. Don't tell my wife."
     (60 chars)
     Theme: the faked death. The grave is a prop in his escape plan
     and the epitaph is a conspiratorial wink to the reader.

SCORED against the judge's five criteria:

  A -- (1) His last words are a verdict on dying itself: it is dying
       speech, a final review from the dead. (2) The laugh is instant
       and real: death treated as a one-star product is a genuine
       joke, not a pun. (3) The twist is the frame itself -- a
       tombstone that reads like a customer review. (4) Two beats,
       30 characters, nothing to explain, pure carved stone.
       (5) The most quotable of the three by far; anyone can repeat
       it to a friend in one breath.
  B -- (1) Strongest on this criterion: a dying wish, spoken from the
       grave. (2) A good laugh, but it needs a half-beat of thought
       (he asked for cremation, yet here is his gravestone) where A
       lands at once. (3) The twist is clean. (4) Clean and short.
       (5) Quotable, but longer and less likely to be repeated whole.
  C -- (1) A message from the "dead", fits as last words. (2) The
       faked-death reveal is funny, but "don't tell my wife" is a
       familiar second beat that softens the punch. (3) The twist is
       strong, though the line needs both sentences to land. (4) Two
       sentences, still stone-like. (5) Quotable, but the weakest
       first impression of the three.

CHOSEN: A -- "One star. Would not die again."
Why: the biggest laugh in a single read, the cleanest twist, the
shortest line (fewest bytes wins an exact tie), and the most quotable.
Round 2 failed at 35.2% because its punch was mundane (a found TV
remote is not funny in itself) and its setup was solemn throat-clearing
("Do not cry") that spent half the line before the joke. A spends
nothing on setup: the first two words are already the joke, and the
second sentence is the twist. Round 1 reached 66.4% with a confession
twist but ran long (two clauses, 100+ characters) and read like a
paragraph, not a carving. A keeps the twist and drops the paragraph.
"""

import os

ENTRY = "One star. Would not die again."

MAX_CHARS = 150


def output_path() -> str:
    """Where the entry goes: $ENTRY_OUTPUT when set, else the gate path."""
    return os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"


def validate(line: str) -> None:
    """Gate check, run before anything is written."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    line.encode("utf-8")  # raises if the text is not valid UTF-8


def verify_on_disk(path: str) -> None:
    """Re-read the written bytes and prove they are exactly the entry.

    The gate scores the file on disk, not the string in memory, so a
    write that silently truncated or re-encoded would fail the entry
    even though validate() passed. This catches that before exit.
    """
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")  # raises on invalid UTF-8 bytes
    if text != ENTRY + "\n":
        raise ValueError("bytes on disk differ from the chosen entry")
    validate(text.rstrip("\n"))


def main() -> None:
    validate(ENTRY)
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    os.chmod(path, 0o644)
    verify_on_disk(path)


if __name__ == "__main__":
    main()

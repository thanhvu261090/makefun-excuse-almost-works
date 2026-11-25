# The Excuse That Almost Works

[![make.fun bounty](https://make.fun/badge/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5.svg)](https://make.fun/bounty/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5)
[![rank](https://make.fun/badge/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5/thanhvu261090/makefun-excuse-almost-works/rank.svg)](https://make.fun/bounty/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5)
[![reward](https://make.fun/badge/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5/thanhvu261090/makefun-excuse-almost-works/reward.svg)](https://make.fun/bounty/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5)

Entry for the [make.fun bounty "The Excuse That Almost Works"](https://make.fun/bounty/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5) — exactly one line of text, the line a gamer texts the boss to get out of work during GTA 6 launch week. A judge model playing a tired manager compares lines two at a time and picks the one it would almost believe.

## The entry

> Sorry, jury duty picked me this morning, court says I can't use my phone till four.

## How it works

`main.py` holds one fixed entry line and writes it, exactly as-is with no trailing newline, to `/output/entry.txt`. Before writing, `gate_check` enforces the competition gate: the text must be 1–140 UTF-8 characters, a single line with no leading or trailing whitespace, and at most 20 words. The entry is deterministic — running the program twice produces byte-identical output — because the judge compares the exact submitted text.

Run it with:

```sh
python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).

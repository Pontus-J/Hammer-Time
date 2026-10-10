# Updating

How every state-changing run ends: record it, package it, get the user to save it.

## 1. Record

```
python3 <skill>/scripts/ht.py score --topic t03 --result guided --note "Knew LEFT JOIN keeps unmatched rows; missed that WHERE on the right table turns it into an inner join"
```

- `--result` is one of `first_try`, `guided`, `partial`, `missed` (see `reference/scoring.md`).
- `--note` is one line on what they showed or what was missing. Reviews are written from these
  notes, so make it specific enough to be useful three weeks from now.

Never edit `state.json` yourself, even to fix a typo. If a score went in wrong, tell the user and
record the next answer properly. Don't try to reverse it.

## 2. Package

- **claude.ai**: `python3 <skill>/scripts/ht.py package`. It writes
  `/mnt/user-data/outputs/<skill-name>.skill`. Present that file to the user.
- **Claude Code**: `python3 <skill>/scripts/ht.py package --install ~/.claude/skills` (or wherever
  the skill is installed). Nothing more for the user to do.

## 3. The save message

Show the scores and the save step together, in this order, every time. Keep the wording close to
this. On Claude Code, drop the save block and say it's installed.

```
**<Topic title>: <old> → <new>** (<band>)
<one line: what to review, only if the result was partial or missed>

| topic | score | band |
|---|---|---|
| ... | ... | ... |

---

## 💾 Save the skill now

Click **Save skill** on the file above. It replaces your current `<skill-name>`.

**If you skip this, today's score is gone.** The next run starts from your old scores.
```

If `ht.py` printed `LEVEL UP`, add one line after the table offering a harder version of that topic
next time (`guides/onboarding.md`, part B). Don't start it in this run.

Then stop. Don't offer another question. One a day is the design.

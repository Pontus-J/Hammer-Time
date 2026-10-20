# Updating

How every state-changing run ends: record it, package it, get the user to save it.

## 1. Record

```
python3 <skill>/scripts/ht.py score --topic t03 --result guided --note "Asked why a LEFT JOIN report lost suppliers. Knew unmatched rows are kept; missed that WHERE on the right table turns it into an inner join"
```

- `--result` is one of `first_try`, `guided`, `partial`, `missed` (see `reference/scoring.md`).
- `--note` is one line. Start with what you asked, then what they showed and what was missing.
  Later questions avoid repeats and reviews find patterns from these notes, so make it specific
  enough to be useful three weeks from now.

Never edit `state.json` yourself, even to fix a typo. If a score went in wrong, tell the user and
record the next answer properly. Don't try to reverse it.

## 2. Package

- **claude.ai**: `python3 <skill>/scripts/ht.py package`. It writes
  `/mnt/user-data/outputs/<skill-name>.skill`. Present that file to the user.
- **Claude Code**: `python3 <skill>/scripts/ht.py package --install`. It replaces the installed
  skill in place. Nothing more for the user to do.

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

End with one short line: **One more?** Nothing else. If they say yes, run `status` again and go
back to `guides/asking.md`; scores from this chat carry over. Otherwise stop. After onboarding or a
review, skip the line.

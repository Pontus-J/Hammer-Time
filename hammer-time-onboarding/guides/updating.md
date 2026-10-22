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

```
python3 <skill>/scripts/ht.py package
```

Always exactly this, with no flags, on every platform. The script decides how the run is saved:

- `INSTALLED`: a local Claude Code install on the user's own computer, updated in place. Nothing
  for the user to save.
- `SAVE REQUIRED`: everywhere else, claude.ai and cloud sessions included. It wrote a `.skill`
  file and printed what to do: give the user the file, and show its save block word for word.

Never pass `--install` or `--out` during a run, and never decide for yourself that a run is saved.
A session that can write to the skill folder can still be thrown away when the chat ends, and then
the scores are lost without anyone noticing.

## 3. The save message

Show the scores and the save step together, in this order, every time:

```
**<Topic title>: <old> → <new>** (<band>)
<one line: what to review, only if the result was partial or missed>

| topic | score | band |
|---|---|---|
| ... | ... | ... |

<the save block `package` printed, from the --- line to the end, word for word>
```

If `package` printed `INSTALLED`, put one line in place of the save block: "Saved: the skill is
updated in place." Never shorten or skip the save block, and never put anything before it.

If `ht.py` printed `LEVEL UP`, add one line after the table offering a harder version of that topic
next time (`guides/onboarding.md`, part B). Don't start it in this run.

End with one short line: **One more?** Nothing else. If they say yes, run `status` again and go
back to `guides/asking.md`; scores from this chat carry over. Otherwise stop. After onboarding or a
review, skip the line.

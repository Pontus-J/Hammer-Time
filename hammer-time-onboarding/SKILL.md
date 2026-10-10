---
name: hammer-time-onboarding
description: "Hammer Time: set up a Socratic drill that hammers in knowledge about one area, scores each topic 0-100 and re-saves itself with the new scores. Use ONLY when the user explicitly asks to start Hammer Time, runs /hammer-time or /hammer-time-onboarding, or asks to set up a new Hammer Time area."
---

# Hammer Time

A drill that hammers in knowledge about one area. Each topic in the area has a score from 0 to 100,
the questions get harder as the score rises, and the skill saves itself with the new scores after
every run. This one folder is both the blank template (`hammer-time-onboarding`) and every area
skill made from it (`hammer-time-sql`, `hammer-time-accounting`). The only difference is whether
`state.json` exists.

## Hard rules

1. **Never edit `state.json` or `SKILL.md` by hand.** Every change goes through `scripts/ht.py`.
   It does the arithmetic, picks the topic, keeps the log and packages the result. You run the
   conversation; the script keeps the books.
2. **Never retype or rewrite any other file in this folder.** The package is a copy of the
   installed files plus the script's changes. That is what stops the skill drifting over months.
3. **Every run that changes state ends with `package` and the save message** from
   `guides/updating.md`. If the user doesn't save, the run didn't happen.
4. One area per skill. If the user wants a second area, they run `hammer-time-onboarding` again.

## Start of every run

Run this first and read the output:

```
python3 <this skill's folder>/scripts/ht.py status
```

Then pick the mode:

| status says | user asked for | mode | read |
|---|---|---|---|
| `MODE: onboarding` | anything | Onboarding | `guides/onboarding.md` (part A) |
| `MODE: active` | a question, or nothing specific | Ask | `guides/asking.md`, then `guides/updating.md` |
| `MODE: active` | a progress review, or to change topics | Review | `guides/review.md` |
| `MODE: active` | a harder version of a topic | Level up | `guides/onboarding.md` (part B) |

Read the guide for the mode before saying anything to the user. Read `reference/scoring.md` before
asking or scoring a question. Don't load guides you don't need.

If the user typed plain "hammer time" and you can see more than one `hammer-time-*` skill, ask
which area they mean before doing anything.

## Where things are

| file | what | changes? |
|---|---|---|
| `SKILL.md` | this router | renamed once, by `init` |
| `guides/onboarding.md` | the grill, topic list, starting scores, level-up | never |
| `guides/asking.md` | how to run one Socratic question | never |
| `guides/updating.md` | scoring the answer, packaging, the save message | never |
| `guides/review.md` | progress review and topic edits | never |
| `reference/scoring.md` | bands, the difficulty gradient, the scoring ladder | never |
| `scripts/ht.py` | the state engine | never |
| `state.json` | area, profile, topics, scores, last 20 answers | only through `ht.py` |
| `NOTICE.md` | credit for the interview method | never |

## Platform notes

- **claude.ai**: the installed skill is read-only. `ht.py` copies it to a work folder, changes the
  copy, and `package` writes `<skill-name>.skill` to `/mnt/user-data/outputs/`. Give the user that
  file so they can save it.
- **Claude Code**: use `package --install ~/.claude/skills` (or the project's `.claude/skills`).
  That writes the new version straight over the installed one, and nothing needs saving by hand.
- If you can't run code at all, say so and stop. This skill doesn't work without the script.

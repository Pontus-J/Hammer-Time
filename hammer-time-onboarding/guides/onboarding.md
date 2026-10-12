# Onboarding

Part A turns the blank template into an area skill. Part B makes one topic in an existing area
harder once its score passes 90.

The interview method is adapted from Matt Pocock's `grilling` skill (MIT,
github.com/mattpocock/skills). Credit stays in `NOTICE.md`.

---

## Part A: new area

### Before the first question

Tell the user, in two or three short lines:
- this is a long interview, often 20 to 40 minutes, and nothing is saved until the end, so start
  when they have the time
- at the end they get a new skill named after their area, and they must save it
- what they say about their role and goals gets stored in that skill file, so keep that in mind
  if they plan to share it

### The grill

Interview the user relentlessly until you both understand exactly what they want to learn. Treat it
as a **decision tree**: each answer opens the questions that hang off it.

Work in **rounds**. The **frontier** is every question you can ask now without guessing at answers
you haven't heard yet. Ask the whole frontier in one round, number each question, give your
recommended answer, then wait. A question that depends on another question still open in this
round belongs to a later round.

Format each round like this:

```
❓ **Q1** - **<short title>**: <the question, with options if there are any>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

Word each question so that "yes" accepts your recommendation. Where only the user can know the
answer (their job, their goal), write `➡️ (your answer)` instead of guessing.

Facts about the subject are your job, never the user's. Don't ask "what are the main parts of
IFRS 17?"; propose them and ask whether that's the right cut.

The branches to cover. Not every area needs every one, and answers will open others:

1. **Area and boundary.** What exactly is in, and what's next door but out? ("Accounting" is too
   wide. "IFRS 17 for a UK annuity writer" is an area.)
2. **Why now.** Exam, new job, a project, curiosity? This sets how practical the questions get.
3. **Where they'll use it.** Role, industry, tools, who they explain it to. This is what makes the
   scenario questions from score 35 up feel real.
4. **Where they are now.** What they can already do and what confuses them. Probe with one or two
   concrete questions instead of taking "intermediate" at face value.
5. **Depth versus breadth.** Fewer topics in depth, or a wide map?
6. **Standards and versions.** Which jurisdiction, framework, dialect or version. (UK or US GAAP,
   Postgres or T-SQL, Python 3.12.)
7. **What to leave out.** Things they already know cold, or don't care about.
8. **Tone.** Default is blunt and Socratic: no praise words, talk about the answer and not the
   person. Ask only whether they want it softer. Softer changes the wording, not the scoring.

The grill is done when the frontier is empty: every branch visited, nothing silently assumed.
Then summarise what you heard in five or six lines and ask the user to confirm before moving on.

### Topic list

Propose 5 to 15 topics. For each give:
- a short **title** (2 to 6 words)
- a **description** of two to four sentences that says what the topic covers in *this user's*
  context and where its edges are. Later runs build questions from this text, so be specific.

Topics should be roughly even in size, related to each other, and not overlapping. Present them as
a numbered list and let the user add, cut, merge, split or reword. Repeat until they approve.

### Starting scores

Only after the topic list is approved. Show the three bands from `reference/scoring.md` in plain
words, then ask for a starting score for each topic.

- The default suggestion is 20 to 35. Starting high skips the basics, and the basics are where
  most of the learning is.
- **Nothing above 50.** The script refuses it.
- If someone wants above 35, ask them to explain the core idea of that topic in a sentence or two.
  If they can't, suggest 30.

### Finish

1. Write the spec to a temp file, e.g. `/tmp/hammer-time-spec.json`:

```json
{
  "area": {"title": "SQL for finance reporting", "slug": "sql"},
  "profile": {
    "role": "Finance systems manager at a UK pension insurer",
    "goal": "Write and review reporting queries without leaning on IT",
    "context": "Oracle Fusion, Oracle EPM, Power BI. Explains numbers to the CFO's team.",
    "current_level": "Comfortable with SELECT and simple joins, shaky on window functions",
    "out_of_scope": "DBA work, indexing internals",
    "tone": "blunt",
    "language": "English"
  },
  "topics": [
    {"title": "Joins and their traps", "description": "...", "score": 30}
  ]
}
```

   `slug` becomes the skill name (`hammer-time-sql`). Keep it short: lowercase letters, digits and
   hyphens, and not containing "claude" or "anthropic" (claude.ai refuses those names). The area
   title can be 60 characters at most. `language` is the language the user spoke during onboarding; ask questions in it later.

2. Run `python3 <skill>/scripts/ht.py init --file /tmp/hammer-time-spec.json`. If it errors, fix
   the spec and run it again. Don't work around it.
3. Run `package` and finish with the save message from `guides/updating.md`. Add one line: their
   onboarding template is untouched, so they can run it again for a different area.

Don't ask a first quiz question in the same run. Saving is the whole point of this step.

---

## Part B: level up a topic

When a topic reaches 90 or more, `ht.py` flags it at the end of a run and in reviews. Offer a
harder version; never force it.

1. Ask a short grill, one or two rounds, about where they want to go next with this topic. Propose
   the harder topic: "Joins and their traps" might become "Query plans and join performance".
2. Agree a title and a description, written the same way as in Part A.
3. Starting score: default 30. The new topic has its own basics, and starting low means they get
   asked. The cap is still 50.
4. Run:

```
python3 <skill>/scripts/ht.py levelup --topic t03 --title "..." --description "..." [--score 30]
```

The old topic is archived with its final score and stays in the history. Then `package` and the
save message.

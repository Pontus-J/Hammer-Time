# Onboarding

Part A turns the blank template into an area skill. Part B makes one topic in an existing area
harder once its score passes 90.

---

## Part A: new area

The user may know nothing about this skill beyond its name, and setup decides whether they come
back tomorrow. Keep it light: short rounds, plain words, one thing at a time. "Grill",
"frontier" and "decision tree" below are words for you; never use them with the user.

### Welcome

Send the `## Welcome` section of `README.md` close to word for word, from its bold title to
"**Ready?**", then **stop and wait**.

- If `status` printed `SAVING: ... installs in place`, replace step 3 with "**Your scores save
  themselves.** Nothing to do after each day."
- If they already have another `hammer-time-*` skill, or say they've used Hammer Time before, skip
  the welcome. Say in one line that you're setting up a new subject and go straight to step 1.
- **yes**: start step 1.
- **tell me more**, or a question: answer from "The big picture" in `README.md` (see "Explaining"
  in `SKILL.md`), then ask again whether they're ready.
- **not now**: tell them to type **hammer time** whenever they're ready, and stop.

### Four steps

Setup has four steps, then saving. Open the first message of each step with its marker on a line
of its own, so they always know where they are and how much is left:

- `**Step 1 of 4 · Your subject**`
- `**Step 2 of 4 · About you**`
- `**Step 3 of 4 · Topics**`
- `**Step 4 of 4 · Starting level**`

### Step 1: Your subject

Settle this before anything else. Everything later is built on it.

Open with one plain question: no number, no suggested answer.

```
**Step 1 of 4 · Your subject**

What do you want to learn, and what's it for? A sentence or two is plenty, e.g. "FP&A basics, I've
just joined the team" or "Power BI, we're rolling it out next quarter".
```

A good area has all four:
- **Judgement, not lookup.** Answers have a why, and a half-right answer can be corrected. That's
  where the back and forth earns its keep.
- **A general field.** A discipline, a body of practice, or the ideas behind a widely used tool,
  so public knowledge covers it well.
- **Depth.** Room for definitions, then scenarios, then trade-offs and defending a call. Roughly
  5 to 8 topics.
- **A reason to need it soon.** A new job, a new area, a tool being launched, a project. Work is
  the easiest frame; a personal subject (cooking, say) is fine too.

Sort what they asked for:

| kind | examples | what to do |
|---|---|---|
| Great | FP&A as a new joiner, controlling, accounting basics for a non-accountant, business partnering, Power BI data modelling | Go ahead |
| Lookup | shortcuts, formula syntax, acronyms, a list of rules | Say it works but mostly tests recall, and offer the judgement version. Go with their choice |
| Context-bound | a particular team or person, how my company does X, our internal system | Say why: you don't know the internals of any company, theirs included (its people, systems, processes or numbers), so your feedback would be guesswork. Offer the flip |
| Too narrow | one task or deliverable ("build the Q3 forecast") | A project, not a field; it runs out of topics. Offer the field underneath |
| Too wide | "finance", "AI" | Ask which slice matters for their role and goal |

**The flip.** Find the general field under the specific problem, and keep the specific problem as
context:
- **A person or team** → that side's field and what it needs, plus the general skill. "I struggle
  to work with marketing" → "Marketing basics for finance: how marketing measures success, what it
  needs from finance, and stakeholder management."
- **A company process** → the discipline behind it. "How our month-end works" → "Month-end close
  fundamentals: accruals, cut-off, reconciliations, review."
- **A tool** → its toolkit and areas of work, not its clicks. "Learn Power BI" → "Power BI: data
  modelling, Power Query and DAX." Teaching a widely used tool is fine; you know its concepts and
  languages well, but not where every button sits in the current release, so never quiz on that.
  A tool too new or niche for you to know → the ideas it's built on ("driver-based planning and
  model design").
- **A lookup list** → the judgement around it. "Excel shortcuts" → "Spreadsheet modelling:
  structure, checks, choosing the right formula."
- **One task** → the field. "Build the Q3 forecast" → "Forecasting: methods, drivers and
  assumptions."

Put the flip to them as a question, `➡️` the reworked area, with one line on why. Their original
problem goes into `profile.context`, so questions from score 35 up are set in it.

How hard to push:
- **Lookup:** say it once, then go with their choice.
- **Vague, context-bound, too narrow or too wide:** push back up to two more times, each time with
  a sharper proposal. Ten minutes of onboarding on a badly cut area costs more than two extra
  questions now. If they still want their own, go with it and name the limit once.
- **Through step 2:** keep honing. As answers come in, tighten the area and say so in one line
  ("Narrowing this to budgeting and forecasting; month-end is out").

Then restate the area in one line: what they want to be able to do or understand, and where they'll
use it. Ask whether that's it. That line becomes `profile.goal`.

### Step 2: About you (the grill)

Interview the user until you both understand exactly what they want to learn. Treat it as a
**decision tree**: each answer opens the questions that hang off it.

Work in **rounds**. The **frontier** is every question you can ask now without guessing at answers
you haven't heard yet. A question that depends on another question still open in this round belongs
to a later round.

**At most three questions per round.** If more are open, ask the three that the most others hang
off, and keep the rest for the next round. A wall of questions is what makes setup feel like an
exam.

Don't ask what you can already tell from their answers. Put your reading in the summary at the end
for them to correct.

Format each round like this. In the first round only, put this line above the first question:
"Reply with the number and **yes** to take my suggestion (`Q1 yes`), or answer in your own words."

```
❓ **Q1** - **<short title>**: <the question, with options if there are any>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

Word each question so that "yes" accepts your recommendation. Where only the user can know the
answer (their job, their goal), write `➡️ (your answer)` instead of guessing.

If replies don't map cleanly to the numbers (fewer answers than questions, bare "yes" lines), don't
guess silently. Say in one line which question you took each answer for, and carry on.

Facts about the subject are your job, never the user's. Don't ask "what are the main parts of
IFRS 17?"; propose them and ask whether that's the right cut.

The branches to cover. Not every area needs every one, and answers will open others:

1. **Boundary.** The area itself is settled in step 1. Here: what exactly is in, and what's next
   door but out?
2. **Why now.** Exam, new job, a project, curiosity? This sets how practical the questions get.
3. **Where they'll use it.** Role, industry, tools, who they explain it to. This is what makes the
   scenario questions from score 35 up feel real. Their own setup is fine as scenery, but topics
   stay on the field: company specifics go stale, and the field underneath lasts.
4. **Where they are now.** What they can already do and what confuses them, in their words. Don't
   take "intermediate" at face value; the warm-up in step 4 tests it.
5. **Depth versus breadth.** Fewer topics in depth, or a wide map?
6. **Standards and versions.** Which jurisdiction, framework, dialect or version. (UK or US GAAP,
   Postgres or T-SQL, Python 3.12.)
7. **What to leave out.** Things they already know cold, or don't care about.
8. **Tone.** Default is friendly and encouraging, like a good colleague teaching: hints instead
   of answers, credit for the essence. Ask only whether they want it more direct. Tone changes the
   wording, never the scoring.

Step 2 is done when the frontier is empty: every branch visited, nothing silently assumed. Then
summarise what you heard in five or six lines and ask the user to confirm before moving on.

### Map the field (for yourself)

Before proposing topics, sketch the field. Don't show the sketch; it shapes the list.

1. **Anchor on a published structure**, not your own sense of "the main parts": a professional
   syllabus or exam outline (ICAEW, ACCA, CIMA, CFA, IFoA), a standard's own structure, the
   chapters of a recognised textbook, or a tool's official documentation areas. Search the web if
   you can; otherwise use what you know and say which source you're working from.
2. **List the core ideas and what each depends on**, so basics come before what's built on them.
3. **Mark the key ideas** (the ones that change how everything else looks once they click) and the
   **classic misconceptions** learners in this field hold. That's where the questions bite.
4. **Cut to the user's goal and boundary**, and group what's left into topics.

### Step 3: Topics

Propose 5 to 8 topics. Fewer topics come round more often, so each one gets drilled. Go up to 15
only if the user asked for a wide map (branch 5). For each give:
- a short **title** (2 to 6 words)
- a **description** of two to four sentences: what the topic covers in *this user's* context,
  where its edges are, its key idea, and one or two misconceptions to test. Later runs build
  questions from this text, so be specific.

**Depth check, before showing the list.** For each topic, draft one Foundation, one Applied and
one Advanced question for yourself (see `reference/scoring.md`). No good Advanced question: the
topic is too thin, merge it. A Foundation question that needs two ideas: too wide, split it. A
question that could be scored against two topics: they overlap, redraw the line.

Order the list basics first: new topics are asked in list order. Open with one line naming the
source you anchored on. Present it as a numbered list and let the user add, cut, merge, split or
reword. Repeat until they approve.

### Step 4: Starting level

Only after the topic list is approved.

**Warm-up first.** Introduce it in your own words along these lines: "A quick warm-up so I start
you at the right level. It isn't scored, and 'not sure' is a perfectly good answer: it just means
we start with the basics." Then one round of two or three short questions, each on a different
topic, at Foundation level, answerable in a sentence or two. Pick the topics where you're least
sure of their level. Don't teach; one friendly line on each answer is enough.

Then propose a starting score for each topic in plain words, as a numbered list with a one-line
reason each, e.g. "I'd start you at 15 on most of these, and 25 on joins because you explained
them well." Add one line on why low is normal: starting high skips the basics. Don't show the band
table. Word it so "yes" accepts, and let them change any of them.

- Base every score on the warm-up answers and what they told you in branch 4. Don't set one number
  for every topic, and don't guess where they gave you nothing to go on: ask.
- Most topics land at 15 to 20, lower if the topic is new to them. Starting high skips the basics,
  and the basics are where most of the learning is.
- Above 20 only where they showed real knowledge in the warm-up or step 2. If they want higher,
  ask them to explain the core idea of that topic in a sentence or two. If they can't, suggest 20.
- **Nothing above 50.** The script refuses it.

### Daily reminder

One last question, in the same format:

```
❓ **Q1** - **Daily reminder**: Want a calendar event that reminds you every day? Pick a time and
weekdays or every day.

➡️ Yes, weekdays at 08:30
```

If yes, run this after `init` and before `package` (it reads the new area's name):

```
python3 <skill>/scripts/ht.py reminder --time 08:30 --days weekdays
```

`--days` is `weekdays` or `daily`. It writes the `.ics` file to the claude.ai outputs folder, or
elsewhere to `~/Downloads`, and prints the path. Give the user the file and tell them to open it to add the event
to their calendar. If they ask for a reminder later, from an area skill, run the same command.

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
    "tone": "friendly",
    "language": "English"
  },
  "topics": [
    {"title": "Joins and their traps", "description": "...", "score": 20}
  ]
}
```

   `slug` becomes the skill name (`hammer-time-sql`). Keep it short: lowercase letters, digits and
   hyphens, and not containing "claude" or "anthropic" (claude.ai refuses those names). The area
   title can be 60 characters at most. `language` is the language the user spoke during onboarding; ask questions in it later.

2. Run `python3 <skill>/scripts/ht.py init --file /tmp/hammer-time-spec.json`. If it errors, fix
   the spec and run it again. Don't work around it.
3. If they wanted a reminder, run `reminder` now.
4. Run `package` and finish with the save message from `guides/updating.md`. This is the first
   time they handle a skill file, so in place of the topic headline write one line saying what it
   is: "**Your new skill is ready: `<skill name>`.** It holds your topics and starting scores."
   After the save block, add:
   - how to start: "Tomorrow, open a new chat and type **hammer time <area words>**." (the skill
     name without `hammer-time-`, hyphens as spaces)
   - their onboarding skill is untouched, so they can type "hammer time" again for another subject.
   - if you made a reminder: open the `.ics` file to add it to their calendar.
   - sharing: the new skill holds what they told you about their role and goals, so share
     `hammer-time-onboarding` with colleagues, not this one.
   - "Ask **how does Hammer Time work?** any time."

Don't ask a first quiz question in the same run. Saving is the whole point of this step.

---

## Part B: level up a topic

When a topic reaches 90 or more, `ht.py` flags it at the end of a run and in reviews. Offer a
harder version; never force it.

1. Ask a short grill, one or two rounds, about where they want to go next with this topic. Propose
   the harder topic: "Joins and their traps" might become "Query plans and join performance".
2. Agree a title and a description, written the same way as in Part A.
3. Starting score: ask one warm-up question on the new topic, as in step 4 of Part A. If they nail it, 30;
   otherwise 15 to 20 (default 20). The new topic has its own basics, and starting low means they
   get asked. The cap is still 50.
4. Run:

```
python3 <skill>/scripts/ht.py levelup --topic t03 --title "..." --description "..." [--score 20]
```

The old topic is archived with its final score and stays in the history. Then `package` and the
save message.

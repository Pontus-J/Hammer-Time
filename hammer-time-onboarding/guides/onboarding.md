# Onboarding

Part A turns the blank template into an area skill. Part B makes one topic in an existing area
harder once its score passes 90.

---

## Part A: new area

### Before the first question

The user may know nothing about this skill beyond its name. This message is their whole manual.
Send it close to word for word, then **stop and wait**. Start round 1 only when they say they're ready.

```
**Welcome to Hammer Time.** It drills one subject into you, one question a day. Each topic gets a
score from 0 to 100, and the questions get harder as your score rises.

**First, a short setup (about 10 minutes, longer if you go deep).** I'll ask what you want to
learn and why, then propose topics and starting scores.

**How to answer:** questions come in numbered rounds, each with my suggested answer (➡️).
- Agree: reply with the number and "yes" (`Q1 yes`).
- Disagree or unsure: say so in your own words. The more detail you give, the better it fits you.

**What I know:** what's public, what you tell me, and what you ask me to look up. I don't know the
internals of any company, yours included (its systems, processes or numbers), so questions stay
with the subject itself plus whatever you describe to me.

**Picking a subject:** it works best on a field you're new to or about to need, where the hard
part is the judgement you'd normally pick up over years from experience and your manager.
- Great: "FP&A as a new joiner: budgeting, variances, business partnering", "Accounting basics
  for non-accountants", "Power BI for a team rolling it out: data modelling and DAX"
- Works, but wastes it: things you could look up, like Excel shortcuts. Right or wrong, nothing
  to reason about.
- Won't work as is: anything that hangs on your company's people or systems, like "working with
  my tricky marketing team". I'll help turn it into one that does: marketing basics for finance,
  plus stakeholder management.

**At the end** you get a new skill named after your subject. Save it, and from then on start each
day's question by typing its name. What you tell me about your role and goals is stored in it, so
keep that in mind if you share it.

Ready to start?
```

If `status` printed `SAVING: ... installs in place`, replace "Save it" with "It installs itself".
Don't add more explanation than that.
If they say not now, tell them to type "hammer time" whenever they're ready, and stop.

### Choosing the area

Settle this in round 1, before anything else. Everything later is built on it.

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
| Context-bound | a particular team or person, how my company does X, our internal system | Say why: the answers sit in people, history and systems you can't see, so your feedback would be guesswork. Offer the flip |
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
- **Through the grill:** keep honing. As answers come in, tighten the area and say so in one line
  ("Narrowing this to budgeting and forecasting; month-end is out").

Then restate the area in one line: what they want to be able to do or understand, and where they'll
use it. That line becomes `profile.goal`.

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

If replies don't map cleanly to the numbers (fewer answers than questions, bare "yes" lines), don't
guess silently. Say in one line which question you took each answer for, and carry on.

Facts about the subject are your job, never the user's. Don't ask "what are the main parts of
IFRS 17?"; propose them and ask whether that's the right cut.

The branches to cover. Not every area needs every one, and answers will open others:

1. **Boundary.** The area itself is settled above. Here: what exactly is in, and what's next door
   but out?
2. **Why now.** Exam, new job, a project, curiosity? This sets how practical the questions get.
3. **Where they'll use it.** Role, industry, tools, who they explain it to. This is what makes the
   scenario questions from score 35 up feel real. Their own setup is fine as scenery, but topics
   stay on the field: company specifics go stale, and the field underneath lasts.
4. **Where they are now.** What they can already do and what confuses them, in their words. Don't
   take "intermediate" at face value; the check questions under Starting scores test it.
5. **Depth versus breadth.** Fewer topics in depth, or a wide map?
6. **Standards and versions.** Which jurisdiction, framework, dialect or version. (UK or US GAAP,
   Postgres or T-SQL, Python 3.12.)
7. **What to leave out.** Things they already know cold, or don't care about.
8. **Tone.** Default is friendly and encouraging, like a good colleague teaching: hints instead
   of answers, credit for the essence. Ask only whether they want it more direct. Tone changes the
   wording, never the scoring.

The grill is done when the frontier is empty: every branch visited, nothing silently assumed.
Then summarise what you heard in five or six lines and ask the user to confirm before moving on.

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

### Topic list

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

### Starting scores

Only after the topic list is approved.

**Check questions first.** One round of two or three short questions, each on a different topic,
at Foundation level, answerable in a sentence or two. Pick the topics where you're least sure of
their level. Say they're not scored. Don't teach; one line on each answer is enough.

Then show the three bands from `reference/scoring.md` in plain words and propose a starting score
for each topic, with a one-line reason. Word it so "yes" accepts, and let them change any of them.

- Base every score on the check answers and what they told you in branch 4. Don't set one number
  for every topic, and don't guess where they gave you nothing to go on: ask.
- Most topics land at 15 to 20, lower if the topic is new to them. Starting high skips the basics,
  and the basics are where most of the learning is.
- Above 20 only where they showed real knowledge in the check questions or the grill. If they want higher, ask them to
  explain the core idea of that topic in a sentence or two. If they can't, suggest 20.
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
4. Run `package` and finish with the save message from `guides/updating.md`. Then add:
   - how to start: "Tomorrow, open a new chat and type **hammer time <area words>**." (the skill
     name without `hammer-time-`, hyphens as spaces)
   - their onboarding skill is untouched, so they can type "hammer time" again for another subject.
   - if you made a reminder: open the `.ics` file to add it to their calendar.

Don't ask a first quiz question in the same run. Saving is the whole point of this step.

---

## Part B: level up a topic

When a topic reaches 90 or more, `ht.py` flags it at the end of a run and in reviews. Offer a
harder version; never force it.

1. Ask a short grill, one or two rounds, about where they want to go next with this topic. Propose
   the harder topic: "Joins and their traps" might become "Query plans and join performance".
2. Agree a title and a description, written the same way as in Part A.
3. Starting score: ask one check question on the new topic, as in Part A. If they nail it, 30;
   otherwise 15 to 20 (default 20). The new topic has its own basics, and starting low means they
   get asked. The cap is still 50.
4. Run:

```
python3 <skill>/scripts/ht.py levelup --topic t03 --title "..." --description "..." [--score 20]
```

The old topic is archived with its final score and stays in the history. Then `package` and the
save message.

# Hammer Time

This page explains what Hammer Time is and how to use it. You don't need to read it to get
started: type **hammer time** in a chat and Claude walks you through it. The Welcome below is what
Claude says the first time you start. After that, ask "how does Hammer Time work?" at any point and
Claude answers from the rest of this page.

## Welcome

**Welcome to Hammer Time** 🔨
It helps you learn one subject properly, a few minutes a day. You get one question, answer in your
own words, and if you're stuck I'll help you work it out. No multiple choice, no trick questions.

**How it works**
1. **Setup, once (about 10 minutes).** We talk about what you want to learn and why. I suggest
   topics, and you say yes or change them.
2. **One question a day.** Type **hammer time** and your subject in a new chat (say,
   **hammer time fpa**). Each topic has a score from 0 to 100 that rises as you get things right,
   and the questions get harder as it does.
3. **Save after each day.** I give you an updated copy of the skill with your new scores.

Nothing is scored during setup, and you can stop at any time. Ask "how does Hammer Time work?"
whenever you want the full picture.

**Ready?** Reply **yes**, or **tell me more**.

## The big picture

### What it's for

Hammer Time drills one subject into you over a few weeks, one question a day. Claude asks, you
answer in your own words, and you talk it through until it clicks. Each answer moves a score, and
the score decides how hard the next question is.

It works best on a field you're new to or about to need, where the hard part is judgement you'd
normally pick up over years from experience and a good manager. For example:
- FP&A as a new joiner: budgeting, variances, business partnering
- Accounting basics for non-accountants
- Power BI for a team rolling it out: data modelling and DAX

It works less well for things you could look up, like keyboard shortcuts or formula syntax: an
answer is right or wrong, with nothing to reason about. And it can't teach what only exists inside
your company, like a particular team or an internal system, because Claude doesn't know it. Ask for
one of those and Claude offers the general field underneath instead ("working with marketing"
becomes "marketing basics for finance, plus stakeholder management").

### Your skills

Hammer Time comes as two kinds of skill:

| skill | what it is | what you do with it |
|---|---|---|
| `hammer-time-onboarding` | The one you installed first. It sets up a new subject and never changes. | Keep it. Type **hammer time** to set up another subject. |
| `hammer-time-<subject>`, e.g. `hammer-time-fpa` | Made at the end of setup, one per subject. It holds your topics, scores and every question you've been asked. | Use it every day: type **hammer time fpa**. |

Deleting a subject skill deletes its scores.

### Setup

About 10 minutes, in four steps:

1. **Your subject.** What you want to learn and what it's for. If the subject won't suit the drill,
   Claude suggests a version that does.
2. **About you.** A few short rounds of questions: your role, where you'll use it, what you know
   already, what to leave out. Each question comes numbered with Claude's suggested answer. Reply
   `Q1 yes` to take the suggestion, or answer in your own words.
3. **Topics.** Claude proposes 5 to 8 topics, built from a published syllabus, standard or textbook
   where one exists. You add, cut, merge or reword until they're right.
4. **Starting level.** Two or three warm-up questions, not scored, set a starting score for each
   topic. Most start at 15 to 20, so the basics get asked first.

Then, if you want, a daily calendar reminder, and you save your new skill.

### A day with Hammer Time

1. Open a new chat and type **hammer time fpa** (your subject's name).
2. Claude picks the topic that's due: new topics first, then the one asked least recently. Never
   the same topic twice in a row. You can also ask for a topic.
3. One question, never one you've had before. Now and then it comes back to something you found
   hard weeks ago, from a new angle. Answer in a few sentences, in your own words.
4. If you've got it, Claude says what you got right and adds a bit of detail. If not, it gives you
   hints, up to three, and lets you work it out. Say "I don't know" and it helps you make a guess;
   say it again and it gives you the answer.
5. Whatever happens, you finish with a clear explanation, your new score and a file to save.
6. "One more?" Say yes for another question. Scores from earlier in the chat carry over.

About five minutes.

### Scores

Every topic has a score from 0 to 100. It measures how deep your understanding goes, not how many
answers you've got right.

| score | level | what the questions ask |
|---|---|---|
| 0-34 | Foundation | definitions, how and why things work |
| 35-64 | Applied | scenarios from your own work, trade-offs |
| 65-100 | Advanced | tying topics together, defending a decision, teaching it back |

| result | change |
|---|---|
| right first time | +5 |
| right with hints | +2 |
| partly right | 0 |
| missed, or gave up | -5 |

You're marked on understanding, not wording: a short answer that gets the idea counts in full. At
90, Claude offers a harder version of the topic. The old one is archived with its final score.

### Saving, and why

Your scores live inside your subject skill, so after each day Claude gives you an updated copy:

- **claude.ai:** click **Save skill** on the file at the end of the chat. It replaces your current
  copy. (Or upload the file under **Settings > Capabilities > Skills**.)
- **Claude Code on your own computer:** it saves itself. Nothing to do.

If you skip saving, that day's score is lost and next time starts from your previous scores.
Nothing else breaks.

### Things you can ask for

- **hammer time fpa**: today's question
- **hammer time fpa review**: where you stand, how many questions you've answered, how far each
  topic has come, what keeps tripping you up, and a chance to add, cut, merge or reword topics
- a question on a particular topic
- a harder version of a topic once it reaches 90
- a daily reminder: a calendar event to add to your calendar
- "how does this work?" or "what have I set up?": an explanation from this page, with your own
  topics and scores

### What Claude knows, and what the skill keeps

Claude knows what's public about your subject, what you tell it, and what you ask it to look up. It
doesn't know the internals of any company, yours included (its systems, processes or numbers), so
scenarios use what you describe and stay general otherwise.

Your subject skill keeps:
- what you said in setup: your role, goal and context, where you started, what to leave out, and
  your preferred tone and language
- your topics and their scores
- every question you've been asked, with the date, the result and a one-line note on what you
  showed and what was missing. Your answers and the back and forth aren't kept.

It lives in your Claude account, or on your computer in Claude Code, like any other skill. Hammer
Time itself sends nothing anywhere.

### Sharing with colleagues

Share `hammer-time-onboarding`, so they set up their own subject. Don't share your subject skill: it
holds what you told Claude about yourself and notes on your answers, and they'd start on your
scores. If someone sent you theirs, ask them for `hammer-time-onboarding` instead and set up your
own.

### When something goes wrong

- **"Hammer Time needs code execution."** On claude.ai go to **Settings > Capabilities**, turn on
  **Code execution and file creation**, start a new chat and type **hammer time** again.
- **It asks which subject you mean.** You have more than one. Say which.
- **You forgot to save.** That day's score is gone. Carry on from your previous scores.
- **A score went in wrong.** Say so. Claude can't undo it, but the next answer on that topic is
  scored normally.
- **Too easy or too hard.** Questions follow your score, so they adjust within a week or two. For
  bigger changes, ask for a review and change the topics.
- **You've been away.** Nothing is lost. After two weeks or more, the first question back starts a
  little easier.
- **You want to start a subject over.** Delete the subject skill (**Settings > Capabilities >
  Skills** on claude.ai, or its folder in `~/.claude/skills/` in Claude Code), then type
  **hammer time** to set it up again.

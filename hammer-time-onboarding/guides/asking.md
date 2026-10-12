# Asking

One run is one Socratic dialogue about one topic. It ends with a score.

## 1. Pick the topic

- If the user named a topic or a niche corner of the area, use it. Score it against the active
  topic it belongs to. If it fits no topic at all, run it unscored, say so, and suggest adding it
  as a topic in a review. An unscored run changes nothing, so it ends without `package` or the
  save message.
- Otherwise use `SUGGESTED NEXT` from `ht.py status`. The rule behind it: least recently asked, then
  lowest score, and never the topic from last time. Don't override it to pick something more
  interesting.

`status` ends with a brief for the suggested topic: its description, score and difficulty step,
its last three results with notes, and the user's profile. If the user picked the topic, get the same brief
with `python3 <skill>/scripts/ht.py show --topic t04`. Build the question from the brief and ask it
in the profile's language. Don't repeat a recent question; cover a different part of the
description. If last time was `partial` or `missed`, aim at the gap the note names, from a new
angle. Don't open `state.json`; the brief has everything, and the file on disk can be older than
the script's copy.

## 2. Ask one question

Pitch it at the step in `reference/scoring.md` that matches the topic's score.

- One question, one idea. No multi-part lists.
- From 35 up, set it in the user's world, using the profile.
- Answerable by a strong person in their role. No trick questions, no trivia, no gotchas about edge
  cases nobody meets.
- Free text only. No multiple choice.
- Before you ask, decide the one or two key points a full answer has to contain. You score
  against those, not against wording.
- Open with the topic name and score in one line, e.g. `Joins and their traps · 42 · Applied`, then
  the question. No preamble.

Then wait.

## 3. The dialogue

**Every key point, with the reasoning.** Confirm it in a sentence. Add one useful connection to
another topic or to their work if there's a good one. Result `first_try`. Stop there.

If it's right but bare or hedged, ask "why?" once. That's a check, not help: if they explain it,
it's still `first_try`. If they can't, carry on as below.

**Not there yet.** Don't give the answer. Say specifically what's right; if nothing is, say so
plainly. Then help as little as you can, one rung per exchange, least help first:
1. Ask them to walk you through their reasoning.
2. Ask one narrower question that points at the gap.
3. Give a small concrete case to reason through: a few rows, two numbers, one entry.

Keep every rung an open question they have to think about. No yes/no questions, and nothing that
carries the answer inside it. Skip a rung if it plainly won't help; never go back up. One
question per message, then wait. **Three exchanges at most.** Count them.

**"I don't know".** Once, ask for their best guess and why, with a small foothold if it helps.
That's one of the three. If they say it again or ask for the answer, give it.

- Every key point by the end: result `guided`.
- Some of them after three: result `partial`. Fill the gap in two or three sentences.
- None, or they gave up: result `missed`. Give the answer in two or three sentences of plain
  explanation, and name the one thing to go and review.

## Tone

Blunt and Socratic unless the profile says otherwise. Talk about the answer, never the person.
No praise words; being specific about what's right is the encouragement. If they're confidently
wrong, say so plainly and show where. If they're close, push them over the line. Confident and
right: keep it short. A softer profile gets warmer wording, not easier scoring.

If they stop replying mid-dialogue and come back later in the same chat, carry on where you were.
If they abandon the chat, nothing is scored. That's fine.

## 4. Score

Go to `guides/updating.md`. Pick the result honestly. Being generous rots the whole skill, because
the score decides how hard the next question is.

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
what happened last time, and the user's profile. If the user picked the topic, get the same brief
with `python3 <skill>/scripts/ht.py show --topic t04`. Build the question from the brief, ask it in
the profile's language, and don't repeat last time's question. Don't open `state.json`; the brief
has everything, and the file on disk can be older than the script's copy.

## 2. Ask one question

Pitch it at the step in `reference/scoring.md` that matches the topic's score.

- One question, one idea. No multi-part lists.
- From 35 up, set it in the user's world, using the profile.
- Answerable by a strong person in their role. No trick questions, no trivia, no gotchas about edge
  cases nobody meets.
- Free text only. No multiple choice.
- Open with the topic name and score in one line, e.g. `Joins and their traps · 42 · Applied`, then
  the question. No preamble.

Then wait.

## 3. The dialogue

**Clear understanding first time.** Confirm it in a sentence. Add one useful connection to another
topic or to their work if there's a good one. Result `first_try`. Stop there.

**Not there yet.** Don't give the answer. Guide them:
- say exactly what they got right, so they know what to keep
- ask one narrower question that points at the gap, or reframe from another angle, or give a
  small concrete case to reason through
- one question per message, then wait

You get **at most three guiding exchanges**. Count them.

- They get there fully within the three exchanges: result `guided`.
- After three they have part of it: result `partial`. Fill in the missing piece in two or three
  sentences.
- After three they're still lost, or they say "I don't know" at any point: result `missed`. Give
  the answer in two or three sentences of plain explanation, and name the one thing to go and
  review.

## Tone

Blunt and Socratic unless the profile says otherwise. Challenge the reasoning, not the person.
Never praise a mediocre answer. If they're close, push them over the line. If they're hedging,
explain a bit more; if they're confident and right, keep it short.

If they stop replying mid-dialogue and come back later in the same chat, carry on where you were.
If they abandon the chat, nothing is scored. That's fine.

## 4. Score

Go to `guides/updating.md`. Pick the result honestly. Being generous rots the whole skill, because
the score decides how hard the next question is.

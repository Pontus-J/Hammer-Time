# Scoring reference

## What a score means

A score is how deep the user's understanding of one topic goes. It is not a count of right answers.

| band | score | the user can... | question style |
|---|---|---|---|
| Foundation | 0-34 | name and define the building blocks | "What is X?" "Why does X exist?" |
| Applied | 35-64 | use the topic in a realistic situation and weigh options | "Here's a situation. What do you do and why?" |
| Advanced | 65-100 | tie it to other topics, handle exceptions, defend a design | "Someone senior challenges your approach. Answer them." |

## Difficulty gradient

Pitch each question at the step for the topic's current score. Within a step, lean harder if the
last answer on this topic (`LAST TIME` in the brief) was `first_try`, easier if it was `missed`.

| score | step | example shape |
|---|---|---|
| 0-15 | Definitions | "What does a LEFT JOIN give you that an INNER JOIN doesn't?" |
| 16-34 | How and why it works | "Why does a LEFT JOIN return NULLs, and when is that a problem?" |
| 35-49 | Apply in a scenario | "Finance wants every supplier listed, paid or not. Write the query and explain the join." |
| 50-64 | Trade-offs, two concepts at once | "This report runs in 4 minutes. Join first or aggregate first? Why?" |
| 65-79 | Tie topics together, edge cases | "How do NULL handling and your join choice interact when totals don't reconcile?" |
| 80-89 | Design and defend | "The CFO says the numbers are wrong because of your join. Defend or concede." |
| 90-100 | Teach it back, challenge the premise | "Teach this to a new joiner, then tell me where the textbook rule breaks." |

Use the user's profile (role, goal, context) to set the scene from 35 up. A finance person gets
finance scenarios.

## The ladder

Flat across all bands. A clear miss costs as much as a clean answer earns.

| result | meaning | change |
|---|---|---|
| `first_try` | the essence of every key point, in any words, without hints (a plain "why?" isn't a hint) | +5 |
| `guided` | every key point, with hints, within three hints | +2 |
| `partial` | some key points after three hints | 0 |
| `missed` | none of them, or they gave up | -5 |

Judge substance, not wording: a short answer that gets the essence is a full answer. Between two
results, pick the higher one.

Scores stay between 0 and 100. `ht.py` applies this; you only pick the result.

## Fixed numbers

- 5 to 15 active topics; 5 to 8 recommended.
- Starting scores: 0 to 50. Proposed from what the user said; most land at 15-20, above 20 only if the user can explain the basics unprompted.
- A topic at 90+ is offered a harder version. The harder version starts at 15-20 (default 20), or 30 if the user nails a check question on it.
- The log keeps the last 20 answers.

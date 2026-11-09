# Review

A look at where the user stands, plus a chance to change the topic list. No quiz question in this
run.

## 1. Get the data

```
python3 <skill>/scripts/ht.py review
```

This prints every topic with its score, band and change since the last review, the last 20
answers with their notes, topics ready to level up (90+), topics close to it (85-89), topics
never asked, and topics whose last three results were all first try (`ALWAYS FIRST TRY`) or all
partial or missed (`STUCK`).

## 2. Write the review

Keep it short and specific. Base it only on the data; don't invent progress.

1. **The table** from the output, as is.
2. **Where you stand**, two or three sentences. Read the notes in the log for patterns: the same
   gap showing up across different topics ("keeps confusing timing with measurement"), strengths
   that carry over, topics drifting because they're rarely asked. Name the pattern and the one
   thing that would move the most scores.
3. **Weakest topics**, the two or three lowest, each with one line on what's holding it back if the
   notes show it.
4. **Ready for harder**, any topic at 90+: offer a harder version (`guides/onboarding.md`, part B).
   Topics at 85-89: say they're close.
5. **Topic shape**, only if the data shows it:
   - `ALWAYS FIRST TRY`: it started too low and will climb on its own, or it's too easy for them.
     Suggest a level up if it's past 65, otherwise let it run.
   - `STUCK`: too big, or missing a basic underneath. Suggest splitting it, or adding the missing
     basic as its own topic.
   - Notes in the log that would fit another topic just as well: the two overlap. Suggest
     redrawing the line with `edit-topic`.
6. **Topic list check**, one question: anything to add, cut, merge or reword?

If there are fewer than five answers in the log, say there isn't enough to see a pattern yet, and
show just the table and the topic list check.

## 3. Apply changes

Only what the user agrees to. Each one goes through the script:

```
python3 <skill>/scripts/ht.py add-topic --title "..." --description "..." --score 20
python3 <skill>/scripts/ht.py retire-topic --topic t07
python3 <skill>/scripts/ht.py edit-topic --topic t04 [--title "..."] [--description "..."]
python3 <skill>/scripts/ht.py levelup --topic t02 --title "..." --description "..." [--score 20]
```

Limits: 5 to 15 active topics; new topics start at 50 at most, 15 to 20 suggested.

## 4. Finish

Always run `python3 <skill>/scripts/ht.py mark-review`, so the next review shows change since today. Then `package` and the
save message from `guides/updating.md`, using the full table and no single-topic headline.

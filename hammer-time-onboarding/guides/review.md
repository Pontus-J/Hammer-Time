# Review

A look at where the user stands, plus a chance to change the topic list. No quiz question in this
run.

## 1. Get the data

```
python3 <skill>/scripts/ht.py review
```

This prints every topic with its score, band and change since the last review, the last 20
answers with their notes, topics near the top (85+), and topics never asked.

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
5. **Topic list check**, one question: anything to add, cut, merge or reword?

If there are fewer than five answers in the log, say there isn't enough to see a pattern yet, and
show just the table and the topic list check.

## 3. Apply changes

Only what the user agrees to. Each one goes through the script:

```
ht.py add-topic --title "..." --description "..." --score 30
ht.py retire-topic --topic t07
ht.py edit-topic --topic t04 [--title "..."] [--description "..."]
ht.py levelup --topic t02 --title "..." --description "..." [--score 30]
```

Limits: 5 to 15 active topics; new topics start at 50 at most, 20 to 35 suggested.

## 4. Finish

Always run `ht.py mark-review`, so the next review shows change since today. Then `package` and the
save message from `guides/updating.md`, using the full table and no single-topic headline.

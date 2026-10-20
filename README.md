# Hammer Time

A Claude skill that hammers in knowledge about one area, one Socratic question at a time.

## Get started (claude.ai, 2 minutes)

1. **[Download hammer-time-onboarding.skill](https://github.com/Pontus-J/Hammer-Time/raw/main/dist/hammer-time-onboarding.skill)**.
   That one file is all you need. You don't need anything else from this page.
2. On claude.ai, go to **Settings → Capabilities → Skills** and upload the file.
3. Start a new chat and type **hammer time**. It explains the rest.

You run it, it asks you one question about one topic, pushes back until you either get it or clearly
don't, and scores you. Every topic has a score from 0 to 100, and the score decides how hard the
next question is:

| score | band | questions |
|---|---|---|
| 0-34 | Foundation | definitions, how and why things work |
| 35-64 | Applied | scenarios from your own job, trade-offs |
| 65-100 | Advanced | tying topics together, defending a design, teaching it back |

Right first time is +5. A clear miss is -5. Past 90, it offers you a harder version of the topic.

## How it works

1. **Onboarding.** It grills you on what you want to learn, why, where you'll use it and where you
   are now, in numbered rounds with a suggested answer for each: reply `Q1 yes` to agree, or say
   more. Usually about 10 minutes. It checks your subject is narrow enough and something it can
   know (public knowledge, not your company's internals), proposes 5 to 8 topics for you to edit,
   then proposes a starting score for each from what you told it (usually 15 to 20, 50 at most).
   It can also give you a daily calendar reminder.
2. **It hands you a new skill**, e.g. `hammer-time-sql`. Save it. Your onboarding template stays as
   it was, so you can onboard another area later.
3. **Every day after that**, say "hammer time sql". One question, a short back and forth, a score,
   and an updated skill file. **Save it every time.** That's how the scores persist. Say yes to
   "One more?" if you want another.
4. **Now and then**, ask for "hammer time sql review" to see where you stand, what keeps tripping
   you up and whether to change topics.

One area per skill. Keep the topics in an area related to each other.

## Why the script

The skill changes itself after every run, and a model asked to rewrite a long file while changing
one number will eventually paraphrase a rule or drop a line without anyone noticing. So the model
never rewrites anything. `scripts/ht.py` changes the scores in `state.json`, keeps a log of the last
20 answers, picks the next topic, and repackages the skill as an exact copy of what's installed plus
the new state. The model runs the conversation; the script keeps the books.

## Install

**claude.ai**: see [Get started](#get-started-claudeai-2-minutes) above. Don't download just
`SKILL.md` or use the green Code → Download ZIP button: the skill also needs its `scripts/` and
guides, and the `.skill` file has them packed in the right shape. If code execution is off, the
skill tells you how to turn it on.

**Claude Code**: copy the `hammer-time-onboarding` folder into `~/.claude/skills/` and type
"hammer time". Runs update the installed skill directly, so there's nothing to save by hand.

**Status:** in daily use on claude.ai, where **Save skill** keeps the whole folder and the scores
carry over, and tested end to end in Claude Code.

**Moving an area between the two**: in Claude Code, run
`python3 ~/.claude/skills/hammer-time-<area>/scripts/ht.py package --out ~/Desktop` and upload the
`.skill` file on claude.ai. Use one platform per area from then on; the two copies don't sync.

## Credits

The onboarding interview is adapted from Matt Pocock's
[`grilling`](https://github.com/mattpocock/skills) skill (MIT). See
`hammer-time-onboarding/NOTICE.md`.

MIT License.

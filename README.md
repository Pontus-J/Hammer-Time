# Hammer Time

A Claude skill that hammers in knowledge about one area, one Socratic question at a time.

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

1. **Install `hammer-time-onboarding`** (see below) and say "start hammer time".
2. **Onboarding.** It grills you on what you want to learn, why, where you'll use it and where you
   are now, in numbered rounds with a suggested answer for each: reply `Q1 yes` to agree, or say
   more. Usually about 10 minutes. It proposes 5 to 15 topics, you edit them, then you set a
   starting score for each (50 at most; 20 to 35 is usually right).
3. **It hands you a new skill**, e.g. `hammer-time-sql`. Save it. Your onboarding template stays as
   it was, so you can onboard another area later.
4. **Every day after that**, say "hammer time sql". One question, a short back and forth, a score,
   and an updated skill file. **Save it every time.** That's how the scores persist.
5. **Now and then**, ask for "hammer time sql review" to see where you stand, what keeps tripping
   you up and whether to change topics.

One area per skill. Keep the topics in an area related to each other.

## Install

**claude.ai**: needs code execution turned on (Settings → Capabilities). Download
`hammer-time-onboarding.skill` from `dist/` and upload it under Settings → Capabilities → Skills.
After each run, click **Save skill** on the file Claude gives you.

**Claude Code**: copy the `hammer-time-onboarding` folder into `~/.claude/skills/`. Runs update the
installed skill directly, so there's nothing to save by hand.

**Status:** tested end to end in Claude Code. On claude.ai, whether **Save skill** from a chat keeps
the whole folder (scripts and guides) or only `SKILL.md` is not yet confirmed. If only `SKILL.md`
survives, download the file after each run and re-upload it in Settings instead.

**Moving an area between the two**: in Claude Code, run
`python3 ~/.claude/skills/hammer-time-<area>/scripts/ht.py package --out ~/Desktop` and upload the
`.skill` file on claude.ai. Use one platform per area from then on; the two copies don't sync.

## Why the script

The skill changes itself after every run, and a model asked to rewrite a long file while changing
one number will eventually paraphrase a rule or drop a line without anyone noticing. So the model
never rewrites anything. `scripts/ht.py` changes the scores in `state.json`, keeps a log of the last
20 answers, picks the next topic, and repackages the skill as an exact copy of what's installed plus
the new state. The model runs the conversation; the script keeps the books.

## Credits

The onboarding interview is adapted from Matt Pocock's
[`grilling`](https://github.com/mattpocock/skills) skill (MIT). See
`hammer-time-onboarding/NOTICE.md`.

MIT License.

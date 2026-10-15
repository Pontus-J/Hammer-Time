#!/usr/bin/env python3
"""Hammer Time state engine.

Every change to the skill's state goes through this script, so the arithmetic,
the topic choice and the packaging never depend on the model's memory.

The installed skill folder is treated as read-only (it is on claude.ai). The
first command that changes anything copies the skill into a work folder, all
later commands read and write that copy, and `package` turns it into a .skill
file the user saves (or installs it locally in Claude Code).

Python 3.8+, standard library only.
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile

SCHEMA_VERSION = 1

# Scoring ladder. Flat across all bands, symmetric at the ends.
RESULTS = {
    "first_try": 5,   # clear understanding straight away
    "guided": 2,      # got there fully with guiding, within three exchanges
    "partial": 0,     # partly there after guiding
    "missed": -5,     # still lost after three guiding exchanges, or "I don't know"
}

MIN_SCORE, MAX_SCORE = 0, 100
APPLIED_FROM, ADVANCED_FROM = 35, 65  # band edges
START_CAP = 50          # nobody self-estimates above this
LEVELUP_DEFAULT = 30    # where a levelled-up topic starts unless the user says otherwise
LEVELUP_THRESHOLD = 90  # at or above this, suggest a harder version of the topic
MIN_TOPICS, MAX_TOPICS = 5, 15
LOG_LIMIT = 20
RECENT_LIMIT = 3  # results kept per topic, so questions don't repeat once the log has moved on
TITLE_MAX = 60          # keeps the generated SKILL.md description under claude.ai's 1024 limit
DESCRIPTION_MAX = 1024
RESERVED_WORDS = ("anthropic", "claude")  # claude.ai refuses skill names containing these

# Difficulty steps, lowest score of each step first. Must match reference/scoring.md.
STEPS = [
    (0, "Definitions"),
    (16, "How and why it works"),
    (35, "Apply in a scenario"),
    (50, "Trade-offs, two concepts at once"),
    (65, "Tie topics together, edge cases"),
    (80, "Design and defend"),
    (90, "Teach it back, challenge the premise"),
]

TEMPLATE_NAME = "hammer-time-onboarding"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_ROOT = os.path.join(tempfile.gettempdir(), "hammer-time-work")
CLAUDE_AI_OUTPUTS = "/mnt/user-data/outputs"


# ---------------------------------------------------------------- helpers

def die(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def today():
    return dt.date.today().isoformat()


def band(score):
    if score < APPLIED_FROM:
        return "Foundation"
    if score < ADVANCED_FROM:
        return "Applied"
    return "Advanced"


def step(score):
    return [name for lowest, name in STEPS if score >= lowest][-1]


def clamp(n):
    return max(MIN_SCORE, min(MAX_SCORE, n))


def rmtree(path):
    """shutil.rmtree that also clears read-only leftovers."""
    def retry(fn, p, exc):
        os.chmod(p, 0o700)
        parent = os.path.dirname(p)
        os.chmod(parent, os.stat(parent).st_mode | 0o700)
        fn(p)
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=retry)  # onerror warns from 3.12
    else:
        shutil.rmtree(path, onerror=retry)


def read_frontmatter_name(skill_dir):
    with open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
    if not m:
        die("SKILL.md has no name in its frontmatter")
    return m.group(1)


def work_dir_for(name):
    return os.path.join(WORK_ROOT, name)


def redirect_path():
    # Written by `init`, which renames the work copy away from the installed skill's name.
    return os.path.join(WORK_ROOT, read_frontmatter_name(SKILL_DIR) + ".renamed-to")


def active_dir():
    """Where to read from: the work copy if this session already changed something."""
    name = read_frontmatter_name(SKILL_DIR)
    if os.path.isfile(redirect_path()):
        with open(redirect_path(), encoding="utf-8") as f:
            name = f.read().strip()
    wd = work_dir_for(name)
    if os.path.isfile(os.path.join(wd, "SKILL.md")):
        return wd
    return SKILL_DIR


def clear_redirect():
    if os.path.isfile(redirect_path()):
        os.remove(redirect_path())


def ensure_work_copy():
    src = active_dir()
    if src != SKILL_DIR:
        return src
    name = read_frontmatter_name(SKILL_DIR)
    wd = work_dir_for(name)
    if os.path.exists(wd):
        rmtree(wd)
    shutil.copytree(SKILL_DIR, wd, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    # The installed skill may be read-only (it is on claude.ai); the copy must not be.
    for root, dirs, files in os.walk(wd):
        for n in dirs + files:
            p = os.path.join(root, n)
            os.chmod(p, os.stat(p).st_mode | 0o200)
    os.chmod(wd, os.stat(wd).st_mode | 0o200)
    return wd


def begin_change():
    """Check there is state to change, then return the work copy and its state."""
    load_state()  # dies before any copying if this copy was never onboarded
    wd = ensure_work_copy()
    return wd, load_state(wd)


def state_path(d):
    return os.path.join(d, "state.json")


def load_state(d=None, required=True):
    d = d or active_dir()
    p = state_path(d)
    if not os.path.isfile(p):
        if required:
            die("no state.json yet. This copy has not been onboarded; follow guides/onboarding.md")
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_state(state, d):
    state["updated"] = today()
    with open(state_path(d), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_topic(state, topic_id):
    for t in state["topics"]:
        if t["id"] == topic_id:
            return t
    die("no active topic with id %r. Run `status` to see ids" % topic_id)


def next_topic_id(state):
    used = [t["id"] for t in state["topics"]] + [t["id"] for t in state.get("archived_topics", [])]
    n = max([int(i[1:]) for i in used if re.fullmatch(r"t\d+", i)] or [0]) + 1
    return "t%02d" % n


def valid_start_score(n, label):
    if not isinstance(n, int) or n < MIN_SCORE or n > START_CAP:
        die("%s: starting score must be a whole number from 0 to %d, got %r" % (label, START_CAP, n))


def pick_topic(state):
    """Least recently asked, then lowest score, never the topic asked last time."""
    topics = list(state["topics"])
    log = state.get("log") or []
    # Position of each topic's latest answer in the log. A topic missing from the log was last
    # asked before everything in it, so its last_asked date orders it among the others like it.
    recent = {e["topic"]: i for i, e in enumerate(log)}
    last = log[-1]["topic"] if log else None
    pool = [t for t in topics if t["id"] != last] or topics
    pool.sort(key=lambda t: (recent.get(t["id"], -1), t["last_asked"] or "", t["score"], t["id"]))
    return pool[0]


def table(state):
    rows = ["| id | topic | score | band | asked | last asked |", "|---|---|---|---|---|---|"]
    for t in state["topics"]:
        rows.append("| %s | %s | %d | %s | %d | %s |" % (
            t["id"], t["title"], t["score"], band(t["score"]), t["times_asked"], t["last_asked"] or "never"))
    return "\n".join(rows)


def print_brief(state, t):
    """Everything Claude needs to ask about one topic, so it never reads state.json itself."""
    print("TOPIC: %s %s" % (t["id"], t["title"]))
    print("SCORE: %d, %s band, step: %s" % (t["score"], band(t["score"]), step(t["score"])))
    print("DESCRIPTION: %s" % t["description"])
    last = None
    if t.get("last_result"):
        last = (t["last_asked"], t["last_result"], t.get("last_note", ""))
    else:  # skills scored before last_result was stored: fall back to the log
        for e in reversed(state["log"]):
            if e["topic"] == t["id"]:
                last = (e["date"], e["result"], e["note"])
                break
    if last:
        print("LAST TIME: %s, %s. %s" % last)
        for e in t.get("recent", [])[1:]:
            print("BEFORE THAT: %s, %s. %s" % (e["date"], e["result"], e["note"]))
    elif t["times_asked"]:
        print("LAST TIME: %s, result no longer in the log" % t["last_asked"])
    else:
        print("LAST TIME: never asked")
    print("PROFILE:")
    for k, v in (state.get("profile") or {}).items():
        print("- %s: %s" % (k, v))


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:40].strip("-")


# ---------------------------------------------------------------- commands

def cmd_status(args):
    state = load_state(required=False)
    if state is None:
        print("MODE: onboarding")
        print("This copy has no state. Follow guides/onboarding.md.")
        return
    print("MODE: active")
    print("AREA: %s (skill name %s)" % (state["area"]["title"], state["skill_name"]))
    if active_dir() != SKILL_DIR:
        print("UNPACKAGED CHANGES: an earlier run changed state but never ran `package`. "
              "These scores include them; `package` at the end of this run saves them too.")
    print()
    print(table(state))
    print()
    pick = pick_topic(state)
    print("SUGGESTED NEXT: %s %s (score %d, %s band)" % (pick["id"], pick["title"], pick["score"], band(pick["score"])))
    high = [t for t in state["topics"] if t["score"] >= LEVELUP_THRESHOLD]
    if high:
        print("READY TO LEVEL UP: " + ", ".join("%s %s (%d)" % (t["id"], t["title"], t["score"]) for t in high))
    print()
    print_brief(state, pick)


def cmd_show(args):
    state = load_state()
    print_brief(state, find_topic(state, args.topic))


def cmd_init(args):
    if load_state(required=False) is not None:
        die("this copy is already onboarded. Use `levelup`, `add-topic` or `retire-topic` instead")
    with open(args.file, encoding="utf-8") as f:
        spec = json.load(f)

    area = spec.get("area") or {}
    title = (area.get("title") or "").strip()
    if not title:
        die("area.title is required")
    if len(title) > TITLE_MAX:
        die("area.title is %d characters; keep it to %d" % (len(title), TITLE_MAX))
    slug = slugify(area.get("slug") or title)
    if not slug:
        die("could not make a slug from the area title; pass area.slug (lowercase letters, digits, hyphens)")
    if any(w in slug for w in RESERVED_WORDS):
        die("slug %r contains a word claude.ai reserves (%s); pass a different area.slug"
            % (slug, ", ".join(RESERVED_WORDS)))
    skill_name = "hammer-time-" + slug

    topics_in = spec.get("topics") or []
    if not MIN_TOPICS <= len(topics_in) <= MAX_TOPICS:
        die("need %d to %d topics, got %d" % (MIN_TOPICS, MAX_TOPICS, len(topics_in)))
    topics = []
    for i, t in enumerate(topics_in, 1):
        if not t.get("title") or not t.get("description"):
            die("topic %d needs a title and a description" % i)
        valid_start_score(t.get("score"), t["title"])
        topics.append({
            "id": "t%02d" % i,
            "title": t["title"].strip(),
            "description": t["description"].strip(),
            "score": t["score"],
            "start_score": t["score"],
            "times_asked": 0,
            "last_asked": None,
            "added": today(),
        })

    state = {
        "schema_version": SCHEMA_VERSION,
        "skill_name": skill_name,
        "area": {"title": title, "slug": slug, "created": today()},
        "profile": spec.get("profile") or {},
        "topics": topics,
        "archived_topics": [],
        "log": [],
        "last_review": {"date": today(), "scores": {t["id"]: t["score"] for t in topics}},
    }

    wd = ensure_work_copy()
    # Rename the work copy to the area skill.
    new_wd = work_dir_for(skill_name)
    if new_wd != wd:
        if os.path.exists(new_wd):
            rmtree(new_wd)
        os.rename(wd, new_wd)
        wd = new_wd
        with open(redirect_path(), "w", encoding="utf-8") as f:
            f.write(skill_name)
    rewrite_frontmatter(wd, skill_name, title)
    save_state(state, wd)
    print("Onboarded %s as skill %s with %d topics." % (title, skill_name, len(topics)))
    print()
    print(table(state))
    print()
    print("NEXT: run `package`, then hand the file to the user to save.")


def rewrite_frontmatter(d, skill_name, area_title):
    p = os.path.join(d, "SKILL.md")
    with open(p, encoding="utf-8") as f:
        text = f.read()
    desc = ("Hammer Time drill for %s: a Socratic quiz that tracks a 0-100 score per topic and "
            "re-saves itself with the new scores. Use ONLY when the user explicitly asks for "
            "\"hammer time %s\", \"/%s\", or a Hammer Time progress review for %s. Do not use "
            "for ordinary questions about %s." % (
                area_title, skill_name[len("hammer-time-"):].replace("-", " "), skill_name, area_title, area_title))
    desc = desc.replace("<", "").replace(">", "")
    if len(desc) > DESCRIPTION_MAX:
        die("generated description is %d characters, over the %d limit; shorten area.title"
            % (len(desc), DESCRIPTION_MAX))
    text = re.sub(r"^name:.*$", "name: " + skill_name, text, count=1, flags=re.M)
    text = re.sub(r"^description:.*$", "description: " + json.dumps(desc, ensure_ascii=False),
                  text, count=1, flags=re.M)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def cmd_score(args):
    wd, state = begin_change()
    if not args.note.strip():
        die("--note can't be empty. Reviews are written from these notes")
    t = find_topic(state, args.topic)
    delta = RESULTS[args.result]
    before = t["score"]
    t["score"] = clamp(before + delta)
    t["times_asked"] += 1
    t["last_asked"] = today()
    t["last_result"] = args.result
    t["last_note"] = args.note.strip()
    t["recent"] = ([{"date": today(), "result": args.result, "note": args.note.strip()}]
                   + t.get("recent", []))[:RECENT_LIMIT]
    entry = {
        "date": today(),
        "topic": t["id"],
        "result": args.result,
        "delta": t["score"] - before,
        "score_after": t["score"],
        "note": args.note.strip(),
    }
    state["log"].append(entry)
    state["log"] = state["log"][-LOG_LIMIT:]
    save_state(state, wd)

    print("SCORED: %s %s" % (t["id"], t["title"]))
    print("RESULT: %s (%+d)" % (args.result, entry["delta"]))
    print("SCORE: %d -> %d (%s band%s)" % (
        before, t["score"], band(t["score"]),
        ", was " + band(before) if band(before) != band(t["score"]) else ""))
    if t["score"] >= LEVELUP_THRESHOLD:
        print("LEVEL UP: this topic is at %d. Offer the user a harder version (guides/onboarding.md, part B)."
              % t["score"])
    print()
    print(table(state))
    print()
    print("NEXT: run `package`, then show the save message from guides/updating.md.")


def cmd_levelup(args):
    wd, state = begin_change()
    old = find_topic(state, args.topic)
    score = LEVELUP_DEFAULT if args.score is None else args.score
    valid_start_score(score, args.title)
    new = {
        "id": next_topic_id(state),
        "title": args.title.strip(),
        "description": args.description.strip(),
        "score": score,
        "start_score": score,
        "times_asked": 0,
        "last_asked": None,
        "added": today(),
        "levelled_up_from": old["id"],
    }
    archived = dict(old, archived=today(), final_score=old["score"], replaced_by=new["id"])
    state["archived_topics"].append(archived)
    i = state["topics"].index(old)
    state["topics"][i] = new
    save_state(state, wd)
    print("LEVELLED UP: %s %s (final %d) -> %s %s (starts at %d)" % (
        old["id"], old["title"], old["score"], new["id"], new["title"], score))
    print()
    print(table(state))
    print()
    print("NEXT: run `package`.")


def cmd_add_topic(args):
    wd, state = begin_change()
    if len(state["topics"]) >= MAX_TOPICS:
        die("already %d topics. Retire or level one up first" % MAX_TOPICS)
    valid_start_score(args.score, args.title)
    t = {
        "id": next_topic_id(state),
        "title": args.title.strip(),
        "description": args.description.strip(),
        "score": args.score,
        "start_score": args.score,
        "times_asked": 0,
        "last_asked": None,
        "added": today(),
    }
    state["topics"].append(t)
    save_state(state, wd)
    print("ADDED: %s %s (starts at %d)" % (t["id"], t["title"], t["score"]))
    print("NEXT: run `package`.")


def cmd_retire_topic(args):
    wd, state = begin_change()
    if len(state["topics"]) <= MIN_TOPICS:
        die("only %d topics left; the minimum is %d. Add one first" % (len(state["topics"]), MIN_TOPICS))
    t = find_topic(state, args.topic)
    state["topics"].remove(t)
    state["archived_topics"].append(dict(t, archived=today(), final_score=t["score"], replaced_by=None))
    save_state(state, wd)
    print("RETIRED: %s %s (final %d)" % (t["id"], t["title"], t["score"]))
    print("NEXT: run `package`.")


def cmd_edit_topic(args):
    wd, state = begin_change()
    t = find_topic(state, args.topic)
    if args.title:
        t["title"] = args.title.strip()
    if args.description:
        t["description"] = args.description.strip()
    save_state(state, wd)
    print("EDITED: %s %s" % (t["id"], t["title"]))
    print("NEXT: run `package`.")


def cmd_review(args):
    state = load_state()
    prev = state.get("last_review", {})
    print("AREA: %s" % state["area"]["title"])
    print("LAST REVIEW: %s" % prev.get("date", "never"))
    print()
    rows = ["| id | topic | score | band | since last review |", "|---|---|---|---|---|"]
    for t in state["topics"]:
        old = prev.get("scores", {}).get(t["id"])
        change = "new" if old is None else "%+d" % (t["score"] - old)
        rows.append("| %s | %s | %d | %s | %s |" % (t["id"], t["title"], t["score"], band(t["score"]), change))
    print("\n".join(rows))
    print()
    print("LAST %d ANSWERS (oldest first, the log keeps %d):" % (len(state["log"]), LOG_LIMIT))
    names = {t["id"]: t["title"] for t in state["topics"] + state.get("archived_topics", [])}
    for e in state["log"]:
        print("- %s %s %s %+d -> %d. %s" % (
            e["date"], e["topic"], names.get(e["topic"], "?"), e["delta"], e["score_after"], e["note"]))
    if not state["log"]:
        print("- none yet")
    ready = [t for t in state["topics"] if t["score"] >= LEVELUP_THRESHOLD]
    close = [t for t in state["topics"] if LEVELUP_THRESHOLD - 5 <= t["score"] < LEVELUP_THRESHOLD]
    if ready or close:
        print()
    if ready:
        print("READY TO LEVEL UP (%d+): " % LEVELUP_THRESHOLD
              + ", ".join("%s %s (%d)" % (t["id"], t["title"], t["score"]) for t in ready))
    if close:
        print("CLOSE (%d-%d): " % (LEVELUP_THRESHOLD - 5, LEVELUP_THRESHOLD - 1)
              + ", ".join("%s %s (%d)" % (t["id"], t["title"], t["score"]) for t in close))
    never = [t for t in state["topics"] if t["times_asked"] == 0]
    if never:
        print("NEVER ASKED: " + ", ".join("%s %s" % (t["id"], t["title"]) for t in never))


def cmd_mark_review(args):
    wd, state = begin_change()
    state["last_review"] = {"date": today(), "scores": {t["id"]: t["score"] for t in state["topics"]}}
    save_state(state, wd)
    print("Review snapshot saved for %s." % today())
    print("NEXT: run `package`.")


def write_skill_zip(src, name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name + ".skill")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in sorted(files):
                if fn.endswith(".pyc") or fn == ".DS_Store":
                    continue
                full = os.path.join(root, fn)
                z.write(full, os.path.join(name, os.path.relpath(full, src)))
    return out


def cmd_package(args):
    wd = active_dir()
    if wd == SKILL_DIR:
        # Nothing changed. Still allow an explicit export, e.g. to move an area to claude.ai.
        if args.out and not args.install and os.path.isfile(state_path(wd)):
            out = write_skill_zip(wd, read_frontmatter_name(wd), args.out)
            print("EXPORTED: %s" % out)
            print("Upload it under Settings > Capabilities > Skills on claude.ai.")
            return
        die("nothing has changed in this session, so there is nothing to package. "
            "To export the current skill as a file, pass `--out <folder>`")
    if not os.path.isfile(state_path(wd)):
        die("no state.json in the work copy, so onboarding did not finish. Fix the spec and rerun `init`")
    name = read_frontmatter_name(wd)

    if args.install:
        dest_root = os.path.abspath(os.path.expanduser(args.install))
        dest = os.path.join(dest_root, name)
        if os.path.exists(dest):
            rmtree(dest)
        shutil.copytree(wd, dest)
        rmtree(wd)
        clear_redirect()
        print("INSTALLED: %s" % dest)
        return

    out_dir = args.out or (CLAUDE_AI_OUTPUTS if os.path.isdir(CLAUDE_AI_OUTPUTS) else None)
    if out_dir is None:
        die("not on claude.ai, so there is no Save button. In Claude Code use `package --install`; "
            "to get a .skill file anyway, pass `--out <folder>`")
    out = write_skill_zip(wd, name, out_dir)
    rmtree(wd)
    clear_redirect()
    print("PACKAGED: %s" % out)
    print("The user must save this file as their skill, or today's scores are lost.")


def main():
    p = argparse.ArgumentParser(prog="ht.py", description="Hammer Time state engine")
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    sub.add_parser("status", help="show mode, scores and the suggested next topic").set_defaults(fn=cmd_status)

    s = sub.add_parser("show", help="print the brief for one topic: description, last result, profile")
    s.add_argument("--topic", required=True)
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("init", help="finish onboarding from a JSON spec")
    s.add_argument("--file", required=True)
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("score", help="record the result of one question")
    s.add_argument("--topic", required=True)
    s.add_argument("--result", required=True, choices=sorted(RESULTS))
    s.add_argument("--note", required=True, help="one line: what they showed or what was missing")
    s.set_defaults(fn=cmd_score)

    s = sub.add_parser("levelup", help="archive a topic and replace it with a harder version")
    s.add_argument("--topic", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--description", required=True)
    s.add_argument("--score", type=int)
    s.set_defaults(fn=cmd_levelup)

    s = sub.add_parser("add-topic")
    s.add_argument("--title", required=True)
    s.add_argument("--description", required=True)
    s.add_argument("--score", type=int, required=True)
    s.set_defaults(fn=cmd_add_topic)

    s = sub.add_parser("retire-topic")
    s.add_argument("--topic", required=True)
    s.set_defaults(fn=cmd_retire_topic)

    s = sub.add_parser("edit-topic")
    s.add_argument("--topic", required=True)
    s.add_argument("--title")
    s.add_argument("--description")
    s.set_defaults(fn=cmd_edit_topic)

    sub.add_parser("review", help="print the data for a progress review").set_defaults(fn=cmd_review)
    sub.add_parser("mark-review", help="snapshot scores as the new review baseline").set_defaults(fn=cmd_mark_review)

    s = sub.add_parser("package", help="turn this session's changes into a .skill file, or install locally")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--out", help="folder for the .skill file (default: claude.ai outputs)")
    g.add_argument("--install", nargs="?", const=os.path.dirname(SKILL_DIR),
                   help="Claude Code: install in place. Defaults to the skills folder this skill is in")
    s.set_defaults(fn=cmd_package)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

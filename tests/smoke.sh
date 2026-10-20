#!/bin/sh
# End-to-end check of the state engine against a read-only install, like claude.ai.
# Usage: tests/smoke.sh   (exits non-zero on the first failure)
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
trap 'chmod -R u+w "$T"; rm -rf "$T"' EXIT
# Keep the work copies inside $T, away from any real session's.
export TMPDIR="$T/tmp"; mkdir -p "$TMPDIR"
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "ok   $*"; }

install() {  # install <dir-with-skill-folder> as read-only into $T/skills
  [ -d "$T/skills" ] && chmod -R u+w "$T/skills"; rm -rf "$T/skills"; mkdir -p "$T/skills"
  cp -R "$1" "$T/skills/"; chmod -R a-w "$T/skills"
}

# 1. Onboarding ---------------------------------------------------------------
install "$REPO/hammer-time-onboarding"
H="$T/skills/hammer-time-onboarding/scripts/ht.py"
python3 "$H" status | grep -q "MODE: onboarding" || fail "fresh template should be in onboarding mode"
ok "fresh template is in onboarding mode"

python3 - "$T/spec.json" <<'EOF'
import json, sys
t = [{"title": "Topic %d" % i, "description": "Desc %d" % i, "score": s}
     for i, s in enumerate([10, 20, 30, 35, 50], 1)]
json.dump({"area": {"title": "SQL for Finance", "slug": "sql"},
           "profile": {"role": "tester", "language": "English"}, "topics": t}, open(sys.argv[1], "w"))
EOF
sed 's/"score": 50/"score": 51/' "$T/spec.json" > "$T/bad.json"
python3 "$H" init --file "$T/bad.json" 2>/dev/null && fail "score 51 should be refused"
ok "starting score above 50 refused"
python3 "$H" package --out "$T/out" 2>/dev/null && fail "package before init should be refused"
ok "package refused before onboarding finished"
python3 "$H" score --topic t01 --result missed --note "n" 2>/dev/null && fail "score before init should be refused"
[ -d "$TMPDIR/hammer-time-work/hammer-time-onboarding" ] && fail "refused score left a work copy behind"
ok "refused command leaves no work copy"

python3 - "$T" <<'EOF2'
import json, sys
t = [{"title": "T%d" % i, "description": "d", "score": 20} for i in range(5)]
for name, area in [("long", {"title": "X" * 61}), ("reserved", {"title": "Claude API"})]:
    json.dump({"area": area, "topics": t}, open("%s/%s.json" % (sys.argv[1], name), "w"))
EOF2
python3 "$H" init --file "$T/long.json" 2>/dev/null && fail "61-character area title should be refused"
python3 "$H" init --file "$T/reserved.json" 2>/dev/null && fail "reserved word in skill name should be refused"
ok "long titles and reserved names refused"
python3 - "$REPO" <<'EOF2'
import sys; sys.path.insert(0, sys.argv[1] + "/hammer-time-onboarding/scripts"); import ht
assert ht.slugify("Bokföring för försäkring") == "bokforing-for-forsakring", ht.slugify("Bokföring för försäkring")
EOF2
ok "non-ASCII titles slug cleanly"

python3 "$H" init --file "$T/spec.json" >/dev/null
python3 "$H" package --out "$T/out" >/dev/null
[ -f "$T/out/hammer-time-sql.skill" ] || fail "no hammer-time-sql.skill"
(cd "$T/out" && unzip -q hammer-time-sql.skill)
grep -q "^name: hammer-time-sql$" "$T/out/hammer-time-sql/SKILL.md" || fail "skill not renamed"
ok "onboarding packaged as hammer-time-sql"

DIFF="$(diff -rq "$REPO/hammer-time-onboarding" "$T/out/hammer-time-sql" | grep -v -e "SKILL.md differ" -e "Only in $T/out/hammer-time-sql: state.json" || true)"
[ -z "$DIFF" ] || fail "rules files changed in the package: $DIFF"
ok "every rules file is byte-identical in the package"
python3 "$H" status | grep -q "MODE: onboarding" || fail "template should still be blank"
ok "onboarding template left untouched"

# 2. Daily runs on the area skill ---------------------------------------------
install "$T/out/hammer-time-sql"
H="$T/skills/hammer-time-sql/scripts/ht.py"
python3 "$H" status | grep -q "SUGGESTED NEXT: t01" || fail "should suggest t01 (never asked, lowest score)"
ok "topic choice: least recently asked, then lowest score"

python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 10 -> 5" || fail "missed should be -5"
python3 "$H" status | grep -q "SUGGESTED NEXT: t02" || fail "should not repeat t01"
ok "missed is -5, and the same topic is not asked twice in a row"
python3 - "$REPO" <<'EOF2'
import sys; sys.path.insert(0, sys.argv[1] + "/hammer-time-onboarding/scripts"); import ht
# t1 was asked 30 times but not lately; t2 is new and was asked twice since. t1 is due.
topics = [{"id": "t1", "score": 60, "times_asked": 30, "last_asked": "2026-01-01"},
          {"id": "t2", "score": 20, "times_asked": 2, "last_asked": "2026-02-02"},
          {"id": "t3", "score": 10, "times_asked": 9, "last_asked": "2026-02-03"}]
log = [{"topic": "t2"}, {"topic": "t3"}, {"topic": "t2"}, {"topic": "t3"}]
assert ht.pick_topic({"topics": topics, "log": log})["id"] == "t1"
EOF2
ok "a topic asked often but long ago beats a new one asked lately"
python3 - "$REPO" <<'EOF2'
import sys; sys.path.insert(0, sys.argv[1] + "/hammer-time-onboarding/scripts"); import ht
topics = [{"id": "t1", "score": 30, "times_asked": 0, "last_asked": None},
          {"id": "t2", "score": 10, "times_asked": 0, "last_asked": None}]
assert ht.pick_topic({"topics": topics, "log": []})["id"] == "t1"
EOF2
ok "topics never asked go in list order, basics first"
python3 "$H" status | grep -q "^DESCRIPTION: Desc 2$" || fail "status should end with the brief for t02"
python3 "$H" status | grep -q "^- language: English$" || fail "brief should carry the profile"
python3 "$H" status | grep -q "^LAST TIME: never asked$" || fail "t02 was never asked"
python3 "$H" show --topic t01 | grep -q "^LAST TIME: .*, missed. n$" || fail "show should give t01's last result and note"
python3 "$H" show --topic t04 | grep -q "^SCORE: 35, Applied band, step: Apply in a scenario$" || fail "brief step"
python3 - "$REPO" <<'EOF2'
import sys; sys.path.insert(0, sys.argv[1] + "/hammer-time-onboarding/scripts"); import ht
ref = open(sys.argv[1] + "/hammer-time-onboarding/reference/scoring.md", encoding="utf-8").read()
for lowest, name in ht.STEPS:
    assert "| %s |" % name in ref, "step %r missing from scoring.md" % name
EOF2
ok "status and show hand Claude the topic brief; steps match scoring.md"
python3 "$H" score --topic t02 --result missed --note "" 2>/dev/null && fail "empty note should be refused"
python3 "$H" score --topic t02 --result missed 2>/dev/null && fail "missing note should be refused"
ok "score needs a note"
python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 5 -> 0" || fail "floor at 0"
python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 0 -> 0" || fail "floor at 0"
ok "score floors at 0"
python3 "$H" score --topic t05 --result first_try --note "a" | grep -q "SCORE: 50 -> 55" || fail "first_try +5"
python3 "$H" score --topic t05 --result guided --note "b" | grep -q "SCORE: 55 -> 57" || fail "guided +2"
python3 "$H" score --topic t05 --result partial --note "c" | grep -q "SCORE: 57 -> 57" || fail "partial 0"
ok "ladder +5 / +2 / 0"
python3 "$H" score --topic t05 --result partial --note "d" >/dev/null
python3 "$H" show --topic t05 | grep -A2 "^LAST TIME" > "$T/recent"
grep -q "^LAST TIME: .*, partial. d$" "$T/recent" || fail "latest result first"
[ "$(grep -c "^BEFORE THAT" "$T/recent")" = 2 ] || fail "brief should carry two earlier results"
grep -q "^BEFORE THAT: .*, guided. b$" "$T/recent" || fail "earlier results newest first"
python3 "$H" show --topic t05 | grep -q ", first_try. a$" && fail "only the last three results are kept"
ok "brief shows the last three results on the topic"

i=0; while [ $i -lt 20 ]; do python3 "$H" score --topic t02 --result first_try --note "n" >/dev/null; i=$((i+1)); done
python3 - "$T" <<'EOF'
import json, os, sys, tempfile
s = json.load(open(os.path.join(tempfile.gettempdir(), "hammer-time-work", "hammer-time-sql", "state.json")))
assert len(s["log"]) == 20, len(s["log"])
assert [t for t in s["topics"] if t["id"] == "t02"][0]["score"] == 100
EOF
ok "log capped at 20, score capped at 100"
python3 "$H" status | grep -q "READY TO LEVEL UP: t02" || fail "t02 at 100 should be flagged"
ok "90+ flagged for level up"

python3 "$H" levelup --topic t02 --title "Hard t02" --description "d" | grep -q "starts at 20" || fail "levelup default 20"
python3 "$H" levelup --topic t03 --title "x" --description "d" --score 60 2>/dev/null && fail "levelup above 50 should be refused"
ok "level up starts at 20, cap 50"
python3 "$H" retire-topic --topic t03 2>/dev/null && fail "should refuse going below 5 topics"
ok "minimum 5 topics enforced"
i=0; while [ $i -lt 10 ]; do python3 "$H" add-topic --title "Extra $i" --description "d" --score 20 >/dev/null; i=$((i+1)); done
python3 "$H" add-topic --title "One too many" --description "d" --score 20 2>/dev/null && fail "16th topic should be refused"
ok "maximum 15 topics enforced"
python3 "$H" edit-topic --topic t04 --title "Renamed" >/dev/null
python3 "$H" status | grep -q "| t04 | Renamed | 35 |" || fail "edit-topic should rename and keep the score"
ok "edit-topic renames and keeps the score"
python3 "$H" status | grep -q "UNPACKAGED CHANGES" || fail "status should flag unpackaged changes"
python3 "$H" package 2>/dev/null && fail "plain package off claude.ai should be refused"
ok "status flags unpackaged changes; plain package refused off claude.ai"

python3 "$H" review | grep -q "Hard t02 | 20 | Foundation | new" || fail "review should mark the level-up topic as new"
python3 "$H" review | grep -q "t01 | Topic 1 | 0 | Foundation | -10" || fail "review delta after several scores"
python3 "$H" review | grep -q "^READY TO LEVEL UP" && fail "nothing is at 90+ after the level up"
ok "review shows deltas since the last review"
python3 "$H" review | grep -q "^STUCK.*t01 Topic 1" || fail "three misses in a row should flag the topic as stuck"
python3 "$H" review | grep -q "^ALWAYS FIRST TRY" && fail "nothing active has three first tries in a row"
ok "review flags stuck topics"
python3 "$H" mark-review >/dev/null
python3 "$H" package --out "$T/out2" >/dev/null
(cd "$T/out2" && unzip -q hammer-time-sql.skill)
python3 - "$T/out2/hammer-time-sql/state.json" <<'EOF'
import json, sys
s = json.load(open(sys.argv[1]))
assert len(s["archived_topics"]) == 1 and s["archived_topics"][0]["final_score"] == 100
assert s["topics"][1]["title"] == "Hard t02"
EOF
ok "second package carries level-up, archive and review snapshot"
python3 "$H" status | grep -q "UNPACKAGED CHANGES" && fail "status right after package should not flag unpackaged changes"
python3 "$H" score --topic t01 --result first_try --note "one more" | grep -q "SCORE: 0 -> 5" || fail "one more should build on the packaged run"
python3 "$H" status | grep -q "UNPACKAGED CHANGES" || fail "a score after package should flag unpackaged changes"
python3 "$H" package --out "$T/out3" >/dev/null
(cd "$T/out3" && unzip -q hammer-time-sql.skill)
grep -q '"note": "one more"' "$T/out3/hammer-time-sql/state.json" || fail "second package in a chat should carry both runs"
ok "one more in the same chat builds on the first run"

python3 "$H" reminder --time 8:30 --out "$T/rem" 2>/dev/null && fail "time must be HH:MM"
python3 "$H" reminder --time 08:30 --out "$T/rem" >/dev/null
ICS="$T/rem/hammer-time-sql-reminder.ics"
grep -q "^RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR" "$ICS" || fail "weekdays by default"
grep -q "^DTSTART:[0-9]\{8\}T083000" "$ICS" || fail "start at 08:30 local time"
grep -q "^SUMMARY:Hammer time sql" "$ICS" || fail "event named after the area"
python3 "$H" reminder --time 07:00 --days daily --out "$T/rem" >/dev/null
grep -q "^RRULE:FREQ=DAILY" "$ICS" || fail "daily rule"
ok "reminder writes a recurring calendar event"

# 3. Claude Code install path ---------------------------------------------------
# A new chat starts with no work copies (a fresh sandbox on claude.ai).
rm -rf "$TMPDIR/hammer-time-work"
mkdir -p "$T/cc"
cp -R "$T/out2/hammer-time-sql" "$T/cc/"
H="$T/cc/hammer-time-sql/scripts/ht.py"
python3 "$H" score --topic t01 --result first_try --note "n" >/dev/null
python3 "$H" package --install >/dev/null
python3 "$H" status | grep -q "| t01 | Topic 1 | 5 |" || fail "install should update in place"
ok "Claude Code --install (no path) updates the skill in place"

python3 "$H" package --out "$T/export" >/dev/null || fail "export of an unchanged skill should work"
(cd "$T/export" && unzip -q hammer-time-sql.skill)
grep -q "| t01 | Topic 1 | 5 |" <<EOF || fail "export should carry the current scores"
$(python3 "$T/export/hammer-time-sql/scripts/ht.py" status)
EOF
[ -f "$T/cc/hammer-time-sql/state.json" ] || fail "export must not touch the installed skill"
python3 "$H" package 2>/dev/null && fail "plain package with no changes should still be refused"
ok "unchanged skill exports with --out and stays installed"

echo "all passed"

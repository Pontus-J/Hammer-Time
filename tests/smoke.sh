#!/bin/sh
# End-to-end check of the state engine against a read-only install, like claude.ai.
# Usage: tests/smoke.sh   (exits non-zero on the first failure)
set -eu
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
trap 'chmod -R u+w "$T"; rm -rf "$T"' EXIT
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
ok "topic choice: fewest asked, then lowest score"

python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 10 -> 5" || fail "missed should be -5"
python3 "$H" status | grep -q "SUGGESTED NEXT: t02" || fail "should not repeat t01"
ok "missed is -5, and the same topic is not asked twice in a row"
python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 5 -> 0" || fail "floor at 0"
python3 "$H" score --topic t01 --result missed --note "n" | grep -q "SCORE: 0 -> 0" || fail "floor at 0"
ok "score floors at 0"
python3 "$H" score --topic t05 --result first_try | grep -q "SCORE: 50 -> 55" || fail "first_try +5"
python3 "$H" score --topic t05 --result guided | grep -q "SCORE: 55 -> 57" || fail "guided +2"
python3 "$H" score --topic t05 --result partial | grep -q "SCORE: 57 -> 57" || fail "partial 0"
ok "ladder +5 / +2 / 0"

i=0; while [ $i -lt 20 ]; do python3 "$H" score --topic t02 --result first_try >/dev/null; i=$((i+1)); done
python3 - "$T" <<'EOF'
import json, os, sys, tempfile
s = json.load(open(os.path.join(tempfile.gettempdir(), "hammer-time-work", "hammer-time-sql", "state.json")))
assert len(s["log"]) == 20, len(s["log"])
assert [t for t in s["topics"] if t["id"] == "t02"][0]["score"] == 100
EOF
ok "log capped at 20, score capped at 100"
python3 "$H" status | grep -q "READY TO LEVEL UP: t02" || fail "t02 at 100 should be flagged"
ok "90+ flagged for level up"

python3 "$H" levelup --topic t02 --title "Hard t02" --description "d" | grep -q "starts at 30" || fail "levelup default 30"
python3 "$H" levelup --topic t03 --title "x" --description "d" --score 60 2>/dev/null && fail "levelup above 50 should be refused"
ok "level up starts at 30, cap 50"
python3 "$H" retire-topic --topic t03 2>/dev/null && fail "should refuse going below 5 topics"
ok "minimum 5 topics enforced"

python3 "$H" review | grep -q "Hard t02 | 30 | Foundation | +0" || fail "review should show the new topic"
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

# 3. Claude Code install path ---------------------------------------------------
mkdir -p "$T/cc"
cp -R "$T/out2/hammer-time-sql" "$T/cc/"
H="$T/cc/hammer-time-sql/scripts/ht.py"
python3 "$H" score --topic t01 --result first_try >/dev/null
python3 "$H" package --install "$T/cc" >/dev/null
python3 "$H" status | grep -q "| t01 | Topic 1 | 5 |" || fail "install should update in place"
ok "Claude Code --install updates the skill in place"

echo "all passed"

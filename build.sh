#!/bin/sh
# Build dist/hammer-time-onboarding.skill from the template folder.
set -e
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/hammer-time-onboarding.skill
zip -qr dist/hammer-time-onboarding.skill hammer-time-onboarding -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' '*/state.json'
echo "built dist/hammer-time-onboarding.skill"

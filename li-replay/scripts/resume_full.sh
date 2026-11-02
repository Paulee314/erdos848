#!/bin/bash
# Resume the #848 full build with a cap on parallel Lean processes (default 12; the unbounded run used 28 and ran out of memory).
# The previous log is kept as full_partN.log; modules already built are reused.
cd "$(dirname "$0")" || exit 1
if [ -e full.log ]; then n=$(ls full_part*.log 2>/dev/null | wc -l | tr -d ' '); mv full.log "full_part$((n+1)).log"; fi
export PATH="$HOME/.elan/bin:$PATH"
export LEAN_NUM_THREADS="${1:-12}"
cd repo/lean4 && ( date -u +%FT%TZ; echo "LEAN_NUM_THREADS=$LEAN_NUM_THREADS"; /usr/bin/time -l lake build Erdos848.PaperGeneratedCertificateProvider; echo full_exit=$?; date -u +%FT%TZ ) > ../../full.log 2>&1

#!/bin/bash
# Run our own final #848 check (check_all_N.lean) against the finished build. Only after full.log shows full_exit=0.
E="$HOME/AI-workspace/Claude-Projects/Erdos/e848"; R="$E/li_replay_work/repo/lean4"; F="$E/final"
grep -q 'full_exit=0' "$E/li_replay_work/full.log" || { echo "build not finished with full_exit=0 - not running"; exit 1; }
LP="$R/.lake/build/lib/lean"; for d in "$R"/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$d"; done
cd "$R" && ( date -u +%FT%TZ; LEAN_PATH="$LP" /usr/bin/time -l "$HOME/.elan/toolchains/leanprover--lean4---v4.30.0-rc2/bin/lean" "$F/check_all_N.lean"; echo "final_exit=$?"; date -u +%FT%TZ ) > "$F/final_check.log" 2>&1
cat "$F/final_check.log" | grep -v '^ *[0-9]* *[a-z ]*$' | head -80

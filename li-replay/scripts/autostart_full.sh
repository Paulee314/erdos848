#!/bin/bash
# Start the full #848 re-check as soon as the pilot build ends cleanly (REFRESH step 5, automated 28 Oct 13:20 CT
# so the Studio doesn't sit idle until the next check-in). Does nothing if the pilot failed or a full build exists.
cd "$HOME/AI-workspace/Claude-Projects/Erdos/e848/li_replay_work" || exit 1
echo $$ > autostart_full.pid
while ! grep -q 'pilot_exit=' pilot.log; do sleep 30; done
if grep -q 'pilot_exit=0' pilot.log && [ ! -e full.log ]; then
  export PATH="$HOME/.elan/bin:$PATH"
  cd repo/lean4 && ( date -u +%FT%TZ; /usr/bin/time -l lake build; echo full_exit=$?; date -u +%FT%TZ ) > ../../full.log 2>&1
else
  echo "not started: $(grep -o 'pilot_exit=[0-9]*' pilot.log) full.log_exists=$([ -e full.log ] && echo yes || echo no)" > autostart_full.skipped
fi

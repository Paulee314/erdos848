#!/bin/bash
# Memory guard for the #848 Lean build. Added 28 Oct 2026 after the unbounded build (28 Lean processes at ~8.5 GB each)
# ran the Mac Studio out of memory and macOS restarted it. Every 15 s: if macOS memory pressure is "warn" or worse, or
# free memory is under 12%, on two checks in a row, it stops the build (lake + lean) to protect the Mac.
# Modules already built are kept, so the build resumes later from where it stopped.
cd "$(dirname "$0")" || exit 1
echo $$ > memguard.pid
bad=0; last=0
while true; do
  lvl=$(sysctl -n kern.memorystatus_vm_pressure_level 2>/dev/null); lvl=${lvl:-1}
  free=$(memory_pressure -Q 2>/dev/null | awk -F': ' '/free percentage/ {gsub("%","",$2); print $2+0}'); free=${free:-100}
  if [ "$lvl" -ge 2 ] || [ "$free" -lt 12 ]; then bad=$((bad+1)); else bad=0; fi
  if [ $bad -ge 2 ]; then
    echo "$(date -u +%FT%TZ) STOPPED the Lean build: pressure level $lvl, free ${free}%" >> memguard.log
    pkill -f 'lake build Erdos848'; pkill -x lean; bad=0
  fi
  now=$(date +%s)
  if [ $((now - last)) -ge 300 ]; then echo "$(date -u +%FT%TZ) pressure=$lvl free=${free}% lean=$(pgrep -x lean | wc -l | tr -d ' ')" >> memguard.log; last=$now; fi
  sleep 15
done

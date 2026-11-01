#!/usr/bin/env python3
"""#848: leanchecker on every Erdos848 module, ONE CALL PER NAMESPACE GROUP (31 Oct 2026).
v3 (1 Nov ~01:50Z, after the Studio ran out of memory at 4 groups and restarted): at most 2 groups at once (Paul);
the guard no longer trusts `memory_pressure -Q` (it said 63-83 % free while the Mac was out of memory). It now uses vm_stat
(pages occupied by the compressor, free pages) and the summed RSS of the leanchecker processes; the largest group
(GeneratedTruncatedDiagonalTwoHundredMillionAtoms, ~125 GB at its peak) runs last and alone.
v2 (31 Oct ~22:30Z): CONC is re-read every cycle from lc_groups/conc (if present); groups whose leanchecker is already running
(started by an earlier runner) are adopted - counted against CONC and judged from their log when their process ends; before a
group is launched its verdict is re-checked (skipped if already ok).
Why: one call per module ran 16 at a time at ~370 s each (kernel time from 16 processes mapping the same .olean files; ~10 days);
a single call on the prefix Erdos848.GeneratedFactorCoverage replayed its 338 modules in 560 s with 4 threads (exit 0, 30 GB peak).
The whole-prefix run (16 threads) died of memory at 285 GB; groups load only their own imports.

Groups: Erdos848.<second component> (624 groups: 570 single hand-written modules, 54 generated families up to 4,355 modules).
Each group = `lc_one.sh Erdos848.<group>` (leanchecker matches module-name prefixes component-wise), LEAN_NUM_THREADS=THREADS (4),
nice 5, CONC (2) groups at once, largest first. A group counts as checked only if its log ends with exit=0, has no
"found a problem" line, and its "replaying" lines cover every module of the group listed in all_modules.txt.
Resumable: checked groups are skipped on restart. Memory guard every 5 s: see v3 above (v1 used memory_pressure -Q free %: < 30 % no new group starts;
< 15 % running groups are stopped and re-queued to run alone; a group stopped twice is recorded as failed (memory) and skipped.
Read-only on Li's files. Files in lc_groups/: progress.json, run.log, failures.txt, guard.log, logs/<group>.log, finished.
"""
import os, time, json, subprocess, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'lc_groups'); LOGS = os.path.join(OUT, 'logs'); os.makedirs(LOGS, exist_ok=True)
CONC = int(os.environ.get('CONC', '2')); THREADS = os.environ.get('THREADS', '4')
mods = [l.strip() for l in open(os.path.join(HERE, 'all_modules.txt')) if l.strip()]
groups = collections.defaultdict(set)
for m in mods: groups['.'.join(m.split('.')[:2])].add(m)
order = sorted(groups, key=lambda g: (-len(groups[g]), g))
open(os.path.join(OUT, 'pid'), 'w').write(str(os.getpid()))


def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def log(name, s):
    with open(os.path.join(OUT, name), 'a') as f: f.write(f'{now()} {s}\n')


def verdict(g):
    p = os.path.join(LOGS, g + '.log')
    if not os.path.exists(p): return None, 0
    t = open(p, errors='replace').read()
    if 'exit=' not in t: return None, 0
    if 'found a problem' in t: return 'problem', 0
    rep = set(l.split()[1] for l in t.splitlines() if l.startswith('replaying ') and len(l.split()) > 1)
    miss = groups[g] - rep
    if t.rstrip().splitlines()[-1].strip() != 'exit=0': return 'fail', len(miss)
    return ('ok', 0) if not miss else ('incomplete', len(miss))


MAXCONC = 2                                    # Paul, 1 Nov 2026 20:47 CT: never more than 2 groups at once
SOLO = {'Erdos848.GeneratedTruncatedDiagonalTwoHundredMillionAtoms'}
HOLD_RSS, STOP_RSS = 190.0, 230.0              # GB, summed RSS of leanchecker processes
HOLD_COMP, STOP_COMP = 15.0, 30.0              # GB occupied by the memory compressor
PAGE = 16384


def mem():
    """(leanchecker RSS sum GB, compressor GB, free GB) from ps and vm_stat."""
    rss = 0.0
    try:
        for l in subprocess.run(['ps', '-Ao', 'rss=,comm='], capture_output=True, text=True, timeout=20).stdout.splitlines():
            p = l.split(None, 1)
            if len(p) == 2 and os.path.basename(p[1].strip()) == 'leanchecker': rss += int(p[0]) / 1048576
    except Exception: pass
    comp = free = None
    try:
        for l in subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=20).stdout.splitlines():
            if l.startswith('Pages occupied by compressor:'): comp = int(l.split(':')[1].strip().rstrip('.')) * PAGE / 1e9
            if l.startswith('Pages free:'): free = int(l.split(':')[1].strip().rstrip('.')) * PAGE / 1e9
    except Exception: pass
    return rss, comp, free


def live_groups():
    o = subprocess.run(['ps', '-Ao', 'pid=,args='], capture_output=True, text=True).stdout
    r = {}
    for l in o.splitlines():
        p = l.split()
        if len(p) >= 4 and os.path.basename(p[1]) == 'leanchecker' and p[2] == '-v' and p[3] in groups: r[p[3]] = int(p[0])
    return r


adopted = live_groups()
todo = collections.deque(g for g in order if verdict(g)[0] != 'ok' and g not in adopted and g not in SOLO)
todo.extend(g for g in order if g in SOLO and verdict(g)[0] != 'ok' and g not in adopted)
ok_mods = sum(len(groups[g]) for g in order if g not in todo)
start = time.time(); ok_mods0 = ok_mods
ok_mods = sum(len(groups[g]) for g in order if verdict(g)[0] == 'ok'); ok_mods0 = ok_mods
log('run.log', f'start (v2): {len(order)} groups / {len(mods)} modules; {ok_mods} modules already checked; adopted running: '
               f'{sorted(adopted)}; CONC {CONC}, THREADS {THREADS}')
adopted_t = {g: time.time() for g in adopted}
running = {}; solo = set(SOLO); mem_stops = collections.Counter(); fails = 0; problems = 0; held = False; last = 0
env = dict(os.environ, LEAN_NUM_THREADS=THREADS)
while todo or running or adopted:
    try: CONC = int(open(os.path.join(OUT, 'conc')).read().strip())
    except Exception: pass
    CONC = max(1, min(CONC, MAXCONC))
    if adopted:
        live = live_groups()
        for g in [g for g in adopted if g not in live]:
            del adopted[g]; v, miss = verdict(g)
            if v == 'ok': ok_mods += len(groups[g]); log('run.log', f'ok {g} ({len(groups[g])} modules, adopted)')
            elif v is None:                                   # killed (e.g. by the guard): run it again, alone
                solo.add(g); todo.appendleft(g); log('run.log', f'adopted {g} ended without a verdict - re-queued')
            else:
                fails += 1; problems += (v == 'problem')
                log('failures.txt', f'{g} verdict={v} missing_modules={miss} (adopted run)')
    rss, comp, free = mem(); fp = None
    over = rss > STOP_RSS or (comp is not None and comp > STOP_COMP)
    if over and running:
        g = max(running, key=lambda x: running[x][1])          # stop the most recently started group, keep the older one going
        p = running[g][0]; p.terminate()
        try: p.wait(timeout=60)
        except Exception: p.kill()
        for pid_ in subprocess.run(['pgrep', '-f', 'leanchecker -v ' + g + '$'], capture_output=True, text=True).stdout.split():
            subprocess.run(['kill', pid_])
        del running[g]; mem_stops[g] += 1
        if mem_stops[g] >= 2:
            fails += 1; log('failures.txt', f'{g} verdict=memory (stopped twice by the guard) modules={len(groups[g])}')
        else:
            solo.add(g); todo.append(g)
        log('guard.log', f'leanchecker RSS {rss:.0f} GB, compressor {comp} GB, free {free} GB: stopped {g} (re-queued to run alone)')
    was = held; held = rss > HOLD_RSS or (comp is not None and comp > HOLD_COMP)
    if held != was: log('guard.log', f'leanchecker RSS {rss:.0f} GB, compressor {comp} GB: ' + ('holding - no new groups' if held else 'recovered'))
    while todo and not held and len(running) + len(adopted) < CONC:
        g = todo[0]
        if verdict(g)[0] == 'ok': todo.popleft(); continue
        if g in solo and running: break                       # memory-heavy group: wait until it can run alone
        if any(r in solo for r in running): break
        todo.popleft()
        lf = open(os.path.join(LOGS, g + '.log'), 'w')
        running[g] = (subprocess.Popen(['nice', '-n', '5', os.path.join(HERE, 'lc_one.sh'), g], stdout=lf,
                                       stderr=subprocess.STDOUT, env=env), time.time())
        lf.close(); log('run.log', f'started {g} ({len(groups[g])} modules)')
    for g, (p, t0) in list(running.items()):
        if p.poll() is None: continue
        del running[g]; v, miss = verdict(g)
        if v == 'ok': ok_mods += len(groups[g]); log('run.log', f'ok {g} ({len(groups[g])} modules, {time.time() - t0:.0f} s)')
        else:
            fails += 1; problems += (v == 'problem')
            log('failures.txt', f'{g} verdict={v} missing_modules={miss} returncode={p.returncode} secs={time.time() - t0:.0f}')
    if time.time() - last > 30 or not (todo or running or adopted):
        last = time.time(); el = (time.time() - start) / 3600; rate = (ok_mods - ok_mods0) / el if el > 0.1 else None
        left = sum(len(groups[g]) for g in todo) + sum(len(groups[g]) for g in running) + sum(len(groups[g]) for g in adopted)
        json.dump(dict(time=now(), modules_total=len(mods), modules_ok=ok_mods, groups_total=len(order),
                       groups_left=len(todo) + len(running) + len(adopted), running={g: len(groups[g]) for g in list(running) + list(adopted)},
                       failures=fails, problems=problems, leanchecker_rss_gb=round(rss), compressor_gb=round(comp, 1) if comp is not None else None,
                       free_gb=round(free, 1) if free is not None else None, held=held, conc=CONC, threads=THREADS,
                       started=datetime.datetime.fromtimestamp(start, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                       modules_per_h=round(rate) if rate else None, eta_h=round(left / rate, 1) if rate else None),
                  open(os.path.join(OUT, 'progress.tmp'), 'w'))
        os.replace(os.path.join(OUT, 'progress.tmp'), os.path.join(OUT, 'progress.json'))
    time.sleep(5)
log('run.log', f'end: {ok_mods} of {len(mods)} modules checked ok; {fails} groups not ok ({problems} with "found a problem")')
open(os.path.join(OUT, 'finished'), 'w').write(f'{now()} modules_ok={ok_mods} failures={fails} problems={problems}\n')

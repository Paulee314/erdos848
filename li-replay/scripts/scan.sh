#!/bin/bash
# Look for any Lean construct that could run code (IO) at build time, or weaken the kernel check, in the Li repo.
cd "$(dirname "$0")/repo/lean4" || exit 1
echo "HEAD $(git -C .. log -1 --format='%H %cd')"
echo "lean files: $(find . -name '*.lean' | wc -l)"
echo "--- toolchain: $(cat lean-toolchain)"
echo "--- risky constructs (count by kind; comments included):"
grep -rhoE '#eval|run_cmd|run_elab|run_meta|^initialize|builtin_initialize|IO\.Process|IO\.FS|System\.FilePath|@\[extern|implemented_by|native_decide|unsafe |ofReduceBool|^[[:space:]]*(elab|macro|syntax|macro_rules|elab_rules)[[:space:]]' --include='*.lean' . | sort | uniq -c
echo "--- files containing any of them:"
grep -rlE '#eval|run_cmd|run_elab|run_meta|^initialize|builtin_initialize|IO\.Process|IO\.FS|System\.FilePath|@\[extern|implemented_by|native_decide|unsafe |ofReduceBool|^[[:space:]]*(elab|macro|syntax|macro_rules|elab_rules)[[:space:]]' --include='*.lean' . | head -20
echo "--- top-level import roots:"
grep -rhoE '^import [A-Za-z0-9_]+' --include='*.lean' . | sort | uniq -c
echo "--- sorry/axiom declarations:"
grep -rhoE '^\s*(axiom|sorry)\b|\bsorry\b' --include='*.lean' . | sort | uniq -c
echo SCAN_DONE

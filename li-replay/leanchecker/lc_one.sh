#!/bin/bash
# Run the toolchain's leanchecker (lean4checker, upstreamed) on the given modules of Li's #848 project. Read-only.
R=$HOME/AI-workspace/Claude-Projects/Erdos/e848/li_replay_work/repo/lean4
LP=$R/.lake/build/lib/lean; for d in $R/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
export LEAN_PATH=$LP PATH=$HOME/.elan/toolchains/leanprover--lean4---v4.30.0-rc2/bin:$PATH
cd $R && /usr/bin/time -l leanchecker -v "$@"
echo "exit=$?"

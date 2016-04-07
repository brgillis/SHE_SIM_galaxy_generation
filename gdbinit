shell build.x86_64-fc22-gcc51-dbg/run | sed -e ’s/ˆ/set environment /’ > /tmp/gdbinitvars
source /tmp/gdbinitvars

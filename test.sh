#!/bin/sh
aarch64-linux-android-gdb vmlinux SYS_MINI_RDUMP << SHIT 
x/g $1
quit
SHIT

#!/usr/bin/env python
import re
import os
import commands




def addr_info (addr):
    cmd = "./test.sh " + "0x" + addr + " 2>/dev/null | grep \"(gdb).*<\"" + " | sed 's/:.*//g'" + " | sed 's/(gdb) //g'"
    ret, output = commands.getstatusoutput(cmd)
    print output,
    cmd = "aarch64-linux-android-addr2line -e vmlinux " + addr + " | sed 's/.*kernel-3.18\///g'"
    ret, output =  commands.getstatusoutput(cmd)
    print " " + output


logi = open("log1")

lines_read = logi.readlines()
for line in  lines_read:
    print "-----------------------------------------------------"
    print line,
    str = re.findall(r"_ADDR_d: 0x(.*) <== FUNC: 0x(.*)", line)
    if len(str) :
        addr_info(str[0][1])
        continue
    str = re.findall(r"_ACTN_f: 0x(.*) ===   LR: 0x(.*)", line)
    if len(str) :
        addr_info(str[0][0])
        addr_info(str[0][1])
        continue
    
logi.close()

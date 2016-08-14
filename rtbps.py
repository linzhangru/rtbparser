#!/usr/bin/env python
import re
import os
import commands

def addr_info (addr, fd):
    cmd = "./test.sh " + "0x" + addr + " 2>/dev/null | grep \"(gdb).*<\"" + " | sed 's/:.*//g'" + " | sed 's/(gdb) //g'"
    ret0, output0 = commands.getstatusoutput(cmd)
    print output0,
    fd.write(output0)
    cmd = "aarch64-linux-android-addr2line -e vmlinux " + addr + " | sed 's/.*kernel-3.18\///g'"
    ret1, output1 =  commands.getstatusoutput(cmd)
    print " " + output1
    fd.write(" " + output1 + "\n")
    
global log
log = []

def main():

    for i in range(0,8):
        tmp = "cpu" + str(i) + ".txt"
        fd = open(tmp, 'w')
        log.append(fd)
    
    #print logfilename
    

    logi = open("log1")
    idx = 0

    lines_read = logi.readlines()
    for line in  lines_read:
        fd = idx%8
        idx = idx + 1;
        print "-----------------------------------------------------\n",
        log[fd].write("-----------------------------------------------------\n")
        print line,
        log[fd].write(line)
        vals = re.findall(r"_ADDR_d: 0x(.*) <== FUNC: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][1], log[fd])
            continue
        vals = re.findall(r"_ACTN_f: 0x(.*) ===   LR: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][0], log[fd])
            addr_info(vals[0][1], log[fd])
            continue
    
    logi.close()

    for i in range(0,8):
        log[i].close()

if __name__== "__main__":
    main()

#!/usr/bin/env python
import re
import os
import commands
import sys
import getopt

test_sh = []
cache = {}

def addr_info (addr, fd, gdbscript, verbose, debug):
    #print "addr_info", 
    if cache.has_key(addr):
        #print  cache[addr]
        return cache[addr]
    else:
        cmd = "aarch64-linux-android-addr2line -apfs -e vmlinux " + addr + " | sed 's/.*kernel-3.18\///g'"
        ret1, output1 =  commands.getstatusoutput(cmd)
        vals = re.findall(r"0x.*: (.*) at (.*:.*)", output1)
        #print  vals
        cache[addr] = vals 
        return cache[addr]
        
def Usage():
    print "rtbps"
    print "rtbps -t"
    print "rtbps -t -v"
    print "rtbps -t -v -d"
        
        
global log
log = []


gdb_script = """#!/bin/sh
aarch64-linux-android-gdb vmlinux SYS_MINI_RDUMP << SHIT 
x/g $1
quit
SHIT
"""


def main():
    ret, output = commands.getstatusoutput("rtbp")
    lines_read = output.split("\n") 
    #print len(lines_read)
    global test_sh
    #test_sh = sys.argv[1]
    #print test_sh
    verbose = False
    time_info = False
    debug = False
    opts, args = getopt.getopt(sys.argv[1:], "dvth", ["debug", "verbose","time_info","help"])
    gdbscript = ".gdbscript"
    
    
    gdbsc = open(gdbscript, "w")
    gdbsc.write(gdb_script)
    gdbsc.close()
    os.system("chmod u+x ./" + gdbscript)
    
    #exit(0)
    
    print "opts : " + str(opts)
    print "args : " + str(args)

    for opt,arg in opts:
        if   opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-t", "--time_info"):
            time_info = True
        elif opt in ("-h", "--help"):
            Usage()
            exit(0)
        else:
            assert False, "unknown option \"%s\"" % (opt,)

    print "Debug: " + str(debug)
            
    if debug:
        print "test_sh   : " + str(test_sh)
        print "debug     : " + str(debug)
        print "verbose   : " + str(verbose)
        print "time_info : " + str(time_info)
            
    #exit(0)
    if time_info:
        os.system("date")
    
    for i in range(0,8):
        tmp = "cpu" + str(i) + ".txt"
        fd = open(tmp, 'w')
        log.append(fd)
    
    idx = 0

    #lines_read = logi.readlines()
    for line in  lines_read:
        fd = idx%8
        idx = idx + 1;
        if debug:
            print "CPU" + str(fd) + ":",  
            print "-----------------------------------------------------\n",
        #log[fd].write("-----------------------------------------------------\n")
        if debug:
            print line
        #log[fd].write(line+" ")
        vals = re.findall(r"\[(.*)\] LOGK_.*_ADDR_d: 0x(.*) <== FUNC: 0x(.*)", line)
        #print vals
        if len(vals) :
            #log[fd].write(line+" ")
            log[fd].write("[" + vals[0][0] + "] " + "0x" + vals[0][1] + " <== 0x" + vals[0][2] + " ")
            info = addr_info(vals[0][2], log[fd], gdbscript, verbose, debug)
            #print "info: ",
            #print info
            log[fd].write(info[0][0] + " @ " + info[0][1]);
            log[fd].write("\n")
            continue
        
        vals = re.findall(r"\[(.*)\] LOGK_.*_ACTN_f: 0x(.*) === _LR_: 0x(.*)", line)
        print vals
        if len(vals) :
            #log[fd].write(line+" ")
            log[fd].write("[" + vals[0][0] + "] " + "0x" + vals[0][1] + " === 0x" + vals[0][2] + " ")
            info_1 = addr_info(vals[0][1], log[fd], gdbscript, verbose, debug)
            info_2 = addr_info(vals[0][2], log[fd], gdbscript, verbose, debug)
            #print info_1
            #print info_2
            log[fd].write(info_1[0][0] + "/" + info_2[0][0] + " @ " + info_1[0][1] + "/" + info_2[0][1]);
            log[fd].write("\n")
            continue

        vals = re.findall(r"(\[.*\].*)",line)
        #log[fd].write(line+" ")
        log[fd].write(vals[0])
        log[fd].write("\n")
        
    #logi.close()

    for i in range(0,8):
        log[i].close()

    if time_info:
        os.system("date")

        
if __name__== "__main__":
    main()

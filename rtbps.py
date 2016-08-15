#!/usr/bin/env python
import re
import os
import commands
import sys
import getopt

test_sh = []
cache0 = {}
cache1 = {}

def addr_info (addr, fd, gdbscript, verbose, debug):
    
    if verbose:
        if cache0.has_key(addr):
            if debug:
                print "(hit ): " + cache0[addr]
            fd.write(cache0[addr])
        else:
            #global test_sh
            cmd = "./" + gdbscript + " " + "0x" + addr + " 2>/dev/null | grep \"(gdb).*<\"" + " | sed 's/:.*//g'" + " | sed 's/(gdb) //g'"
            #print cmd
            ret0, output0 = commands.getstatusoutput(cmd)
            if debug:
                print "(miss): " + output0
            fd.write(output0)
            cache0[addr] = output0
    else:
        if debug:
            print "0x" + addr + " "
        fd.write("0x" + addr + " ")
        
    if cache1.has_key(addr):
        if debug:
            print "(hit ): " + "0x" + addr + cache1[addr]
        fd.write(cache1[addr]+"\n")
    else:
        cmd = "aarch64-linux-android-addr2line -e vmlinux " + addr + " | sed 's/.*kernel-3.18\///g'"
        ret1, output1 =  commands.getstatusoutput(cmd)
        if debug:
            print "(miss): " + "0x" + addr +  " " + output1
        fd.write(" " + output1 + "\n")
        cache1[addr] = " " + output1 

def Usage():
    print "./rtbps.py"
    print "./rtbps.py -t"
    print "./rtbps.py -t -v -s ./test.sh"
        
        
global log
log = []


gdb_script = """#!/bin/sh
aarch64-linux-android-gdb vmlinux SYS_MINI_RDUMP << SHIT 
x/g $1
quit
SHIT
"""


def main():
    ret, output = commands.getstatusoutput("./rtbp")
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
        log[fd].write("-----------------------------------------------------\n")
        if debug:
            print line
        log[fd].write(line+"\n")
        vals = re.findall(r"_ADDR_d: 0x(.*) <== FUNC: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][1], log[fd], gdbscript, verbose, debug)
            continue
        vals = re.findall(r"_ACTN_f: 0x(.*) === _LR_: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][0], log[fd], gdbscript, verbose, debug)
            addr_info(vals[0][1], log[fd], gdbscript, verbose, debug)
            continue
        #print "\n"
        
    #logi.close()

    for i in range(0,8):
        log[i].close()

    if time_info:
        os.system("date")

        
if __name__== "__main__":
    main()

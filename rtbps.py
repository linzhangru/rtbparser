#!/usr/bin/env python
import re
import os
import commands
import sys
import getopt

test_sh = []
cache0 = {}
cache1 = {}

def addr_info (addr, fd, verbose):
    
    if verbose:
        if cache0.has_key(addr):
            #print "hit " + cache0[addr]
            fd.write(cache0[addr])
        else:
            global test_sh
            cmd = str(test_sh) + " " + "0x" + addr + " 2>/dev/null | grep \"(gdb).*<\"" + " | sed 's/:.*//g'" + " | sed 's/(gdb) //g'"
            #print cmd
            ret0, output0 = commands.getstatusoutput(cmd)
            print "miss " + output0,
            fd.write(output0)
            cache0[addr] = " " + output0
    else:
        #print "0x" + addr + " ",
        fd.write("0x" + addr + " ")
        
    if cache1.has_key(addr):
        print "hit " + cache1[addr]
        fd.write(cache1[addr]+"\n")
    else:
        cmd = "aarch64-linux-android-addr2line -e vmlinux " + addr + " | sed 's/.*kernel-3.18\///g'"
        ret1, output1 =  commands.getstatusoutput(cmd)
        print "miss " + output1
        fd.write(" " + output1 + "\n")
        cache1[addr] = " " + output1 

        
global log
log = []

def main():
    ret, output = commands.getstatusoutput("./rtbp")
    lines_read = output.split("\n") 
    #print len(lines_read)
    global test_sh
    #test_sh = sys.argv[1]
    #print test_sh
    verbose = False
    opts, args = getopt.getopt(sys.argv[1:], "s:v:i", ["script", "verbose","time_info"])
    #print "opts : " + str(opts)
    #print "args : " + str(args)

    for opt,arg in opts:
        if opt in ("-s", "--script"):
            test_sh = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-i", "--time_info"):
            time_info = True
        else:
            assert False, "unknown option \"%s\"" % (opt,) 
    print "test_sh: " + str(test_sh)
    print "verbose: " + str(verbose)
            
    #exit(0)
    if time_info:
        os.system("date")
    
    for i in range(0,8):
        tmp = "cpu" + str(i) + ".txt"
        fd = open(tmp, 'w')
        log.append(fd)
    
    #print logfilename
    

    #logi = open("log1")
    idx = 0

    #lines_read = logi.readlines()
    for line in  lines_read:
        fd = idx%8
        idx = idx + 1;
        #print "-----------------------------------------------------\n",
        log[fd].write("-----------------------------------------------------\n")
        #print line
        log[fd].write(line+"\n")
        vals = re.findall(r"_ADDR_d: 0x(.*) <== FUNC: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][1], log[fd], verbose)
            continue
        vals = re.findall(r"_ACTN_f: 0x(.*) ===   LR: 0x(.*)", line)
        if len(vals) :
            addr_info(vals[0][0], log[fd], verbose)
            addr_info(vals[0][1], log[fd], verbose)
            continue
        #print "\n"
        
    #logi.close()

    for i in range(0,8):
        log[i].close()

    if time_info:
        os.system("date")

        
if __name__== "__main__":
    main()

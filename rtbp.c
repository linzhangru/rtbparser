#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


struct msm_rtb_layout 
{
    unsigned char sentinel[3];
    unsigned char log_type;
    unsigned int  idx;
    unsigned long caller;
    unsigned long data;
    unsigned long timestamp;
} __attribute__ ((__packed__));
 


enum logk_event_type {
    LOGK_NONE = 0,
    LOGK_READL = 1,
    LOGK_WRITEL = 2,
    LOGK_LOGBUF = 3,
    LOGK_HOTPLUG = 4,
    LOGK_CTXID = 5,
    LOGK_TIMESTAMP = 6,
    LOGK_L2CPREAD = 7,
    LOGK_L2CPWRITE = 8,
    LOGK_IRQ = 9,
    LOGK_DIE = 20,
    LOGK_INITCALL = 21,
    LOGK_SOFTIRQ = 22,
    LOGK_MAX
};

#define LOGTYPE_NOPC 0x80

char log_type[LOGK_MAX][16] = {
    [LOGK_NONE]      = "LOGK_NONE",
    [LOGK_READL]     = "LOGK_READL",
    [LOGK_WRITEL]    = "LOGK_WRITEL",
    [LOGK_LOGBUF]    = "LOGK_WRITEL",
    [LOGK_HOTPLUG]   = "LOGK_HOTPLUG",
    [LOGK_CTXID]     = "LOGK_CTXID",
    [LOGK_TIMESTAMP] = "LOGK_TIMESTAMP",
    [LOGK_L2CPREAD]  = "LOGK_L2CPREAD",
    [LOGK_L2CPWRITE] = "LOGK_L2CPWRITE",
    [LOGK_IRQ]       = "LOGK_IRQ",
    /* HTC DEFINE: START FROM 20 */
    [LOGK_DIE]       = "LOGK_DIE",
    [LOGK_INITCALL]  = "LOGK_INITCALL",
    [LOGK_SOFTIRQ]   = "LOGK_SOFTIRQ",

};

    




int main()
{
    int fd;
    unsigned char *buf;
    struct msm_rtb_layout rtb_entry;
    int i;

    buf = (char*)(&rtb_entry);
    //printf("sizeof(unsigned int) : %ld\n", sizeof(unsigned int));
    //printf("sizeof(unsigned long): %ld\n", sizeof(unsigned long));
    printf("%s\n", log_type[LOGK_READL]);
    
#if 1
    fd = open("SYS_RTB_RAW", O_RDONLY);
    while(read(fd, &rtb_entry, 32) > 0) {
#if 0	
	for(i = 0; i < 32; i++) {
	    if((i%16==0)&&(i%32!=0)) printf("\n");
	    printf("%02x", buf[i]);
	}
	printf("\n");
	printf("rtb_entry.sentinel  :%02x%02x%02x\n", rtb_entry.sentinel[0], rtb_entry.sentinel[1], rtb_entry.sentinel[2]);	
#endif
	//printf("------------------------------------------\n");
	//printf("rtb_entry.idx       :%08x\n",  rtb_entry.idx);
	//printf("rtb_entry.timestamp :[%09.6f]\n",   rtb_entry.timestamp*1.0/(1000*1000*1000));
	printf("%08x [%09.6f] %-16.14s",
	       rtb_entry.idx,
	       rtb_entry.timestamp*1.0/(1000*1000*1000),
	       (rtb_entry.log_type & LOGTYPE_NOPC) ? log_type[rtb_entry.log_type&(~LOGTYPE_NOPC)] : log_type[rtb_entry.log_type]);
	if(rtb_entry.log_type & LOGTYPE_NOPC){
	    //printf("rtb_entry.log_type  :%s\n",  log_type[rtb_entry.log_type&(~LOGTYPE_NOPC)]);
	    switch(rtb_entry.log_type&(~LOGTYPE_NOPC)) {
	    case LOGK_TIMESTAMP:
		printf("[%09.6f]\n", (rtb_entry.data<<32|rtb_entry.caller)*1.0/(1000*1000*1000));
		break;
	    default:
		printf("\n");
		printf("unknown log_type  :%s\n ", log_type[rtb_entry.log_type&(~LOGTYPE_NOPC)]);
		printf("rtb_entry.caller  :%08lx\n",  rtb_entry.caller);
		printf("rtb_entry.data    :%08lx\n",  rtb_entry.data);
	    }
	    
	} else {
	    //printf("rtb_entry.log_type  :%s\n",  log_type[rtb_entry.log_type]);
	    //printf("rtb_entry.caller    :%08lx\n",    rtb_entry.caller);
	    //printf("rtb_entry.data      :%08lx\n",    rtb_entry.data);
	    switch(rtb_entry.log_type){
	    case LOGK_READL:
	    case LOGK_WRITEL:
		printf("_ADDR_d: 0x%08lx <== FUNC: 0x%08lx\n", rtb_entry.data, rtb_entry.caller);
		break;
	    case LOGK_IRQ:
		printf("_TSTP_ms:%-10ld, IRQ_nr:%ld\n", rtb_entry.caller, rtb_entry.data);
		break;
	    case LOGK_CTXID:
		printf("_TSTP_ms:%-10ld, TASKPID:%ld\n", rtb_entry.caller, rtb_entry.data);
		break;
	    case LOGK_SOFTIRQ:
		printf("_ACTN_f: 0x%08lx ===   LR: 0x%08lx\n", rtb_entry.data, rtb_entry.caller);
		break;
	    default:
		printf("unsupported type\n");
	    }
	}
    }
    
    close(fd);
#endif    
}

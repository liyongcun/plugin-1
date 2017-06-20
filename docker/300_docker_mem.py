#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author：yanwen
#Date：2016.12.04
#Version：1.0
#V1.0 Description：docker虚拟机mem监控

import subprocess
import json
import time
import os
import commands
import logging
import sys
data=[]
logging.basicConfig(level=logging.ERROR,  
                    filename='/home/work/open-falcon/agent/plugin/error.log',  
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

ip=commands.getoutput("/usr/sbin/ifconfig|egrep 'inet 192\.168|inet 10|inet 172\.1[6-9]|inet 172\.2[0-9]|inet 172\.3[01]'| awk '{print $2}'")
re=subprocess.Popen("/usr/bin/sh /home/work/open-falcon/agent/plugin/docker/docker-monitor -m",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
#value=re.communicate()[0].split('\n')[2].split()[3].split('%')[0]
try:
    value=float(re.communicate()[0].split('\n')[2].split()[3].split('%')[0])
except Exception,err:
    logging.error("Run command failed:%s" %str(err))
    sys.exit(2)
def create_record(value):
    record={}
    record['metric'] = 'docker.mem'
    record['endpoint'] = ip.split('\n')[0]+'_'+os.uname()[1]
    record['timestamp'] = int(time.time())
    record['step'] = 300
    record['value'] = value
    record['counterType'] = 'GAUGE'
    record['tags'] = ''
    data.append(record)
create_record(value)
if data:
   print json.dumps(data)
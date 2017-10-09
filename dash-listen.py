#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import urllib2
import json
from datetime import datetime

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    # if pkt[ARP].psrc == '192.168.0.1': # ARP Probe
    if pkt[ARP].hwsrc[0:8] == '34:d2:70':
      print "ARP Probe : " + pkt[ARP].psrc
      print "ARP Probe from: " + pkt[ARP].hwsrc
      if pkt[ARP].hwsrc == '34:d2:70:7d:a9:72':
        # blue
        post_ifttt("sleep_button_pressed")
        sys.exit(0)
      elif pkt[ARP].hwsrc == '34:d2:70:08:9f:1c':
        # red
        post_ifttt("not_sleep_button_pressed")
        sys.exit(0)


def post_ifttt(button_id):
  try :
    params_raw = ''
    url = "https://maker.ifttt.com/trigger/%s/with/key/c40ujsL_WXII98c3an1wdp" % (button_id)
    now_hms = datetime.now().strftime("%H:%M:%S")
    params_raw = {"value1":now_hms}
    params = urllib.urlencode(params_raw)
    # params = urllib.urlencode({ "value1" : "", "value2" : "", "value3" : "" })
    # req.add_data(json.dumps(params))
    req = urllib2.Request(url, params)
    res = urllib2.urlopen(req)
    r = res.read()
    print r
  except Exception as e:
    print e

# print sniff(prn=arp_display, filter="arp", store=0, count=10)
print sniff(prn=arp_display, filter="arp", store=0)
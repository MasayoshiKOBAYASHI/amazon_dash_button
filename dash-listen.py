#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import urllib2
import json
import yaml
from datetime import datetime

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    # if pkt[ARP].psrc == '192.168.0.1': # ARP Probe
    settings = load_settings()
    if pkt[ARP].hwsrc[0:8] == settings['mac']['head']:
      print "ARP Probe : " + pkt[ARP].psrc
      print "ARP Probe from: " + pkt[ARP].hwsrc
      if pkt[ARP].hwsrc == settings['mac']['sleep']:
        # blue
        post_ifttt("sleep_button_pressed")
        sys.exit(0)
      elif pkt[ARP].hwsrc == settings['mac']['no_sleep']:
        # red
        post_ifttt("not_sleep_button_pressed")
        sys.exit(0)

def load_settings():
  with open("settings.yaml", "r") as ya:
    settings = yaml.load(ya)
  return settings

def post_ifttt(button_id):
  try :
    settings = load_settings()
    params_raw = ''
    url = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (button_id, settings['ifttt']['key'])
    now_hms = datetime.now().strftime("%H:%M:%S")
    params_raw = {"value1": now_hms}
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
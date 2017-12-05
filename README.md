# Read Me

このスクリプトは amazon dash button を押すとIFTTT連携する機能が搭載されています

この[サイト](https://qiita.com/noexpect/items/efcd5065830021905a60)を参考に作成しました

### python環境の準備

```
$ sudo apt-get install tcpdump python-crypto python-scapy
# scapyを使いたいだけだけどあれこれいれる

$ pip show scapy
Name: scapy
Version: 2.2.3
Location: /usr/lib/python2.7/dist-packages
Requires:
# scapyがインストールできてればOK
```

### DashボタンのMACアドレスの取得

以下のpythonスクリプトを実行して、実行中に amazon dash button を押す

``` dash-listen-1.py
from scapy.all import *

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print "ARP Probe from: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
```

```
$ sudo python dash-listen-1.py 
WARNING: No route found for IPv6 destination :: (no default route?)
# ここまで出力されるのでDashボタンを押下
ARP Probe from: XX:XX:XX:XX:XX:XX
ARP Probe from: XX:XX:XX:XX:XX:XX
ARP Probe from: XX:XX:XX:XX:XX:XX
^C[]
$ 
```

### 準備完了

あとは settings.yml を書き換えて、dash-listen.py 実行してください

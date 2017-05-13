#!/usr/bin/env python
import os
import platform
import subprocess

class Engine(object):
 def __init__(self):
  self.fail = []
  self.rslt = 'log.txt'
  self.cmd0 = 'apt-get'
  self.cmd1 = 'apt-cache policy'
  self.cmd2 = ['pysocks','mechanize']
  self.cmd3 = ['update','python-pip','proxychains','tor']

 def cmdform(self,cmd):
  return cmd.split()

 def fetch(self):
  for line,cmd in enumerate(self.cmd3):
   subprocess.call(['clear'])
   if not line:
    print '[-] Updating ...'
    cmd=self.cmdform('{} {}'.format(self.cmd0,cmd))
   else:
    print '[-] Installing: {} ...'.format(cmd)
    if  not 'Ubuntu' in platform.platform():
     cmd=self.cmdform('{} install {} -y'.format(self.cmd0,cmd))
    else:
     cmd=self.cmdform('{} install {} -y --allow-unauthenticated'.format(self.cmd0,cmd))
   subprocess.Popen(cmd,stdout=devnll,stderr=devnll).wait()

  if 'Ubuntu' in platform.platform():
   for cmd in self.cmd2:
    subprocess.call(['clear'])
    print '[-] Installing: {} ...'.format(cmd)
    cmd=self.cmdform('pip install -U {}'.format(cmd))
    subprocess.Popen(cmd,stdout=devnll,stderr=devnll).wait()
  
 def examine(self):
  with open(self.rslt,'r') as file:
   for num,line in enumerate(file):
    line=line.split()
    if not num:
     name=line[0][:-1]
    else:
     line=line[1][1:][:-1]
     if line=='none':
      self.fail.append(name)
     break

 def check(self):
  for cmd in self.cmd3[1:]:
   log=open(self.rslt,'w+')
   cmd=self.cmdform('{} {}'.format(self.cmd1,cmd))
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()
   self.examine()
  self.exit()

 def exit(self):
  subprocess.call(['clear'])
  os.remove(self.rslt)
  if self.fail:
   for item in self.fail:
    print '[!] Failed to install: {}'.format(item)
  else:
   print '[-] Installation Completed'

 def source(self):
  srcs    = ['deb http://old.kali.org/kali sana main non-free contrib','deb-src http://http.kali.org/kali kali-rolling main contrib non-free','deb http://http.kali.org/kali kali-rolling main contrib non-free']
  srclist = [line.replace('\n','').strip() for line in open('/etc/apt/sources.list','r') if len(line.replace('\n','').strip())]

  for a,file in enumerate(srclist):
   for b,src in enumerate(srcs):
    if file==src:
     del srcs[srcs.index(src)]

  if srcs:
   subprocess.Popen(self.cmdform('apt-key adv --keyserver pgp.mit.edu --recv-keys ED444FF07D8D0BF6'),stdout=devnll,stderr=devnll).wait()
   with open('/etc/apt/sources.list','a') as update:
    for src in srcs:
     update.write('{}\n'.format(src))

if __name__ == '__main__':
 if os.getuid():
  exit('root access required')

 engine = Engine()
 devnll = open(os.devnull,'w')

 engine.source()
 engine.fetch()
 engine.check()#!/usr/bin/env python
import os
import platform
import subprocess

class Engine(object):
 def __init__(self):
  self.fail = []
  self.rslt = 'log.txt'
  self.cmd0 = 'apt-get'
  self.cmd1 = 'apt-cache policy'
  self.cmd2 = ['pysocks','mechanize']
  self.cmd3 = ['update','python-pip','proxychains','tor']

 def cmdform(self,cmd):
  return cmd.split()

 def fetch(self):
  for line,cmd in enumerate(self.cmd3):
   print cmd
   '''subprocess.call(['clear'])
   if not line:
    print '[-] Updating ...'
    cmd=self.cmdform('{} {}'.format(self.cmd0,cmd))
   else:
    print '[-] Installing: {} ...'.format(cmd)
    if  not 'Ubuntu' in platform.platform():
     cmd=self.cmdform('{} install {} -y'.format(self.cmd0,cmd))
    else:
     cmd=self.cmdform('{} install {} -y --allow-unauthenticated'.format(self.cmd0,cmd))
   subprocess.Popen(cmd,stdout=devnll,stderr=devnll).wait()'''
  #if 'Ubuntu' in platform.platform():
  # for cmd in self.cmd2:
  #  subprocess.call(['clear'])
  #  print '[-] Installing: {} ...'.format(cmd)
  #  cmd=self.cmdform('pip install -U {}'.format(cmd))
  #  subprocess.Popen(cmd,stdout=devnll,stderr=devnll).wait()
  
 def examine(self):
  with open(self.rslt,'r') as file:
   for num,line in enumerate(file):
    line=line.split()
    if not num:
     name=line[0][:-1]
    else:
     line=line[1][1:][:-1]
     if line=='none':
      self.fail.append(name)
     break

 def check(self):
  for cmd in self.cmd3[1:]:
   log=open(self.rslt,'w+')
   cmd=self.cmdform('{} {}'.format(self.cmd1,cmd))
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()
   self.examine()
  self.exit()

 def exit(self):
  subprocess.call(['clear'])
  os.remove(self.rslt)
  if self.fail:
   for item in self.fail:
    print '[!] Failed to install: {}'.format(item)
  else:
   print '[-] Installation Completed'

 def source(self):
  srcs    = ['deb http://old.kali.org/kali sana main non-free contrib','deb-src http://http.kali.org/kali kali-rolling main contrib non-free','deb http://http.kali.org/kali kali-rolling main contrib non-free']
  srclist = [line.replace('\n','').strip() for line in open('/etc/apt/sources.list','r') if len(line.replace('\n','').strip())]

  for a,file in enumerate(srclist):
   for b,src in enumerate(srcs):
    if file==src:
     del srcs[srcs.index(src)]

  if srcs:
   subprocess.Popen(self.cmdform('apt-key adv --keyserver pgp.mit.edu --recv-keys ED444FF07D8D0BF6'),stdout=devnll,stderr=devnll).wait()
   with open('/etc/apt/sources.list','a') as update:
    for src in srcs:
     update.write('{}\n'.format(src))

if __name__ == '__main__':
 if os.getuid():
  exit('root access required')

 engine = Engine()
 devnll = open(os.devnull,'w')

 engine.source()
 engine.fetch()
 engine.check()

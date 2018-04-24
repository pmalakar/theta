import sys
import numpy as np
from subprocess import *
from collections import OrderedDict

from parsejobnodes import readAllocation_

global nodecfg, nidstrfile, ostfile

nodecfg = ""
nidstrfile = ""
ostfile = ""

osts = []

#expects a line of osts separated by spaces
#e.g. 50 32 26 22
def parse_osts():

 global osts, ostfile

 f = open(ostfile, 'r')

 while True:
   line = f.readline()
   if not line: break
   osts = line.split()
 
 f.close()

#system name
machine = sys.argv[1]

#config file
nodecfg = machine+'.allnodes' #sys.argv[4]

#current allocation
nidstrfile = sys.argv[2] 

#current ost allocated
ostfile = sys.argv[3] 

#ost connections 
osts_conn = machine+'_osts_conn'

#lnet routes
routesconf = machine+'.routesconf'

print nodecfg, nidstrfile, ostfile

parse_osts()

it = 0

ost_lnet_file = ostfile + '.ost2lnet'
o2lfile = open(ost_lnet_file, 'w')

ostlnet_dict = OrderedDict()
for i in osts:
  hex_i = 'OST%04x' % int(i)
  #print i, hex_i
  cmd = 'grep ' + hex_i + '  ' + osts_conn + ' | awk \'{print $3}\' | awk -F\'@\' \'{print $2}\''
  output1 = Popen(cmd, shell=True, stdout=PIPE).communicate()[0] 
  output1 = output1.strip()
  cmd = 'grep ' + output1 + ' ' + routesconf + ' | awk \'{print $3}\' | awk -F\'@\' \'{print $1}\'' # | awk -F\'\[\' \'{print $2}\''
  output2 = Popen(cmd, shell=True, stdout=PIPE).communicate()[0] 
  output2 = output2.strip()
  output2 = output2.rstrip(']')
  output2 = output2.lstrip('[')
#  print i, hex_i, output1, output2 
  writestr = str(i) + ' ' + str(hex_i)  + ' ' + output1 + ' ' + output2.replace(',',' ') + '\n'
  o2lfile.write(writestr)

  ostlnet_dict[i] = output2
  it = it + 1
 
o2lfile.close()

for key in ostlnet_dict:
 #words = ostlnet_dict[key].split(',')
 lnetfile = nidstrfile + '.ost.' + key
# print lnetfile
 f = open(lnetfile, 'w')
 f.write(ostlnet_dict[key])
 f.write('\n')
 f.close()
 
 readAllocation_(nodecfg, lnetfile)
# lnet_ost0_map = 'jobmap_'+lnetfile

print 


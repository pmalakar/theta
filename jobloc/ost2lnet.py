import sys
from subprocess import *

nidstrfile = ""
ostfile = ""
lnet_ost0_file = ""

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

#current ost allocated
ostfile = sys.argv[1] 

#system name
machine = sys.argv[2]

#ost connections 
osts_conn = machine+'_osts_conn'

#lnet routes
routesconf = machine+'.routesconf'

#config file
#nodecfg = sys.argv[4]

#current allocation
#nidstrfile = sys.argv[5] 

parse_osts()

lnet0 = '' #[]
it = 0

ost_lnet_file = ostfile + '.ost2lnet'
o2lfile = open(ost_lnet_file, 'w')

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

  if it == 0:
    lnet0 = output2 #.split(',') #.append(output2)

  it = it + 1
 
o2lfile.close()

#print

#lnet_ost0_file = nidstrfile + '.lnet_ost0'
#f = open(lnet_ost0_file, 'w')
#f.write(lnet0)
#f.write('\n')
#f.close()

#readAllocation_(nodecfg, lnet_ost0_file)
#lnet_ost0_map = 'jobmap_'+lnet_ost0_file

#print 


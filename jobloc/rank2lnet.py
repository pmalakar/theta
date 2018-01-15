import sys
import numpy as np
import math
from subprocess import *
from collections import OrderedDict

maxosts = 56
ppn = 32  #64

osts = []
ostlnet_dict = OrderedDict()
servicenode_dict = OrderedDict()

#global nodecfg, nidstrfile, ostfile

#nodecfg = ""
#nidstrfile = ""
#ostfile = ""

nodes = []

def expand_node_list():

  global nodes

  f = open(nidstrfile, "r")
  nidstring = f.readline()
  f.close()
 
  nodegroups = []
  if nidstring.find(',') == -1:
    nodegroups.append(nidstring)
  else:
    nodegroups = nidstring.split(',')

  for group in nodegroups:
    if group.find('-') > 0:
      words = group.split('-')
      for node in range(int(words[0]),int(words[1])+1):
        nodes.append(node)
    else:
      nodes.append(int(group))

  #print nodes


def parse_osts():

 global osts #, ostfile
 f = open(ostfile, 'r')

 while True:
   line = f.readline()
   if not line: break
   osts = line.split()
 
 f.close()


def get_lnet_mapping():

 global ostlnet_dict
 
 it = 0
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
#  writestr = str(i) + ' ' + str(hex_i)  + ' ' + output1 + ' ' + output2.replace(',',' ') + '\n'
   ostlnet_dict[i] = output2
   it = it + 1

def read_nodecfg():

 global servicenode_dict
 cab_position, cab_row, cage, slot, cpu, processor_id = '', '', '', '', '', ''

 f = open(nodecfg, 'r')

 while True:
    line = f.readline()
    if not line: break
    if 'compute' in line: continue
    words = line.split(',')
    for word in words:
      if 'cab_position' in word:
       cab_position=word.split('=')[1]
      elif 'cab_row' in word:
       cab_row=word.split('=')[1]
      elif 'cage=' in word:
       cage=word.split('=')[1]
      elif 'slot=' in word:
       slot=word.split('=')[1]
      elif 'cpu=' in word:
       cpu=word.split('=')[1]
      elif 'processor_id=' in word:
       processor_id=word.split('=')[1]

   # if int(processor_id) == node_id:
  
    servicenode_dict[processor_id] = (cab_position, cab_row, cage, slot, cpu)
    #print processor_id, cab_position, cab_row, cage, slot, cpu
 
 f.close()


def readfile():

 #global osts, ostfile

 rankmap = []
 frank = open(nidstrmapfile, 'r')
 cnt=0
 while True:
   line = frank.readline()
   if not line: break
   words = line.split()
   rankmap.append([])
   rankmap[cnt] = words
   cnt = cnt+1
 frank.close()
 
 f = open(rank2ostfile, 'r')
 fout = open(rank2lnetfile, 'w')
 fout_ = open(rank2lnetfile_, 'w')

 while True:
   line = f.readline()
   if not line: break
   words = line.split()
# print words[0], words[1], words[5] 
  #for each rank and ost id, read the nidstrmapfile (node index, nid, coords)
   rank = int(words[0])
   segment = int(words[1])
   wtime = float(words[4])
   ostid = words[5]

   #this is the chronological node id
   nodeidx = int(math.floor(rank / ppn))
    
   lnetidx = int(segment % 7)

  #source - rankmap[nodeidx]
  #dest - ostlnet_dict[ostid] - index 
  
   destidx_ = ostlnet_dict[ostid].split(',')[lnetidx]
   print nodeidx, nodes[nodeidx], rankmap[nodeidx], segment, lnetidx, ostlnet_dict[ostid], destidx_, servicenode_dict[destidx_]
  # print nodeidx, nodes[nodeidx], rankmap[nodeidx], segment, lnetidx, wtime, destidx_, servicenode_dict[destidx_]
   #op = str(rank) + ' ' + destidx_
   op = str(nodes[nodeidx]) + ' ' + destidx_ #+ ' ' + str(wtime)
   fout.write(op)
   fout.write('\n')
   op = str(nodes[nodeidx]) + ' ' + destidx_ + ' ' + str(wtime)
   fout_.write(op)
   fout_.write('\n')

 f.close()
 fout.close()
 fout_.close()

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

#rank2ost file name
rank2ostfile = sys.argv[4]

#jobmap of current allocation
nidstrmapfile = 'jobmap_' + nidstrfile #sys.argv[5] 

rank2lnetfile = nidstrfile + '.lnetroutes' # ostfile + '.lnetroutes'
rank2lnetfile_ = nidstrfile + '.lnetroutes.wtime' # ostfile + '.lnetroutes'

expand_node_list()

parse_osts()

get_lnet_mapping()

read_nodecfg()

#print ostlnet_dict
#print servicenode_dict

readfile()

print 


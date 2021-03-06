import os
import sys
import numpy as np
from subprocess import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import OrderedDict

from parsejobnodes import readAllocation_

patterns = ['-', 'x', 'o', 'O', '.', '*']  # more patterns

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


def draw_():

 fig = plt.figure(figsize=(15,10))
 ax = fig.add_subplot(111, aspect='equal')

 ax.set_xlim([0,100])
 ax.set_ylim([0,18])

 for cab_row in range(0,2):
  for cab_pos in range(0,12):
   if cab_row == 1 and cab_pos > 7:
    break
   cab_str = 'C'+str(cab_pos)+'-'+str(cab_row)
   cabinets.append(cab_str)
   data =(cab_pos, cab_row, cab_str)
   cabinet_positions.append(data)

 #print cabinets
 #print locations
 #print cabinet_positions

 xwidth = 6.4
 ywidth = 3.6

 routerwidth = xwidth/16
 routerheight = ywidth/3

 spacer1 = 0.1
 spacer2 = 3
 spacer3 = 5
 xdist  = spacer2 + xwidth
 ydist  = spacer3 + ywidth

 idx = -1
 for j in range(0,2):
  for i in range(0,10):
   
   idx = idx + 1
   posx = spacer2 + (i * xdist)
   posy = spacer2 + (j * ydist)
   p = patches.Rectangle(
        (posx, posy),
        xwidth,
        ywidth,
        fill=False, 
        linewidth=2,
        edgecolor='b'
   ) 
   ax.add_patch(p)
   x = posx + xwidth/2
   y = posy - ywidth/2 #- spacer1
   ax.text(x, y, cabinets[idx], horizontalalignment='center', size='large', color='g', fontweight='bold')
   #print posx, posy, cabinets[idx]

 #idx = -1
 #for j in range(0,2):
 # for i in range(0,10):
   
 #  idx = idx + 1
   for item in locations: #cabinet_positions:
     if int(item[2]) == cabinet_positions[idx][0] and int(item[3]) == cabinet_positions[idx][1]:
      print idx, item #, cabinet_positions[idx]
      #ax.text(x, y+spacer2, '*', horizontalalignment='center', color='m', fontweight='bold')
      nodex = posx + int(item[5])*routerwidth
      nodey = posy + int(item[4])*routerheight
      #print nodex, nodey, item[4], item[5], posx, posy, routerheight, routerwidth
      ax.text(nodex, nodey, 'o', horizontalalignment='center', color='r', fontweight='bold')
      
 plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
 plotfilename = 'nodelayout.'+nidstrfile+'.png'
 fig.savefig(plotfilename, bbox_inches='tight')
 #plt.show()


##### Variables

cabinets = []
cabinet_positions = list()

#config file
machine = sys.argv[1]
nodecfg = machine+'.allnodes' 

#current allocation
nidstrfile = sys.argv[2] 

ostfile = nidstrfile + '.ost'

readAllocation_(nodecfg, nidstrfile)

#todo if relative path is given, filter the file name
#if 
jobmap = 'jobmap_'+nidstrfile




#read the jobmap
f = open(jobmap, 'r')
locations, jobcabinets, jobranks = [], [], []

while True:
  line = f.readline()
  if not line: break
  words = line.split()
  locations.append(words)
  jobcabinet="C"+words[2]+"-"+words[3]
  jobcabinets.append(jobcabinet)
  jobranks.append(int(words[1]))
f.close()

#print jobcabinets, jobranks
#print locations

draw_()

print 

if os.path.isfile(ostfile) == False:
  exit()

parse_osts()

lnet0 = '' #[]
it = 0

ost_lnet_file = nidstrfile + '.ost2lnet'
o2lfile = open(ost_lnet_file, 'w')

for i in osts:
  hex_i = 'OST%04x' % int(i)
  #print i, hex_i
  cmd = 'grep ' + hex_i + ' theta_osts_conn | awk \'{print $3}\' | awk -F\'@\' \'{print $2}\''
  output1 = Popen(cmd, shell=True, stdout=PIPE).communicate()[0] 
  output1 = output1.strip()
  cmd = 'grep ' + output1 + ' theta.routesconf | awk \'{print $3}\' | awk -F\'@\' \'{print $1}\'' # | awk -F\'\[\' \'{print $2}\''
  output2 = Popen(cmd, shell=True, stdout=PIPE).communicate()[0] 
  output2 = output2.strip()
  output2 = output2.rstrip(']')
  output2 = output2.lstrip('[')
#  print i, hex_i, output1, output2 
  writestr = str(i) + ' ' + str(hex_i)  + ' ' + output1 + ' ' + output2.replace(',',' ') + '\n'
  o2lfile.write(writestr)

  it = it + 1
 
o2lfile.close()


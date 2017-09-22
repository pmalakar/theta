import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

from parsejobnodes import readAllocation_

patterns = ['-', 'x', 'o', 'O', '.', '*']  # more patterns

def draw_():

 fig = plt.figure(figsize=(15,10))
 ax = fig.add_subplot(111, aspect='equal')

 ax.set_xlim([0,9.5])
 ax.set_ylim([0,26])

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

 xwidth = 3.2
 ywidth = 1.5
 spacer = 1
 xdist  = spacer + xwidth
 ydist  = spacer + ywidth

 idx = -1

 for j in range(0,10):
  for i in range(0,2):
   
   idx = idx + 1
   posx = spacer + (i * xdist)
   posy = spacer + (j * ydist)
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
   y = posy - 0.5
   ax.text(x, y, cabinets[idx],horizontalalignment='center',size='large', color='g', fontweight='bold')
   #print posx, posy, cabinets[idx]

   for item in locations: #cabinet_positions:
     if int(item[2]) == cabinet_positions[idx][0] and int(item[3]) == cabinet_positions[idx][1]:
      print idx, item
      ax.text(x, y + spacer, 'x', horizontalalignment='center', color='m', fontweight='bold')
      

 fig.savefig('nodelayout.png', bbox_inches='tight')
 plt.show()


##### Variables

cabinets = []
cabinet_positions = list()

#config file
nodecfg = sys.argv[1]

#current allocation
nidstrfile = sys.argv[2] 

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



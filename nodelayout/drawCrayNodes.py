import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys
sys.path.append('/Users/preeti/work/projects/ECP17/code/jobmap/')
import parsejobnodes

patterns = ['-', 'x', 'o', 'O', '.', '*']  # more patterns

def draw_():

 fig = plt.figure(figsize=(15,10))
 ax = fig.add_subplot(111, aspect='equal')

 ax.set_xlim([0,9.5])
 ax.set_ylim([0,26])

 cabinets = []
 for cab_row in range(0,2):
  for cab_pos in range(0,12):
   if cab_row == 1 and cab_pos > 7:
    break
   cab_str = 'C'+str(cab_pos)+'-'+str(cab_row)
   cabinets.append(cab_str)

 print cabinets

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

 fig.savefig('nodelayout.png', bbox_inches='tight')
 plt.show()




#config file
nodecfg = sys.argv[1]

#current allocation
nidstrfile = sys.argv[2] 

#readGlobalConfiguration_()
readAllocation_(nodecfg, nidstrfile)

jobmap = 'jobmap_'+nidstrfile

f = open(jobmap, 'r')
while True:
  line = f.readline()
  if not line: break
  words = line.split(',')
  print words
f.close()

draw_()




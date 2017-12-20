import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
from subprocess import *

ostconnfile=sys.argv[1]
routesfile=sys.argv[2]

f = open(ostconnfile, 'r')

ostib=[]
ostidx=[]

while True:
  line = f.readline()
  if not line: break
  words = line.split()
  tokens = words[2].split('@')
  ostib.append(tokens[1])
  tokens = words[0].split('-')
  ostidx.append(tokens[1])
 
f.close()

it=0
for i in ostib:
  cmd = 'grep ' + i + ' ' + routesfile + ' | awk \'{print $3}\' | awk -F\'@\' \'{print $1}\'' # | awk -F\'\[\' \'{print $2}\''
  output = Popen(cmd, shell=True, stdout=PIPE).communicate()[0] 
  output = output.strip()
  output = output.rstrip(']')
  output = output.lstrip('[')
  print ostidx[it], i, output 
  it = it + 1
 


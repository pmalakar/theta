import os
import sys

def readGlobalConfiguration_(f, node_id, rank):

  #f = open("theta.computenodes", "r")
  cab_position, cab_row, cage, slot, cpu, processor_id = '', '', '', '', '', ''

  while True:
    line = f.readline()
    if not line: break
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

    if int(processor_id) == node_id:
      print rank, processor_id, cab_position, cab_row, cage, slot, cpu
      fout.write('%s %s %s %s %s %s %s\n' % (rank, processor_id, cab_position, cab_row, cage, slot, cpu))
      break


def getfnode(nodename):

    if len(str(nodename)) == 1:
     nidname = "nid0000"
    elif len(str(nodename)) == 2:
     nidname = "nid000"
    elif len(str(nodename)) == 3:
     nidname = "nid00"
    elif len(str(nodename)) == 4:
     nidname = "nid0"
 
    nidname+=str(nodename)
    return nidname


#3572-3579,3727-3734
def readAllocation_(nodeconfig, nidstringfile):
 
  global fout
  centroidfile = nidstrfile + ".ctd"
  nodenamefile = nidstrfile + ".nid"
  centroidRankList = []

  jobmap = "jobmap_"+nidstringfile

  f = open(nidstringfile, "r")
  nidstring = f.readline()
  f.close()

	#parse
  nodegroups = []
  if nidstring.find(',') == -1:
    nodegroups.append(nidstring)
  else:
    nodegroups = nidstring.split(',')

  print 'JOB: Number of clusters in current allocation: ', len(nodegroups)
  print

  rank = -1
  cluster = 0
  s=""
  s1=""
  f = open(nodeconfig, "r")
  fout = open(jobmap, "w+")

  for group in nodegroups:
    
    group = group.rstrip('\n')
    nodes = []
    if group.find('-') == -1:
      nodes.append(group)
      nodes.append(group) #to generalize the below loop
    else:
      nodes = group.split('-')
    
    localrank = 0
    for node in range(int(nodes[0]),int(nodes[1])+1):
      rank = rank + 1
      readGlobalConfiguration_(f, node, rank)
      localrank = localrank + 1

      #if rank > 0:
      #  s1+=","
      s1+=str(getfnode(node))
      s1+=":2,"
    
    centroidRank = (int(nodes[1]) - int(nodes[0]))/2 + int(nodes[0])
    centroidRankList.append(centroidRank)
    #if cluster != 0:
    # s+=","
    s+=getfnode(centroidRank)
    s+=":4,"
    cluster = cluster + 1
    print 'JOB: centroid of cluster ', group, centroidRank
    print
    
  f.close()
  fout.close()

  fc = open(centroidfile, "w")
  fc.write(s)
  fc.write("\n")
  fc.close()
 
  nidfp = open(nodenamefile, "w")
  nidfp.write(s1)
  nidfp.write("\n")
  nidfp.close()

#config file
nodecfg = sys.argv[1]

#current allocation
nidstrfile = sys.argv[2] 

#readGlobalConfiguration_()
readAllocation_(nodecfg, nidstrfile)



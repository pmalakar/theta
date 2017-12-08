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

def add_more_ctd():

  global nodelist, nodegroups, numgroups, numnodes, cblist_ctd

  #opt_num_per_grp = 4 # numnodes/numgroups
  #print nodelist, nodegroups, opt_num_per_grp

  cblist_ctd=""
  centroids = 0
  for group in nodegroups:
    
    group = group.rstrip('\n')
    nodes = []
    if group.find('-') == -1:
      nodes.append(group)
      nodes.append(group) #to generalize the below loop
    else:
      nodes = group.split('-')
    
   # num_this_group = int(nodes[1]) - int(nodes[0]) +1
   # if opt_num_per_grp < num_this_group:
   #   print opt_num_per_grp, num_this_group 

    localrank = 0
    for node in range(int(nodes[0]),int(nodes[1])+1):
      if localrank%4 == 0:
         print localrank, node
         cblist_ctd+=str(getfnode(node))
         cblist_ctd+=":x,"
         centroids = centroids+1
      localrank = localrank + 1

    print
    
  x = numnodes*2/centroids

  return x


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
 
  global fout, rank, numgroups, nodegroups, numnodes, nodelist, cblist_ctd

  centroidfile = nidstringfile + ".ctd"
  nodenamefile = nidstringfile + ".nid"
  centroidRankList = []
  nodelist = []

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

  numgroups = len(nodegroups)

  print 'JOB: Number of clusters in current allocation: ', len(nodegroups)
  print

  rank = -1
  cluster = 0
  cblist_ctd=""
  cblist_nid=""
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
      nodelist.append(node)
      readGlobalConfiguration_(f, node, rank)
      localrank = localrank + 1

      #if rank > 0:
      #  cblist_nid+=","  #bug in Cray MPI/MPICH? requires ',' at the end
      cblist_nid+=str(getfnode(node))
      cblist_nid+=":2,"
    
    centroidRank = (int(nodes[1]) - int(nodes[0]))/2 + int(nodes[0])
    centroidRankList.append(centroidRank)
    #if cluster != 0:
    # s+=","
    cblist_ctd+=getfnode(centroidRank)
    cblist_ctd+=":x,"
    cluster = cluster + 1
    print 'JOB: centroid of cluster ', group, centroidRank
    print
    

  f.close()
  fout.close()

  numnodes = len(nodelist)

  x=int((rank*2+1)/numgroups) + 1 
  print rank, numgroups, x 
  if (x>3): 
    x=add_more_ctd()
    
  cblist_ctd = cblist_ctd.replace("x", str(x))

  fc = open(centroidfile, "w")
  fc.write(cblist_ctd)
  fc.write("\n")
  fc.close()
 
  nidfp = open(nodenamefile, "w")
  nidfp.write(cblist_nid)
  nidfp.write("\n")
  nidfp.close()

#config file
nodecfg = sys.argv[1]

#current allocation
nidstrfile = sys.argv[2] 

#readGlobalConfiguration_()
readAllocation_(nodecfg, nidstrfile)



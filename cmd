python ost2lnet.py theta tloc16_4 tloc16_4.ost
python parsejobnodes.py theta tloc16_4

python ost2lnet.py <machinename> <ranklocationfile> <listofostsfilename>
python ost2lnet.py theta tloc_165332.txt tloc_165332.txt.ost 

generated jobmap_<listofostsfilename>.<ostid>
 
python rank2lnet.py theta tloc_165332.txt tloc_165332.txt.ost input.ost

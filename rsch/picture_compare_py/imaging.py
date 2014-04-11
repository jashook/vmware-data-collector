#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: imaging.py
#
# Modifications: 
#
# 14-Feb-14: Version 1.0: Updated
# 22-Jan-14: Version 1.0: Created
#
################################################################################
################################################################################

import sys
from cluster import *

if __name__ == "__main__":

   if (len(sys.argv) == 2): 

      _Directory = sys.argv[1]
      
      _Cluster = cluster(_Directory)
      
      _Cluster.build_dictionary()

      #print "Dictionary size: " + str(_Cluster.dictionary_size())
      
      #_Cluster.print_dictionary()

      _Cluster.build_cluster()

      #print "Unique Hashes in Dictionary " + str(_Cluster.unique_hash_count())

      #_Cluster.print_cluster()

      _Cluster._write_cluster()
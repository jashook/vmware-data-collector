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

if __name__ == "__main__":

   _Cluster = dict()

   if (len(sys.argv) == 2): 

      _Directory = sys.argv[1]

      _Dictionary = build_dictionary(_Directory)


   print _Cluster


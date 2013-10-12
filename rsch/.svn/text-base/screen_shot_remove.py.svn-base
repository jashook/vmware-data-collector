#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: screen_shot_remove.py
#
# Modifications:
#
# 27-Sept-13: Version 1.0: Last Updated
# 27-Sept-13: Version 1.0: Created
#
# Timeperiod: ev7n
#
################################################################################
################################################################################

import os
import subprocess
import sys

################################################################################
################################################################################

if __name__ == '__main__':

   _Args = sys.argv[1:] # ignore the first arguement

   if (len(_Args) != 1):

      print "Incorrect usage.  For help type (executable --help)."

      exit()

   if (_Args[0] == '--help'):

      print "Usage: (executable) directory"

      exit()

   _Directory = _Args[0]

   _Process = subprocess.Popen(["ls " + _Directory], stdout=subprocess.PIPE, shell=True)
   
   (_Output, _Error) = _Process.communicate()
   
   _Output = _Output.split('\n')

   _Output = _Output[:-1]

   for _Folder in _Output:

      print './ss_remove ' + _Directory + '/' + _Folder + '/screenshots/'

      #os.system('./ss_remove ' + _Folder + '/screenshots/')

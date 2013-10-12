#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: processurls.py
#
# Modifications:
#
# 24-June-13: Version 1.0: Last Updated
# 20-June-13: Version 1.0: Created
#
# Timeperiod: ev6n
#
################################################################################
################################################################################

import re
import sys

################################################################################
################################################################################

if __name__ == "__main__":

   if len(sys.argv) < 2: print "Error, enter a correct number of arguements"; exit()

   _File = open(sys.argv[1])

   _Urls = []

   for _Line in _File:

      if re.match("<li>*", _Line):

         _String = _Line[4:-6]

         print _String

         _String = "Http://" + _String

         _Urls.append(_String)

   _OutputFile = open("processedurls.txt", 'w')

   for _String in _Urls:

      _OutputFile.write(_String + "\n")


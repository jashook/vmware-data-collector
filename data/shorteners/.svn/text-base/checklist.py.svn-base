#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: checkweblist.py
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

import socket
import urllib2
import requests
import sys
import ssl

################################################################################
################################################################################

_OutputFile = open("redirectedurls.txt", "w")
_TimeoutFile = open("timedouturls.txt", "w")
_GoodFile = open("goodurls.txt", "w")

def set_timeout(_TimeOutSize):

   socket.setdefaulttimeout(_TimeOutSize)

def connect_to_website(_Url):

   _Request = urllib2.Request(_Url)
   
   try:
      
      _Response = urllib2.urlopen(_Request)

      _Response.read()

   except urllib2.URLError, _Exception:

      print _Url + ": " + "TIMEOUT"

      _TimeoutFile.write(_Url + "\n")

   except socket.timeout:

      print _Url+ ": " + "TIMEOUT"

      _TimeoutFile.write(_Url + "\n")

   except ssl.SSLError:

      _GoodFile.write(_Url + "\n")

      print _Url + ": " 

   except socket.error:

      print _Url + "ERROR"

   else:

      if _Response.geturl() == _Url:

         print _Url + ": "
         _GoodFile.write(_Url + "\n") 

      else:

         _OutputFile.write(_Url + ":" + _Response.geturl() + "\n")

         print _Url + ": " + "Redirected!"

def traverse_list(_List):

   set_timeout(10)
   
   for _Url in _List:

      connect_to_website(_Url)

if __name__ == "__main__":

   set_timeout(15)

   if len(sys.argv) < 0: "Error, include a file with urls to visit as an arguement"; exit()

   _File = open(sys.argv[1])

   for _Lines in _File:

      connect_to_website(_Lines[:-1])


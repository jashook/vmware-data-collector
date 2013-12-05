################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: selenium_driver.py
#
# Modifications:
#
# 18-July-13: Version 1.0: Last Updated
# 18-July-13: Version 1.0: Recovered
# 1-July-13: Version 1.0: Created
#
# Timeperiod: ev7n
#
# Notes: Windows only
#
################################################################################
################################################################################

from selenium import webdriver
import time

################################################################################
################################################################################

if __name__ == "__main__":

   _UrlFile = open("E:/url.txt")

   _Lines = _UrlFile.readlines()

   _UrlFile.close()

   _Url = _Lines[0][:-1] # get rid of /n

   print _Url

   _Driver = webdriver.Ie()

   _Driver.get(_Url)

   _SourceFile = open("Z:/source/page.txt", "w")

   print "Writing"

   _SourceFile.write(_Driver.page_source.encode("ascii", "ignore"))

   print "Finished Writing"

   _SourceFile.close()

   _CookieFile = open("Z:\\cookies\\page\\page_cookies.txt", "w")

   for _Cookie in _Driver.get_cookies():

      _CookieFile.write("%s -> %s" % (_Cookie['name'], _Cookie['value']))

   _CookieFile.close()

   time.sleep(15)


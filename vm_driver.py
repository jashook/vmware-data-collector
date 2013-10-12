#!/usr/bin/env python
################################################################################
################################################################################
#
# Authors: Jarret Shook
#
# Module: vm_util.py
#
# Modifications: 
#
# 12-Oct-13: Version 1.1: Last updated
# 12-Oct-13: Version 1.1: Cleaned and Commented
# 12-Oct-13: Version 1.1: Added new command options
# 28-May-13: Version 1.0: Created
#
# Timeperiod: ev6
#
# Notes:
#
#
################################################################################
################################################################################

from vm_util import *

import sys
import time

################################################################################
################################################################################

# path to virtual machine
# number of concurrent machines
# directory of startup file

def determine_parameters():

   def _check_parameter(_Parameter):

      # -v = virtual machine
      # -d = destination
      # -c = number of concurrent machines
      # -s = startup script
      # -es = entry and exit script
      # --help = help

      if _Parameter == "-v": return True

      elif _Parameter == "-d": return True

      elif _Parameter == "-c": return True

      elif _Parameter == "-s": return True

      elif _Parameter == "-es": return True

      elif _Parameter == "-con": return True

      elif _Parameter == '-urls': return True

      elif _Parameter == '-gui': return True
   
      elif _Parameter == '-ss': return True
   
      elif _Parameter == '-collection': return True

      elif _Parameter == "--help": return True

      else: return False

   _Parameters = list()

   for _Item in range(10):

      _Parameters.append(None);

   _LastParameter = None

   _Args = sys.argv[1:] # ignore the first arguement

   _Next = False

   for _Parameter in _Args:

      if (_check_parameter(_Parameter)):

         if _Parameter == "--help": 

            print_help()

            exit() # in case there were more parameters

         else: 

            _LastParameter = _Parameter

            _Next = True

      else:

         if _Next:

            _Next = False

            if (_LastParameter == "-v"): _Parameters[0] = _Parameter
         
            elif (_LastParameter == "-c"): _Parameters[1] = _Parameter

            elif (_LastParameter == "-s"): _Parameters[2] = _Parameter

            elif (_LastParameter == "-es"): _Parameters[3] = _Parameter

            elif (_LastParameter == "-d"): _Parameters[4] = _Parameter

            elif (_LastParameter == "-con"): _Parameters[5] = _Parameter

            elif (_LastParameter == '-urls'): _Parameters[6] = _Parameter

            elif (_LastParameter == "-gui"): _Parameters[7] = _Parameter

            elif (_LastParameter == "-ss"): _Parameters[8] = _Parameter

            elif (_LastParameter == '-collection'): _Parameters[9] = _Parameter

            else:

               print "Incorrect parameter try using --help"

               return None

         else:

            print "Incorrect formatting of parameters, recheck syntax"

            exit()

   if _Next:

      print "Incorrect formatting of parameters, recheck syntax"

      exit()

   return _Parameters

def main(_VirtualMachine, _Destination, _NumberOfMachines, _StartupFile, _EntryExitScript, _Continue, _Gui = True, _Ss = True, _Collection = None):

   if _VirtualMachine == None: 

      print "Error you must provide a Virtual Machine's directory at a minimum"

      exit()

   if _Destination == None:

      print "Error you must provide a Virtual Machine's directory at a minimum"

      exit()

   if _EntryExitScript == None:

      print "Error you must provide a python script that defines an vmware_pre_run and vmware_post_run function at a minimum"

   if _Continue is None: _Continue = 0

   if _StartupFile == None:

      start_machines(_VirtualMachine, _Destination, _NumberOfMachines, _StartupFile, _EntryExitScript, False, _Continue, _Gui, _Ss, _Collection)

   elif _StartupFile != None:

      start_machines(_VirtualMachine, _Destination, _NumberOfMachines, _StartupFile, _EntryExitScript, True, _Continue, _Gui, _Ss, _Collection)

def print_help():

   print "Commands:"

   print ""

   print "-v path to a vmware virtual machine folder to clone"

   print "-d destination folder"

   print "-s path to a startup file that will be run on the cloned machine"

   print "-es path to a script containing an entry and exit function"

   print "-c amount of concurrent machines"

   print "-con number of urls to go through, (goes through at least one)"

   print "-urls file that contain the urls"

   print "-gui Should the gui be shown [y/n]"

   print "-ss save a snapshot after each url? [y/n]"

   print "-collection root destination for the collected information"

   print "--help help"

def start_machines(_VirtualMachine, _Destination, _NumberOfMachines, _StartupFile, _ExitFile, _IsStartupFile, _Continue, _Gui, _Ss, _Collection):

   _NewVmdk = "NewMachine" + ".vmdk"

   _NewVmx = "NewMachine" + ".vmx"

   _MachinesOnDisk = dict()

   for _Number in range(_NumberOfMachines):

      _Filename = "NewMachine" + str(_Number)

      _MachinesOnDisk[_Filename] = None

   for _FileName in os.listdir(_Destination):

      _MachinesOnDisk[_FileName] = 1

   for _Number in range(_NumberOfMachines):

      _NewName = "NewMachine" + str(_Number)

      _NewDir = _Destination + _NewName + "/"

      _CloneMachine = False # assume the machine exists

      if _MachinesOnDisk[_NewName] is None:

         _CloneMachine = True # else if it is not found then clone

         _Command = "mkdir " + "\"" + _NewDir + "\""

         print _Command

         os.system(_Command)

         _Command = "mkdir " + "\"" + _NewDir + "mnt/" + "\""

         print _Command

         os.system(_Command)

      else: 

         print "Found old machine, attempting to use that Virtual Machine"

         print "Reverting to snapshot"

         _Command = "vmrun -T ws revertToSnapshot " + "\"" + _NewDir + _NewVmx + "\"" + " NewMachineSnapshot"

         os.system(_Command)

         time.sleep(15)

         print "Reverted to snapshot, continuing execution..."

      if not _IsStartupFile: _ClonedMachine = vmware_create(_VirtualMachine, _NewDir, _NewVmx, _NewVmdk, _CloneMachine, _Continue / _NumberOfMachines, _Gui, _Ss, _Collection)

      else: vmware_create(_VirtualMachine, _NewDir, _StartupFile, _NewVmx, _NewVmdk, _CloneMachine, _Continue / _NumberOfMachines, _Gui, _Ss, _Collection)

if __name__ == '__main__':

   _Parameters = determine_parameters()  

   _VirtualMachine = None

   _Destination = None

   _NumberOfMachines = 1

   _StartupFile = None
   
   _Script = None

   _Continue = None

   _UrlFile = None

   _Gui = "False"

   if len(sys.argv) == 1: 

      print "Incorrect amount of parameters, try --help for more information"

      exit()

   if _Parameters == None: exit()

   if _Parameters[0] != None:

      _VirtualMachine = _Parameters[0]

   if _Parameters[2] != None:

      _StartupFile = _Parameters[2]

   if _Parameters[3] != None:

      _Script = _Parameters[3]

   if _Parameters[1] != None:

      _NumberOfMachines = int(_Parameters[1])

   if _Parameters[4] != None:

      _Destination = _Parameters[4]

   if _Parameters[5] != None:

      _Continue = _Parameters[5]

      _Continue = int(_Continue)

   if _Parameters[6] != None:

      _UrlFile = _Parameters[6]

   if _Parameters[6] is None:

      _UrlFile = 'urls.txt'
   
   if _Parameters[7] != None:

      _Gui = _Parameters[7]

   if _Parameters[8] != None:

      _Ss = _Parameters[8]

   if _Parameters[9] != None:

      _Collection = _Parameters[9]

   _FileOfUrls = open(_UrlFile)

   _UrlList = _FileOfUrls.readlines()

   _FileOfUrls.close()

   _FileOfUrls = open(_UrlFile, 'w')

   _Count = 0

   for _Url in _UrlList:

      if _Count < _Continue:

         _Count = _Count + 1

      else:

         _FileOfUrls.write(_Url)

   set_url_list(_UrlList)

   if (_Gui == "no" or _Gui == "n" or _Gui == "N"): _Gui = False

   if (_Gui == "Y" or _Gui == "y"): _Gui = True

   if (_Ss == "no" or _Ss == 'n' or _Ss == 'N'): _Ss = False

   if (_Ss == 'Y' or _Ss == 'y'): _Ss = True

   main(_VirtualMachine, _Destination, _NumberOfMachines, _StartupFile, _Script, _Continue, _Gui, _Ss, _Collection)

   # go through the list of threads and join them to the main thread

   vmware_join()

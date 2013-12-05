#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: vm_util.py
#
# Modifications:
#
# 12-Oct-13: Version 1.1: Last Updated
# 12-Oct-13: Version 1.1: Commented and cleaned
# 28-Aug-13: Version 1.1: Cleaning and minor changes
# 2-April-13: Version 1.0: Created
#
# Timeperiod: ev6
#
################################################################################
################################################################################

from multiprocessing import Value, Lock
import os

import re
import shelve
import time

from heavy_thread import heavy_thread
from vm import vm

################################################################################
################################################################################
# Global Variables
################################################################################
################################################################################

_ThreadList = [] # empty thread list

_MachineCount = Value('i', 0) # integer value that will be shared between threads

_Lock = Lock()
_CloneLock = Lock()
_MountLock = Lock()

_NumLock = Lock()
_CollectionNumber = 0

_ContinueLock = Lock()
_ContinueLooping = True

URLList = None # set by vm_driver

_UrlLock = Lock()

_UrlIndex = Value('i', 0)

_Shelve = shelve.open("shelve.txt", writeback = True)

################################################################################
################################################################################
# Function: clone_vm
#
# Parameters:
#
#     _VirtualMachine: main virtual machine to be copying from
#     _ClonedMachine: machine that will act as the end copy
#
# Returns
#
#     _ClonedMachine: The machine that has been copied
#     _Thread: A reference to the thread copying the vmdk file
#
# Notes:
#
#     Cloning a VM is defined to be copying the .vmdk file or the virtual hard drive
#     and its .vmx configuration file
#
#     The function will insert two lines in order to make sure the VM will not hang
#     and ask if the machine has been copied
#
################################################################################
################################################################################

def clone_vm(_VirtualMachine, _ClonedMachine):

   _CloneLock.acquire() # ram intensive process therefore cloning will be limited to one VM at a time

   def _os_clone_and_copy(_StartArg):

      print "Copying the virtual disk (this operation will take some time)..."

      print "Forking this operation to a seperate thread..."

      _Thread.set_active(True)

      os_copy(_StartArg)

      _ClonedMachine.set_disk_created(True)

      print "Disk Cloned"

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun -T ws snapshot " + "\"" + _ClonedMachine._m_directory + _ClonedMachine._m_config_file + "\"" + " NewMachineSnapShot"

      else:

         _Command = "sudo vmrun -T ws snapshot " + "\"" + _ClonedMachine._m_directory + _ClonedMachine._m_config_file + "\"" + " NewMachineSnapShot"

      print "Creating Snapshot"

      os.system(_Command)

      _Thread.sleep(20) # make sure the snapshot finishes before starting

      _ClonedMachine._m_disk_file = find_snapshot(_ClonedMachine)

      print "Snapshot Created continuing..."

      print "Completed copying the virtual disk, joining back to main thread..."

      _Thread.set_active(False)
   
      _ThreadList.remove(_Thread)

      _CloneLock.release()

      #####################################################
      # Call the callback function from the VM class
      #####################################################

      _ClonedMachine()

   ########################################################
   # vmware-vdiskmanager -r <path to source .vmdk> -t 0 <path to destination .vmdk>
   #
   # -r:
   # source disk location
   #
   # -t
   # 0 - to create a growable virtual disk contained in a single virtual disk file
   # 1 - to create a growable virtual disk split into 2GB files
   # 2 - to create a preallocated virtual disk contained in a single virtual disk file
   # 3 - to create a preallocated virtual disk split into 2GB files
   ########################################################

   _CopyDiskCommand = "vmware-vdiskmanager -r " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_disk_file + "\"" + " -t 0 " + "\"" + _ClonedMachine._m_directory + _ClonedMachine._m_disk_file + "\"" # long operation, fork to a seperate thread

   _Thread = heavy_thread(_os_clone_and_copy, (_CopyDiskCommand,))

   ########################################################
   # Makes and starts thread then continues execution here
   ########################################################

   _ThreadList.append(_Thread)

   _Url = get_url()

   if _Url is None: return

   _DirUrl = _Url[7:]

   if (_Shelve.has_key(_DirUrl)):

      while(_Shelve.has_key(_DirUrl)):

         _Url = get_url()

         if _Url is None: return

         _DirUrl = _Url[7:]

   _SavedUrl = _DirUrl

   _DirUrl = _DirUrl.replace("/", "_")

   _DirUrl = _DirUrl.replace(".", "_")

   _Shelve[_SavedUrl] = _DirUrl

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _DirCommand = "mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

   else:
   
      _DirCommand = "sudo mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

   _ClonedMachine._m_collection = _ClonedMachine._m_collection_destination + _DirUrl

   _ClonedMachine._m_url = _Url

   print _DirCommand

   os.system(_DirCommand)

   _Thread.start()

   _File = open(_VirtualMachine._m_directory + _VirtualMachine._m_config_file) # default open to read only

   ########################################################
   # Check to see if the .vmx file that is being copied 
   # will automatically ignore copying the .vmdk file.
   # If not then add in two lines that will auto answer 
   # the prompted message to be true
   ######################################################## 

   _Matched = False

   _ReWriteFile = True

   for _Line in _File:

      if re.match("uuid.action = *", _Line): _Matched = True

      elif re.match("scsi0:0.fileName = *", _Line):

         if re.match("scsi0:0.fileName = " + _ClonedMachine._m_disk_file, _Line): _ReWriteFile = False

   _File.close()

   _File = open(_VirtualMachine._m_directory + _VirtualMachine._m_config_file) # default read only

   _Lines = _File.readlines()

   if _ReWriteFile:

      _File = open(_ClonedMachine._m_directory + _ClonedMachine._m_config_file, 'w')

      for _Line in _Lines:

         if not re.match("scsi0:0.fileName = *", _Line): _File.write(_Line)

      _File.write("scsi0:0.fileName = " + "\"" + _ClonedMachine._m_disk_file + "\"")

      _File.write("\n")

      _File.close()

   _ClonedMachine.set_config_created(True)
 
   if _ClonedMachine.config_created(): print "VMX file cloned"
  
   if not _Matched:

      _File = open(_ClonedMachine._m_directory + _ClonedMachine._m_config_file, 'a') # open the new file to append

      _File.write("uuid.action = \"create\"")
      _File.write("\n") # new line
      _File.write("msg.autoAnswer = \"TRUE\"")

      _File.close()

   return _ClonedMachine, _Thread

def continue_execution(_ClonedMachine, _Thread, _CloneMachine, _VirtualMachine = None):

   if not _CloneMachine:

      _ClonedMachine() # if the machine is created then just run it

   if _VirtualMachine is not None: 
      
      _ClonedMachine, _Thread = clone_vm(_VirtualMachine, _ClonedMachine)

   if _Thread is not None: _Thread.join()

   if _ClonedMachine._m_thread is not None: _ClonedMachine._m_thread.join()

   _ContinueLock.acquire()

   _ContinueLoop = _ContinueLooping

   _ContinueLock.release()

   while _ContinueLoop is True:

      _ClonedMachine._m_continue = _ClonedMachine._m_continue - 1

      if _ClonedMachine._m_continue == 0: return

      _ContinueLock.acquire()

      _ContinueLoop = _ContinueLooping

      _ContinueLock.release()

      print "Reverting to snapshot"

      if os.environ.get('OS','') == 'Windows_NT':

         _Command = "vmrun -T ws revertToSnapshot " + "\"" + _ClonedMachine._m_directory + _ClonedMachine._m_config_file + "\"" + " NewMachineSnapshot"

      else:

         _Command = "sudo vmrun -T ws revertToSnapshot " + "\"" + _ClonedMachine._m_directory + _ClonedMachine._m_config_file + "\"" + " NewMachineSnapshot"
      
      os.system(_Command)

      time.sleep(25)

      print "Reverted to snapshot, continuing execution..."

      _ClonedMachine._m_disk_file = find_snapshot(_ClonedMachine)

      _Url = get_url()

      if _Url is None: break

      _DirUrl = _Url[7:]

      if (_Shelve.has_key(_DirUrl)):

         while(_Shelve.has_key(_DirUrl)):

            _Url = get_url()

            if _Url is None: break

            _DirUrl = _Url[7:]

      _SavedUrl = _DirUrl

      _DirUrl = _DirUrl.replace("/", "_")

      _DirUrl = _DirUrl.replace(".", "_")

      _Shelve[_SavedUrl] = _DirUrl

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

      else:

         _Command = "sudo mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

      _ClonedMachine._m_collection = _ClonedMachine._m_collection_destination + _DirUrl

      _ClonedMachine._m_url = _Url

      print _Command

      os.system(_Command)

      _ClonedMachine() # if the machine is created then just run it

      if _ClonedMachine._m_thread is not None: _ClonedMachine._m_thread.join()

def cp(_Src, _File):

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "copy " + _Src + " " + _File

   else:

      _Command = "sudo cp " + _Src + " " + _File

   os.system(_Command)

   print _Command

def find_files(_Path):

   _Vmdk = None
   _Vmx = None

   for _FileName in os.listdir(_Path):
      
      _Extension = _FileName[-5::]   # .vmdk is 5 characters long

      if _Extension == ".vmdk": _Vmdk = _FileName

      _Extension = _FileName[-4::]   # .vmx is 4 characters long

      if _Extension == ".vmx": _Vmx = _FileName

   return _Vmx, _Vmdk

def find_snapshot(_VirtualMachine):

   _Vmdks = list()

   for _FileName in os.listdir(_VirtualMachine._m_directory):

      _Extension = _FileName[-5::] # .vmdk is 5 characters long

      if _Extension == ".vmdk": _Vmdks.append(_FileName)

   _Vmdk = None

   _Min = 0

   for _File in _Vmdks:

      if len(_File) > _Min:

         _Min = len(_File)
         _Vmdk = _File

   return _Vmdk

def find_last_snapshot(_VirtualMachine):

   _Vmdks = list()

   for _FileName in os.listdir(_VirtualMachine._m_directory):

      _Extension = _FileName[-5::] # .vmdk is 5 characters long

      if _Extension == ".vmdk": _Vmdks.append(_FileName)

   _Vmdk = None

   _Snapshots = list()

   for _File in _Vmdks:

      if re.match("NewMachine-00*", _File):

         _Snapshots.append(_File)

   _Min = 0
   _Index = 0
   _MinIndex = 0

   for _Snapshot in _Snapshots:

      _Sum = 0

      for _Character in _Snapshot:

         _Sum = _Sum + ord(_Character)

      if (_Sum > _Min):

         _Min = _Sum

         _MinIndex = _Index

   return _Snapshots[_MinIndex]

def get_number():

   _NumLock.acquire()

   global _CollectionNumber

   if (_CollectionNumber is 0):

      for _FileName in os.listdir():

         _OldNumber = _CollectionNumber

         _CollectionNumber = int(_FileName[15:])

         if (_CollectionNumber < _OldNumber): _CollectionNumber = _OldNumber

      _CollectionNumber =  _CollectionNumber + 1

   _Num = _CollectionNumber

   _CollectionNumber = _CollectionNumber + 1

   _NumLock.release()

   return _Num

def get_url():

   _Url = ""

   _UrlLock.acquire()

   _CurrentIndex = _UrlIndex.value

   _UrlIndex.value = _UrlIndex.value + 1 

   _ContinueLock.acquire()

   if _UrlIndex.value + 1 >= len(URLList) : _ContinueLooping = False

   else: _Url = URLList[_CurrentIndex][:-1]

   _ContinueLock.release()

   print _UrlIndex.value

   if _UrlIndex.value + 1 >= len(URLList): _Url = None

   _UrlLock.release()

   return _Url

def mount_vmdk(_VirtualMachine, _PartitionNumber = 1, _Path = None):

   _MountLock.acquire() # make sure not to overmount a previous mount

   if not _Path: _Path = "/mnt"

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "vmware-mount " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_disk_file + "\"" + " " + str(_PartitionNumber) + " " + "\"" + _Path + "\""

   else:

      _Command = "sudo vmware-mount " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_disk_file + "\"" + " " + str(_PartitionNumber) + " " + "\"" + _Path + "\""

   os.system(_Command)

   print _Command

   _MountLock.release()

def os_copy(_Command):

   print _Command # print what command is being run

   os.system(_Command)

def umount_vmdk(_VirtualMachine, _Path = None):

   if not _Path: _Path = "\mnt"

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "vmware-mount -d " + "\"" + _Path + "\""

   else:

      _Command = "sudo vmware-mount -d " + "\"" + _Path + "\""

   os.system(_Command)

   print _Command

def set_url_list(_UrlList):

   global URLList

   URLList = _UrlList

def vmware_create(_WorkingDirectory, _DestinationDirectory, _StartUpFile = None, _NewVmx = "default.vmx", _NewVmdk = "default.vmdk", _CloneMachine = True, _ContinueNumber = 0, _Gui = True, _Ss = True, _Collection = None):

   _Vmx, _Vmdk = find_files(_WorkingDirectory)

   _VirtualMachine = vm(_WorkingDirectory, _Vmx, _Vmdk, _StartUpFile, True, True, _ContinueNumber, _Gui, _Ss, _Collection)

   _Vmx = _NewVmx

   _Vmdk = _NewVmdk

   if _CloneMachine:

      _ClonedMachine = vm(_DestinationDirectory, _Vmx, _Vmdk, _StartUpFile, False, False, _VirtualMachine._m_continue, _Gui, _Ss, _Collection)

   else:

      _ClonedMachine = vm(_DestinationDirectory, _Vmx, _Vmdk, _StartUpFile, True, True, _VirtualMachine._m_continue, _Gui, _Ss, _Collection)

   _ClonedMachine.set_function(vmware_entry_point)

   ########################################################
   # increasing machine count ** need to lock **
   ########################################################

   _Lock.acquire()

   _MachineCount.value = _MachineCount.value + 1

   _Lock.release() # synchronize finished

   if _CloneMachine: 

      _ContinueThread = heavy_thread(continue_execution, (_ClonedMachine, None, True, _VirtualMachine,))

      _ThreadList.append(_ContinueThread)
   
      _ContinueThread.start()

   else: 

      _ClonedMachine._m_disk_file = find_snapshot(_ClonedMachine)

      _Url = get_url()

      if _Url is None: return

      _DirUrl = _Url[7:]

      if (_Shelve.has_key(_DirUrl)):

         while(_Shelve.has_key(_DirUrl)):

            print "Found key"

            _Url = get_url()

            if _Url is None: return

            _DirUrl = _Url[7:]

      _SavedUrl = _DirUrl

      _DirUrl = _DirUrl.replace("/", "_")

      _DirUrl = _DirUrl.replace(".", "_")

      _Shelve[_SavedUrl] = _DirUrl

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _DirCommand = "mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

      else:

         _DirCommand = "sudo mkdir " + "\"" + _ClonedMachine._m_collection_destination + _DirUrl + "\""

      _ClonedMachine._m_collection = _ClonedMachine._m_collection_destination + _DirUrl

      _ClonedMachine._m_url = _Url

      print _DirCommand

      os.system(_DirCommand)

      _Thread = heavy_thread(continue_execution, (_ClonedMachine, None, False,))

      _ThreadList.append(_Thread)

      _Thread.start()

   return _ClonedMachine

def vmware_entry_point(_VirtualMachine):

   _Thread = heavy_thread(vmware_run, (_VirtualMachine, _MachineCount))

   _ThreadList.append(_Thread)

   _VirtualMachine._m_thread = _Thread

   # pre run code here

   _VirtualMachine.pre_run_function()

   _Thread.set_active(True)

   _Thread.start()

def vmware_is_running(_VirtualMachine):

   if _VirtualMachine._m_gui:

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun list >> running_vms.txt"

      else:

        _Command = "sudo vmrun list >> running_vms.txt"

      os.system(_Command)

      _File = open("running_vms.txt")

      _Running = False

      for _Line in _File:

         if re.match(_VirtualMachine._m_directory + _VirtualMachine._m_config_file, _Line): _Running = True

      _File.close()

      _File = open("running_vms.txt", 'w')

      _File.close()

   else:

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "dir " + "\"" + _VirtualMachine._m_directory + "\"" + " | findstr .vmdk.lck" + " >> running_vms.txt"

      else:

         _Command = "sudo ls " + "\"" + _VirtualMachine._m_directory + "\"" + " | grep .vmdk.lck" + " >> running_vms.txt"

      os.system(_Command)

      _File = open("running_vms.txt")

      _Running = False

      _RunningList = _File.readlines()

      if len(_RunningList) > 0: _Running = True

      _File.close()

      _File = open("running_vms.txt", 'w')

      _File.close()

   return _Running

def vmware_run(_VirtualMachine, _MachineCount):

   _Thread = _VirtualMachine._m_thread

   if _VirtualMachine._m_gui:

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

      else:

         _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

   else: 

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

      else:
         
         _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

   print _Command

   _Thread.sleep(2)

   os.system(_Command)

   _Thread.sleep(5)

   _Count = 0

   _Retried = False

   while vmware_is_running(_VirtualMachine) is False:

      _Thread.sleep(10) # sleep for a little to make sure it does not prematurely exit

      if _Retried is True and _Count > 2:

         print "Second Timeout, quitting..."

         break

      if _Count > 2: 

         print "Timeout..."

         print "Virtual Machine failed to start, retrying.."

         if _VirtualMachine._m_gui:

            if os.environ.get('OS','') == 'Windows_NT':

               ############################################
               # Win32 Support
               ############################################

               _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""
            
            else:

               _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

         else: 

            if os.environ.get('OS','') == 'Windows_NT':

               ############################################
               # Win32 Support
               ############################################

               _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

            else:

               _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

         print _Command

         os.system(_Command)

         _Count = 0

         _Retried = True

      else:
      
         _Count = _Count + 1

   _Timeout = 420 # 420 seconds or 7 minutes timeout

   while True:

      if not vmware_is_running(_VirtualMachine): break

      if _Timeout <= 0:

         print "Error starting machine, attempting to restart"

         if os.environ.get('OS','') == 'Windows_NT':

            ############################################
            # Win32 Support
            ############################################

            _Command = "vmrun stop " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

         else:

            _Command = "sudo vmrun stop " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

         print _Command
   
         os.system(_Command)

         if os.environ.get('OS','') == 'Windows_NT':

            ############################################
            # Win32 Support
            ############################################

            _Command = "vmware-mount -d " + "\"" + _VirtualMachine._m_mount_directory + "\""

         else:

            _Command = "sudo vmware-mount -d " + "\"" + _VirtualMachine._m_mount_directory + "\""

         print _Command
   
         os.system(_Command)

         if _VirtualMachine._m_gui:

            if os.environ.get('OS','') == 'Windows_NT':

               ############################################
               # Win32 Support
               ############################################

               _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

            else:

               _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\""

         else:

            if os.environ.get('OS','') == 'Windows_NT':

               ############################################
               # Win32 Support
               ############################################

               _Command = "vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

            else:

               _Command = "sudo vmrun start " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " nogui"

         print _Command
   
         os.system(_Command)

         _Timeout = 300

      _Thread.sleep(3) # sleep for 2.5 seconds

      _Timeout = _Timeout - 3
 
   _Thread.sleep(1)
 
   # decreasing machine count ** need to lock **

   _Lock.acquire()

   _MachineCount.value = _MachineCount.value - 1

   _Lock.release() # synchronize finished

   _VirtualMachine.post_run_function()

   _Thread.set_active(False)

def vmware_join():

   for _Thread in _ThreadList:

      if _Thread.is_active():

         print "Thread joining..."

         _Thread.join() #if alive join

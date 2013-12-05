#!/usr/bin/env python
################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: entry.py
#
# Modifications:
#
# 28-Aug-13: Version 1.1: Last Updated
# 28-Aug-13: Version 1.1: Cleaning and minor changes
# 6-June-13: Version 1.0: Created
#
# Timeperiod: ev6
#
# Notes:
#
# VMware tools gives command line programs to create and delete snapshots, however
# they are non-blocking procedures and I could not find a way to successfully check
# to see if they are finished. Therefore as a poor work around the program will just
# wait a predefined abitrary time in hope that it is long enough
#
################################################################################
################################################################################

from multiprocessing import Value, Lock
import os
import re
import time

import vm_util

################################################################################
################################################################################
# Function: vmware_pre_run
#
# Parameters:
#
#     _VirtualMachine: vm object that is about the be run
#
# Returns:
#
#     Void
#
# Notes:
#
#     This function will implant a url into the machine that is about to be run.
#     It is the last point of set up for the machine so doing things like copying
#     a selenium script or any other scripts would be appropriate here.
#
################################################################################
################################################################################

def vmware_pre_run(_VirtualMachine):

   ########################################################
   # Mount the second partition of the Virtual Machine
   # Check the User Manual for a reference to VM partitions
   ########################################################

   vm_util.mount_vmdk(_VirtualMachine, 2, _VirtualMachine._m_mount_directory)

   ########################################################
   # sudo echo <url assigned to the current Virtual Machine> <path to the mounted directory> url.txt
   # The selenium script expects the file to be read to be "url.txt"
   ########################################################

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "echo " + _VirtualMachine._m_url + " > " + "\"" + _VirtualMachine._m_mount_directory + "url.txt" + "\""

   else:

      _Command = "sudo echo " + _VirtualMachine._m_url + " > " + "\"" + _VirtualMachine._m_mount_directory + "url.txt" + "\""

   print _Command

   os.system(_Command)

   ########################################################
   # Unmount the partition and return to start running
   ########################################################

   vm_util.umount_vmdk(_VirtualMachine, _VirtualMachine._m_mount_directory)

################################################################################
################################################################################
# Function: vmware_post_run
#
# Parameters:
#
#     _VirtualMachine: vm object that is about the be run
#
# Returns:
#
#     Void
#
# Notes:
#
#     This function will copy all of the relevent data off of the VM and onto
#     the host's machine.  There is an option to save the Snapshot of the Virtual
#     Machine at the point of executions end.  Keep them only if space is not an
#     issue and they will be used.
#
#     Snapshot average size: 70-100MB
#
################################################################################
################################################################################

def vmware_post_run(_VirtualMachine):

   if _VirtualMachine._m_snap_shot:

      #####################################################
      # Logic:
      #
      # Create a new Snapshot
      # Copy it to the output destination
      # delete the Snapshot so it looks like it was never made.
      #####################################################

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun -T ws snapshot " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " NewMachineSnapShot2"

      else:

         _Command = "sudo vmrun -T ws snapshot " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " NewMachineSnapShot2"

      print "Creating Snapshot"

      os.system(_Command)

      time.sleep(15) # make sure the snapshot finishes before starting

      _Vmdk = vm_util.find_last_snapshot(_VirtualMachine)

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "copy " + "\"" + _VirtualMachine._m_directory + _Vmdk + "\"" + " " + "\"" + _VirtualMachine._m_collection + "\""

      else:

         _Command = "sudo cp " + "\"" + _VirtualMachine._m_directory + _Vmdk + "\"" + " " + "\"" + _VirtualMachine._m_collection + "\""

      print _Command

      os.system(_Command)

      print "Deleting snapshot"

      if os.environ.get('OS','') == 'Windows_NT':

         ############################################
         # Win32 Support
         ############################################

         _Command = "vmrun -T ws deleteSnapshot " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " NewMachineSnapshot2"

      else:

         _Command = "sudo vmrun -T ws deleteSnapshot " + "\"" + _VirtualMachine._m_directory + _VirtualMachine._m_config_file + "\"" + " NewMachineSnapshot2"

      os.system(_Command)

      time.sleep(20) # make sure there is enough time for the snapshot to be deleted

   ########################################################
   # Mount the third partition, which contains output data
   # Check the User Manual for a reference to VM partitions
   ########################################################

   vm_util.mount_vmdk(_VirtualMachine, 3, _VirtualMachine._m_mount_directory)

   ########################################################
   # sudo cp -r <directory of mounted VM filesystem>/* <directory of output>
   ########################################################

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "copy " + "\"" + _VirtualMachine._m_mount_directory + "pcaps" + "\"" + " " +"\"" + _VirtualMachine._m_collection + "/" + "\""

   else:

      _Command = "sudo cp -r " + "\"" + _VirtualMachine._m_mount_directory + "pcaps" + "\"" + " " +"\"" + _VirtualMachine._m_collection + "/" + "\""
      
   print _Command

   os.system(_Command)

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "copy " + "\"" + _VirtualMachine._m_mount_directory + "cookies" + "\"" + " " + "\"" + _VirtualMachine._m_collection + "/" + "\""

   else:

      _Command = "sudo cp -r " + "\"" + _VirtualMachine._m_mount_directory + "cookies" + "\"" + " " + "\"" + _VirtualMachine._m_collection + "/" + "\""
      
   print _Command

   os.system(_Command)

   
   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "copy " + "\"" + _VirtualMachine._m_mount_directory + "pictures" + "\"" + " " + "\"" + _VirtualMachine._m_collection + "/" + "\""

   else:

      _Command = "sudo cp -r " + "\"" + _VirtualMachine._m_mount_directory + "pictures" + "\"" + " " + "\"" + _VirtualMachine._m_collection + "/" + "\""
      
   print _Command

   os.system(_Command)

   if os.environ.get('OS','') == 'Windows_NT':

      ############################################
      # Win32 Support
      ############################################

      _Command = "copy " + "\"" + _VirtualMachine._m_mount_directory + "source" + "\"" + " " +"\"" + _VirtualMachine._m_collection + "/" + "\""

   else:

      _Command = "sudo cp -r " + "\"" + _VirtualMachine._m_mount_directory + "source" + "\"" + " " +"\"" + _VirtualMachine._m_collection + "/" + "\""
      
   print _Command

   os.system(_Command)

   time.sleep(5)

   ########################################################
   # Unmount the partition and return to continue execution
   ########################################################

   vm_util.umount_vmdk(_VirtualMachine, _VirtualMachine._m_mount_directory)

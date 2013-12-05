################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: vm.py
#
# Modifications:
#
# 28-Aug-13: Version 1.1: Last Updated
# 28-Aug-13: Version 1.1: Cleaning and minor changes
# 25-May-13: Version 1.0: Created
#
# Timeperiod: ev6
#
################################################################################
################################################################################

from entry import *
from vm_util import *

################################################################################
################################################################################

class vm:

   def __call__(_Self):

      #####################################################
      # Callback function usage: <vm name>()
      #####################################################

      if _Self._m_function is not None: _Self._m_function(_Self)

      #####################################################
      # End of __call__
      #####################################################

   def __init__(_Self, _Directory = None, _ConfigFile = None, _DiskFile = None, _StartupFile = None, _ConfigCreated = False, _DiskCreated = False, _Continue = 0, _Gui = True, _SnapShot = False, _Destination = None):

      #####################################################
      # Member Variables
      ####################################################

      _Self._m_collection = None
      _Self._m_collection_destination = _Destination
      _Self._m_config_created = _DiskCreated
      _Self._m_config_file = _ConfigFile
      _Self._m_continue = _Continue
      _Self._m_directory = _Directory
      _Self._m_disk_created = _ConfigCreated
      _Self._m_disk_file = _DiskFile
      _Self._m_function = None
      _Self._m_gui = _Gui
      _Self._m_mount_directory = _Directory + "mnt/"
      _Self._m_snap_shot = _SnapShot
      _Self._m_startup_file = _StartupFile
      _Self._m_thread = None
      _Self._m_url = None

      #####################################################
      # End of __init__
      #####################################################

   def config_created(_Self): return _Self._m_config_created
   def disk_created(_Self): return _Self._m_disk_created
   def post_run_function(_Self): vmware_post_run(_Self)
   def pre_run_function(_Self): vmware_pre_run(_Self)
   def set_config(_Self, _ConfigFile): _Self._m_config_file = _ConfigFile
   def set_config_created(_Self, _Created): _Self._m_config_created = _Created
   def set_directory(_Self, _Directory): _Self._m_directory = _Directory
   def set_disk(_Self, _DiskFile): _Self._m_disk_file = _DiskFile
   def set_disk_created(_Self, _Created): _Self._m_disk_created = _Created
   def set_function(_Self, _Function): _Self._m_function = _Function
   def set_startup_file(_Self, _File): _Self._m_startup_file = _File

################################################################################
################################################################################
# End of class vm
################################################################################
################################################################################

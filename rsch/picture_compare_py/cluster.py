################################################################################
################################################################################
#
# Author: Jarret Shook
#
# Module: cluster.py
#
# Modifications:
#
# 14-Feb-14: Version 1.0: Updated
# 14-Feb-14: Version 1.0: Created
#
################################################################################
################################################################################

import os
import sys
import hashlib
from PIL import Image
import re
from image import *

################################################################################
################################################################################

class cluster:
   ###############################################################################
   ###############################################################################
   ## Constructor: __init__ (cluster)
   ##
   ## Member Variables:
   ##
   ##   m_hashes: a dictionary mapping hashed images to a set of image objects
   ##   m_stored_pictures: a dictionary mapping image filenames to image objects
   ##   m_image_names: a list containing image filenames
   ##   m_directory: directory to pull the images from
   ##
   ###############################################################################
   ###############################################################################
   
   def __init__(_Self, _Directory):
      
      ######################################################
      # Member Variables
      ######################################################
      
      _Self.m_hashes = dict()

      _Self.m_stored_pictures = dict()

      _Self.m_image_names = []

      _Self.m_directory = _Directory

      ######################################################
      # End of init
      ######################################################

   ################################################################################
   # Member Functions
   ################################################################################
   
   def build_dictionary(_Self): _Self._build_dictionary()
   def build_cluster(_Self): _Self._build_cluster()
   def cluster_size(_Self): return _Self.cluster_size()
   def dictionary_size(_Self): return _Self._dictionary_size()
   
   ################################################################################
   # Helper Functions
   ################################################################################
   
   ###############################################################################
   ###############################################################################
   ## Function: _accurate_build (cluster)
   ##
   ## Arguments: None
   ## Returns: Void
   ##
   ## Notes:
   ##   Builds a dictionary of hashed images to a set of image objects that
   ##   share that like hash
   ##
   ###############################################################################
   ###############################################################################
   
   def _accurate_build(_Self):
   
      _TrackedPairs = collections.defaultdict(lambda: 0)
   
      for _Index, _Picture in enumerate(_Self.m_pictures):
   
         _Hashes = _Picture.m_hashes

         for _DescendingIndex in range(_Index, len(_Self.m_pictures) - 1):

            for _Hash in _Hashes:

               if _Self.m_pictures[_DescendingIndex] in _Hashes[_Hash]:
                  
                  _Count = 1
                  _SecondCount = 1

                  if _Self.m_pictures[_DescendingIndex].m_count > 0: _Count = _Self.m_pictures[_DescendingIndex].m_count
                  
                  if _Picture.m_count > 0: _SecondCount = 1
                  
                  if _Count > _SecondCount: _Count = _SecondCount

                  _TrackedPairs[(_Picture, _Self.m_pictures[_DescendingIndex])] += _Count
   
   ###############################################################################
   ###############################################################################
   ## Function: _build_dictionary (cluster)
   ##
   ## Arguments: None
   ## Returns: Void
   ##
   ## Notes:
   ##   Builds a dictionary of hashed images to a set of image objects that
   ##   share that like hash
   ##
   ###############################################################################
   ###############################################################################

   def _build_dictionary(_Self):
      _Directory = _Self.m_directory
      _Hashes = _Self.m_hashes
      _StoredPictures = _Self.m_stored_pictures
      _ImageNames = _Self.m_image_names
      
      _Files = os.listdir(_Directory)
      
      for _File in _Files:
         
         if _File[0] == '.' or _File == '..': continue # skip the local directory or the directory above
         
         ###################################################
         # Convert forward slashes for Windows portability
         ###################################################
         if os.name is "nt" and _Directory[-1] != "/":
            
            _Directory = _Directory + "\\"
            
            _Directory = _Directory.replace("\\", "/")
      
      print _Directory + _File
      
      _Image = Image.open(_Directory + _File)
      
      ######################################################
      # image.py for class declaration
      ######################################################
      _InImage = image(_File)

      ######################################################
      # Store the image names
      ######################################################
      _ImageNames.append(_InImage.m_name)

      _StoredPictures[_InImage.m_name] = _InImage
      
      _Width, _Height = _Image.size
      
      _TempWidth = 0
      
      _TempHeight = 0
      
      ######################################################
      # Default size
      ######################################################
      _Offset = 40
      
      _SecondTime = False
      
      _SecondTimeWidth = False
      
      while True:
         
         _Left = _TempWidth
         
         _Top = _TempHeight
         
         _NewSize = [_Left, _Top, _Left + _Offset, _Top + _Offset]
         
         if (_NewSize[2] > _Width): _NewSize[2] = _Width
         
         if (_NewSize[3] > _Height): _NewSize[3] = _Height
         
         _NewPicture = _Image.crop(_NewSize)
         
         _Hash = hashlib.md5(_NewPicture.tostring()).hexdigest()
         
         try:
            
            ################################################
            # Check if dictionary contains the hash value
            #
            # Note: not optimal
            ################################################
            _Hashes[_Hash]
            
            if _InImage in _Hashes[_Hash]:
               
               _SetMember = _Hashes[_Hash]
               
               _SetMember.m_count += 1
               
               _Hashes[_Hash].update(_SetMember)
            
            else:
               #############################################
               # Add a new image at the hash's location
               #############################################
               
               _Hashes[_Hash].add(_InImage)
         
         except:
            ################################################
            # Add a new set at the hash's location
            ################################################
            
            _NewSet = set()
            
            _NewSet.add(_InImage)
            
            _Hashes[_Hash] = _NewSet
         
         ###################################################
         # Store all of the hashes of that image inside that
         # image object
         ###################################################
         _InImage.m_pictures.append(_Hash)
         
         _TempWidth = _TempWidth + _Offset
         
         if (_TempWidth > _Width):
            
            _TempWidth = 0
            
            _TempHeight = _TempHeight + _Offset
         
         if (_TempHeight >= _Height):
            
            break

      _Self.m_hashes = _Hashes
            
   ###############################################################################
   ###############################################################################
   ## Function: _build_cluster (cluster)
   ##
   ## Arguments: None
   ## Returns: Void
   ##
   ## Notes:
   ##   Builds a dictionary of image objects mapped to a
   ##
   ###############################################################################
   ###############################################################################

   def _build_cluster(_Self):
      
      _Self._accurate_build()

################################################################################
################################################################################
# End of class image
################################################################################
################################################################################


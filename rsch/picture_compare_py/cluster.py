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
#
################################################################################
################################################################################

import os
import hashlib
import csv
from PIL import Image
import re
import collections
from image import *
from hash_object import *

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
      
      _Self.m_hashes = collections.defaultdict(lambda: set())
      
      _Self.m_hash_images = collections.defaultdict(lambda: set())
      
      _Self.m_multiple_hashes = dict()

      _Self.m_stored_pictures = dict()

      _Self.m_image_names = []

      _Self.m_directory = _Directory
   
      _Self.m_cluster = dict()
   
      _Self.m_magic_number = .75

      ######################################################
      # End of init
      ######################################################

   ################################################################################
   # Member Functions
   ################################################################################
   
   def build_dictionary(_Self, _Debug = False): _Self._build_dictionary(_Debug)
   def build_cluster(_Self): _Self._build_cluster()
   def cluster_size(_Self): return _Self._cluster_size()
   def dictionary_size(_Self): return _Self._dictionary_size()
   def print_cluster(_Self): _Self._print_cluster()
   def print_dictionary(_Self): _Self._print_dictionary()
   def unique_hash_count(_Self): return _Self._unique_hash_count()
   
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
      
      ######################################################
      # Handle key errors
      ######################################################
      _TrackedPairs = collections.defaultdict(lambda: 0)
   
      ######################################################
      # Keep track of the index, while looping through the
      # image names
      ######################################################
      for _Index, _Picture in enumerate(_Self.m_image_names):
         
         _Picture = _Self.m_stored_pictures[_Picture]
         
         _Hashes = _Picture.m_pictures

         ######################################################
         # For every index, go through and compare it with every
         # other index
         ######################################################
         for _DescendingIndex in range(_Index + 1, len(_Self.m_image_names)):

            ###################################################
            # If that picture is inside the large dictionary of
            # hashes at the location of the hashes from the other
            # picture then keep track of those intersections
            ###################################################
            for _Hash in _Hashes:

               ################################################
               # Create a list of images at the hash location
               # Note that hash object contains the iamge and
               # the count of times it was found
               ################################################
               _HObjects = [_Item.m_image for _Item in _Self.m_hashes[_Hash]]
               
               ################################################
               # _Self.m_stored_pictures maps an image's name to
               # an image object, while _Self.m_image_names
               # contains a list of image names for that mapping
               ################################################
               if _Self.m_stored_pictures[_Self.m_image_names[_DescendingIndex]] in _HObjects:
               
                  _Count = 1
                  _SecondCount = 1

                  _HashMember = _Self.m_hashes[_Hash]
                     
                  _FoundSetMember = None
                  
                  for _SetMember in _HashMember:
                     
                     if _SetMember.m_image is _Self.m_stored_pictures[_Self.m_image_names[_DescendingIndex]]:
                        
                        _FoundSetMember = _SetMember
                        
                        break

                  ################################################
                  # Get the count of the picture
                  ################################################
                  if _FoundSetMember.m_count > 0: _Count = _FoundSetMember.m_count
                  
                  _FoundPictureMember = None
                  
                  for _SetMember in _HashMember:
                     
                     if _SetMember.m_image is _Picture:
                        
                        _FoundPictureMember = _SetMember
                        
                        break
                  
                  if _FoundPictureMember.m_count > 0: _SecondCount = _FoundPictureMember.m_count
                  
                  if _Count > _SecondCount:
                     _Count = _SecondCount
                     _Count *= 2
                  
                  else:
                     _Count *= 2
               
                  #############################################
                  # Pair of image objects mapped to a count
                  # of how many times they are grouped together
                  #############################################
                  _TrackedPairs[(_Picture, _Self.m_stored_pictures[_Self.m_image_names[_DescendingIndex]])] += _Count
                  
      _DictionarySize = _Self.dictionary_size()
      
      _Index = 0

      for _TrackedPair in _TrackedPairs:
         _FirstCount = 0
         _SecondCount = 0

         for _HashObject in _TrackedPair[0].m_pictures:
            _HashMember = _Self.m_hashes[_HashObject]
            
            for _SetMember in _HashMember:
                     
               if _SetMember.m_image is _TrackedPair[0]:
                  
                  _FoundSetMember = _SetMember
               
               break
            
            _FirstCount += _FoundSetMember.m_count
         
         for _HashObject in _TrackedPair[1].m_pictures:
            _HashMember = _Self.m_hashes[_HashObject]
            
            for _SetMember in _HashMember:
                     
               if _SetMember.m_image is _TrackedPair[1]:
                  
                  _FoundSetMember = _SetMember
               
               break
            
            _FirstCount += _FoundSetMember.m_count
            
         if _FirstCount + _SecondCount is 0: _FirstCount = 1

         _Appended = False
         
         _FoundTrackedPairOne = -1
         _FoundTrackedPairTwo = -1
         
         try:
            for _ClusterKey in _Self.m_cluster:
               if _TrackedPair[0] in _Self.m_cluster[_ClusterKey]:
                  _FoundTrackedPairOne = _ClusterKey
            
               elif _TrackedPair[1] in _Self.m_cluster[_ClusterKey]:
                  _FoundTrackedPairTwo = _ClusterKey

         except KeyError:
         
            pass

         if (float(_TrackedPairs[_TrackedPair]) / (_TrackedPair[0].m_picture_size + _TrackedPair[1].m_picture_size) > _Self.m_magic_number):
         
            _Appended = False
            
            if _FoundTrackedPairOne is -1 and _FoundTrackedPairTwo is not -1:
               _Self.m_cluster[_FoundTrackedPairTwo].add(_TrackedPair[0])
                  
               _Appended = True
                  
            if _FoundTrackedPairTwo is -1 and _FoundTrackedPairOne is not -1:
               _Self.m_cluster[_FoundTrackedPairOne].add(_TrackedPair[1])
                  
               _Appended = True
            
            if _FoundTrackedPairTwo is not -1 and _FoundTrackedPairOne is not -1:
               _SmallerPair = 0
               _Smaller = len(_Self.m_cluster[_FoundTrackedPairOne])
               
               if len(_Self.m_cluster[_FoundTrackedPairTwo]) < _Smaller: _SmallerPair = 1
               
               if _SmallerPair == 0:
                  _ToBeInserted = _Self.m_cluster[_FoundTrackedPairOne]
                  
                  for _TempClust in _ToBeInserted:
                     _Self.m_cluster[_FoundTrackedPairTwo].add(_TempClust)
               
                  _Self.m_cluster[_FoundTrackedPairOne] = None
               
                  del _Self.m_cluster[_FoundTrackedPairOne]
                  
               else:
                  _ToBeInserted = _Self.m_cluster[_FoundTrackedPairTwo]
                  
                  for _TempClust in _ToBeInserted:
                     _Self.m_cluster[_FoundTrackedPairOne].add(_TempClust)
            
                  _Self.m_cluster[_FoundTrackedPairTwo] = None
            
                  del _Self.m_cluster[_FoundTrackedPairTwo]
            
            if _FoundTrackedPairOne is -1 and _FoundTrackedPairTwo is -1:
               _Self.m_cluster[_Index] = set()
               _Self.m_cluster[_Index].add(_TrackedPair[0])
               _Self.m_cluster[_Index].add(_TrackedPair[1])

               _Index += 1

         else:
            if _FoundTrackedPairOne is -1:
               _Self.m_cluster[_Index] = set()
               _Self.m_cluster[_Index].add(_TrackedPair[0])

               _Index += 1

            if _FoundTrackedPairTwo is -1:
               _Self.m_cluster[_Index] = set()
               _Self.m_cluster[_Index].add(_TrackedPair[1])

               _Index += 1

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

   def _build_dictionary(_Self, _Debug = False):
      _Directory = _Self.m_directory
      
      _Files = os.listdir(_Directory)
      
      for _File in _Files:
         
         if _File[0] == '.' or _File == '..': continue # skip the local directory or the directory above
         
         ###################################################
         # Convert forward slashes for Windows portability
         ###################################################
         if os.name is "nt" and _Directory[-1] != "/":
            
            _Directory = _Directory + "\\"
            
            _Directory = _Directory.replace("\\", "/")
   
         if _Debug is True: print _Directory + _File
  
         _Path = _Directory + _File

         if os.path.islink(_Path): _Path = os.path.realpath(_Path)
  
         if os.path.isfile(_Path):
            _Image = Image.open(_Path)
         
         else: continue

         ######################################################
         # image.py for class declaration
         ######################################################
         _InImage = image(_File)

         ######################################################
         # Store the image names
         ######################################################
         _Self.m_image_names.append(_InImage.m_name)

         _Self.m_stored_pictures[_InImage.m_name] = _InImage
         
         _Width, _Height = _Image.size
         
         _TempWidth = 0
         
         _TempHeight = 0
         
         ######################################################
         # Default size
         ######################################################
         _Offset = 20
         
         _SecondTime = False
         
         _SecondTimeWidth = False
         
         while True:
            
            _Left = _TempWidth
            
            _Top = _TempHeight
            
            _NewSize = [_Left, _Top, _Left + _Offset, _Top + _Offset]
            
            if (_NewSize[2] < _Width) and (_NewSize[3] < _Height):
            
               _NewPicture = _Image.crop(_NewSize)
               
               _Hash = hashlib.md5(_NewPicture.tostring()).hexdigest()
               
               ################################################
               # Check if dictionary contains the hash value
               ################################################
               if len(_Self.m_hashes[_Hash]) is not 0:
               
                  #_HObjects = [_Item.m_image for _Item in _Self.m_hashes[_Hash]]
                  
                  if _InImage in _Self.m_hash_images:
                     _HashMember = _Self.m_hashes[_Hash]
                     
                     _FoundSetMember = None

                     _SetMember = None
                     
                     for _SetMember in _HashMember:
                     
                        if _SetMember.m_image is _InImage:
                     
                           _FoundSetMember = _SetMember
                     
                           break

                     _FoundSetMember.m_count += 1
                     
                     _InImage.m_picture_size += 1
                     
                     if _FoundSetMember not in _Self.m_multiple_hashes:
                     
                        _Self.m_multiple_hashes[_FoundSetMember] = _FoundSetMember
                     
                     _HashMember.discard(_FoundSetMember)
                     
                     _Self.m_hash_images[_InImage].discard(_FoundSetMember)

                     _HashMember.add(_FoundSetMember)
                     
                     _Self.m_hash_images[_InImage].add(_FoundSetMember)
                  
                  else:
                     #############################################
                     # Add a new image at the hash's location
                     #############################################
                     
                     _Object = hash_object(_InImage)
                     
                     _Self.m_hashes[_Hash].add(_Object)
                     
                     _Self.m_hash_images[_InImage].add(_Object)
            
                     _InImage.m_picture_size += 1
            
                     _InImage.m_pictures.append(_Hash)
               
               else:
                  ################################################
                  # Add a new set at the hash's location
                  ################################################
                  
                  _Self.m_hashes[_Hash].add(hash_object(_InImage))
                  
                  _Self.m_hash_images[_InImage].add(hash_object(_InImage))

                  ###################################################
                  # Store all of the hashes of that image inside that
                  # image object
                  ###################################################
                  _InImage.m_pictures.append(_Hash)
         
                  _InImage.m_picture_size += 1
            
            _TempWidth = _TempWidth + _Offset
            
            if (_TempWidth > _Width):
               
               _TempWidth = 0
               
               _TempHeight = _TempHeight + _Offset
            
            if (_TempHeight >= _Height):
               
               break

   ###############################################################################
   ###############################################################################
   ## Function: _build_cluster (cluster)
   ##
   ## Arguments: None
   ## Returns: Void
   ##
   ## Notes:
   ##   Builds a dictionary of image object pairs mapped to a set of image objects
   ##
   ###############################################################################
   ###############################################################################

   def _build_cluster(_Self):
      
      _Self._accurate_build()

   ###############################################################################
   ###############################################################################
   ## Function: _cluster_size (cluster)
   ##
   ## Arguments: None
   ## Returns: Size of the cluster
   ##
   ## Notes:
   ##   Returns zero if build_cluster has not been run
   ##
   ###############################################################################
   ###############################################################################

   def _cluster_size(_Self):

      return len(_Self.m_cluster)

   ###############################################################################
   ###############################################################################
   ## Function: _dictionary_size (cluster)
   ##
   ## Arguments: None
   ## Returns: Size of the dictionary containing all the hashes
   ##
   ## Notes:
   ##   Returns zero if build_dictionary has not been run
   ##
   ###############################################################################
   ###############################################################################

   def _dictionary_size(_Self):
      
      _Count = 0

      for _Hash in _Self.m_hashes:
         for _Object in _Self.m_hashes[_Hash]:
            _Count += _Object.m_count + 1
   
      return _Count

   ###############################################################################
   ###############################################################################
   ## Function: _print_cluster (cluster)
   ##
   ## Arguments: None
   ## Returns: None
   #
   ###############################################################################
   ###############################################################################
   
   def _print_cluster(_Self):
   
      _Cluster = []
   
      for _ClusterObject in _Self.m_cluster:
   
         _Cluster.append([_Item.m_name for _Item in _Self.m_cluster[_ClusterObject]])


      _Cluster.sort()
      
      for _ClusterObject in _Cluster:
         
         print _ClusterObject

   ###############################################################################
   ###############################################################################
   ## Function: _print_dictionary (cluster)
   ##
   ## Arguments: None
   ## Returns: None
   #
   ###############################################################################
   ###############################################################################

   def _print_dictionary(_Self):

      for _DictionaryObject in _Self.m_hashes:

         print _Self.m_hashes[_DictionaryObject]

   ###############################################################################
   ###############################################################################
   ## Function: _unique_hash_count (cluster)
   ##
   ## Arguments: None
   ## Returns: Size of the dictionary containing all the hashes
   ##
   ## Notes:
   ##   Returns zero if build_dictionary has not been run
   ##
   ###############################################################################
   ###############################################################################

   def _unique_hash_count(_Self):
      
      _Count = 0
      
      for _Hash in _Self.m_hashes:
         
         _Repeated = False

         for _SetMember in _Self.m_hashes[_Hash]:
         
            if _SetMember.m_count > 0:
         
               _Repeated = True
         
            if len(_Self.m_hashes[_Hash]) is 1 and not _Repeated:

               _Count += 1

      return _Count

   ###############################################################################
   ###############################################################################
   ## Function: _write_cluster (cluster)
   ##
   ## Arguments: None
   ## Returns: None
   #
   ###############################################################################
   ###############################################################################
   
   def _write_cluster(_Self):
   
      _Cluster = []
   
      for _ClusterObject in _Self.m_cluster:
   
         _Cluster.append([_Item.m_name for _Item in _Self.m_cluster[_ClusterObject]])


      _Cluster.sort()
      
      _Outputfile  = open('output.csv', "wb")
      _Writer = csv.writer(_Outputfile)

      _Writer.writerow(["A1","Layout_Cluster"])

      _ClusterIndex = 0

      for _ClusterRow in _Cluster:
         for _ClusterObject in _ClusterRow:
            _Writer.writerow([_ClusterObject, str(_ClusterIndex)])

         _ClusterIndex += 1

################################################################################
################################################################################
# End of class image
################################################################################
################################################################################

